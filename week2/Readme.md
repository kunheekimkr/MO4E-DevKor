# Week2: Apache Airflow

## 1. Airflow 환경 세팅

```bash
docker-compose up
```

Docker Compose를 통해 간단하게 Airflow 서비스를 로컬 환경에서 실행할 수 있다. 다음과 같은 컨테이너가 실행된다.

- `postgres` : airflow DB
- `redis` : Task Queue를 관리하고 Scheduler에서 worker에게 message를 전달하는 broker
- `airflow-webserver` : 8080포트에 웹서버를 열어 UI로 Airflow를 사용할 수 있다.
- `airflow-scheduler` : tasks와 DAGs를 모니터링하고 실행할 Task 스케쥴링
- `airflow-worker` : 스케줄러에 의해 주어진 tasks를 실행
- `airflow-triggerer` : 지연된(Deffered) 태스크를 비동기적으로 모니터링해 완료되면 태스크를 worker에 전달
- `airflow-init` : 서비스 초기화
- `airflow-cli` :CLI를 통해 Airflow 사용
- `flower` :Celery cluster 관리 및 모니터링



### 추가 Dependency 설치하기

Docker-compose 템플릿 내에 친절하게 방법이 설명되어 있다.

```yaml
# In order to add custom dependencies or upgrade provider packages you can use your extended image.
# Comment the image line, place your Dockerfile in the directory where you placed the docker-compose.yaml
# and uncomment the "build" line below, Then run `docker-compose build` to build the images.
```



우선 Conda 환경에 설치된 Dependency들을 Requirements.txt 파일로 추출한다.

```bash
pip list --format=freeze > requirements.txt
```

Airflow 컨테이너 내에 해당 Dependency를 설치할 수 있도록 DockerFile을 작성한다. 로컬 환경과 맞추기 위해 airflow의 latest-python3.8 이미지를 사용하였다.

```dockerfile
FROM apache/airflow:latest-python3.8
COPY requirements.txt .
RUN pip install -r requirements.txt
```

Docker-Compose를 해당 Dockerfile을 이용해 빌드가 이루어지도록 수정한다.

```yaml
# image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.5.3}
  build: .
```





## Volume Mount

데이터를 불러와 처리한 후 CSV에 꾸준히 쌓는 Workflow를 구상하였다. 이를 수행하기 위해 Local 환경의 파일을 불러와, 써야 되는데, Worker는 작업을 Container에서 수행하므로 이를 위해서는 Docker Container에 Volume Mount를 수행해 Local Folder와 Container를 연결해 주어야 한다.

Docker-Compose에서 dag, log, plugin폴더를 mount하는 부분에 data 폴더도 mount하도록 설정하였다.

```yaml
  volumes:
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
    - ${AIRFLOW_PROJ_DIR:-.}/data:/opt/airflow/data
```





## 2. Workflow DAG 작성하기

```python
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
```

Kospi data와 News Headline 두개의 데이터를 매일 수집해 저장하는 간단한 Workflow를 작성하였다. 의존성을 따로 명시하지 않아 두 Task는 병렬적으로 시행된다.



Airflow webserver를 통해 Schedule에 맞춰 제대로 Execution된 것 및 해당 Log를 확인할 수 있다.

![workflow](./images/workflow.png)

분기, Task간 데이터 전달, Slack 알림 연동 등 다양하게 해보고 싶은 것이 있는데 다른 일로 조금 바빴어서 많이 못 해 봤다. 시험기간동안 해봐야겠다.
