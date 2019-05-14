import os, sys, PyQt5
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from PyQt5.QtCore import *
from PyQt5.QtGui import *

import datetime
import mysql.connector
import h5py

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from Scripts_UI.CNN import Pipeline_CNN
from Scripts_UI.CNN.Page_2 import Settings_CNN
from Scripts_UI._DataBase_ import Database
from Scripts_UI._DataBase_ import Converter
from Scripts_UI._MainPage_._Auth_ import Auth_Page

from Scripts_UI.CNN.Page_1.Load_Images import *
from Scripts_UI.CNN.Page_2.Settings_CNN import *
from Scripts_UI.CNN.Pipeline_CNN import *

class Graph_page(QMainWindow):
 
	def __init__(self):
		super(Graph_page, self).__init__()
		loadUi('Scripts_UI/CNN/Page_3/GraphPage.ui', self) # Load UI File

		#Database.Connection.query(self)

		self.graph_acc.clicked.connect(self.plot_acc)
		self.graph_loss.clicked.connect(self.plot_loss)
		self.save.clicked.connect(self.save_settings_cnn)
		self.delete_.clicked.connect(self.delete_settings_cnn)

		self.back.clicked.connect(self.clicked_back)
		self.main_menu.clicked.connect(self.clicked_main_menu)

		self.acc_values()
		self.loss_values()

		self.show_values()
		self.center() # Center Function
		self.show()


	def center(self):

		# Center Window

		frameGm = self.frameGeometry()
		screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
		centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

#------------------------- Load Graphics ---------------

	def plot_acc(self):
		History = Settings_CNN.Set_Settings_CNN.stock_history(self) 

		plt.plot(History.history['acc'])
		plt.plot(History.history['val_acc'])
		plt.title('model accuracy')
		plt.ylabel('accuracy')
		plt.xlabel('Epoch')
		plt.legend(['accuracy','Val_acc'],loc = 'lower right')
		plt.show()

	def plot_loss(self):
		History = Settings_CNN.Set_Settings_CNN.stock_history(self) 

		plt.plot(History.history['loss'])
		plt.plot(History.history['val_loss'])
		plt.title('model Loss')
		plt.ylabel('Loss')
		plt.xlabel('Epoch')
		plt.legend(['Loss','Val_Loss'])
		plt.show()

	def acc_values(self):
		History_t = Settings_CNN.Set_Settings_CNN.stock_history(self)

		self.acc = round(History_t.history['acc'][-1],2)
		return self.acc

	def loss_values(self):
		History_t = Settings_CNN.Set_Settings_CNN.stock_history(self)

		self.loss = round(History_t.history['loss'][-1],2)
		return self.loss

#------------------- Show Graphics ---------------


	def show_values(self):

		self.acc_value.setText(str(self.acc))
		self.loss_value.setText(str(self.loss))


	def save_settings_cnn(self):

		self.hide()
		self.window = Main_Page.Main_Page()
		Main_Page.Main_Page.style(self)

		if 'History' in globals():
			del History

		os.remove(Settings_CNN.filepath_train + '/' + Settings_CNN.name_train_f)

	def delete_settings_cnn(self):

		name_model = Settings_CNN.Set_Settings_CNN.stock_model_name(self)
		filepath = Settings_CNN.Set_Settings_CNN.stock_filepath_train(self)

		if os.path.exists():
			os.remove(filepath + '/' + name_model)

		self.hide()
		self.window = Main_Page.Main_Page()
		Main_Page.Main_Page.style(self)

		if 'History' in globals():
			del History

		os.remove(Settings_CNN.filepath_train + '/' + Settings_CNN.name_train_f)


	def clicked_back(self):
		self.hide()
		self.window = Settings_CNN.Set_Settings_CNN()
		Main_Page.Main_Page.style(self)

	def clicked_main_menu(self):
		self.hide()
		self.window = Main_Page.Main_Page()
		Main_Page.Main_Page.style(self)

		# # ----- Connection ----- #

		# config = {
		#     'user'    : 'flo',
		#     'host'    : 'localhost',
		#     'password': '',
		#     'database': 'automatic_learning'
		# }

		# conn = mysql.connector.connect(**config)
		# conn.set_converter_class(Converter.NumpyMySQLConverter)

		# cursor = conn.cursor()

		# # ----- Get Variables ----- #

		# name_model = Settings_CNN.Set_Settings_CNN.stock_model_name(self)
		# filepath = Settings_CNN.Set_Settings_CNN.stock_filepath_train(self)
	
		# #t_model = h5py.File(filepath + '/' + name_model, 'r')

		# with open(filepath + '/' + name_model, 'rb') as file:
		# 	model = file.read()


		# date = datetime.datetime.now()
		# name = self.settings_name.text() if not self.settings_name.text() == '' else str(date.strftime("%d/%m/%Y %H:%M"))
		# fk_profile = "SELECT id FROM profile WHERE username ='" + Auth_Page.Auth.stock_username(self) + "'"
		# cursor.execute(fk_profile)

		# # ----- Execute Query ----- #

		# rows = cursor.fetchall()

		# sql = "INSERT INTO cnn_settings (date, model, name, fk_profile) VALUES (%s, %s, %s, %s)"
		# val = (date, model, name, rows[0][0])

		# cursor.execute(sql, val)
		# conn.commit()

		# # ---- Back to Main Page ---- #

		# self.hide()
		# self.window = Main_Page.Main_Page()
		# Main_Page.Main_Page.style(self)

		# if 'History' in globals():
		# 	del History

		# # ------------------------ #
