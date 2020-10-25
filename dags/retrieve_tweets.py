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

def trigger_hook_1(**kwargs):
    tweets = TweetReader().get_all_tweets
    ti = kwargs['ti']
    ti.xcom_push(key="tweets", value=tweets)

def trigger_hook_2(**kwargs):
    ti = kwargs['ti']
    file_to_read = ti.xcom_pull(key='message', task_ids='new_push_task')
    CsvToPostgresHook().copy_rows('./store_files_airflow/{}.csv'.format(file_to_read), 'postgres_conn')
    print("done")

t1 = PythonOperator(task_id='twitter_feed', python_callable=trigger_hook_1, provide_context=True, dag=dag)
t2 = PythonOperator(task_id = 'csv_to_postgres', python_callable = trigger_hook_2, provide_context=True, dag=dag)


t1 >> t2