#Este task inserta metadata para la parte de selección del modelo, son 2 metadatas:
#fecha de inserción, número de registros.
import luigi
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.pipeline.test_seleccion import test_seleccionar
from datetime import datetime
import pandas as pd
import boto3
import pickle

class metadata_seleccionar(CopyToTable):
    #Parámetros de las tareas anteriores
    tipo_ingesta = luigi.Parameter()
    fecha = luigi.Parameter() 
    bucket = luigi.Parameter()
    tamanio= luigi.IntParameter()
    proceso= luigi.Parameter() #Puede ser "entrenamiento" o "prediccion"
    

    #Obteniendo las credenciales para conectarse a la base de datos de chicago
    db_creds = get_database_connection('conf/local/credentials.yaml')
    user = db_creds['user']
    password = db_creds['password']
    database = db_creds['database']
    host = db_creds['host']
    port = db_creds['port']

    #Tabla y columnas donde ingresará la metadata
    table = 'metadata.metadata_seleccionar'
    columns = [
                ('fecha_insercion', 'VARCHAR'),
                ('num_registros', 'INTEGER')
              ]

    def requires(self):
        return test_seleccionar(self.tipo_ingesta, self.fecha, self.bucket, self.tamanio, self.proceso)

    def rows(self):
        if self.proceso=='entrenamiento':
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            primer_metadata=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos

            s3_creds = get_s3_credentials('conf/local/credentials.yaml')
            session = boto3.Session(aws_access_key_id=s3_creds['aws_access_key_id'],
                                        aws_secret_access_key=s3_creds['aws_secret_access_key'])
            cliente_s3 = session.client('s3')
            objeto_s3 = cliente_s3.get_object(
                                                Bucket=self.bucket,
                                                Key=f'seleccion/{self.fecha}-MejorModelo.pkl'
                                             )
            contenido_objeto=objeto_s3['Body'].read()
            datos_selecc= pd.DataFrame(query_database("SELECT * from data.ingenieria;"))
            datos_selecc.columns=[i[0] for i in query_database("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where table_name='ingenieria';")]
            datos_selecc[datos_selecc.columns]=datos_selecc[datos_selecc.columns].apply(pd.to_numeric, errors='coerce')
            datos_selecc=datos_selecc.fillna(0)
            segundo_metadata=pickle.loads(contenido_objeto).predict(datos_selecc.drop(['results'], axis=1)).size
            lista_metadata = [(primer_metadata[0], segundo_metadata)]

            #Metemos la información en la base de datos        
            for element in lista_metadata:
                yield element
        else:
            exit()