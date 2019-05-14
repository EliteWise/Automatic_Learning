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

from Scripts_UI._DataBase_ import Database
from Scripts_UI._DataBase_ import Converter
from Scripts_UI._MainPage_.Main import Main_Page
from Scripts_UI.CNN.Page_2 import Settings_CNN
from Scripts_UI._MainPage_.Main_Create import Choose_Model
from Scripts_UI.CNN.Page_3 import Graphics
from Scripts_UI._Predict_.Page_1 import Model_Confirmation
from Scripts_UI._MainPage_.Main_Predict import Choose_Loaded_Model
from Scripts_UI._MainPage_._Auth_ import Auth_Page

import cv2
import numpy as np

class Popup(QMainWindow):

	def __init__(self):
		super(Popup, self).__init__()
		loadUi('Scripts_UI/CNN/Popups/popup_img.ui', self) # Load UI File

		self.resetPopup.clicked.connect(self.close)

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


class Previous_Model(QMainWindow):

	def __init__(self):
		super(Previous_Model, self).__init__()
		loadUi('Scripts_UI/_Predict_/Page_0/Select_Previous_Model.ui', self) # Load UI File

		self.model_type = Choose_Loaded_Model.Choose_Model.stock_model_type(self)
		self.back.clicked.connect(self.clicked_back)

		if self.model_type == 'CNN' or self.model_type == 'RNN':

			self.path = 'C:/Users/Dell/Desktop/[ Automatic Learning ]/Models/' + self.model_type

			for root, dirs, files in os.walk(self.path):
				self.listWidget.addItems(files)

			self.listWidget.itemClicked.connect(self.clicked_model)

		else:

			self.get_resultats()


	def center(self):

		# Center Window

		frameGm = self.frameGeometry()
		screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
		centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())


	def clicked_model(self, item):
		print('Model: {}'.format(item.text()))

		# global model
		# model = load_model(self.path + '/' + item.text())

		self.hide()
		self.window = Model_Confirmation.Confirm()

		Main_Page.Main_Page.style(self)		


	def stock_model(self):
		return model.summary()

	def get_resultats(self):
		global model_name
		global date

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

		# ----- Execute Query ----- #

		self.username = Auth_Page.Auth.stock_username(self)

		sql = "SELECT date, name, username, algo FROM model_machine_learning \
				INNER JOIN profile ON model_machine_learning.fk_profile = profile.id \
		 		INNER JOIN algo ON model_machine_learning.fk_algo = algo.id \
		 	 	WHERE profile.username = '" + self.username + "' \
		 	 	AND algo.algo = LOWER('" + self.model_type + "')"
		cursor.execute(sql)

		# ----- Get and Return Datas ----- #

		try:

			rows = cursor.fetchall()

			model_name = rows[0][1]
			date = rows[0][0]

			self.listWidget.addItem('Date: ' + str(rows[0][0]) + ' | Name: ' + str(rows[0][1]))
			self.listWidget.itemClicked.connect(self.clicked_model)

		except IndexError:
			print('Query Error')
			self.window = Popup()

		# ------------------------ #

		self.center() # Center Function
		self.show()

	def get_model_name(self):
		return model_name

	def get_date(self):
		return date

	def clicked_back(self):
		self.hide()
		self.window = Choose_Loaded_Model.Choose_Model()
		Main_Page.Main_Page.style(self)
