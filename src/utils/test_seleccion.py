import pandas as pd

class DataCleanning():
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def cleanning(self):
        #self.dataframe.dropna(subset=["Inspection Date", "License #", "Latitude", "Longitude"], inplace=True)
        limpieza_1=self.dataframe.dropna(subset=["inspection_date", "license_", "latitude", "longitude"])
        limpieza_2=limpieza_1[~limpieza_1.results.isin(["Out of Business", "Business Not Located", "No Entry", "Not Ready"])]
        limpieza_3=limpieza_2.drop_duplicates()
        limpieza_4=limpieza_3.fillna(0)
        return limpieza_4