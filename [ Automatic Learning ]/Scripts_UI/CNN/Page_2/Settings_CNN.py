import os, sys, PyQt5
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PIL import Image
import matplotlib.image as mpimg
import numpy as np

import mysql.connector

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.callbacks import EarlyStopping, ModelCheckpoint, Callback 
from keras.models import load_model

from sklearn.model_selection import train_test_split

from Scripts_UI._MainPage_.Main import Main_Page
from Scripts_UI.CNN.Page_3 import Graphics
from Scripts_UI.CNN import Pipeline_CNN

from Scripts_UI.CNN.Page_1.Load_Images import *
from Scripts_UI.CNN.Page_3.Graphics import *

from Scripts_UI.CNN.Page_1 import Load_Images
from Scripts_UI._MainPage_.Main_Create import Choose_Model

# Popup #

class popup_alert(QMainWindow):

	def __init__(self):
		super(popup_alert, self).__init__()
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

class Set_Settings_CNN(QMainWindow):
 
	def __init__(self):
		super(Set_Settings_CNN, self).__init__()
		loadUi('Scripts_UI/CNN/Page_2/SettingsPage_CNN.ui', self) # Load UI File

		# Set connections buttons/def

		self.image_size.clicked.connect(self.img_page)
		self.neurons.clicked.connect(self.neurons_page)
		self.functions.clicked.connect(self.Activations_page)
		self.compile.clicked.connect(self.compile_page)

		self.back.clicked.connect(self.main_settings)
		self.back_2.clicked.connect(self.main_settings)

		self.model.clicked.connect(self.model_page)
		self.train.clicked.connect(self.train_page)

		self.filepath_train.clicked.connect(self.openFolder)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
		self.run.clicked.connect(self.set_neurons) # Set parameters

		self.run.clicked.connect(self.parsing_data)
		self.run.clicked.connect(self.define_model)
		self.run.clicked.connect(self.training)
		self.run.clicked.connect(self.open_graph)

		self.back_.clicked.connect(self.clicked_back)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

		# Hide all pages except img

		self.img_layer.show()
		self.neurons_layer.hide()
		self.function_layer.hide()
		self.compile_layer.hide()
		
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
		self.center() # Center Function
		self.show()

	def center(self):

		# Center Window

		frameGm = self.frameGeometry()
		screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
		centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

	def set_neurons(self):

		global name_train_f

#------------------- IMG SIZE -----------------------------

		self.img_x_f = int(self.img_x.text()) if not self.img_x.text() == '' else 56
		self.img_y_f = int(self.img_y.text()) if not self.img_y.text() == '' else 56
		self.img_dim_f = int(self.img_dim.text()) if not self.img_dim.text() == '' else 3

#------------------- NEURONS -----------------------------

		self.n_1_f = int(self.n_1.text()) if not self.n_1.text() == '' else 32
		self.n_2_f = int(self.n_2.text()) if not self.n_2.text() == '' else 32
		self.n_3_f = int(self.n_3.text()) if not self.n_3.text() == '' else 64
		self.n_4_f = int(self.n_4.text()) if not self.n_4.text() == '' else 100
		self.n_5_f = int(self.n_5.text()) if not self.n_5.text() == '' else 62 # -> a faire : nombre de classe (nombre de label uniques)

#------------------ ACTIVATION ----------------------------	

		self.a_1_f = self.a_1.text() if not self.a_1.text() == '' else 'relu'
		self.a_2_f = self.a_2.text() if not self.a_2.text() == '' else 'relu'
		self.a_3_f = self.a_3.text() if not self.a_3.text() == '' else 'relu'
		self.a_4_f = self.a_4.text() if not self.a_4.text() == '' else 'relu'
		self.a_5_f = self.a_5.text() if not self.a_5.text() == '' else 'softmax'

		self.padding_f = self.padding.text() if not self.padding.text() == '' else 'valid'

#--------------------- COMPILE ----------------------------

		self.optimizer_f = self.optimizer.text() if not self.optimizer.text() == '' else 'adam'
		self.metrics_f = self.metrics.text() if not self.metrics.text() == '' else 'accuracy'

#----------------------- TRAINING -------------------------
		

		self.b_size_f = int(self.b_size.text()) if not self.b_size.text() == '' else 32
		self.epochs_f = int(self.epochs.text()) if not self.epochs.text() == '' else 100

		name_train_f = self.name_train.text()

		# If Model Name is null

		if name_train_f == '':
			self.window = popup_alert() # Load Popup
			Main_Page.Main_Page.style(self)
			return
		else:
			pass

		self.validation_split_f = int(self.validation_split.text()) if not self.validation_split.text() == '' else 0.2
		self.verbose_f = int(self.verbose.text()) if not self.verbose.text() == '' else 2

		self.container = [self.img_x_f,self.img_y_f,self.img_dim_f,self.n_1_f,self.n_2_f,self.n_3_f,self.n_4_f,self.n_5_f,self.a_1_f,self.a_2_f,self.a_3_f,self.a_4_f,self.a_5_f,self.padding_f,self.optimizer_f,self.metrics_f,self.b_size_f,self.epochs_f,name_train_f,self.validation_split_f,self.verbose_f]
	
		return self.container
#------------------- Switch Page -----------------------

	def compile_page(self):
		self.img_layer.hide()
		self.neurons_layer.hide()
		self.function_layer.hide()
		self.compile_layer.show()

	def img_page(self):
		self.img_layer.show()
		self.neurons_layer.hide()
		self.function_layer.hide()
		self.compile_layer.hide()

	def neurons_page(self):
		self.img_layer.hide()
		self.neurons_layer.show()
		self.function_layer.hide()
		self.compile_layer.hide()

	def Activations_page(self):
		self.img_layer.hide()
		self.neurons_layer.hide()
		self.function_layer.show()
		self.compile_layer.hide()

	def main_settings(self):
		self.model_frame.hide()
		self.train_frame.hide()
		self.main_frame.show()

	def model_page(self):
		self.model_frame.show()
		self.train_frame.hide()
		self.main_frame.hide()
		self.train_main_frame.hide()
		self.img_layer.show()

	def train_page(self):
		self.model_frame.hide()
		self.train_main_frame.show()
		self.img_layer.hide()
		self.neurons_layer.hide()
		self.function_layer.hide()
		self.compile_layer.hide()

	#-------------------- SAVE MODEL FOLDER -----------------

	def openFolder(self):
		global filepath_train

		filepath_train = QFileDialog.getExistingDirectory(self, 'Open Directory')

		return filepath_train

	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	# Pipeline Model
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	#------------------ Parse Data ----------------------------
	def parsing_data(self):

		self.X_test = []
		self.X_train = []
		self.y_train = []
		self.y_test = []

		imgs,labels = Load_Images.Import_Image.stock_img(self)

		# Define data variables
		self.X_train_full = imgs
		self.y_train_full = labels
		self.X_train,self.X_test,self.y_train,self.y_test = train_test_split(self.X_train_full,self.y_train_full,test_size=0.2)

		# Convert list to array
		self.X_train = np.asarray(self.X_train)
		self.X_test = np.asarray(self.X_test)
		self.y_train = np.asarray(self.y_train)
		self.y_test = np.asarray(self.y_test)

    #------------------ define the model ----------------------------	

	def define_model(self):

		self.model = Sequential()
		self.model.add(Conv2D(self.container[3], (3, 3), padding=self.container[13], input_shape=(self.container[0],self.container[1],self.container[2]), activation=self.container[8]))
		self.model.add(MaxPooling2D(pool_size=(2, 2)))

		self.model.add(Conv2D(self.container[4], (3, 3), padding=self.container[13], activation=self.container[9]))
		self.model.add(MaxPooling2D(pool_size=(2, 2)))

		self.model.add(Conv2D(self.container[5], (3, 3), padding=self.container[13], activation=self.container[10]))
		self.model.add(MaxPooling2D(pool_size=(2, 2)))

		# the model so far outputs 3D feature maps (height, width, features)

		self.model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
		self.model.add(Dense(self.container[6], activation=self.container[11]))
		self.model.add(Dropout(0.5))
		self.model.add(Dense(self.container[7], activation=self.container[12]))
		# COMPILE
		self.model.compile(loss='sparse_categorical_crossentropy',
		              optimizer=self.container[14],
		              metrics=[self.container[15]])

		print(self.model.summary())
    
    #------------------ Train the model ----------------------------

	def training(self):

		global History

		self.callbacks = [EarlyStopping(monitor='val_acc', patience=4),
		             ModelCheckpoint(filepath=filepath_train +'/'+ self.container[18], monitor='val_acc', save_best_only=True)]

		# TRAINING

		History = self.model.fit(self.X_train, self.y_train,
		                    validation_split= self.container[19],
		                    batch_size = self.container[16],
		                    callbacks = self.callbacks,
		                    epochs= self.container[17],
		                    verbose= self.container[20]
		                   )
		return History

	def stock_history(self):
		return History

	def stock_acc(self):
		return round(History.history['acc'][-1], 2)

	def stock_loss(self):
		return round(History.history['loss'][-1], 2)

	def stock_model_name(self):
		return name_train_f

	def stock_filepath_train(self):
		return filepath_train

	#--------------------------------------------------------

	def open_graph(self):
		self.hide()
		self.window = Graphics.Graph_page()
		Main_Page.Main_Page.style(self)

    #--------------------------------------------------------


	def clicked_back(self):
		self.hide()
		self.window = Load_Images.Import_Image()
		Main_Page.Main_Page.style(self)