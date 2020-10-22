from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.hooks import CsvToPostgresHook
from datetime import datetime, timedelta

from tweet_reader import TweetReader

yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2020, 10, 11),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG('retrieve_tweets', default_args=default_args, schedule_interval='@daily', catchup=False)

def trigger_hook():
    CsvToPostgresHook().copy_rows('./store_files_airflow/*.csv', 'postgres_conn')
    print("done")
# t1 = PythonOperator(task_id='twitter_feed', python_callable=TweetReader().get_all_tweets)
# @TODO: Add xcom to pass twitter screen_name
t1 = PythonOperator(task_id = 'csv_to_postgres', python_callable = trigger_hook, dag=dag)


t1