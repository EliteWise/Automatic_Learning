import os, sys, PyQt5
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

import mysql.connector
import datetime
import time

from Scripts_UI.KNN.Page_1 import DataFrame_Viewer
from Scripts_UI._MainPage_.Main_Create import Choose_Model
from Scripts_UI._DataBase_ import Database
from Scripts_UI._DataBase_ import Converter
from Scripts_UI._MainPage_._Auth_ import Auth_Page
from Scripts_UI._MainPage_.Main import Main_Page

class Load_Settings(QMainWindow):

	def __init__(self):
		super(Load_Settings, self).__init__()
		loadUi('Scripts_UI/KNN/Page_4/Settings_KNN.ui', self) # Load UI File

		self.run.clicked.connect(self.pipeline_knn)
		self.save_settings.clicked.connect(self.save_settings_knn)

		self.back.clicked.connect(self.clicked_back)
		self.main_menu.clicked.connect(self.clicked_main_menu)

		self.center() # Center Function
		self.show()

	def center(self):

		# Center Window

		frameGm = self.frameGeometry()
		screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
		centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())


	def pipeline_knn(self):

		# ------ Get DataFrame ------ #

		df = DataFrame_Viewer.Show_Datas.stock_df(self)

		# ------ Drop Columns with NaN ------ #

		df.dropna(axis='columns', thresh=100, inplace=True)

		# ------ Main Settings ------ #

		self.y = self.y_.text() if not self.y_.text() == '' else df.select_dtypes(['object']).columns[0]
		self.X = df.drop([self.y], axis=1)
		self.test_size = float(self.test_size_.text()) if not self.test_size_.text() == '' else 0.20
		self.n_neighbors = int(self.n_neighbors_.text()) if not self.n_neighbors_.text() == '' else 5

		# ------ Preprocess ------ #

		X_train, X_test, y_train, y_test = train_test_split(self.X, df[self.y], test_size = self.test_size)

		# ------ Standardize ------ #

		scaler = StandardScaler()
		scaler.fit(X_train)

		X_train = scaler.transform(X_train)  
		X_test = scaler.transform(X_test)

		# ------ Training ------ #

		classifier = KNeighborsClassifier(n_neighbors=self.n_neighbors)  
		classifier.fit(X_train, y_train)

		# ------ Prediction ------ #

		y_pred = classifier.predict(X_test)

		# ------ Evaluate ------ #

		print(confusion_matrix(y_test,y_pred))  
		self.evaluate_label.setText(classification_report(y_test,y_pred))

		# ---------------------- #

	def get_settings(self):

		# ----- Connection ----- #

		config = {
		    'user'    : 'flo',
		    'host'    : 'localhost',
		    'password': '',
		    'database': 'automatic_learning'
		}

		conn = mysql.connector.connect(**config)
		conn.set_converter_class(Converter.NumpyMySQLConverter)

		cursor = conn.cursor()

		# ----- Execute Query ----- #

		sql = "SELECT test_size, n_neighbors FROM knn_settings"
		cursor.execute(sql)

		# ----- Return Datas ----- #

		rows = cursor.fetchall()

		return rows[0][0], rows[0][1]

		# ------------------------ #


	def save_settings_knn(self):

		# ----- Connection ----- #

		config = {
		    'user'    : 'flo',
		    'host'    : 'localhost',
		    'password': '',
		    'database': 'automatic_learning'
		}

		conn = mysql.connector.connect(**config)
		conn.set_converter_class(Converter.NumpyMySQLConverter)

		cursor = conn.cursor()

		# ----- Get Variables ----- #

		date = datetime.datetime.now()
		name = self.settings_name.text() if not self.settings_name.text() == '' else str(date.strftime("%d/%m/%Y %H:%M"))
		fk_profile = "SELECT id FROM profile WHERE username ='" + Auth_Page.Auth.stock_username(self) + "'"
		cursor.execute(fk_profile)

		# ----- Execute Query ----- #

		rows = cursor.fetchall()

		sql = "INSERT INTO knn_settings (date, test_size, neighbors, name, fk_profile) VALUES (%s, %s, %s, %s, %s)"
		val = (date, self.test_size, self.n_neighbors, name, rows[0][0])

		cursor.execute(sql, val)
		conn.commit()

		# ----- Back to Main Page ----- #
		
		time.sleep(1)

		self.hide()
		self.window = Main_Page.Main_Page()
		Main_Page.Main_Page.style(self)

		# ------------------------ #

	def clicked_back(self):
		self.hide()
		self.window = DataFrame_Viewer.Show_Datas()
		Main_Page.Main_Page.style(self)

	def clicked_main_menu(self):
		self.hide()
		self.window = Main_Page.Main_Page()
		Main_Page.Main_Page.style(self)	