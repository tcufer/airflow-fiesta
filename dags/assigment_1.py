from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "tomaz",
    "depends_on_past": False,
    "start_date": datetime(2020, 5, 16),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
# Instantiate DAG
dag = DAG("asgmnt_1", default_args=default_args, schedule_interval=timedelta(1))

# t1 task that creates new directory
t1 = BashOperator(task_id="create_dir", bash_command="mkdir test_dir", dag=dag)
