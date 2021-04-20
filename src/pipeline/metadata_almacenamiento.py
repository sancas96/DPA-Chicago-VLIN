#Este task genera la metadata de almacenamiento que está en s3 y la inserta en rds.
#La metadata es fecha de inserción, tamaño del archivo, tipo de archivo
import luigi
import boto3
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.pipeline.almacenamiento import almacenar
from datetime import *

class metadata_almacenar(CopyToTable):
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
    
    #Tabla y columnas donde ingresará la metadata
    table = 'metadata.metadata_almacenamiento'
    columns = [
                ('fecha_insercion', 'VARCHAR'),
                ('size', 'INTEGER'),
                ('nombre', 'VARCHAR'),
              ]
    
    def requires(self):
        return almacenar(self.tipo_ingesta, self.fecha, self.bucket)    
    
    def rows(self):
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        primer_metadata=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
        #Segunda metadata: tamanio_archivo
        s3_creds = get_s3_credentials('conf/local/credentials.yaml')
        session = boto3.Session(aws_access_key_id=s3_creds['aws_access_key_id'],
                                    aws_secret_access_key=s3_creds['aws_secret_access_key'])
        cliente_s3 = session.client('s3')
        lista_archivos = cliente_s3.list_objects_v2(Bucket = self.bucket, Prefix = 'ingesta')['Contents']
        segundo_metadata = max(lista_archivos, key=lambda x: x['LastModified'])['Size']
        #Tercera metadata: nombre archivo
        tercer_metadata = max(lista_archivos, key=lambda x: x['LastModified'])['Key']
        lista_metadata = [(primer_metadata[0], segundo_metadata, tercer_metadata)]
        print("########### metadata_almacenamiento", lista_metadata)
        #Metemos la información en la base de datos        
        for element in lista_metadata:
            yield element