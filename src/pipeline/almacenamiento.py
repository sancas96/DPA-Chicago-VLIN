import luigi
import luigi.contrib.s3

from ingesta import *
from src.utils.general import *
import src.utils.constants as constants


class almacenar(luigi.Task):
    
    limite = luigi.IntParameter()
    bucket = luigi.Parameter()
    
    def requires(self):
        return ingestar(self.limite)

    def run(self):
        
        #Guardamos el archivo pickle en el bucket de S3.
        with self.input().open() as infile, self.output().open('w') as outfile:
            outfile.write(infile.read())

    def output(self):
        s3_creds= get_s3_credentials('../../conf/local/credentials.yaml')
        cliente_s3=luigi.contrib.s3.S3Client(s3_creds['aws_access_key_id'],s3_creds['aws_secret_access_key'])
        output_path = "s3://{}/test.pkl".format(self.bucket)
        return luigi.contrib.s3.S3Target(path=output_path,client=cliente_s3,format=luigi.format.Nop)
    

    

