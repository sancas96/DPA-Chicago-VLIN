import luigi
import luigi.contrib.s3
import os

from src.pipeline.metadata_ingesta import metadata_ingestar
from src.pipeline.ingesta import ingestar
from src.utils.general import *

class almacenar(luigi.Task):
    
    tipo_ingesta = luigi.Parameter() #Puede ser histórica o consecutiva.
    fecha = luigi.Parameter() #Fecha en la que se está haciendo la ingesta con respecto a inspection date.
    bucket = luigi.Parameter()


    def requires(self):
        return metadata_ingestar(self.tipo_ingesta, self.fecha, self.bucket)
        

    def run(self):
        #Guardamos el archivo pickle en el bucket de S3.
        with ingestar(self.tipo_ingesta, self.fecha, self.bucket).output().open() as infile, self.output().open('w') as outfile:
            outfile.write(infile.read())

    def output(self):
        s3_creds = get_s3_credentials('conf/local/credentials.yaml')
        cliente_s3 = luigi.contrib.s3.S3Client(s3_creds['aws_access_key_id'],s3_creds['aws_secret_access_key'])
        output_path = f"s3://{self.bucket}/ingesta/{self.tipo_ingesta}-{self.fecha}.pkl"
        return luigi.contrib.s3.S3Target(path=output_path,client=cliente_s3,format=luigi.format.Nop)