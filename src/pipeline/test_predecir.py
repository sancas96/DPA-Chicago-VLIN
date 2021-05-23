#Este código hace las pruebas unitarias de los datos de prediccion, prueba que la tabla no tenga valores infinitos.
import luigi
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.utils.test_predice import *
from src.pipeline.predecir import predice
from datetime import *
import pandas as pd

class test_prediccion(CopyToTable):
    #Parámetros de las tareas anteriores y se agrega uno nuevo
    tipo_ingesta = luigi.Parameter() #Puede ser "historica" o "consecutiva".
    fecha = luigi.Parameter() #Fecha en la que se está haciendo la ingesta con respecto a inspection date.
    bucket = luigi.Parameter()
    tamanio= luigi.IntParameter()
    tipo_prueba= luigi.Parameter() #"infinito" o "shape"
    proceso= luigi.Parameter() #Puede ser "entrenamiento" o "prediccion"
    
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
        return predice(self.tipo_ingesta, self.fecha, self.bucket, self.tamanio,self.proceso)

    def rows(self):
        if self.proceso=='prediccion':
            datos = pd.DataFrame (query_database("select * from data.prediccion;"))

            #Esta es la prueba unitaria
            if self.tipo_prueba=="infinito":
                test_predic(datos).test_noinfs()
            else:
                test_predic(datos).test_shape()

            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            primer_metadata=date_time.split("|") #Convertir a lista para poder meterlo a la base de datos
            segundo_metadata=self.tipo_prueba
            tercer_metadata="test_prediccion"
            lista_metadata = [(primer_metadata[0], segundo_metadata, tercer_metadata)]

            #Metemos la información en la base de datos        
            for element in lista_metadata:
                yield element
        else:
            exit()