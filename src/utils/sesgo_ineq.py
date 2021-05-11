#Calcula la matriz de sesgos e inequidades del modelo punitivo. Como entrada un dataframe, como salida un dataframe.
from aequitas.group import Group
from aequitas.bias import Bias
from aequitas.fairness import Fairness

class SesgIneq():
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def sesgar(self):
        xtab, attrbs = Group().get_crosstabs(self.dataframe)
        majority_bdf = Bias().get_disparity_major_group(xtab, original_df=xtab)
        fdf = Fairness().get_group_value_fairness(majority_bdf)
        matriz_sesgo=majority_bdf[['attribute_name','attribute_value','fdr','fpr','fdr_disparity','fpr_disparity', 'FDR Parity', 'FPR Parity','Statistical Parity']]

        return matriz_sesgo