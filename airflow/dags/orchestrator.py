from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
import sys
sys.path.append('/opt/airflow/api_requests')
from insert_records import main
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    "description": "a dag to orchestrate weather data pipeline",
    "start_date": datetime(2026, 1, 10),
    "catchup": False,
}

dag = DAG(
    dag_id = "weather_api_dbt_orchestrator",
    default_args = default_args,
    schedule=timedelta(minutes=5)
)

with dag:
    task1 = PythonOperator(
        task_id='ingest_weather_data_task',
        python_callable=main,
    )

    task2 = DockerOperator(
        task_id='transform_data_task',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='run',
        working_dir='/usr/app',
        mounts=[
            Mount(source='/home/elhadi/repos/weather_data_pipeline/.dbt/my_project', target='/usr/app', type='bind'),
            Mount(source='/home/elhadi/repos/weather_data_pipeline/.dbt', target='/root/.dbt', type='bind')
        ],
        network_mode='weather_data_pipeline_my_network',
        docker_url='unix://var/run/docker.sock',
        auto_remove='success',
    )

    task1 >> task2