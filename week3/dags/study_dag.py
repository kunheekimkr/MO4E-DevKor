import os
from datetime import timedelta, datetime, date
from pprint import pprint
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator


import os
import pendulum
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator

from src.get_news_headline import get_news_headline
from src.get_kospi_data import get_kospi_data


seoul_time = pendulum.timezone('Asia/Seoul')
dag_name = os.path.basename(__file__).split('.')[0]

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
    )
    get_news_headline_task = PythonOperator(
        task_id='get_news_headline_task',
        python_callable=get_news_headline,
    )
    branch_op = BranchPythonOperator(
	    task_id="branch_task",
	    python_callable=branch_func,
    )
    stop_op = EmptyOperator(task_id="stop_task")
	
    get_kospi_data_task >> branch_op >> [get_news_headline_task, stop_op]
	
