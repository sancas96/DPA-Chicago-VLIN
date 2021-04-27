#Este task inserta metadata para la parte de ingeniería de características, son 3 metadatas:
#fecha de inserción, número de registros de la tabla, conteo de nulos en las columnas critical_count, serious_count, minor_count
import luigi
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.pipeline.test_entrenamiento import test_entrenar
from datetime import datetime
import pickle

class metadata_entrenar(CopyToTable):
    #Pasando parámetros de las tareas anteriores
    tipo_ingesta = luigi.Parameter() #Puede ser "historica" o "consecutiva".
    fecha = luigi.Parameter() #Fecha en la que se está haciendo la ingesta con respecto a inspection date.
    bucket = luigi.Parameter()
    tamanio= luigi.IntParameter()
    tipo_prueba= luigi.Parameter() #"infinito" o "shape"
    
    #Obteniendo las credenciales para conectarse a la base de datos de chicago
    db_creds = get_database_connection('conf/local/credentials.yaml')
    user = db_creds['user']
    password = db_creds['password']
    database = db_creds['database']
    host = db_creds['host']
    port = db_creds['port']
    
    #Tabla y columnas donde ingresará la metadata
    table = 'metadata.metadata_entrenamiento'
    columns = [
                ('fecha_insercion', 'VARCHAR'),
                ('modelo', 'VARCHAR'),
                ('metadata', 'VARCHAR')
              ]
    
    def requires(self):
        return test_entrenar(self.tipo_ingesta, self.fecha, self.bucket, self.tamanio, self.tipo_prueba)
    
    def rows(self):
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        primer_metadata1=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
        segundo_metadata1='modelo_xgb'
        with open('data/entrenamiento_xgb_parametros.pkl', 'rb') as pickle_file:
             tercer_metadata1 = pickle.load(pickle_file)
        
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        primer_metadata2=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
        segundo_metadata2='modelo_lr'
        with open('data/entrenamiento_lr_parametros.pkl', 'rb') as pickle_file:
            tercer_metadata2 = pickle.load(pickle_file)
            
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        primer_metadata3=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
        segundo_metadata3='modelo_knn'
        with open('data/entrenamiento_knn_parametros.pkl', 'rb') as pickle_file:
            tercer_metadata3 = pickle.load(pickle_file)
            
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        primer_metadata4=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
        segundo_metadata4='modelos_precisiones'
        with open('data/precision_modelos.pkl', 'rb') as pickle_file:
            tercer_metadata4 = pickle.load(pickle_file)
        

        lista_metadata = [
                            (primer_metadata1[0], segundo_metadata1, tercer_metadata1),
                            (primer_metadata2[0], segundo_metadata2, tercer_metadata2),
                            (primer_metadata3[0], segundo_metadata3, tercer_metadata3),
                            (primer_metadata4[0], segundo_metadata4, tercer_metadata4)
                         ]
        
        #Metemos la información en la base de datos        
        for element in lista_metadata:
            yield element          