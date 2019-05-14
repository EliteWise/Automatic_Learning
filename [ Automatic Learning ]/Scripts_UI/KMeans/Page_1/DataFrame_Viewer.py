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

from Scripts_UI.CNN.Page_1.Load_Images import *
from Scripts_UI.CNN.Page_2.Settings_CNN import *
from Scripts_UI.CNN.Pipeline_CNN import *

from Scripts_UI.KMeans.Page_1_1 import GlobalStats_Page
from Scripts_UI.CNN import Pipeline_CNN
from Scripts_UI.KMeans.Page_2 import Plot_Page
from Scripts_UI.KMeans.Page_4 import Settings_KMeans
from Scripts_UI.KMeans.Page_0 import Dataset_Selection_Mode

# --------------------------- Function to Show DataFrame Correctly ----------------------------- #

class PandasModel(QtCore.QAbstractTableModel): 
	def __init__(self, df = pd.DataFrame(), parent=None): 
		QtCore.QAbstractTableModel.__init__(self, parent=parent)
		self._df = df

	def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
		if role != QtCore.Qt.DisplayRole:
			return QtCore.QVariant()

		if orientation == QtCore.Qt.Horizontal:
			try:
				return self._df.columns.tolist()[section]
			except (IndexError, ):
				return QtCore.QVariant()
		elif orientation == QtCore.Qt.Vertical:
			try:
				# return self.df.index.tolist()
				return self._df.index.tolist()[section]
			except (IndexError, ):
				return QtCore.QVariant()

	def data(self, index, role=QtCore.Qt.DisplayRole):
		if role != QtCore.Qt.DisplayRole:
			return QtCore.QVariant()

		if not index.isValid():
			return QtCore.QVariant()

		return QtCore.QVariant(str(self._df.ix[index.row(), index.column()]))

	def setData(self, index, value, role):
		row = self._df.index[index.row()]
		col = self._df.columns[index.column()]
		if hasattr(value, 'toPyObject'):
			value = value.toPyObject()
		else:
			# PySide gets an unicode
			dtype = self._df[col].dtype
			if dtype != object:
				value = None if value == '' else dtype.type(value)
			self._df.set_value(row, col, value)
		return True

	def rowCount(self, parent=QtCore.QModelIndex()): 
		return len(self._df.index)

	def columnCount(self, parent=QtCore.QModelIndex()): 
		return len(self._df.columns)

	def sort(self, column, order):
		colname = self._df.columns.tolist()[column]
		self.layoutAboutToBeChanged.emit()
		self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
		self._df.reset_index(inplace=True, drop=True)
		self.layoutChanged.emit()

# --------------------------- Class ----------------------------- #

class Show_Datas(QMainWindow):
 
	def __init__(self):
		super(Show_Datas, self).__init__()
		loadUi('Scripts_UI/KMeans/Page_1/DataFrame_Viewer.ui', self) # Load UI File

		# --------------- Default Dataset Mode --------------- #

		global get_df

		self.mode = Dataset_Selection_Mode.Select_Mode.stock_mode(self)

		if self.mode == 'default':

			self.path_csv.hide()
			self.label_2.hide()

			# Define path
			path = 'Datasets/KMeans/College.csv'
			self.df = pd.read_csv(path)
			get_df = pd.DataFrame(self.df)
			model = PandasModel(self.df)
			self.view_dataframe.setModel(model)

		# ---------------------------------------------------- #

		self.show_data.clicked.connect(self.manage_all)
		self.choose_plot.clicked.connect(self.from_df_to_plot)
		self.stats.clicked.connect(self.from_df_to_global_stats)
		self.settings.clicked.connect(self.from_df_to_fit)

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

	# Manage Selection

	def manage_all(self):
		global get_df

		# Define path
		if self.mode != 'default':
			path = 'CSV/' + self.path_csv.text()
			self.df = pd.read_csv(path)
			get_df = pd.DataFrame(self.df)
		
		# Select Row + Column
		if self.select_row.text() != '' and self.select_column.text() != '':
			row = self.select_row.text()
			df_r = self.df.loc[[int(row)],self.select_column.text()]
			df_r = df_r.reset_index()
			a = df_r.drop(['index'], axis=1)
			model = PandasModel(a)
			self.view_dataframe.setModel(model)


		# Select Only Row
		elif self.select_row.text() != '':
			row = self.select_row.text()
			df_r = self.df[self.df.index == int(row)]
			df_r = df_r.reset_index()
			a = df_r.drop(['index'], axis=1)
			model = PandasModel(a)
			self.view_dataframe.setModel(model)


		# Select Only Column
		elif self.select_column.text() != '':
			column = self.select_column.text()
			df1 = pd.DataFrame(self.df[column])
			model = PandasModel(df1)
			self.view_dataframe.setModel(model)


		# Select All DataFrame
		else:
			model = PandasModel(self.df)
			self.view_dataframe.setModel(model)

# --------------------------- Plot Page ----------------------------- #			

	def from_df_to_plot(self):
		self.hide()
		self.window = Plot_Page.Plot()
		Main_Page.Main_Page.style(self)

	def from_df_to_global_stats(self):
		self.hide()
		self.window = GlobalStats_Page.Global_Stats()
		Main_Page.Main_Page.style(self)

	def from_df_to_fit(self):
		self.hide()
		self.window = Settings_KMeans.Load_Settings()
		Main_Page.Main_Page.style(self)

	def stock_df(self):
		return get_df

	def clicked_back(self):
		self.hide()
		self.window = Dataset_Selection_Mode.Select_Mode()
		Main_Page.Main_Page.style(self)


				

