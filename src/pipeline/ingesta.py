import luigi
import luigi.contrib.s3
import src.utils.constants as constants
import pickle
import boto3

from src.utils.general import *
from sodapy import Socrata
from datetime import *

class ingestar(luigi.Task):
    
    tipo_ingesta = luigi.Parameter() #Puede ser historica o consecutiva.
    fecha = luigi.Parameter() #Fecha en la que se está haciendo la ingesta con respecto a inspection date.
    bucket = luigi.Parameter()
        

    def run(self):
        """
        Esta función recibe como parámetros:
            client: el cliente con el que nos podemos comunicar con la API.
            token: el token generado por la API para poder hacer la ingesta.
            limite: el límite de registros que queremos obtener al llamar a la API.
        """

        token = get_api_token('conf/local/credentials.yaml')['api_token']
        client = Socrata(constants.url_api, token)
        
        if self.tipo_ingesta=='historica':
            datos = client.get(constants.id_data_set, where = f"inspection_date<='{self.fecha}'")
            with self.output().open('w') as outfile:
                pickle.dump(datos, outfile)
        else:
            """
            Toma el último archivo cargado en la S3 en la carpeta de ingesta y genera el delta.
            """
            s3_creds = get_s3_credentials('conf/local/credentials.yaml')
            session = boto3.Session(aws_access_key_id=s3_creds['aws_access_key_id'],
                                    aws_secret_access_key=s3_creds['aws_secret_access_key'])
            cliente_s3 = session.client('s3')
            lista_archivos = cliente_s3.list_objects_v2(Bucket = self.bucket, Prefix = 'ingesta')['Contents']
            fecha_ultimo = max(lista_archivos, key=lambda x: x['LastModified'])['Key'][-26:-4]
            fecha_ultimo_formato = (datetime.strptime(fecha_ultimo, '%Y-%m-%dT%H:%M:%S.%f') +
                                    timedelta(days=1)).date()
            print("########### ", fecha_ultimo)
            print("########### ", fecha_ultimo_formato)
            datos=client.get(constants.id_data_set,
                             where = f"inspection_date between '{fecha_ultimo_formato}' and '{self.fecha}'")
            with self.output().open('w') as outfile:
                pickle.dump(datos, outfile)

                
    #Esto deberá cambiar para que llegue a la EC2 en lugar de a lo local.
    def output(self):
        return luigi.local_target.LocalTarget(f"./data/luigi/{self.tipo_ingesta}-{self.fecha}.pkl",format=luigi.format.Nop)