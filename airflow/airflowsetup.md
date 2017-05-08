sudo apt-get install build-essential libsasl2-dev binutils
sudo easy_install -U setuptools
export AIRFLOW_HOME=~/airflow
sudo pip install airflow[s3,python]

airflow initdb
cd airflow/
mkdir dags
mkdir logs

vim airflow.cfg
airflow webserver
airflow scheduler

#test
python airflowdag.py airflow test dag_1 scrape_market 2017-0
