import os
from datetime import timedelta
import os
import pendulum

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.slack.notifications.slack_notifier import SlackNotifier

from src.get_news_headline import get_news_headline
from src.get_kospi_data import get_kospi_data


seoul_time = pendulum.timezone('Asia/Seoul')
dag_name = os.path.basename(__file__).split('.')[0]

SLACK_CONNECTION_ID = "slack_conn"
SLACK_CHANNEL = "airflow"

default_args = {
    'owner': 'KunheeKim',
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}


def branch_func(ti):
	xcom_value = bool(ti.xcom_pull(task_ids="get_kospi_data_task"))
	if xcom_value == True:
		return "get_news_headline_task"
	elif xcom_value == False:
		return "stop_task"
	else:
		return None



with DAG(
    dag_id=dag_name,
    default_args=default_args,
    description='Get KOSPI & New Headline Data and append to previous data every 6pm on weekdays',
    schedule_interval='0 18 * * MON-FRI',
    start_date=pendulum.datetime(2023, 10, 9, tz=seoul_time),
    catchup=False,
    tags=[]
) as dag:
    get_kospi_data_task = PythonOperator(
        task_id='get_kospi_data_task',
        python_callable=get_kospi_data,
		on_execute_callback=SlackNotifier(
        	slack_conn_id=SLACK_CONNECTION_ID,
            text="""
			:eyes: KOSPI Market data & News Headline parsing workflow initiated ({{ds}}).:eyes:
            """,
            channel=SLACK_CHANNEL,
        )
    )
    get_news_headline_task = PythonOperator(
        task_id='get_news_headline_task',
        python_callable=get_news_headline,
		on_success_callback=SlackNotifier(
			slack_conn_id=SLACK_CONNECTION_ID,
            text="""
			:white_check_mark: Workflow successed parsing KOSPI market data and news headlines for today({{ds}})!:tada:
            """,
            channel=SLACK_CHANNEL,
        )
    )
    branch_op = BranchPythonOperator(
	    task_id="branch_task",
	    python_callable=branch_func,
    )
    stop_op = EmptyOperator(task_id="stop_task",
			on_success_callback=SlackNotifier(
            slack_conn_id=SLACK_CONNECTION_ID,
            text="""
			:red_siren:Terimanted workflow since the KOSPI market is closed today({{ds}}).:red_siren:
            """,
            channel=SLACK_CHANNEL,
        )
	)
	
    get_kospi_data_task >> branch_op >> [get_news_headline_task, stop_op]
	
