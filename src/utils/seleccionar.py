#Selecciona el mejor modelo de acuerdo a la precisión
class selecciona():
    def __init__(self, diccionario):
        self.diccionario = diccionario
  
    def seleccion(self):
        mejor_modelo=max(self.diccionario, key=self.diccionario.get)
        precision_modelo=max(self.diccionario.values())
      
        return mejor_modelo,precision_modelo
