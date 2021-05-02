#Este task inserta metadata para la parte de selección del modelo, son 2 metadatas:
#fecha de inserción, número de registros.
import luigi
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.pipeline.test_seleccion import test_seleccionar
from datetime import datetime

class metadata_seleccionar(CopyToTable):
    #Parámetros de las tareas anteriores
    tipo_ingesta = luigi.Parameter()
    fecha = luigi.Parameter() 
    bucket = luigi.Parameter()
    tamanio= luigi.IntParameter()
    tipo_prueba= luigi.Parameter()
    
    #Obteniendo las credenciales para conectarse a la base de datos de chicago
    db_creds = get_database_connection('conf/local/credentials.yaml')
    user = db_creds['user']
    password = db_creds['password']
    database = db_creds['database']
    host = db_creds['host']
    port = db_creds['port']
    
    #Tabla y columnas donde ingresará la metadata
    table = 'metadata.metadata_seleccionar'
    columns = [
                ('fecha_insercion', 'VARCHAR'),
                ('num_registros', 'INTEGER')
              ]
    
    def requires(self):
        return test_seleccionar(self.tipo_ingesta, self.fecha, self.bucket, self.tamanio, self.tipo_prueba)
    
    def rows(self):
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        primer_metadata=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
        segundo_metadata=query_database("SELECT count(*) from data.seleccion;")
        lista_metadata = [(primer_metadata[0], segundo_metadata[0][0])]
        
        #Metemos la información en la base de datos        
        for element in lista_metadata:
            yield element