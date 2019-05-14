import os, sys, PyQt5
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Scripts_UI.CNN import Pipeline_CNN
from Scripts_UI.KMeans.Page_3 import SettingsPlot_Page
from Scripts_UI.KMeans.Page_1 import DataFrame_Viewer

from Scripts_UI.CNN.Page_1.Load_Images import *
from Scripts_UI.CNN.Page_2.Settings_CNN import *
from Scripts_UI.CNN.Pipeline_CNN import *

class Plot(QMainWindow):
 
	def __init__(self):
		super(Plot, self).__init__()
		loadUi('Scripts_UI/KMeans/Page_2/select_plot.ui', self) # Load UI File

		global type_plot
		type_plot = []

		self.scatter_matrix.clicked.connect(self.scatter_m)
		self.dindrogram.clicked.connect(self.dindro)
		self.scatter_plot.clicked.connect(self.scatter_p)

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


	def load_settings_page(self, page):
		self.hide()
		self.window = page.Settings()
		Main_Page.Main_Page.style(self)


	def scatter_m(self):
		type_plot.append('scatter matrix')
		self.num_page = self.load_settings_page(SettingsPlot_Page)

	def dindro(self):
		type_plot.append('dindrogram')
		self.num_page = self.load_settings_page(SettingsPlot_Page)

	def scatter_p(self):
		type_plot.append('scatter plot')
		self.num_page = self.load_settings_page(SettingsPlot_Page)

	def stock_plot(self):
		print(type_plot[0])
		return type_plot[0]


	def clicked_back(self):
		self.hide()
		self.window = DataFrame_Viewer.Show_Datas()
		Main_Page.Main_Page.style(self)