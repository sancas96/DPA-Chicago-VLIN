import bulwark.decorators as dc
from src.utils.general import *

class test_limpia():
    
    def __init__(self, dataframe):
        self.dataframe = dataframe

    @dc.HasNoInfs()
    def test_noinfs(self):
        return(self.dataframe)
    
    @dc.IsShape((1,5)) #Esta función es para hacer fallar la prueba unitaria en la demo
    def test_shape(self):
        return(self.dataframe)
    