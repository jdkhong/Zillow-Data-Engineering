from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2017, 5, 3),
    'email': ['jerrykhong@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dag_1', default_args=default_args, schedule_interval='30 12 * * *')

t1 = BashOperator(
    task_id='scrape_market',
    bash_command='python ~/Programming/zillow/scripts/market_test.py',
    dag=dag)

t2 = BashOperator(
    task_id='scrape_sold',
    bash_command='python ~/Programming/zillow/scripts/zillow_recently_sold.py',
    dag=dag)

t2.set_upstream(t1)
