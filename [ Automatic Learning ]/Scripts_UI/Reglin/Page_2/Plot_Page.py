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
from Scripts_UI.Reglin.Page_3 import SettingsPlot_Page
from Scripts_UI.Reglin.Page_1 import DataFrame_Viewer

from Scripts_UI.CNN.Page_1.Load_Images import *
from Scripts_UI.CNN.Page_2.Settings_CNN import *
from Scripts_UI.CNN.Pipeline_CNN import *

class Plot(QMainWindow):
 
	def __init__(self):
		super(Plot, self).__init__()
		loadUi('Scripts_UI/Reglin/Page_2/select_plot.ui', self) # Load UI File

		self.load_plot.clicked.connect(self.create_plot)

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


	def create_plot(self):
		global type_plot

		type_plot = []
		self.num_page = None

		if self.line_plot.isChecked():
			type_plot.append('line')

		elif self.bar_plot.isChecked():
			type_plot.append('bar')

		elif self.pie_plot.isChecked():
			type_plot.append('pie')

		elif self.histo_plot.isChecked():
			type_plot.append('hist')

		elif self.box_plot.isChecked():
			type_plot.append('box')

		elif self.scatter_plot.isChecked():
			type_plot.append('scatter')

		elif self.reg_plot.isChecked():
			type_plot.append('reg_plot')

		elif self.heatmap.isChecked():
			type_plot.append('heatmap')

		self.num_page = self.load_settings_page(SettingsPlot_Page)


	def stock_plot(self):
		print(type_plot[0])
		return type_plot[0]

	def clicked_back(self):
		self.hide()
		self.window = DataFrame_Viewer.Show_Datas()
		Main_Page.Main_Page.style(self)	