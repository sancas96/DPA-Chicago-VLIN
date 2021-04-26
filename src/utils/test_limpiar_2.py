from src.utils.general import *
from src.utils.test_limpiar import *
import pandas as pd


df = pd.DataFrame (query_database("Select * from metadata.metadata_limpieza;"))
print(df)
test_limpia(df).test_shape()
test_limpia(df).test_noinfs()

