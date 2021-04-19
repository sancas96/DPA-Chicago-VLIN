#Este task limpia el delta y lo mete a la RDS.
import luigi
import pickle
import boto3
import pandas as pd
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.utils.limpiar import *
from src.pipeline.almacenamiento import almacenar

class limpiar(CopyToTable):
    #Parámetros de las tareas anteriores
    tipo_ingesta = luigi.Parameter() #Puede ser "historica" o "consecutiva".
    fecha = luigi.Parameter() #Fecha en la que se está haciendo la ingesta con respecto a inspection date.
    bucket = luigi.Parameter()
    
    #Obteniendo las credenciales para conectarse a la base de datos de chicago
    db_creds = get_database_connection('conf/local/credentials.yaml')
    user = db_creds['user']
    password = db_creds['password']
    database = db_creds['database']
    host = db_creds['host']
    port = db_creds['port']
    
    table = 'prueba2'
    columns = [
                ('col_1', 'VARCHAR'),
                ('col_2', 'VARCHAR'),
                ('col_3', 'VARCHAR'),
                ('col_4', 'VARCHAR'),
                ('col_5', 'VARCHAR'),
                ('col_6', 'VARCHAR'),
                ('col_7', 'VARCHAR'),
                ('col_8', 'VARCHAR'),
                ('col_9', 'VARCHAR'),
                ('col_10', 'VARCHAR'),
                ('col_11', 'VARCHAR'),
                ('col_12', 'VARCHAR'),
                ('col_13', 'VARCHAR'),
                ('col_14', 'VARCHAR'),
                ('col_15', 'VARCHAR'),
                ('col_16', 'VARCHAR'),
                ('col_17', 'VARCHAR'),
                ('col_18', 'VARCHAR')
            ]
    
    def requires(self):
        return almacenar(self.tipo_ingesta, self.fecha, self.bucket)    
    
    def rows(self):
        #Generamos una conexión al bucket de s3
        s3_creds = get_s3_credentials("conf/local/credentials.yaml")
        session = boto3.Session(aws_access_key_id=s3_creds['aws_access_key_id'],
                                    aws_secret_access_key=s3_creds['aws_secret_access_key'])
        cliente_s3 = session.client('s3')
        
        #Obtenemos los datos
        with open('archivo_io', 'wb') as obtiene_datos:
            cliente_s3.download_fileobj(self.bucket, f"ingesta/{self.tipo_ingesta}-{self.fecha}.pkl", obtiene_datos)
            
        with open('archivo_io', 'rb') as obtiene_datos:
            datos_pkl = pickle.load(obtiene_datos)
    
        datos_dataframe=pd.json_normalize(datos_pkl)
        datos_limpieza=DataCleanning(datos_dataframe).cleanning()
        datos_lista=datos_limpieza.values.tolist()

        for element in datos_lista:
            yield element