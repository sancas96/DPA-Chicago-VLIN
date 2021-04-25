# import marbles.core
# from marbles.mixins import mixins
# from src.utils.general import *

# class test_limpia(marbles.core.TestCase, mixins.FileMixins):
    
#     def test_cifrado(self, nombre_archivo, cifrado_archivo):
#         self.nombre_archivo=nombre_archivo
#         self.cifrado_archivo=cifrado_archivo
#         self.assertFileEncodingEqual(self.nombre_archivo,self.cifrado_archivo, msg='La codificación del archivo es incorrecta.')

# class test_limpia(marbles.core.TestCase, mixins.FileMixins):
    
#     def test_cifrado(self):
#         a=str (query_database("Select * from metadata.metadata_limpieza;"))
#         self.assertFileEncodingEqual(a,"utf-8", msg='La codificación del archivo es incorrecta.')
        
        
import bulwark.decorators as dc
import pandas as pd
from src.utils.general import *
import math

@dc.HasNoInfs()

def compute(df):
    return df

df = pd.DataFrame({'a': [1,2,3,4,5], 'b': [1,"f",math.inf,1,0]})
#df = pd.DataFrame (query_database("Select * from metadata.metadata_limpieza;"))
compute(df)

