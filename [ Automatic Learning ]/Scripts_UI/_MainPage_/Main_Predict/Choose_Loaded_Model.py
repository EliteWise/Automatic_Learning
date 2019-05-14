import os, sys, PyQt5
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Scripts_UI._MainPage_.Main import Main_Page
from Scripts_UI.CNN.Page_1 import Load_Images
from Scripts_UI.CNN.Page_2 import Settings_CNN
from Scripts_UI._Predict_.Page_0 import Select_Previous_Model

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

class Choose_Model(QMainWindow):

	def __init__(self):
		super(Choose_Model, self).__init__()
		loadUi('Scripts_UI/_MainPage_/Main_Predict/Choose_Model.ui', self) # Load UI File

		self.category = Main_Page.Main_Page.stock_category(self)

		if self.category == 'Machine Learning':
			self.cnn_model.hide()
			self.rnn_model.hide()

		elif self.category == 'Deep Learning':
			self.knn_model.hide()
			self.reglin_model.hide()
			self.kmeans_model.hide()
			self.svm_model.hide()

		self.cnn_model.clicked.connect(self.load_model_cnn)
		self.rnn_model.clicked.connect(self.load_model_rnn)
		self.knn_model.clicked.connect(self.load_model_knn)
		self.svm_model.clicked.connect(self.load_model_svm)
		self.kmeans_model.clicked.connect(self.load_model_kmeans)
		self.reglin_model.clicked.connect(self.load_model_reglin)

		self.back.clicked.connect(self.clicked_back)

		self.center() # Center Function
		self.show()


	def center(self):

		# Center Window

		frameGm = self.frameGeometry()
		screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
		centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

	def load_model_cnn(self):
		global model_type
		model_type = 'CNN'

		self.hide()
		self.window = Select_Previous_Model.Previous_Model()
		Main_Page.Main_Page.style(self)

	def load_model_rnn(self):
		global model_type
		model_type = 'RNN'

		self.hide()
		self.window = Select_Previous_Model.Previous_Model()
		Main_Page.Main_Page.style(self)

	def load_model_knn(self):
		global model_type
		global list_params
		global list_results
		model_type = 'KNN'

		list_params = ['test_size', 'neighbors']
		list_results = ['accuracy']

		self.hide()
		self.window = Select_Previous_Model.Previous_Model()
		Main_Page.Main_Page.style(self)

	def load_model_svm(self):
		global model_type
		global list_params
		global list_results
		model_type = 'SVM'

		list_params = ['test_size', 'kernel']
		list_results = ['accuracy']

		self.hide()
		self.window = Select_Previous_Model.Previous_Model()
		Main_Page.Main_Page.style(self)

	def load_model_kmeans(self):
		global model_type
		global list_params
		global list_results
		model_type = 'KMEANS'

		list_params = ['nb_clusters', 'category_name']
		list_results = ['score']

		self.hide()
		self.window = Select_Previous_Model.Previous_Model()
		Main_Page.Main_Page.style(self)

	def load_model_reglin(self):
		global model_type
		global list_params
		global list_results
		model_type = 'REGLIN'

		list_params = ['test_size']
		list_results = ['mae', 'mse', 'rmse']

		self.hide()
		self.window = Select_Previous_Model.Previous_Model()
		Main_Page.Main_Page.style(self)

	def clicked_back(self):
		self.hide()
		self.window = Main_Page.Main_Page()
		Main_Page.Main_Page.style(self)

	def stock_model_type(self):
		return model_type

	def stock_list_params(self):
		return list_params

	def stock_list_results(self):
		return list_results