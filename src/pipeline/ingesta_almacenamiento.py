from datetime import date
from sodapy import Socrata
from src.utils.general import *

import boto3
import pickle
import io


def get_client():

    """
    Esta función regresa un
        client: cliente que se puede conectar a la API
    """

    token=get_api_token('conf/local/credentials.yaml')['api_token']
    client = Socrata('data.cityofchicago.org',token)
    return client


def get_s3_resource():

    """
    Esta función regresa
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
        limmit: el límite de registros que queremos obtener al llamar a la API

    Regresa:
        datos_binario: una lista de los elementos que la API regresó.
    """
    datos=client.get('4ijn-s7e5', limit=limite)
    datos_binario=io.BytesIO()
    pickle.dump(datos, datos_binario)
    datos_binario.seek(0)
    return datos_binario

    
def ingesta_consecutiva(client,fecha,limite):
    """
    Esta función recibe como parámetros
        client: el cliente con el que nos podemos comunicar con la API,
        fecha: la fecha de la que se quieren obtener nuevos datos al llamar a la API,
        limit: el límite de registros para obtener de regreso.
    """
    datos=client.get('4ijn-s7e5', limit=limite, where=f"inspection_date='{fecha}'")
    datos_binario=io.BytesIO()
    pickle.dump(datos, datos_binario)
    datos_binario.seek(0)
    return datos_binario


def guardar_ingesta(data, bucket, bucket_path):
    """
    Esta función recibe como parámetros:
        data: los datos ingestados en pkl,
        bucket: nombre de tu bucket de S3,
        bucket_path: la ruta en el bucket en donde se guardarán los datos.
    """
    get_s3_resource().upload_fileobj(data, bucket, f"{bucket_path}{date.today()}.pkl")
    pass