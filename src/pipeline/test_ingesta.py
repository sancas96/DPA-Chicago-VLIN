#Este código hace las pruebas unitarias de la ingesta, toma como entrada lo ingestado y como salida genera metadata de la prueba unitaria
import luigi
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.utils.test_ingestar import *
from src.pipeline.ingesta import ingestar
from datetime import *


class test_ingestar(CopyToTable):
    #Parámetros de las tareas anteriores
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
        return ingestar(self.tipo_ingesta, self.fecha, self.bucket)
    
    def rows(self):
        prueba_unitaria=test_ingesta().test_tamanio(nombre_archivo=f"./data/luigi/{self.tipo_ingesta}-{self.fecha}.pkl", tamanio_archivo=self.tamanio)
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        primer_metadata=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
        segundo_metadata=self.tamanio
        tercer_metadata="test_ingestar"
        lista_metadata = [(primer_metadata[0], segundo_metadata, tercer_metadata)]
        
        
        #Metemos la información en la base de datos        
        for element in lista_metadata:
            yield element          

