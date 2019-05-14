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
from Scripts_UI.KMeans.Page_1 import DataFrame_Viewer
from Scripts_UI.KMeans.Page_1_2 import NaN_Page
from Scripts_UI.KMeans.Page_1_1 import GlobalStats_Page
from Scripts_UI.KMeans.Page_1 import DataFrame_Viewer


from Scripts_UI.CNN.Page_1.Load_Images import *
from Scripts_UI.CNN.Page_2.Settings_CNN import *
from Scripts_UI.CNN.Pipeline_CNN import *
from Scripts_UI.KMeans.Page_1.DataFrame_Viewer import *

class NaN_Stats(QMainWindow):
 
	def __init__(self):
		super(NaN_Stats, self).__init__()
		loadUi('Scripts_UI/KMeans/Page_1_2/NaN_Stats.ui', self) # Load UI File

		self.g_button.clicked.connect(self.switch_to_global)

		self.back.clicked.connect(self.clicked_back)

		self.nan_generator()
		self.center() # Center Function
		self.show()


	def center(self):

		# Center Window

		frameGm = self.frameGeometry()
		screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
		centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())


	def switch_to_global(self):
		self.hide()
		self.window = GlobalStats_Page.Global_Stats()
		Main_Page.Main_Page.style(self)


	def nan_generator(self):
		self.df = DataFrame_Viewer.Show_Datas.stock_df(self) # Get DataFrame selected from Reglin_Page

		try:
			for i in range(len(self.df)):
				all_nan = getattr(self, "nan_" + str(i))
				all_nan.setText(str(self.df.iloc[:,i].isnull().sum()))

		except IndexError as e:
			print('[Is_Catched]',e)

		try:
			for i in range(len(self.df)):
				all_columns = getattr(self, "col_" + str(i))
				all_columns.setText(self.df.columns[i])

		except IndexError as e:
			print('[Is_Catched]',e)

		self.nan_total.setText(str(self.df.isnull().sum().sum()))

	def clicked_back(self):
		self.hide()
		self.window = DataFrame_Viewer.Show_Datas()
		Main_Page.Main_Page.style(self)
