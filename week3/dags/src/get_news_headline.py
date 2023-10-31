from datetime import date
import requests
from bs4 import BeautifulSoup
import csv


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