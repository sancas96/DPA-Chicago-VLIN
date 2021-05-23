#Este task inserta en el esquema monitoreo los campos necesarios para el dashboard con respecto al entrenamiento del modelo.
import luigi
import pickle
import pandas as pd
import boto3
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.pipeline.metadata_sesgo_ineq import metadata_sesg_ineq

class monitoreo_entrena(CopyToTable):
    tipo_ingesta = luigi.Parameter() #Puede ser "historica" o "consecutiva".
    fecha = luigi.Parameter() #Fecha en la que se está haciendo la ingesta con respecto a inspection date.
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

    #Tabla y columnas donde se creará la tabla predicción
    table = 'monitoreo.restaurante_scores'
    columns = [
                ('inspection_id', 'VARCHAR'),
                ('fecha_parametro','VARCHAR'),
                ('facility_type', 'VARCHAR'),
                ('entrenamiento', 'VARCHAR'),
                ('prediccion', 'VARCHAR')
              ]
    
    def requires(self):
        return metadata_sesg_ineq(self.tipo_ingesta, self.fecha, self.bucket, self.tamanio, self.proceso)

    def rows(self):
        if self.proceso=='entrenamiento':
            #Obtenemos la predicción del mejor modelo de toda la tabla de ingenieria.
            s3_creds = get_s3_credentials('conf/local/credentials.yaml')
            session = boto3.Session(aws_access_key_id=s3_creds['aws_access_key_id'],
                                    aws_secret_access_key=s3_creds['aws_secret_access_key'])
            cliente_s3 = session.client('s3')
            objeto_s3 = cliente_s3.get_object(
                                                Bucket=f"{self.bucket}",
                                                Key=f"seleccion/{self.fecha}-MejorModelo.pkl"
                                             )
            contenido_objeto=objeto_s3['Body'].read()

            datos_predic= pd.DataFrame(query_database("SELECT * from data.ingenieria;"))
            datos_predic.columns=[i[0] for i in query_database("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where table_name='ingenieria';")]
            datos_predic[datos_predic.columns]=datos_predic[datos_predic.columns].apply(pd.to_numeric, errors='coerce')
            datos_predic=datos_predic.fillna(0)
            probabilidades=pickle.loads(contenido_objeto).predict(datos_predic.drop(['results'], axis=1))

            #Trayéndonos los campos que nos interesan de la tabla de limpieza
            datos_entrena= pd.DataFrame(query_database("select inspection_id,fecha_parametro, facility_type, 1 as entrenamiento from data.limpieza;"))
            datos_entrena.columns=['inspection_id','fecha_parametro','facility_type','entrenamiento']

            lista_monitoreo=datos_entrena.values.tolist()

            for i in range(len(lista_monitoreo)):
                lista_monitoreo[i].append(probabilidades[i])

            for element in lista_monitoreo:
                yield element
            
        else:
            exit()