#Este código hace las pruebas unitarias del set de entrenamiento, toma como entrada lo almacenado y como salida genera metadata de la prueba unitaria, que es el tamaño del objeto en s3
import luigi
import boto3
from io import BytesIO
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.utils.test_entrenar import *
from src.pipeline.entrenamiento import entrenar
from datetime import *

class test_entrenar(CopyToTable):
    #Parámetros de las tareas anteriores
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

    #Tabla y columnas donde ingresará la metadata
    table = 'test.pruebas_unitarias'
    columns = [
                ('fecha_insercion', 'VARCHAR'),
                ('size_param', 'VARCHAR'),
                ('nombre_prueba', 'VARCHAR')
              ]

    def requires(self):
        return entrenar(self.tipo_ingesta, self.fecha, self.bucket, self.tamanio, self.proceso)

    def rows(self):
        if self.proceso=='entrenamiento':
            s3_creds = get_s3_credentials('conf/local/credentials.yaml')
            session = boto3.Session(aws_access_key_id=s3_creds['aws_access_key_id'],
                                        aws_secret_access_key=s3_creds['aws_secret_access_key'])
            cliente_s3 = session.client('s3')
            modelo_xgb = cliente_s3.get_object(Bucket=f'{self.bucket}',Key=f'entrenamiento/{self.fecha}-modelo_xgb.pkl')
            modelo_ls = cliente_s3.get_object(Bucket=f'{self.bucket}',Key=f'entrenamiento/{self.fecha}-modelo_lr.pkl')
            modelo_knn = cliente_s3.get_object(Bucket=f'{self.bucket}',Key=f'entrenamiento/{self.fecha}-modelo_knn.pkl')

            unitaria1=test_entrena().test_tamanio(nombre_archivo=BytesIO(modelo_xgb['Body'].read()),tamanio_archivo=self.tamanio)
            unitaria2=test_entrena().test_tamanio(nombre_archivo=BytesIO(modelo_ls['Body'].read()),tamanio_archivo=self.tamanio)
            unitaria3=test_entrena().test_tamanio(nombre_archivo=BytesIO(modelo_knn['Body'].read()),tamanio_archivo=self.tamanio)

            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            primer_metadata1=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
            segundo_metadata1=self.tamanio
            tercer_metadata1="test_entrenar_xgb"

            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            primer_metadata2=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
            segundo_metadata2=self.tamanio
            tercer_metadata2="test_entrenar_lr"

            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            primer_metadata3=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
            segundo_metadata3=self.tamanio
            tercer_metadata3="test_entrenar_knn"

            lista_metadata = [
                                (primer_metadata1[0], segundo_metadata1, tercer_metadata1), \
                                (primer_metadata2[0], segundo_metadata2, tercer_metadata2), \
                                (primer_metadata3[0], segundo_metadata3, tercer_metadata3)
                             ]


            #Metemos la información en la base de datos        
            for element in lista_metadata:
                yield element
        else:
            exit()