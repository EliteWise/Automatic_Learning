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

from Scripts_UI.Reglin.Page_1_1 import GlobalStats_Page
from Scripts_UI.CNN import Pipeline_CNN
from Scripts_UI.Reglin.Page_2 import Plot_Page
from Scripts_UI.Reglin.Page_4 import Settings_Reglin
from Scripts_UI.Reglin.Page_1 import DataFrame_Viewer

class Select_Mode(QMainWindow):
 
	def __init__(self):
		super(Select_Mode, self).__init__()
		loadUi('Scripts_UI/Reglin/Page_0/Dataset_Selection_Mode.ui', self) # Load UI File

		self.default_dataset.clicked.connect(self.default)
		self.personal_dataset.clicked.connect(self.personal)

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

	
	def default(self):
		global selection_mode

		selection_mode = 'default'

		self.hide()
		self.window = DataFrame_Viewer.Show_Datas()
		Main_Page.Main_Page.style(self)

	def personal(self):
		global selection_mode

		selection_mode = 'personal'

		self.hide()
		self.window = DataFrame_Viewer.Show_Datas()
		Main_Page.Main_Page.style(self)

	def stock_mode(self):
		return selection_mode

	def clicked_back(self):
		self.hide()
		self.window = Choose_Model.Choose_Model()
		Main_Page.Main_Page.style(self)



				

