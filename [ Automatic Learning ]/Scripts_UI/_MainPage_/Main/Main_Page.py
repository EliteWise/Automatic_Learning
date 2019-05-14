import os, sys, PyQt5
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from PyQt5.QtCore import *
from PyQt5.QtGui import *

import time

from Scripts_UI._MainPage_.Main_Create import Choose_Model
from Scripts_UI._MainPage_.Main_Predict import Choose_Loaded_Model
from Scripts_UI._MainPage_._Auth_ import Auth_Page
from Scripts_UI._MainPage_._Profile_ import Profile_Page

class Popup_Sign_Up(QMainWindow):

	def __init__(self):
		super(Popup_Sign_Up, self).__init__()
		loadUi('Scripts_UI/_MainPage_/_Auth_/Popups/Popup_Sign_Up.ui', self) # Load UI File

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


class Main_Page(QMainWindow):

	def __init__(self):
		super(Main_Page, self).__init__()
		loadUi('Scripts_UI/_MainPage_/Main/Main_Page.ui', self) # Load UI File

		self.createButton_ml.clicked.connect(self.choose_model_ml)
		self.loadButton_ml.clicked.connect(self.loaded_model_ml)

		self.createButton_dl.clicked.connect(self.choose_model_dl)
		self.loadButton_dl.clicked.connect(self.loaded_model_dl)

		self.logout.clicked.connect(self.logout_session)
		self.main_menu.clicked.connect(self.main_menu_d)

		self.ml_frame.hide()
		self.dl_frame.hide()
		self.main_menu.hide()

		self.deep_learning.clicked.connect(self.dl_selection)
		self.machine_learning.clicked.connect(self.ml_selection)

		username = Auth_Page.Auth.stock_username(self)
		self.profile_name.setText(username)
		self.profile_name.setAlignment(QtCore.Qt.AlignCenter)

		self.profile_name.mousePressEvent = self.profile_stats

		self.center() # Center Function
		self.show()
		self.success_popup()


	def center(self):

		# Center Window

		frameGm = self.frameGeometry()
		screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
		centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())


	def success_popup(self):

		# ---- Popup of Success ---- #

		# self.window = Popup_Sign_Up()
		# self.style()
		pass


	def choose_model_ml(self):
		global ml_or_dl
		ml_or_dl = 'Machine Learning'

		self.close()
		self.window = Choose_Model.Choose_Model()

		self.style()

	def loaded_model_ml(self):
		global ml_or_dl
		ml_or_dl = 'Machine Learning'

		self.close()
		self.window = Choose_Loaded_Model.Choose_Model()
		
		self.style()

	def choose_model_dl(self):
		global ml_or_dl
		ml_or_dl = 'Deep Learning'

		self.close()
		self.window = Choose_Model.Choose_Model()

		self.style()

	def loaded_model_dl(self):
		global ml_or_dl
		ml_or_dl = 'Deep Learning'

		self.close()
		self.window = Choose_Loaded_Model.Choose_Model()
		
		self.style()

	def logout_session(self):
		self.close()
		self.window = Auth_Page.Auth()

		self.style()

	def profile_stats(self, event):
		self.hide()
		self.window = Profile_Page.Profile_Stats()
		
		self.style()

	def style(self):
		stream = QtCore.QFile("QSS/Style.qss") # Get Style file
		stream.open(QtCore.QIODevice.ReadOnly)
		self.window.setStyleSheet(QtCore.QTextStream(stream).readAll()) # Set it

	def ml_selection(self):
		self.ml_or_dl.hide()
		self.dl_frame.hide()
		self.ml_frame.show()
		self.main_menu.show()

	def dl_selection(self):
		self.ml_or_dl.hide()
		self.ml_frame.hide()
		self.dl_frame.show()
		self.main_menu.show()

	def main_menu_d(self):
		self.ml_or_dl.show()
		self.ml_frame.hide()
		self.dl_frame.hide()
		self.main_menu.hide()

	def stock_category(self):
		return ml_or_dl