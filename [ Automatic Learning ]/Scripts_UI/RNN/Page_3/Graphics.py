import os, sys, PyQt5
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from Scripts_UI.CNN import Pipeline_CNN
from Scripts_UI.CNN.Page_2 import Settings_CNN

from Scripts_UI.CNN.Page_1.Load_Images import *
from Scripts_UI.CNN.Page_2.Settings_CNN import *
from Scripts_UI.CNN.Pipeline_CNN import *


class Graph_page(QMainWindow):
 
	def __init__(self):
		super(Graph_page, self).__init__()
		loadUi('Scripts_UI/CNN/Page_3/GraphPage.ui', self) # Load UI File

		self.graph_acc.clicked.connect(self.plot_acc)
		self.graph_loss.clicked.connect(self.plot_loss)
		self.main_menu.clicked.connect(self.back_to_menu)
		self.save.clicked.connect(self.save_model)

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

	def save_model(self):
		self.hide()
		self.window = Main_Page.Main_Page()
		Main_Page.Main_Page.style(self)

		if 'History' in globals():
			del History

	def back_to_menu(self):
		self.hide()
		self.window = Main_Page.Main_Page()
		Main_Page.Main_Page.style(self)

		if 'History' in globals():
			del History

		os.remove(Settings_CNN.filepath_train + '/' + Settings_CNN.name_train_f)
