#Este código hace las pruebas unitarias de la limpieza, toma como entrada lo ingestado y como salida genera metadata de la prueba unitaria que en este caso son los parámetros insertados.
import luigi
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.utils.test_limpiar import *
from src.pipeline.limpieza import limpiar
from datetime import *
import pandas as pd

class test_limpiar(CopyToTable):
    #Parámetros de las tareas anteriores y se agrega uno nuevo
    tipo_ingesta = luigi.Parameter() #Puede ser "historica" o "consecutiva".
    fecha = luigi.Parameter() #Fecha en la que se está haciendo la ingesta con respecto a inspection date.
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
    table = 'test.pruebas_unitarias'
    columns = [
                ('fecha_insercion', 'VARCHAR'),
                ('size_param', 'VARCHAR'),
                ('nombre_prueba', 'VARCHAR')
              ]
    
    def requires(self):
        return limpiar(self.tipo_ingesta, self.fecha, self.bucket, self.tamanio)
    
    def rows(self):
        datos = pd.DataFrame (query_database("select inspection_date from data.limpieza;"))
        
        #Esta es la prueba unitaria
#         if self.tipo_prueba=="infinito":
#             test_limpia(datos).test_noinfs()
#         else:
#             test_limpia(datos).test_shape()

        test_limpia(datos).test_noinfs()
        
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        primer_metadata=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
        segundo_metadata="infinito"
        tercer_metadata="test_limpieza"
        lista_metadata = [(primer_metadata[0], segundo_metadata, tercer_metadata)]
        
        #Metemos la información en la base de datos        
        for element in lista_metadata:
            yield element          