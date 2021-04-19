#Este task inserta metadata para la parte de la limpieza, son 3 metadatas:
#fecha de inserción, número de registros de la tabla, fecha máxima de inspección en la base de chicago
import luigi
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.pipeline.limpieza import limpiar
from datetime import datetime

class metadata_limpiar(CopyToTable):
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
    table = 'metadata.limpieza_metadata'
    columns = [
                ('fecha_insercion', 'VARCHAR'),
                ('num_registros', 'VARCHAR'),
                ('fecha_max', 'VARCHAR')
              ]
    
    def requires(self):
        return limpiar(self.tipo_ingesta, self.fecha, self.bucket)    
    
    def rows(self):
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        primer_metadata=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
        segundo_metadata=query_database("SELECT count(*) from prueba2;")
        tercer_metadata=query_database("SELECT max(col_11) from prueba2;")
        lista_metadata = [(primer_metadata[0], segundo_metadata[0][0], tercer_metadata[0][0])]
        print("########### ", lista_metadata)
        #Metemos la información en la base de datos        
        for element in lista_metadata:
            yield element