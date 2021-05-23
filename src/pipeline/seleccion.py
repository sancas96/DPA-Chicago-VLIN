#Este task hace la selección del mejor modelo, de acuerdo a la precisión.
import luigi
import luigi.contrib.s3
import pandas as pd
from src.utils.general import *
from src.utils.seleccionar import *
from src.pipeline.metadata_entrenamiento import metadata_entrenar
import pickle


class seleccionar(luigi.Task):
    #Parámetros de las tareas anteriores
    tipo_ingesta = luigi.Parameter() #Puede ser "historica" o "consecutiva".
    fecha = luigi.Parameter() #Fecha en la que se está haciendo la ingesta con respecto a inspection date.
    bucket = luigi.Parameter()
    tamanio= luigi.IntParameter()
    proceso= luigi.Parameter() #Puede ser "entrenamiento" o "prediccion"
    
#     #Obteniendo las credenciales para conectarse a la base de datos de chicago
#     db_creds = get_database_connection('conf/local/credentials.yaml')
#     user = db_creds['user']
#     password = db_creds['password']
#     database = db_creds['database']
#     host = db_creds['host']
#     port = db_creds['port']
    
#     #Tabla y columnas donde ingresará la metadata
#     table = 'data.seleccion'
#     columns = [
#                 ('fecha_insercion', 'VARCHAR'),
#                 ('modelo_seleccionado', 'VARCHAR'),
#                 ('precision','NUMERIC')
#               ]
    
    def requires(self):
        return metadata_entrenar(self.tipo_ingesta, self.fecha, self.bucket, self.tamanio, self.proceso)
    
    def run(self):
        if self.proceso=='entrenamiento':
        
    #         with open('data/precision_modelos.pkl', 'rb') as pickle_file:
    #             diccionario = pickle.load(pickle_file)

            datos_selecc= pd.DataFrame(query_database("SELECT * from data.ingenieria;"))
            datos_selecc.columns=[i[0] for i in query_database("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where table_name='ingenieria';")]
            datos_selecc[datos_selecc.columns]=datos_selecc[datos_selecc.columns].apply(pd.to_numeric, errors='coerce')
            datos_selecc=datos_selecc.fillna(0)
            #Aplicamos la función selección, que busca la máxima accuracy
            seleccion=selecciona(datos_selecc).seleccion()

            if seleccion[0]=='XGB':
                with open('data/entrenamiento_xgb.pkl','rb') as infile, self.output().open('w') as outfile:
                    outfile.write(infile.read())
            elif seleccion[0]=='LR':
                with open('data/entrenamiento_lr.pkl','rb') as infile, self.output().open('w') as outfile:
                    outfile.write(infile.read())
            else:
                with open('data/entrenamiento_knn.pkl','rb') as infile, self.output().open('w') as outfile:
                    outfile.write(infile.read())
        else:
            exit()
        
    def output(self):
        s3_creds = get_s3_credentials('conf/local/credentials.yaml')
        cliente_s3 = luigi.contrib.s3.S3Client(s3_creds['aws_access_key_id'],s3_creds['aws_secret_access_key'])
        output_path = f"s3://{self.bucket}/seleccion/{self.fecha}-MejorModelo.pkl"
        return luigi.contrib.s3.S3Target(path=output_path,client=cliente_s3,format=luigi.format.Nop)