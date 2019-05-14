import os, sys, PyQt5
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import mysql.connector
import time, threading
import datetime

from multiprocessing import Queue

from Scripts_UI._MainPage_.Main_Create import Choose_Model
from Scripts_UI._MainPage_.Main_Predict import Choose_Loaded_Model
from Scripts_UI._MainPage_.Main import Main_Page
from Scripts_UI._DataBase_ import Database
from Scripts_UI._DataBase_ import Converter
from Scripts_UI._MainPage_._Auth_ import Auth_Page

class Stats_Page(QMainWindow):

	def __init__(self):
		super(Stats_Page, self).__init__()
		loadUi('Scripts_UI/_MainPage_/_Profile_/Stats_Page.ui', self) # Load UI File

		model_name = Profile_Stats.stock_model_name(self)
		score_value = Profile_Stats.stock_score_value(self)
		algo = Profile_Stats.stock_algo(self)

		self.closePage.clicked.connect(self.close)

		self.model_name_label.setText(model_name)
		self.model_name_label.setAlignment(QtCore.Qt.AlignCenter)

		# --- Hide all Labels by default --- #

		self.score_label.hide()
		self.mae_label.hide()
		self.mse_label.hide()
		self.accuracy_label.hide()
		self.rmse_label.hide()

		# --------------------------------- #

		if algo == 'KMEANS':
			self.score_label.show()

			self.score_value_label_score_mse_accuracy.setText(str(score_value[0]))

		elif algo == 'REGLIN':
			self.mae_label.show()
			self.mse_label.show()
			self.rmse_label.show()

			self.score_value_label_mae.setText(str(score_value[0][0]))
			self.score_value_label_score_mse_accuracy.setText(str(score_value[0][1]))
			self.score_value_label_rmse.setText(str(score_value[0][2]))

		elif algo == 'KNN' or algo == 'SVM':
			self.accuracy_label.show()

			self.score_value_label_score_mse_accuracy.setText(str(score_value[0]))

		self.center() # Center Function
		self.show()

	def close(self):
		self.hide()

	def center(self):

		# Center Window

		frameGm = self.frameGeometry()
		screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
		centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

class Profile_Stats(QMainWindow):

	def __init__(self):
		super(Profile_Stats, self).__init__()
		loadUi('Scripts_UI/_MainPage_/_Profile_/Profile_Page.ui', self) # Load UI File

		self.path_cnn = 'C:/Users/Dell/Desktop/[ Automatic Learning ]/Models/CNN'
		self.path_rnn = 'C:/Users/Dell/Desktop/[ Automatic Learning ]/Models/RNN'

		for root, dirs, files in os.walk(self.path_cnn):
			self.cnnList.addItems(files)

		for root, dirs, files in os.walk(self.path_rnn):
			self.rnnList.addItems(files)

		self.cnnList.itemClicked.connect(self.clicked_cnn)
		self.rnnList.itemClicked.connect(self.clicked_rnn)

		self.knnList.itemClicked.connect(self.clicked_knn)
		self.kmeansList.itemClicked.connect(self.clicked_kmeans)
		self.svmList.itemClicked.connect(self.clicked_svm)
		self.reglinList.itemClicked.connect(self.clicked_reglin)

		self.back.clicked.connect(self.clicked_back)

		# ----- Connection ----- #

		config = {
		    'user'    : 'flo',
		    'host'    : 'localhost',
		    'password': '',
		    'database': 'automatic_learning_v2'
		}

		self.conn = mysql.connector.connect(**config)
		self.conn.set_converter_class(Converter.NumpyMySQLConverter)

		self.cursor = self.conn.cursor()

		# --------------------- #

		self.show_machine_learning_model()
		self.center() # Center Function
		self.show()


	def center(self):

		# Center Window

		frameGm = self.frameGeometry()
		screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
		centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

	def update_models_list(self, algo_name, list_name):

		# --- Get Username ---  #

		self.username = Auth_Page.Auth.stock_username(self)

		# --- Get Algo --- #

		self.algo = algo_name
		self.list_name = list_name

		# --- Execute Query --- #

		sql = "SELECT name FROM model_machine_learning AS mml \
				INNER JOIN algo ON mml.fk_algo = algo.id \
				INNER JOIN profile ON mml.fk_profile = profile.id \
				WHERE algo.algo = '" + self.algo + "' \
				AND profile.username = '" + self.username + "'"

		self.cursor.execute(sql)
		rows = self.cursor.fetchall()

		# --- Show Models --- #

		for i in range(len(rows)):
			self.list_name.addItems(rows[i])

		# ------------------- #

	def load_score_value(self, model_name_param, algo_name, type_score_selection):
		global model_name
		global score_value
		global algo

		# ----- Get Username ----- #

		self.username = Auth_Page.Auth.stock_username(self)

		# --- Check Type --- #

		if type(type_score_selection) == list:
			type_score_selection = str(type_score_selection).strip('[]')

		print(type_score_selection)

		# --- Query --- #

		sql = "SELECT " + type_score_selection.replace("'","") + " FROM resultats \
				INNER JOIN model_machine_learning AS mml ON resultats.fk_model = mml.id \
				INNER JOIN algo ON mml.fk_algo = algo.id \
				INNER JOIN profile ON mml.fk_profile = profile.id \
				WHERE mml.name = '" + model_name_param + "' \
				AND algo.algo = LOWER('" + algo_name + "') \
				AND profile.username = '" + self.username + "'"

		# --- Execute --- #

		self.cursor.execute(sql)
		rows = self.cursor.fetchall()

		# --- Initialization of Global Values --- #

		score_value = rows
		model_name = model_name_param
		algo = algo_name

		# --- Load Recap Page --- #

		self.window = Stats_Page()
		Main_Page.Main_Page.style(self)


	def show_machine_learning_model(self):

		self.update_models_list('svm', self.svmList)
		self.update_models_list('knn', self.knnList)
		self.update_models_list('kmeans', self.kmeansList)
		self.update_models_list('reglin', self.reglinList)

	def clicked_cnn(self, item):
		pass

	def clicked_rnn(self, item):
		pass

	def clicked_knn(self, item):
		self.load_score_value(item.text(), 'KNN', 'accuracy')

	def clicked_kmeans(self, item):
		self.load_score_value(item.text(), 'KMEANS', 'score')

	def clicked_svm(self, item):
		self.load_score_value(item.text(), 'SVM', 'accuracy')

	def clicked_reglin(self, item):
		self.load_score_value(item.text(), 'REGLIN', type_score_selection=['mae', 'mse', 'rmse'])

	def clicked_back(self):
		self.hide()
		self.window = Main_Page.Main_Page()
		Main_Page.Main_Page.style(self)

	def stock_model_name(self):
		return model_name

	def stock_score_value(self):
		return score_value

	def stock_algo(self):
		return algo