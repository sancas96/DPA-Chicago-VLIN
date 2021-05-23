#Este código hace las pruebas unitarias de la ingeniería de características, toma como entrada la base a la que se le hizo la ingeniería y como salida genera metadata de la prueba unitaria que en este caso son los parámetros de lugi.
import luigi
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.utils.test_seleccionar import *
from src.pipeline.seleccion import seleccionar
from datetime import *
import pandas as pd
import boto3
import pickle

class test_seleccionar(CopyToTable):
    #Parámetros de las tareas anteriores y se agrega uno nuevo
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
        return seleccionar(self.tipo_ingesta, self.fecha, self.bucket, self.tamanio,self.proceso)

    def rows(self):
        if self.proceso=='entrenamiento':
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
            probs=pickle.loads(contenido_objeto).predict(datos_selecc.drop(['results'], axis=1))
            datos=pd.DataFrame(probs, columns = ['Probabilidad_predicha'])

            #Esta es la prueba unitaria
    #         if self.tipo_prueba=="infinito":
    #             test_selecciona(datos).test_noinfs()
    #         else:
    #             test_selecciona(datos).test_shape()

            test_selecciona(datos).test_noinfs()

            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            primer_metadata=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
            segundo_metadata="infinito"
            tercer_metadata="test_seleccion"
            lista_metadata = [(primer_metadata[0], segundo_metadata, tercer_metadata)]

            #Metemos la información en la base de datos        
            for element in lista_metadata:
                yield element
        else:
            exit()