import os
from datetime import timedelta
import os
import pendulum

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator, ShortCircuitOperator
from airflow.providers.slack.notifications.slack_notifier import SlackNotifier
from airflow.providers.slack.operators.slack import SlackAPIFileOperator

from src.get_news_headline import get_news_headline
from src.get_kospi_data import get_kospi_data
from src.train_model import train_model

seoul_time = pendulum.timezone('Asia/Seoul')
dag_name = os.path.basename(__file__).split('.')[0]

SLACK_CONNECTION_ID = "slack_conn"
SLACK_CHANNEL = "workflows"

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
			:eyes: KOSPI Prediction workflow initiated ({{ds}}).:eyes:
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
			:white_check_mark: Workflow successed parsed KOSPI market data and news headlines for today({{ds}})!:tada:
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
			:red_siren:Skipping data collection since the KOSPI market is closed today({{ds}}).:red_siren:
            """,
            channel=SLACK_CHANNEL,
        )
	)
    check_train_day_task = ShortCircuitOperator(
        task_id='check_train_day_task',
        trigger_rule='one_success',
        python_callable=lambda: True if pendulum.now('Asia/Seoul').day in [1, 15] else False,
        on_success_callback=SlackNotifier(
            slack_conn_id=SLACK_CONNECTION_ID,
            text= """
            :calendar: Today is the day to train the model! :calendar:
            """ if pendulum.now('Asia/Seoul').day in [1, 15] else """
            :calendar: Today is not the day to train the model! :calendar:
            Workflow will be terminated.
            """,
            channel=SLACK_CHANNEL,
        ),
    )
    train_model_task = PythonOperator(
        task_id='train_model_task',
        python_callable=train_model,
		on_execute_callback=SlackNotifier(
			slack_conn_id=SLACK_CONNECTION_ID,
			text="""
			:book: Model training... :book:
            """,
            channel=SLACK_CHANNEL,
        ),
        on_success_callback=SlackNotifier(
			slack_conn_id=SLACK_CONNECTION_ID,
            text="""
			:white_check_mark: Model has finished training based on the updated data!:tada:
            \n MAE Score: {{ti.xcom_pull(task_ids="train_model_task")}} 
            """,
            channel=SLACK_CHANNEL,
        ),
    )
    send_plot_task = SlackAPIFileOperator(
        task_id='send_plot_task',
        slack_conn_id=SLACK_CONNECTION_ID,
        filename="""/opt/airflow/data/plot/plot_{{ds}}.png""",
        filetype='png',
        channels=SLACK_CHANNEL,
    )
	
    get_kospi_data_task >> branch_op >> [get_news_headline_task, stop_op] >> check_train_day_task >> train_model_task >> send_plot_task