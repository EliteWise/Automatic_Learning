import os, sys, PyQt5
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn import metrics

import mysql.connector
import datetime
import time

from Scripts_UI.Reglin.Page_1 import DataFrame_Viewer
from Scripts_UI._MainPage_.Main_Create import Choose_Model
from Scripts_UI._DataBase_ import Database
from Scripts_UI._DataBase_ import Converter
from Scripts_UI._MainPage_._Auth_ import Auth_Page
from Scripts_UI._MainPage_.Main import Main_Page

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

class Load_Settings(QMainWindow):

	def __init__(self):
		super(Load_Settings, self).__init__()
		loadUi('Scripts_UI/Reglin/Page_4/Settings_Reglin.ui', self) # Load UI File

		self.run.clicked.connect(self.pipeline_reglin)
		self.save_settings.clicked.connect(self.save_settings_reglin)

		self.back.clicked.connect(self.clicked_back)
		self.main_menu.clicked.connect(self.clicked_main_menu)

		self.center() # Center Function
		self.show()

	def center(self):

		# Center Window

		frameGm = self.frameGeometry()
		screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
		centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())


	def pipeline_reglin(self):

		# ------ Get DataFrame ------ #

		df = DataFrame_Viewer.Show_Datas.stock_df(self)

		# ------ Main Settings ------ #

		self.y = self.y_.text() if not self.y_.text() == '' else df.iloc[:,-1].name
		self.X = df.drop([self.y], axis=1)
		self.test_size = float(self.test_size_.text()) if not self.test_size_.text() == '' else 0.20

		# ------ Drop Objects Columns ------ #

		self.X.drop(self.X.select_dtypes(['object']), inplace=True, axis=1)

		# ------ Preprocess ------ #

		X_train, X_test, y_train, y_test = train_test_split(self.X, df[self.y], test_size = self.test_size)

		# ------ Training ------ #

		regressor = LinearRegression()  
		regressor.fit(X_train, y_train)

		# ------ Predictions ------ #

		y_pred = regressor.predict(X_test)  

		# ------ Coeff ------ #

		coeff_df = pd.DataFrame(regressor.coef_, self.X.columns, columns=['Coefficient'])  
		model = PandasModel(coeff_df)
		self.coeff_view.setModel(model)

		# ------ Evaluate ------ #

		self.mae_view.setText(str(metrics.mean_absolute_error(y_test, y_pred)))
		self.mse_view.setText(str(metrics.mean_squared_error(y_test, y_pred)))
		self.rmse_view.setText(str(np.sqrt(metrics.mean_squared_error(y_test, y_pred))))

		# ---------------------- #

	def get_settings(self):

		# ----- Connection ----- #

		config = {
		    'user'    : 'flo',
		    'host'    : 'localhost',
		    'password': '',
		    'database': 'automatic_learning'
		}

		conn = mysql.connector.connect(**config)
		conn.set_converter_class(Converter.NumpyMySQLConverter)

		cursor = conn.cursor()

		# ----- Execute Query ----- #

		sql = "SELECT test_size FROM reglin_settings"
		cursor.execute(sql)

		# ----- Get and Return Datas ----- #

		rows = cursor.fetchall()

		return rows[0][0]

		# ------------------------ #


	def save_settings_reglin(self):

		# ----- Connection ----- #

		config = {
		    'user'    : 'flo',
		    'host'    : 'localhost',
		    'password': '',
		    'database': 'automatic_learning'
		}

		conn = mysql.connector.connect(**config)
		conn.set_converter_class(Converter.NumpyMySQLConverter)

		cursor = conn.cursor()

		# ----- Get Variables ----- #

		date = datetime.datetime.now()
		name = self.settings_name.text() if not self.settings_name.text() == '' else str(date.strftime("%d/%m/%Y %H:%M"))
		fk_profile = "SELECT id FROM profile WHERE username ='" + Auth_Page.Auth.stock_username(self) + "'"
		cursor.execute(fk_profile)

		# ----- Execute Query ----- #

		rows = cursor.fetchall()

		sql = "INSERT INTO reglin_settings (date, test_size, name, fk_profile) VALUES (%s, %s, %s, %s)"
		val = (date, self.test_size, name, rows[0][0])

		cursor.execute(sql, val)
		conn.commit()

		# ----- Back to Main Page ----- #
		
		time.sleep(1)

		self.hide()
		self.window = Main_Page.Main_Page()
		Main_Page.Main_Page.style(self)

		# ------------------------ #

	def clicked_back(self):
		self.hide()
		self.window = DataFrame_Viewer.Show_Datas()
		Main_Page.Main_Page.style(self)

	def clicked_main_menu(self):
		self.hide()
		self.window = Main_Page.Main_Page()
		Main_Page.Main_Page.style(self)