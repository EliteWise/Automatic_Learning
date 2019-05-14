import os, sys, PyQt5
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PIL import Image
import numpy as np

from Scripts_UI.CNN import Pipeline_CNN
from Scripts_UI.KNN.Page_1 import DataFrame_Viewer
from Scripts_UI.KNN.Page_1_2 import NaN_Page

import matplotlib.pyplot as plt

from Scripts_UI.CNN.Page_1.Load_Images import *
from Scripts_UI.CNN.Page_2.Settings_CNN import *
from Scripts_UI.CNN.Pipeline_CNN import *
from Scripts_UI.KNN.Page_1.DataFrame_Viewer import *

import pandas as pd

class Global_Stats(QMainWindow):
 
	def __init__(self):
		super(Global_Stats, self).__init__()
		loadUi('Scripts_UI/KNN/Page_1_1/Global_Stats.ui', self) # Load UI File

		self.types_view.hide()
		self.globalStats_view.show()

		self.nan_button.clicked.connect(self.switch_to_NaN)
		self.types_button.clicked.connect(self.switch_to_types)
		self.global_button.clicked.connect(self.switch_to_global)

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

	def switch_to_NaN(self):
		self.hide()
		self.window = NaN_Page.NaN_Stats()
		Main_Page.Main_Page.style(self)

	def switch_to_types(self):
		self.globalStats_view.hide()
		self.types_view.show()

		self.df = DataFrame_Viewer.Show_Datas.stock_df(self) # Get DataFrame selected from Reglin_Page

		df_types = pd.DataFrame(self.df.dtypes)
		model = DataFrame_Viewer.PandasModel(df_types)
		self.types_view.setModel(model)

	def switch_to_global(self):
		self.types_view.hide()
		self.globalStats_view.show()

		self.df_2 = DataFrame_Viewer.Show_Datas.stock_df(self) # Get DataFrame selected from Reglin_Page

		df_describe = self.df_2.describe()
		model = DataFrame_Viewer.PandasModel(df_describe)
		self.globalStats_view.setModel(model)


	def clicked_back(self):
		self.hide()
		self.window = DataFrame_Viewer.Show_Datas()
		Main_Page.Main_Page.style(self)