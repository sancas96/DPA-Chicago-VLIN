#Este task inserta en el esquema monitoreo los campos necesarios para el dashboard con respecto a las predicciones del modelo.
import luigi
import pickle
import pandas as pd
import boto3
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.pipeline.almacena_api import api

class monitoreo_predice(CopyToTable):
    tipo_ingesta = luigi.Parameter() #Puede ser "historica" o "consecutiva".
    fecha = luigi.Parameter() #Fecha en la que se está haciendo la ingesta con respecto a inspection date.
    bucket = luigi.Parameter()
    tamanio = luigi.IntParameter()
    tipo_prueba= luigi.Parameter() #"infinito" o "shape"
    proceso = luigi.Parameter() #Puede ser "entrenamiento" o "prediccion"
    
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
        return api(self.tipo_ingesta, self.fecha, self.bucket, self.tamanio, self.tipo_prueba, self.proceso)

    def rows(self):
        if self.proceso=='prediccion':
            #Obtenemos la predicción para la ingesta consecutiva con la tabla predicción.
            probabilidades= pd.DataFrame(query_database(f"SELECT prediccion from data.prediccion where fecha_parametro='{self.fecha}';"))
            probabilidades.columns=['prediccion']
            probabilidades=probabilidades['prediccion'].tolist()
            
            #Trayéndonos los campos que nos interesan de la tabla de limpieza
            datos_predic=pd.DataFrame(query_database(f"select inspection_id,fecha_parametro, facility_type, 0 as entrenamiento from data.limpieza where fecha_parametro='{self.fecha}';"))
            datos_predic.columns=['inspection_id','fecha_parametro','facility_type','entrenamiento']
            
            lista_monitoreo=datos_predic.values.tolist()
                        
            for i in range(len(lista_monitoreo)):
                lista_monitoreo[i].append(probabilidades[i])

            for element in lista_monitoreo:
                yield element
            
        else:
            exit()