#Este código hace las pruebas unitarias de la limpieza, toma como entrada lo ingestado y como salida genera metadata de la prueba unitaria que en este caso es la codificación del objeto.
import luigi
import boto3
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.utils.test_limpiar import *
from src.pipeline.limpieza import limpiar
from datetime import *

class test_almacenar(CopyToTable):
    #Parámetros de las tareas anteriores y se agrega uno nuevo
    tipo_ingesta = luigi.Parameter() #Puede ser "historica" o "consecutiva".
    fecha = luigi.Parameter() #Fecha en la que se está haciendo la ingesta con respecto a inspection date.
    bucket = luigi.Parameter()
    tamanio= luigi.IntParameter()
    encoding= luigi.Parameter()
    
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
        s3_creds = get_s3_credentials('conf/local/credentials.yaml')
        session = boto3.Session(aws_access_key_id=s3_creds['aws_access_key_id'],
                                    aws_secret_access_key=s3_creds['aws_secret_access_key'])
        cliente_s3 = session.client('s3')
        arch = cliente_s3.get_object(Bucket=f'{self.bucket}',Key=f'ingesta/{self.tipo_ingesta}-{self.fecha}.pkl')
        prueba_unitaria=test_almacena().test_tamanio(nombre_archivo=BytesIO(arch['Body'].read()),tamanio_archivo=self.tamanio)
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        primer_metadata=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
        segundo_metadata=self.tamanio
        tercer_metadata="test_almacenar"
        lista_metadata = [(primer_metadata[0], segundo_metadata, tercer_metadata)]
        
        
        #Metemos la información en la base de datos        
        for element in lista_metadata:
            yield element          