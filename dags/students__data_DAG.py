from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.mysql_operator import MySqlOperator
from airflow.contrib.sensors.file_sensor import FileSensor

default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2020, 6, 13),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG('students_data_dag',default_args=default_args,schedule_interval='@daily', template_searchpath=['/usr/local/airflow/sql_files'], catchup=True) as dag:


    t1 = FileSensor(
        task_id='check_file_exists',
        filepath='/usr/local/airflow/store_files_airflow/students_list.csv',
        fs_conn_id='fs_default',
        poke_interval=10,
        timeout=150,
        soft_fail=True
    )

    t2 = MySqlOperator(task_id='create_mysql_table', mysql_conn_id="mysql_conn", sql="create_table_students.sql")

    t3 = MySqlOperator(task_id='insert_into_table', mysql_conn_id="mysql_conn", sql="insert_students.sql")

    t4 = MySqlOperator(task_id='backup_copy_table', mysql_conn_id="mysql_conn", sql="backup_students.sql")

    t1 >> t2 >> t3 >> t4
