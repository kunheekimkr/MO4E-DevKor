import os
from datetime import timedelta, datetime, date
from pprint import pprint
import csv
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

from pykrx import stock
import requests
from bs4 import BeautifulSoup
import datetime


dag_name = os.path.basename(__file__).split('.')[0]
default_args = {
    'owner': 'Kunhee Kim',
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

def get_kospi_data(**kwargs):
    ## Get today's date
    today = date.today().strftime("%Y%m%d")
    ## Get KOSPI Data
    df = stock.get_index_ohlcv(today, today, "1001")

    ## Check if df is empty
    if df.empty:
        print("df is empty")
        return()

    ## Data Preprocessing
    ## Drop '거래대금', '상장시가총액'
    df = df.drop(['거래대금', '상장시가총액'], axis=1)
    ## '종가' Column을 맨 뒤로 이동
    cols = list(df.columns.values)
    cols.pop(cols.index('종가'))
    df = df[cols+['종가']]

    df.to_csv('/opt/airflow/data/stockdata.csv', mode='a', header=False)

def get_news_headline(**kwargs):
    BASE_URL = 'https://media.naver.com/press/001/ranking?type=popular&date='
    ## Get today's date
    today = date.today().strftime("%Y%m%d")

    f = open('/opt/airflow/data/headlines.csv', 'a', encoding='utf-8', newline='')
    wr = csv.writer(f)
    
    response = requests.get(BASE_URL + today)
    html = response.text

    ## parse class "press_ranking_list"
    soup = BeautifulSoup(html, 'html.parser')
    ranking_list = soup.select('.list_title')
    headlines = []
    ## parse all text in ranking_list
    for headline in ranking_list:
        headlines.append(headline.text)
    headlines.insert(0, today)
    wr.writerow(headlines)
    f.close()


with DAG(
    dag_id=dag_name,
    default_args=default_args,
    description='Get KOSPI & New Headline Data and append to previous data every 6pm on weekdays',
    schedule_interval='0 9 * * MON-FRI', ## 18:00 KST = 09:00 UTC
    start_date= datetime.datetime(2023, 10, 1, 00, 00),
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