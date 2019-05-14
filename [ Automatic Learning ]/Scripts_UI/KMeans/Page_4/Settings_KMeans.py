import os, sys, PyQt5
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics

import mysql.connector
import datetime
import time

from Scripts_UI.KMeans.Page_1 import DataFrame_Viewer
from Scripts_UI._MainPage_.Main_Create import Choose_Model
from Scripts_UI._DataBase_ import Database
from Scripts_UI._DataBase_ import Converter
from Scripts_UI._MainPage_._Auth_ import Auth_Page
from Scripts_UI._MainPage_.Main import Main_Page
from Scripts_UI.KMeans.Page_3 import SettingsPlot_Page

class Load_Settings(QMainWindow):

	def __init__(self):
		super(Load_Settings, self).__init__()
		loadUi('Scripts_UI/KMeans/Page_4/Settings_KMeans.ui', self) # Load UI File

		self.run.clicked.connect(self.pipeline_kmeans)
		self.save_settings.clicked.connect(self.save_settings_kmeans)

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


	def pipeline_kmeans(self):

		# ------ Get DataFrame ------ #

		df = DataFrame_Viewer.Show_Datas.stock_df(self)
		X = df

		# ------ Main Settings ------ #

		self.n_clusters = self.n_clusters_.text() if not self.n_clusters_.text() == '' else 4
		self.category_name = self.category_name_.text() if not self.category_name_.text() == '' else 'no_column'

		# ------ Preprocess ------ #

		if self.category_name != 'no_column':

			X = X.drop([self.category_name], axis=1)

		else:
			X = X.drop(X.select_dtypes(['object']), axis=1)

		# ------ Training ------ #

		kmeans = KMeans(n_clusters=self.n_clusters)  
		kmeans.fit(X)

		# ------ Show Score ------ #

		self.score.setText(str(round(metrics.silhouette_score(X, kmeans.labels_), 2)))
		self.score.setAlignment(QtCore.Qt.AlignCenter)

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

		sql = "SELECT n_clusters, category_name FROM kmeans_settings"
		cursor.execute(sql)

		# ----- Return Datas ----- #

		rows = cursor.fetchall()

		return rows[0][0], rows[0][1]

		# ------------------------ #


	def save_settings_kmeans(self):

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

		sql = "INSERT INTO kmeans_settings (date, nb_clusters, name, fk_profile) VALUES (%s, %s, %s, %s)"
		val = (date, self.n_clusters, name, rows[0][0])

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