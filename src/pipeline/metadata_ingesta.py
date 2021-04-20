#Este task inserta metadata para la parte de la ingesta, son 3 metadatas:
#fecha de inserción, tamaño del archivo, tipo de archivo
import luigi
import os
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.pipeline.ingesta import ingestar
from datetime import *

class metadata_ingestar(CopyToTable):
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
    table = 'metadata.metadata_ingesta'
    columns = [
                ('fecha_insercion', 'VARCHAR'),
                ('nombre', 'VARCHAR'),
                ('size', 'INTEGER'),
                ('filetype', 'VARCHAR')
              ]
    
    def requires(self):
        return ingestar(self.tipo_ingesta, self.fecha, self.bucket)    
    
    def rows(self):
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        primer_metadata=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
        segundo_metadata=f"{self.tipo_ingesta}-{self.fecha}.pkl"
        tercer_metadata=os.path.getsize(f"./data/luigi/{self.tipo_ingesta}-{self.fecha}.pkl")
        cuarto_metadata=os.path.splitext(f"./data/luigi/{self.tipo_ingesta}-{self.fecha}.pkl")[1]
        lista_metadata = [(primer_metadata[0], segundo_metadata, tercer_metadata, cuarto_metadata)]
        print("########### metadata_ingesta", lista_metadata)
        #Metemos la información en la base de datos        
        for element in lista_metadata:
            yield element