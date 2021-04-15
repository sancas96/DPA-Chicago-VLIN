from datetime import date, timedelta
from sodapy import Socrata
from src.utils.general import *

import src.utils.constants as constants
import pandas as pd
import boto3
import pickle
import io


def get_client():

    """
    Esta función regresa,
        client: que es el cliente que se puede conectar a la API.
    """

    token=get_api_token('conf/local/credentials.yaml')['api_token']
    client = Socrata(constants.url_api,token)
    return client


def get_s3_resource():

    """
    Esta función regresa,
        s3: un resource de S3 para poder guardar datos en el bucket.
    """

    s3_creds= get_s3_credentials('conf/local/credentials.yaml')
    session = boto3.Session(
        aws_access_key_id=s3_creds['aws_access_key_id'],
        aws_secret_access_key=s3_creds['aws_secret_access_key'])
    s3 = session.client('s3')
    return s3


def ingesta_inicial(client,limite):
    """
    Esta función recibe como parámetros:
        client: el cliente con el que nos podemos comunicar con la API,
        limite: el límite de registros que queremos obtener al llamar a la API

    Regresa:
        datos_binario: una lista de los elementos que la API regresó.
    """
    datos=client.get(constants.id_data_set,limit=limite)
    datos_binario=io.BytesIO()
    pickle.dump(datos, datos_binario)
    datos_binario.seek(0)
    return datos_binario

    
def ingesta_consecutiva(client,fecha,limite, delta=True):
    """
    Esta función recibe como parámetros
        client: el cliente con el que nos podemos comunicar con la API,
        fecha: la fecha de la que se quieren obtener nuevos datos al llamar a la API,
        limit: el límite de registros para obtener de regreso.
    """
    if delta == True:
        today = date.today()
        delta_date = today - timedelta(days=constants.dias_ingesta)
        where = f"inspection_date>='{delta_date}'"
        datos = client.get(constants.id_data_set, limit=limite, where=where)
    else:
        datos=client.get(constants.id_data_set, limit=limite, where=f"inspection_date='{fecha}'")

    datos_binario=io.BytesIO()
    pickle.dump(datos, datos_binario)
    datos_binario.seek(0)
    return datos_binario


def guardar_ingesta(data, bucket, bucket_path):
    """
    Esta función recibe como parámetros:
        data: los datos ingestados en formato .pkl,
        bucket: nombre del bucket de S3,
        bucket_path: la ruta y nombre del bucket donde se guardarán los datos, la función agrega un sufijo con fecha de carga.
    """
    get_s3_resource().upload_fileobj(data, bucket, f"{bucket_path}{date.today()}.pkl")
    pass


def get_service():

    """
    Esta función regresa,
        esta funcion regresa los datos para ingresar a la rds
    """
    user = credentials['user']
    password = credentials['password']
    database = credentials['database']
    host = credentials['host']
    port = credentials['port']
    service=get_service_file('conf/local/credentials.yaml')['service_file']
    pass

