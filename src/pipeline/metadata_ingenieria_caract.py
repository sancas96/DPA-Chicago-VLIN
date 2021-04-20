#Este task inserta metadata para la parte de ingeniería de características, son 3 metadatas:
#fecha de inserción, número de registros de la tabla, conteo de nulos en las columnas critical_count, serious_count, minor_count
import luigi
import pandas as pd
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.pipeline.ingenieria_caract import ingenieria
from datetime import datetime

class metadata_ingenieria(CopyToTable):
    #Pasando parámetros de las tareas anteriores
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
    table = 'metadata.ingenieria_metadata'
    columns = [
                ('fecha_insercion', 'VARCHAR'),
                ('num_registros', 'INTEGER'),
                ('critical_null', 'VARCHAR'),
                ('serious_null', 'VARCHAR'),
                ('minor_null', 'VARCHAR')
              ]
    
    def requires(self):
        return ingenieria(self.tipo_ingesta, self.fecha, self.bucket)    
    
    def rows(self):

        #Obtenemos el delta de los datos de ingeniería de características que está en la base de datos usando como parámetro el número de registros que se insertaron en la tarea que le precede.
        datos_ingenieria= pd.DataFrame(query_database("SELECT * from prueba3 limit (select num_registros - lag(num_registros,1,0) over(order by num_registros)as resultado from metadata.limpieza_metadata order by fecha_insercion desc limit 1) offset (select (max(num_registros) - (select num_registros - lag(num_registros,1,0) over(order by num_registros)as resultado from metadata.limpieza_metadata order by fecha_insercion desc limit 1)) from metadata.limpieza_metadata);"))
        datos_ingenieria.columns=[i[0] for i in query_database(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where table_name='prueba3';")]
        
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        primer_metadata=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
        segundo_metadata=query_database("SELECT count(*) from prueba3;")
        tercer_metadata=query_database("SELECT count(*) from prueba3 where critical_count is null;")
        cuarto_metadata=query_database("SELECT count(*) from prueba3 where serious_count is null;")
        quinto_metadata=query_database("SELECT count(*) from prueba3 where minor_count is null;")
        lista_metadata = [(primer_metadata[0], segundo_metadata[0][0], tercer_metadata[0][0],cuarto_metadata[0][0],quinto_metadata[0][0])]
        
        
        #Metemos la información en la base de datos        
        for element in lista_metadata:
            yield element