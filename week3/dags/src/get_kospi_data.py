from datetime import date, datetime
from pykrx import stock

def get_kospi_data(**kwargs):
    ## Get today's date
    today = date.today().strftime("%Y%m%d")
    #today = datetime(2023,10,29,18,0,0) # Test용 (주말)

    ## Get KOSPI Data
    df = stock.get_index_ohlcv(today, today, "1001")

    ## Check if df is empty
    if df.empty: ## 주식 시장이 열리지 않은 날
        print("df is empty")
        return(False) 

    ## Data Preprocessing
    ## Drop '거래대금', '상장시가총액'
    df = df.drop(['거래대금', '상장시가총액'], axis=1)
    ## '종가' Column을 맨 뒤로 이동
    cols = list(df.columns.values)
    cols.pop(cols.index('종가'))
    df = df[cols+['종가']]

    df.to_csv('/opt/airflow/data/stockdata.csv', mode='a', header=False)
    return(True) ## 주식 시장이 열린 날