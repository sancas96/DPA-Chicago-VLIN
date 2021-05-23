#Este task calcula los sesgos e inequidades del modelo, en este caso punitivo.
#Como entrada es la tabla de feature engineering, como salida tabla en rds data.sesgo_ineq con los campos necesarios.
import luigi
import pickle
import pandas as pd
import boto3
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.utils.sesgo_ineq import *
from src.pipeline.metadata_seleccion import metadata_seleccionar

class sesgo(CopyToTable):
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
    table = 'data.sesgo_inequidad'
    columns = [
                ('attribute_name', 'VARCHAR'),
                ('attribute_value','VARCHAR'),
                ('fdr','VARCHAR'),
                ('fpr','VARCHAR'),
                ('fdr_disparity','VARCHAR'),
                ('fpr_disparity','VARCHAR'),
                ('FDR_Parity','VARCHAR'),
                ('FPR_Parity','VARCHAR'),
                ('Statistical_Parity','VARCHAR')
              ]

    def requires(self):
        return metadata_seleccionar(self.tipo_ingesta, self.fecha, self.bucket, self.tamanio, self.proceso)


    def rows(self):
        if self.proceso=='entrenamiento':
            datos_sesgo=pd.DataFrame(query_database("Select license_, results, facility_type from data.ingenieria"))
            datos_sesgo.columns=['entity_id','label_value','facility_type']

            #Obtenemos la predicción del mejor modelo.
            s3_creds = get_s3_credentials('conf/local/credentials.yaml')
            session = boto3.Session(aws_access_key_id=s3_creds['aws_access_key_id'],
                                        aws_secret_access_key=s3_creds['aws_secret_access_key'])
            cliente_s3 = session.client('s3')
            objeto_s3 = cliente_s3.get_object(
                                                Bucket=f"{self.bucket}",
                                                Key=f"seleccion/{self.fecha}-MejorModelo.pkl"
                                             )
            contenido_objeto=objeto_s3['Body'].read()
            datos_selecc= pd.DataFrame(query_database("SELECT * from data.ingenieria;"))
            datos_selecc.columns=[i[0] for i in query_database("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where table_name='ingenieria';")]
            datos_selecc[datos_selecc.columns]=datos_selecc[datos_selecc.columns].apply(pd.to_numeric, errors='coerce')
            datos_selecc=datos_selecc.fillna(0)
            probs=pickle.loads(contenido_objeto).predict(datos_selecc.drop(['results'], axis=1))
            datos=pd.DataFrame(probs, columns = ['score'])
            datos_sesgo['score']=datos

            #Aplicando función de sesgo e inequidad.
            datos_sesgo=SesgIneq(datos_sesgo).sesgar()

            #Obtenemos los datos
            datos_lista=datos_sesgo.values.tolist()

            for element in datos_lista:
                yield element
        else:
            exit()
