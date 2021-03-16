import luigi
import src.utils.constants as constants
from src.utils.general import *
from sodapy import Socrata
import pickle

class ingestar(luigi.Task):
    
    limite = luigi.IntParameter()
    
    """
    Esta función recibe como parámetros:
        client: el cliente con el que nos podemos comunicar con la API.
        token: el token generado por la API para poder hacer la ingesta.
        limite: el límite de registros que queremos obtener al llamar a la API.
        
    Regresa:
        datos_binario: una lista de los elementos que la API regresó.
    """
    def run(self):
           
        token=get_api_token('../../conf/local/credentials.yaml')['api_token']
        client = Socrata(constants.url_api,token)
        datos=client.get(constants.id_data_set,limit=self.limite)

        with self.output().open('w') as outfile:
            pickle.dump(datos,outfile)
    
    #Esto deberá cambiar para que llegue a la EC2.
    def output(self):
        return luigi.local_target.LocalTarget('/home/vivis/Documents/DPA/repo-proyecto/DPA-Chicago-VLIN/data/test.pkl',format=luigi.format.Nop)