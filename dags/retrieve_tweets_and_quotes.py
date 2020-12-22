import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.hooks.demo_plugin import CsvToPostgresHook
from datetime import datetime, timedelta
from tweet_reader import TweetReader
from goodreads_reader import GoodreadsReader

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2020, 10, 11),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG('retrieve_tweets_and_quotes', default_args=default_args, schedule_interval='@daily', catchup=False)

def trigger_hook_1(**kwargs):
    tweets = TweetReader().get_all_tweets()
    ti = kwargs['ti']
    ti.xcom_push(key="tweets", value=tweets)

def trigger_hook_2(**kwargs):
    ti = kwargs['ti']
    file_to_read = ti.xcom_pull(key='tweets')
    CsvToPostgresHook().copy_rows('{}'.format(file_to_read), 'twitter_data', 'postgres_conn')

def trigger_hook_3(**kwargs):
    quotes = GoodreadsReader().get_quotes()
    ti = kwargs['ti']
    ti.xcom_push(key="quotes", value=quotes)

def trigger_hook_4(**kwargs):
    ti = kwargs['ti']
    file_to_read = ti.xcom_pull(key='quotes')
    CsvToPostgresHook().copy_rows('{}'.format(file_to_read), 'goodreads_data',  'postgres_conn')

t1 = PythonOperator(task_id='twitter_feed', python_callable=trigger_hook_1, provide_context=True, dag=dag)
t2 = PythonOperator(task_id='csv_to_postgres_1', python_callable=trigger_hook_2, provide_context=True, dag=dag)
t3 = PythonOperator(task_id='goodreads_quotes', python_callable=trigger_hook_3, provide_context=True, dag=dag)
t4 = PythonOperator(task_id='csv_to_postgres_2', python_callable=trigger_hook_4, provide_context=True, dag=dag)


t1 >> t2, t3 >> t4