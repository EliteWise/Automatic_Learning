import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

from Scripts_UI.SVM.Page_1 import DataFrame_Viewer

# ------- SIMPLE SVM ------- #

class Pipeline():
    def __init__(self):
        super(Pipeline, self).__init__()


     def preprocessing(self):

     	df = DataFrame_Viewer.Show_Datas.stock_df(self)

     	X = df
     	y = df[target]

     	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)


     def training(self):
     	svclassifier = SVC(kernel='linear')  
		svclassifier.fit(X_train, y_train)


	def prediction(self):
		y_pred = svclassifier.predict(X_test)


	def evaluate(self):
		print(confusion_matrix(y_test,y_pred))  
		print(classification_report(y_test,y_pred))



