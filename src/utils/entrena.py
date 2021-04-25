from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, ParameterGrid
from sklearn.model_selection import cross_validate
from sklearn.linear_model import LogisticRegression, Perceptron, SGDClassifier
from sklearn.metrics import log_loss
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
import xgboost as xgb
from sklearn.metrics import accuracy_score
from time import time
import pandas as pd
import pickle

class MLModeling():
    def __init__(self, dataframe):
        self.dataframe = dataframe
    
    def modeling(self):
      X = self.dataframe.drop(['Results'], axis=1)
      y = self.dataframe['Results']
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
      modelos={}
      
      # xgboost
      model_xgb = xgb.XGBClassifier(
          n_estimators=100,
          max_depth=7,
          learning_rate=0.4,
          colsample_bytree=0.6,
          missing=-999,
          random_state=66
          )
      model_xgb.fit(X_train, y_train)
      yhat_xgb = model_xgb.predict(X_test)
      acc_xgb = accuracy_score(y_test, yhat_xgb)
      modelos['xgb']=acc_xgb

      # logistic regression
      model_lr = LogisticRegression(
              penalty = 'l2',
              C= 1,
              solver='lbfgs'
              )
      model_lr.fit(X_train, y_train)
      yhat_lr = model_lr.predict(X_test)
      acc_lr = accuracy_score(y_test, yhat_lr)
      modelos['lr']=acc_lr

      # KNN
      model_knn=KNeighborsClassifier(
                n_neighbors=100,
                weights='uniform',
                algorithm='auto'
                )
      model_knn.fit(X_train, y_train)
      yhat_knn = model_knn.predict(X_test)
      acc_knn = accuracy_score(y_test, yhat_knn)
      modelos['knn']=acc_knn

      el_elegido=max(modelos, key=modelos.get)
      pkl_filename = "pickle_model.pkl"

      with open(pkl_filename, 'wb') as file:
        if el_elegido=='xgb':
          pickle.dump(model_xgb, file)
        elif el_elegido=='lr':
          pickle.dump(model_lr, file)
        else:
          pickle.dump(model_knn, file)
