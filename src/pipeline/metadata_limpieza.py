#Este task inserta metadata para la parte de la limpieza, son 3 metadatas:
#fecha de inserción, número de registros de la tabla, fecha máxima de inspección en la base de chicago
import luigi
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.pipeline.test_limpieza import test_limpiar
from datetime import datetime

class metadata_limpiar(CopyToTable):
    #Parámetros de las tareas anteriores
    tipo_ingesta = luigi.Parameter()
    fecha = luigi.Parameter() 
    bucket = luigi.Parameter()
    tamanio= luigi.IntParameter()
        
    #Obteniendo las credenciales para conectarse a la base de datos de chicago
    db_creds = get_database_connection('conf/local/credentials.yaml')
    user = db_creds['user']
    password = db_creds['password']
    database = db_creds['database']
    host = db_creds['host']
    port = db_creds['port']
    
    #Tabla y columnas donde ingresará la metadata
    table = 'metadata.metadata_limpieza'
    columns = [
                ('fecha_insercion', 'VARCHAR'),
                ('num_registros', 'INTEGER'),
                ('fecha_max', 'VARCHAR')
              ]
    
    def requires(self):
        return test_limpiar(self.tipo_ingesta, self.fecha, self.bucket, self.tamanio)
    
    def rows(self):
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        primer_metadata=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
        segundo_metadata=query_database("SELECT count(*) from data.limpieza;")
        tercer_metadata=query_database("SELECT max(inspection_date) from data.limpieza;")
        lista_metadata = [(primer_metadata[0], segundo_metadata[0][0], tercer_metadata[0][0])]
        print("########### metadata_limpieza", lista_metadata)
        #Metemos la información en la base de datos        
        for element in lista_metadata:
            yield element