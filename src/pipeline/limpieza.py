#Este task limpia el delta y lo mete a la RDS.
import luigi
import pickle
import boto3
import pandas as pd
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.utils.limpiar import *
from src.pipeline.almacenamiento import almacenar
from src.pipeline.metadata_almacenamiento import metadata_almacenar

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
    
    table = 'data.limpieza'
    columns = [
                ('inspection_id', 'VARCHAR'),
                ('dba_name', 'VARCHAR'),
                ('aka_name', 'VARCHAR'),
                ('license_', 'VARCHAR'),
                ('facility_type', 'VARCHAR'),
                ('risk', 'VARCHAR'),
                ('address', 'VARCHAR'),
                ('city', 'VARCHAR'),
                ('state', 'VARCHAR'),
                ('zip', 'VARCHAR'),
                ('inspection_date', 'VARCHAR'),
                ('inspection_type', 'VARCHAR'),
                ('results', 'VARCHAR'),
                ('violations', 'VARCHAR'),
                ('latitude', 'VARCHAR'),
                ('longitude', 'VARCHAR'),
                ('location_latitude', 'VARCHAR'),
                ('location_longitude', 'VARCHAR')
            ]
    
    def requires(self):
        return metadata_almacenar(self.tipo_ingesta, self.fecha, self.bucket)    
    
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
            
#         with almacenar(self.tipo_ingesta, self.fecha, self.bucket).output().open() as infile, pd.DataFrame().open('w') as outfile:
#             datos_pkl.write(infile.read())
            
 
            
        datos_dataframe=pd.json_normalize(datos_pkl)
        print("########### limpieza", datos_dataframe)
        datos_limpieza=DataCleanning(datos_dataframe).cleanning()
        print("########### limpieza", datos_dataframe)
        datos_lista=datos_limpieza.values.tolist()
        print("########### limpieza", datos_lista)

        for element in datos_lista:
            yield element