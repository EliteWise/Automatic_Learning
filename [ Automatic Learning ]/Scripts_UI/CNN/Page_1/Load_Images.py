import os, sys, PyQt5, os.path
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PIL import Image
from keras.models import load_model
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

import datetime
import mysql.connector
import h5py

from Scripts_UI._DataBase_ import Database
from Scripts_UI._DataBase_ import Converter
from Scripts_UI._MainPage_.Main import Main_Page
from Scripts_UI.CNN.Page_2 import Settings_CNN
from Scripts_UI._MainPage_.Main_Create import Choose_Model
from Scripts_UI.CNN.Page_3 import Graphics

import cv2
import numpy as np

class Popup(QMainWindow):

	def __init__(self):
		super(Popup, self).__init__()
		loadUi('Scripts_UI/CNN/Popups/popup_img.ui', self) # Load UI File

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


class Import_Image(QMainWindow):

	def __init__(self):
		super(Import_Image, self).__init__()
		loadUi('Scripts_UI/CNN/Page_1/Import_Image.ui', self) # Load UI File

		self.get_directory.clicked.connect(self.openFolder)
		self.img_to_settings.clicked.connect(self.load_images)

		self.img_to_settings.clicked.connect(self.stock_img)
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

	def openFolder(self):

		self.filename = QFileDialog.getExistingDirectory(self, 'Open Directory')

	def load_images(self):

		global imgs,labels

		self.format1 = self.format1.text() if not self.format1.text() == '' else '.ppm'
		self.format2 = self.format2.text() if not self.format2.text() == '' else '.jpg'
		self.format3 = self.format3.text() if not self.format3.text() == '' else '.jpg'
		self.format4 = self.format4.text() if not self.format4.text() == '' else '.jpg'

		self.img_x_resize = int(self.img_x_resize.text()) if not self.img_x_resize.text() == '' else 56 
		self.img_y_resize = int(self.img_y_resize.text()) if not self.img_y_resize.text() == '' else 56	
	
		imgs = []
		labels = []

		files = 0
		folders = []

		i = 0
		k = 0

		valid_images = [self.format1, self.format2, self.format3, self.format4]

		path = self.filename

		for _, dirnames, filenames in os.walk(path):
			if k < len(dirnames):
				folders.append(dirnames)
				k += 1
			if i < len(folders[0]):
				for _, dirnames, filenames in os.walk(path + '/' + folders[0][i]):
					for f in os.listdir(path + '/' + folders[0][i]):
						ext = os.path.splitext(f)[1]
						if ext.lower() not in valid_images:
							continue
						labels.append(folders[0][i])
						temp_img = mpimg.imread(path + '/' + folders[0][i] + '/' + f)
						resize_img = cv2.resize(temp_img, dsize=(self.img_x_resize, self.img_y_resize), interpolation=cv2.INTER_CUBIC)
						imgs.append(resize_img)
				i += 1

		previous_settings = Choose_Model.Choose_Model.load_previous_settings(self)

		if previous_settings == 'CNN':

			self.hide()
			self.window = Settings_CNN.Set_Settings_CNN()

			Main_Page.Main_Page.style(self)


			model = load_model(filepath + '/' + name_model)
			model.summary()
		else:
			self.hide()
			self.window = Settings_CNN.Set_Settings_CNN()

			Main_Page.Main_Page.style(self)

		return imgs,labels

	def stock_img(self):
		return imgs,labels


	def clicked_back(self):
		self.hide()
		self.window = Choose_Model.Choose_Model()
		Main_Page.Main_Page.style(self)

