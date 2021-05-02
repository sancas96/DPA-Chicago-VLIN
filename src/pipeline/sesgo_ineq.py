#Este task hace la selección del mejor modelo, de acuerdo a la precisión.
import luigi
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.utils.seleccionar import *
from src.pipeline.metadata_entrenamiento import metadata_entrenar
from datetime import datetime
import pickle

class seleccionar(CopyToTable):
    #Parámetros de las tareas anteriores
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
    table = 'data.seleccion'
    columns = [
                ('fecha_insercion', 'VARCHAR'),
                ('modelo_seleccionado', 'VARCHAR'),
                ('precision','NUMERIC')
              ]
    
    def requires(self):
        return metadata_entrenar(self.tipo_ingesta, self.fecha, self.bucket, self.tamanio, self.tipo_prueba)
    
    def rows(self):
        
        with open('data/precision_modelos.pkl', 'rb') as pickle_file:
            diccionario = pickle.load(pickle_file)
            
        seleccion=selecciona(diccionario).seleccion()
        
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fecha_insercion=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
        
        modelo_seleccionado=seleccion[0]
        precision=seleccion[1]
        
        lista_metadata = [(fecha_insercion[0], modelo_seleccionado, precision)]
        
        #Metemos la información en la base de datos        
        for element in lista_metadata:
            yield element
            