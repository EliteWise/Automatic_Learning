import os, sys, PyQt5, os.path
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PIL import Image
from keras.models import load_model
from io import StringIO
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

import datetime
import mysql.connector
import h5py
import cv2
import numpy as np

from Scripts_UI._DataBase_ import Database
from Scripts_UI._DataBase_ import Converter
from Scripts_UI._MainPage_.Main import Main_Page
from Scripts_UI.CNN.Page_2 import Settings_CNN
from Scripts_UI._MainPage_.Main_Create import Choose_Model
from Scripts_UI.CNN.Page_3 import Graphics
from Scripts_UI._Predict_.Page_0 import Select_Previous_Model
from Scripts_UI._MainPage_.Main_Predict import Choose_Loaded_Model
from Scripts_UI._MainPage_._Auth_ import Auth_Page

class Confirm(QMainWindow):

	def __init__(self):
		super(Confirm, self).__init__()
		loadUi('Scripts_UI/_Predict_/Page_1/Model_Confirmation.ui', self) # Load UI File

		self.model_type = Choose_Loaded_Model.Choose_Model.stock_model_type(self)

		if self.model_type == 'CNN' or self.model_type == 'RNN':

			# ------- Read Model Summary Output ------- #

			stdout = sys.stdout
			s = StringIO()
			sys.stdout = s
			Select_Previous_Model.Previous_Model.stock_model(self)
			sys.stdout = stdout
			s.seek(0)
			self.model_.setText(str(s.read()))
			self.model_.setAlignment(QtCore.Qt.AlignCenter)

		else:

			# ----- Connection ----- #

			config = {
			    'user'    : 'flo',
			    'host'    : 'localhost',
			    'password': '',
			    'database': 'automatic_learning_v2'
			}

			conn = mysql.connector.connect(**config)
			conn.set_converter_class(Converter.NumpyMySQLConverter)

			cursor = conn.cursor()

			# ----- Query - Get Params ----- #

			self.username = Auth_Page.Auth.stock_username(self)
			self.model_name = Select_Previous_Model.Previous_Model.get_model_name(self)
			self.list_params = Choose_Loaded_Model.Choose_Model.stock_list_params(self)
			self.date = Select_Previous_Model.Previous_Model.get_date(self)

			sql = "SELECT model_machine_learning.id, " + (str(self.list_params).strip('[]')).replace("'","") + ", username, algo FROM model_machine_learning \
					INNER JOIN profile ON model_machine_learning.fk_profile = profile.id \
			 		INNER JOIN algo ON model_machine_learning.fk_algo = algo.id \
			 	 	WHERE profile.username = '" + self.username + "' \
			 	 	AND algo.algo = LOWER('" + self.model_type + "')  \
			 	 	AND model_machine_learning.name = '" + self.model_name + "' \
			 	 	AND model_machine_learning.date = '" + str(self.date) + "'"
			cursor.execute(sql)

			# ----- Set Settings Names in Labels ----- #

			rows = cursor.fetchall()
			# self.settings_label.setText((str(self.list_params).strip('[]')).replace("'",""))

			try:
				for i in range(len(self.list_params)):
					all_settings_labels = getattr(self, "settings_label_" + str(i))
					all_settings_labels.setText(self.list_params[i])

			except IndexError as e:
				print('[Is_Catched]',e)

			# ----- Set Settings Values in Labels ----- #

			list_params_values = []

			for i in range(len(self.list_params)):
				list_params_values.append(str(rows[0][i+1]))
				i += 1

			try:
				for i in range(len(list_params_values)):
					all_settings_values = getattr(self, "settings_values_" + str(i))
					all_settings_values.setText(list_params_values[i])

			except IndexError as e:
				print('[Is_Catched]',e)

			# setting_1 = settings_list[0] if len(settings_list) > 0 else ''
			# setting_2 = settings_list[1] if len(settings_list) > 1 else ''

			# self.settings_values.setText(str(setting_1))
			self.id = str(rows[0][0])

			# ----- Query - Get Results ----- #

			self.list_results = Choose_Loaded_Model.Choose_Model.stock_list_results(self)
			self.results = (str(self.list_results).strip('[]')).replace("'","")
			print(self.results)

			sql = "SELECT " + self.results + " FROM resultats \
					WHERE resultats.fk_model = '" + self.id +"'"
			cursor.execute(sql)

			# ----- Set Results Names in Labels ----- #

			rows = cursor.fetchall()

			try:
				for i in range(len(self.list_results)):
					all_score_label = getattr(self, "result_label_" + str(i))
					all_score_label.setText(self.list_results[i])

			except IndexError as e:
				print('[Is_Catched]',e)


			# ----- Set Results Values in Labels ----- #

			list_results_values = []

			for i in range(len(self.list_results)):
				list_results_values.append(str(rows[0][i]))
				i += 1
			
			try:
				for i in range(len(list_results_values)):
					all_result_values = getattr(self, "result_values_" + str(i))
					all_result_values.setText(list_results_values[i])

			except IndexError as e:
				print('[Is_Catched]',e)
				

		# ------- Main Buttons ------- #

		self.back_to_selection.clicked.connect(self.clicked_back)
		self.confirm.clicked.connect(self.confirm_selection)

		self.center() # Center Function
		self.show()


	def center(self):

		# Center Window

		frameGm = self.frameGeometry()
		screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
		centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())


	def clicked_back(self):

		self.hide()
		self.window = Select_Previous_Model.Previous_Model()

		Main_Page.Main_Page.style(self)

	def confirm_selection(self):
		print('Validé !')

