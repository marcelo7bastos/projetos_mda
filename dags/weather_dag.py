from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash   import BashOperator 
from airflow.operators.python import PythonOperator
import os
import json
import pandas as pd

def clean_data(**kwargs):
    file_name = str(datetime.now().date()) + '.json'
    tot_name = os.path.join(os.path.dirname(__file__), 'src/data', file_name)
    
    with open(tot_name, 'r') as inputfile:
        doc = json.load(inputfile)
    
    # extract data
    df_raw = {
        'name': doc['location']['name'],
        'region': doc['location']['region'],
        'country': doc['location']['country'],
        'lat': doc['location']['lat'],
        'lon': doc['location']['lon'],
        'temp_c': doc['current']['temp_c'],
        'wind_mph': doc['current']['wind_mph'],
        'pressure_mb': doc['current']['pressure_mb'],
        'humidity': doc['current']['humidity'],
        'cloud': doc['current']['cloud'],
        'feelslike_c': doc['current']['feelslike_c'],
    }
    
    # convert to dataframe
    df = pd.DataFrame(df_raw, index=[0])
    
    # save to folder
    end_path = os.path.join(os.path.dirname(__file__), 'src/data', 'weather.csv')
    df.to_csv(end_path, index=False)

# define the dag arguments
default_args = {
    'owner': 'Marcelo',
    'depends_on_past': False,
    'email': ['marceloc.bastos@hotmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}

# define the dag
dag = DAG(
    dag_id='weather_dag',
    default_args=default_args,
    start_date=datetime(2024, 7, 29),
    schedule_interval=timedelta(minutes=60)
)

# first task is to query get the weather from API
task1 = BashOperator(
    task_id='get_weather',
    bash_command='python /home/mcb/code/marcelo7bastos/airflow_mda/dags/src/get_weather.py',
    dag=dag
)

# second task - Data transformation
task2 = PythonOperator(
    task_id='clean_data',
    python_callable=clean_data,
    provide_context=True,
    dag=dag
)

# tasks dependency
task1 >> task2 
