from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import pymongo as pm

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def PreprocesaCSVSanFrancisco():
    data_temperature = pd.read_csv('/tmp/API/CC2P2-main/v1/data/temperature.csv', names=['San Francisco'], header=0)
    data_temperature.rename(columns={"San Francisco": "TEMPERATURE"}, inplace=True)
    data_time = pd.read_csv('/tmp/API/CC2P2-main/v1/data/temperature.csv', names=['datetime'], header=0)
    data_time.rename(columns={"datetime": "DATETIME"}, inplace=True)
    data_humidity = pd.read_csv('/tmp/API/CC2P2-main/v1/data/humidity.csv', names=['San Francisco'], header=0)
    data_humidity.rename(columns={"San Francisco": "HUMIDITY"}, inplace=True)

    new_data = pd.concat([data_time, data_temperature, data_humidity], axis=1)

    new_data.to_csv("/tmp/API/CC2P2-main/v1/data/SFData.csv", index=False)

def AlmacenaCSVSanFrancisco():
    data = pd.read_csv('/tmp/API/CC2P2-main/v1/data/SFData.csv')
    data_dict = data.to_dict('records')
    client = pm.MongoClient("mongodb+srv://userp2:patadecaballo@cluster0.zehej.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    client.CC2P2SF.SanFranciscoWeather.insert_many(data_dict)


dag = DAG(
    'practica2',
    default_args=default_args,
    description='Flujo practica 2 Cloud Computing',
    schedule_interval=timedelta(days=1),
)


DescargaRepositorio = BashOperator(
    task_id='DescargaRepositorio',
    bash_command='curl -o /tmp/CC2P2-main.zip -LJ https://github.com/Anglepi/CC2P2/archive/refs/heads/main.zip',
    dag=dag,
)

DescomprimeRepo = BashOperator(
    task_id='DescomprimeRepo',
    bash_command='mkdir -p /tmp/API ; unzip -o /tmp/CC2P2-main.zip -d /tmp/API/',
    dag=dag)


DescargaDatosTemp = BashOperator(
    task_id='DescargaDatosTemp',
    bash_command='curl -o /tmp/temperature.csv.zip https://raw.githubusercontent.com/manuparra/MaterialCC2020/master/temperature.csv.zip',
    dag=dag,
)

DescargaDatosHum = BashOperator(
    task_id='DescargaDatosHum',
    bash_command='curl -o /tmp/humidity.csv.zip https://raw.githubusercontent.com/manuparra/MaterialCC2020/master/humidity.csv.zip',
    dag=dag,
)

DescomprimeDatos = BashOperator(
    task_id='DescomprimeDatos',
    bash_command='mkdir -p /tmp/API/CC2P2-main/v1/data; unzip -o /tmp/temperature.csv.zip -d /tmp/API/CC2P2-main/v1/data ; unzip -o /tmp/humidity.csv.zip -d /tmp/API/CC2P2-main/v1/data',
    dag=dag
)

PreprocesaDatos = PythonOperator(
    task_id='PreprocesaDatos',
    python_callable=PreprocesaCSVSanFrancisco,
    op_kwargs={},
    provide_context=True,
    dag=dag
)

AlmacenaDatos = PythonOperator(
    task_id='AlmacenaDatos',
    python_callable=AlmacenaCSVSanFrancisco,
    op_kwargs={},
    provide_context=True,
    dag=dag
)

EntrenaV1 = BashOperator(
    task_id='EntrenaV1',
    bash_command='mkdir -p /tmp/API/CC2P2-main/v1/models ; python3 /tmp/API/CC2P2-main/v1/trainModels.py',
    dag=dag
)

TesteaV1 = BashOperator(
    task_id='TesteaV1',
    bash_command='cd /tmp/API/CC2P2-main/v1/ ; python3 -m pytest tests.py',
    dag=dag
)

ConstruyeV1 = BashOperator(
    task_id='ConstruyeV1',
    bash_command='cd /tmp/API/CC2P2-main/v1/ ; docker-compose down ; docker-compose build',
    dag=dag
)

LevantaV1 = BashOperator(
    task_id='LevantaV1',
    bash_command='cd /tmp/API/CC2P2-main/v1/ ; docker-compose up -d',
    dag=dag
)

TesteaV2 = BashOperator(
    task_id='TesteaV2',
    bash_command='cd /tmp/API/CC2P2-main/v2/ ; python3 -m pytest tests.py',
    dag=dag
)

ConstruyeV2 = BashOperator(
    task_id='ConstruyeV2',
    bash_command='cd /tmp/API/CC2P2-main/v2/ ; docker-compose down ; docker-compose build',
    dag=dag
)

LevantaV2 = BashOperator(
    task_id='LevantaV2',
    bash_command='cd /tmp/API/CC2P2-main/v2/ ; docker-compose up -d',
    dag=dag
)



#Dependencias - Construcción del grafo DAG
[DescargaRepositorio, DescargaDatosTemp, DescargaDatosHum]
DescargaRepositorio >> DescomprimeRepo
[DescargaDatosTemp, DescargaDatosHum] >> DescomprimeDatos >> PreprocesaDatos >> AlmacenaDatos
[AlmacenaDatos, DescomprimeRepo] >> EntrenaV1 >> TesteaV1 >> ConstruyeV1 >> LevantaV1
[AlmacenaDatos, DescomprimeRepo] >> TesteaV2 >> ConstruyeV2 >> LevantaV2