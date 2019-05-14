import os, sys, PyQt5
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Scripts_UI._MainPage_.Main import Main_Page
from Scripts_UI.Reglin.Page_0 import Dataset_Selection_Mode as Reglin_Mode
from Scripts_UI.KMeans.Page_0 import Dataset_Selection_Mode as KMeans_Mode
from Scripts_UI.KNN.Page_0 import Dataset_Selection_Mode as KNN_Mode
from Scripts_UI.SVM.Page_0 import Dataset_Selection_Mode as SVM_Mode

from Scripts_UI.CNN.Page_1 import Load_Images
from Scripts_UI.CNN.Page_2 import Settings_CNN

class Choose_Model(QMainWindow):

	def __init__(self):
		super(Choose_Model, self).__init__()
		loadUi('Scripts_UI/_MainPage_/Main_Create/Choose_Model.ui', self) # Load UI File

		self.category = Main_Page.Main_Page.stock_category(self)

		if self.category == 'Machine Learning':
			self.cnn_model.hide()
			self.rnn_model.hide()

		elif self.category == 'Deep Learning':
			self.knn_model.hide()
			self.reglin_model.hide()
			self.kmeans_model.hide()
			self.svm_model.hide()

		self.cnn_model.clicked.connect(self.Pipeline_CNN)
		self.knn_model.clicked.connect(self.Pipeline_KNN)
		self.rnn_model.clicked.connect(self.Pipeline_RNN)
		self.reglin_model.clicked.connect(self.Pipeline_REGLIN)
		self.kmeans_model.clicked.connect(self.Pipeline_K_Means)
		self.svm_model.clicked.connect(self.Pipeline_SVM)

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

	def Pipeline_CNN(self):

		self.close()
		self.window = Load_Images.Import_Image()

		Main_Page.Main_Page.style(self)

	def Pipeline_KNN(self):

		self.close()
		self.window = KNN_Mode.Select_Mode()

		Main_Page.Main_Page.style(self)

	def Pipeline_RNN(self):

		self.close()
		self.window = Reglin_Mode.Select_Mode()

		Main_Page.Main_Page.style(self)

	def Pipeline_REGLIN(self):

		self.close()
		self.window = Reglin_Mode.Select_Mode()

		Main_Page.Main_Page.style(self)

	def Pipeline_K_Means(self):

		self.close()
		self.window = KMeans_Mode.Select_Mode()

	def Pipeline_SVM(self):

		self.close()
		self.window = SVM_Mode.Select_Mode()

		Main_Page.Main_Page.style(self)

	def clicked_back(self):
		self.hide()
		self.window = Main_Page.Main_Page()
		Main_Page.Main_Page.style(self)