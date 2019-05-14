import os, sys, PyQt5
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from PyQt5.QtCore import *
from PyQt5.QtGui import *

import time, threading
from multiprocessing import Queue

from Scripts_UI._MainPage_.Main_Create import Choose_Model
from Scripts_UI._MainPage_.Main_Predict import Choose_Loaded_Model
from Scripts_UI._MainPage_.Main import Main_Page
from Scripts_UI._DataBase_ import Database

class Popup_Wrong_Password(QMainWindow):

	def __init__(self):
		super(Popup_Wrong_Password, self).__init__()
		loadUi('Scripts_UI/_MainPage_/_Auth_/Popups/Popup_Wrong_Password.ui', self) # Load UI File

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


class Popup_Wrong_Password_Sign_Up(QMainWindow):

	def __init__(self):
		super(Popup_Wrong_Password_Sign_Up, self).__init__()
		loadUi('Scripts_UI/_MainPage_/_Auth_/Popups/Popup_Wrong_Password_Sign_Up.ui', self) # Load UI File

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


class Auth(QMainWindow):

	def __init__(self):
		super(Auth, self).__init__()
		loadUi('Scripts_UI/_MainPage_/_Auth_/authentication.ui', self) # Load UI File

		self.test.hide()

		self.login_button.clicked.connect(self.login_f)
		self.signup_button.clicked.connect(self.sign_up_f)

		self.validate_login.clicked.connect(self.v_login)
		self.validate_sign_up.clicked.connect(self.v_sign_up)

		# ------ Hide Password ------ #

		self.password.setEchoMode(QLineEdit.Password)
		self.signup_password.setEchoMode(QLineEdit.Password)
		self.signup_password_2.setEchoMode(QLineEdit.Password)

		self.center() # Center Function
		self.show()


	def center(self):

		# Center Window

		frameGm = self.frameGeometry()
		screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
		centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())


# ------- Switch Between Frames ------- #

	def login_f(self):
		self.login_frame.show()
		self.sign_up_frame.hide()

	def sign_up_f(self):
		self.login_frame.hide()
		self.sign_up_frame.show()


# ------- Check Authentication ------- #

	def v_login(self):

		# Check password in Database match with the Client

		if Database.Connection.check_existing_profile(self)[0] == self.username.text() and \
			Database.Connection.check_existing_profile(self)[1] == self.password.text():

			global t_name
			t_name = self.username.text()

			self.hide()
			self.window = Main_Page.Main_Page()
			Main_Page.Main_Page.style(self)

		else:
			self.window = Popup_Wrong_Password()
			Main_Page.Main_Page.style(self)

	def v_sign_up(self):
		
		# Check Password + Register username and password in Database

		if self.signup_password.text() == self.signup_password_2.text():

			self.hide()
			self.window = Main_Page.Main_Page()
			Main_Page.Main_Page.style(self)

			# ---- Query ---- #

			Database.Connection.sign_up(self)

		else:
			self.window = Popup_Wrong_Password_Sign_Up()
			Main_Page.Main_Page.style(self)


	def stock_profile_datas(self):
		return self.signup_username.text(), self.signup_password.text()

	def check(self):
		return self.username.text(), self.password.text()

	def style(self):
		stream = QtCore.QFile("QSS/Style.qss") # Get Style file
		stream.open(QtCore.QIODevice.ReadOnly)
		self.window.setStyleSheet(QtCore.QTextStream(stream).readAll()) # Set it

	def stock_username(self):
		return t_name