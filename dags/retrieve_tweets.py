from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

from all_tweets import get_all_tweets

yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2020, 10, 11),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG('store_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

  t1 = PythonOperator(task_id='twitter_feed', python_callable=get_all_tweets)

t1
