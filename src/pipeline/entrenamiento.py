#Este task entrena 3 modelos y pone como salida en el s3  
import luigi
import pandas as pd
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.utils.entrenar import *
from src.pipeline.metadata_ingenieria_caract import metadata_ingenieria

class entrenar(luigi.Task):
    #Parámetros de las tareas anteriores
    tipo_ingesta = luigi.Parameter() #Puede ser "historica" o "consecutiva".
    fecha = luigi.Parameter() #Fecha en la que se está haciendo la ingesta con respecto a inspection date.
    bucket = luigi.Parameter()
    tamanio = luigi.IntParameter()
    tipo_prueba = luigi.Parameter()
    
    #Obteniendo las credenciales para conectarse a la base de datos de chicago
    def requires(self):
        return metadata_ingenieria(self.tipo_ingesta, self.fecha, self.bucket, self.tamanio, self.tipo_prueba)    
    
            
    def run(self):
        datos_entrenar= pd.DataFrame(query_database("SELECT * from data.ingenieria;"))
        datos_entrenar.columns=[i[0] for i in query_database("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where table_name='ingenieria';")]
        #Cambiando todas las columnas a numérico
        datos_entrenar[datos_entrenar.columns]=datos_entrenar[datos_entrenar.columns].apply(pd.to_numeric, errors='coerce')
        datos_entrenar=datos_entrenar.fillna(0)
        #Ejecutamos el entrenamiento
        MLModeling(datos_entrenar).modeling()
        
        with open('data/entrenamiento_xgb.pkl','rb') as infile, self.output()['outfile_xgb'].open('w') as outfile:
            outfile.write(infile.read())
            
        with open('data/entrenamiento_lr.pkl','rb') as infile, self.output()['outfile_lr'].open('w') as outfile:
            outfile.write(infile.read())
        
        with open('data/entrenamiento_knn.pkl','rb') as infile, self.output()['outfile_knn'].open('w') as outfile:
            outfile.write(infile.read())
            
#         with open('data/entrenamiento_xgb_parametros.pkl','rb') as infile, self.output()['params_xgb'].open('w') as outfile:
#             outfile.write(infile.read())
            
#         with open('data/entrenamiento_lr_parametros.pkl','rb') as infile, self.output()['params_lr'].open('w') as outfile:
#             outfile.write(infile.read())
        
#         with open('data/entrenamiento_knn_parametros.pkl','rb') as infile, self.output()['params_knn'].open('w') as outfile:
#             outfile.write(infile.read())
            
#         with open('data/precision_modelos.pkl','rb') as infile, self.output()['precision_modelos'].open('w') as outfile:
#             outfile.write(infile.read())
        
            
    def output(self):
        s3_creds = get_s3_credentials('conf/local/credentials.yaml')
        cliente_s3 = luigi.contrib.s3.S3Client(s3_creds['aws_access_key_id'],s3_creds['aws_secret_access_key'])
        output_path = f"s3://{self.bucket}/entrenamiento/{self.fecha}"
        return {
                    'outfile_xgb' : luigi.contrib.s3.S3Target(path=output_path + "-modelo_xgb.pkl",client=cliente_s3,format=luigi.format.Nop), \
                    'outfile_lr' : luigi.contrib.s3.S3Target(path=output_path + "-modelo_lr.pkl",client=cliente_s3,format=luigi.format.Nop), \
                    'outfile_knn' : luigi.contrib.s3.S3Target(path=output_path + "-modelo_knn.pkl",client=cliente_s3,format=luigi.format.Nop)
#             , \
#                     'params_xgb' : luigi.contrib.s3.S3Target(path=output_path + "-modelo_xgb_params.pkl",client=cliente_s3,format=luigi.format.Nop), \
#                     'params_lr' : luigi.contrib.s3.S3Target(path=output_path + "-modelo_lr_params.pkl",client=cliente_s3,format=luigi.format.Nop), \
#                     'params_knn' : luigi.contrib.s3.S3Target(path=output_path + "-modelo_knn_params.pkl",client=cliente_s3,format=luigi.format.Nop), \
#                     'precision_modelos' : luigi.contrib.s3.S3Target(path=output_path + "-precision_modelos.pkl",client=cliente_s3,format=luigi.format.Nop)
               }