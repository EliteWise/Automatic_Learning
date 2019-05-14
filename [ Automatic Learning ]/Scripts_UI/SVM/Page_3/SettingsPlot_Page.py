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
from Scripts_UI.SVM.Page_1 import DataFrame_Viewer
from Scripts_UI.SVM.Page_2 import Plot_Page

from Scripts_UI.CNN.Page_1.Load_Images import *
from Scripts_UI.CNN.Page_2.Settings_CNN import *
from Scripts_UI.CNN.Pipeline_CNN import *
from Scripts_UI.SVM.Page_1.DataFrame_Viewer import *

class Settings(QMainWindow):
 
	def __init__(self):
		super(Settings, self).__init__()
		loadUi('Scripts_UI/SVM/Page_3/Settings_Plot.ui', self) # Load UI File

		self.launch_plot.clicked.connect(self.create_plot)

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


# ---------------------------------- Plot Parameters ----------------------------------------- #


	def create_plot(self):

		self.current_df = DataFrame_Viewer.Show_Datas.stock_df(self)

		self.X_size_ = int(self.X_size.text()) if not self.X_size.text() == '' else 8
		self.Y_size_ = int(self.Y_size.text()) if not self.Y_size.text() == '' else 8

		self.X_1_ = self.X_1.text() if not self.X_1.text() == '' else self.current_df.columns[0]
		self.Y_1_ = self.Y_1.text() if not self.Y_1.text() == '' else self.current_df.columns[1]

		self.marker_1_ = self.marker_1.text() if not self.marker_1.text() == '' else 'o'
		self.marker_2_ = self.marker_2.text() if not self.marker_2.text() == '' else 'o'
		self.marker_3_ = self.marker_3.text() if not self.marker_3.text() == '' else 'o'

		self.name_label_Y_ = self.name_label_Y.text() if not self.name_label_Y.text() == '' else self.current_df.columns[0]
		self.name_label_X_ = self.name_label_X.text() if not self.name_label_X.text() == '' else self.current_df.columns[1]

		self.color_Y_label_ = self.color_Y_label.text() if not self.color_Y_label.text() == '' else 'black'
		self.color_X_label_ = self.color_X_label.text() if not self.color_X_label.text() == '' else 'black'

		self.title_ = self.title.text() if not self.title.text() == '' else 'Default Title'
		self.title_color_ = self.title_color.text() if not self.title_color.text() == '' else 'black'

		self.legend_1_ = self.legend_1.text() if not self.legend_1.text() == '' else '?'
		self.legend_2_ = self.legend_2.text() if not self.legend_2.text() == '' else '?'
		self.legend_3_ = self.legend_3.text() if not self.legend_3.text() == '' else '?'


# ---------------------------------- Show Advanced Plot ----------------------------------------- #

		self.type_plot = Plot_Page.Plot.stock_plot(self)
		
		plt.close('all')
		plt.figure(figsize=(self.X_size_, self.Y_size_))

		if self.type_plot == 'line':
			ax = plt.plot(self.current_df[self.X_1_], self.current_df[self.Y_1_], color='cyan', marker=self.marker_1_, label=self.legend_1_)

			if self.X_2.text() != '' and self.Y_2.text() != '':
				ax1 = plt.plot(self.current_df[self.X_2.text()], self.current_df[self.Y_2.text()], color='orange', marker=self.marker_2_, label=self.legend_2_)

			if self.X_3.text() != '' and self.Y_3.text() != '':
				ax2 = plt.plot(self.current_df[self.X_3.text()], self.current_df[self.Y_3.text()], color='brown', marker=self.marker_3_, label=self.legend_3_)

		elif self.type_plot == 'bar':
			ax = plt.bar(self.current_df[self.X_1_], self.current_df[self.Y_1_], color='cyan', label=self.legend_1_)

			if self.X_2.text() != '' and self.Y_2.text() != '':
				ax1 = plt.bar(self.current_df[self.X_2.text()], self.current_df[self.Y_2.text()], color='orange', label=self.legend_2_)

			if self.X_3.text() != '' and self.Y_3.text() != '':
				ax2 = plt.bar(self.current_df[self.X_3.text()], self.current_df[self.Y_3.text()], color='brown', label=self.legend_3_)

		elif self.type_plot == 'pie':
			self.current_df.plot.pie(y=self.current_df[self.Y_1_].name, figsize=(self.X_size_, self.Y_size_))

		elif self.type_plot == 'hist':
			plt.hist(x=self.current_df[self.X_1_].name, density=True)

		plt.ylabel(self.name_label_Y_, color=self.color_X_label_)
		plt.xlabel(self.name_label_X_, color=self.color_Y_label_)
		plt.title(self.title_, color=self.title_color_)

		if self.upper_right.isChecked():
			plt.legend(loc='upper right')
		elif self.upper_left.isChecked():
			plt.legend(loc='upper left')
		elif self.lower_right.isChecked():
			plt.legend(loc='lower right')
		elif self.lower_left.isChecked():
			plt.legend(loc='lower left')
		else:
			plt.legend(loc='upper left')
		plt.show()

	def clicked_back(self):
		self.hide()
		self.window = DataFrame_Viewer.Show_Datas()
		Main_Page.Main_Page.style(self)	

# ---------------------------------- Show Classic Plot ----------------------------------------- #

		# self.type_plot = Plot_Page.Plot.stock_plot(self)
		
		# plt.close('all')

		# fig, axes = plt.subplots(nrows=2, ncols=2)
		# self.current_df.plot(x=self.current_df[self.X_1_], kind=self.type_plot, figsize=(self.X_size_, self.Y_size_), ax=axes[0,0])
		# self.current_df.plot(x=self.current_df[self.X_2_], kind=self.type_plot, figsize=(self.X_size_, self.Y_size_), ax=axes[0,1])
		# self.current_df.plot(x=self.current_df[self.X_3_], kind=self.type_plot, figsize=(self.X_size_, self.Y_size_), ax=axes[1,0])
		# self.current_df.plot(x=self.current_df[self.X_3_], kind=self.type_plot, figsize=(self.X_size_, self.Y_size_), ax=axes[1,1])

		# # plt.ylabel(self.name_label_Y_, color=self.color_X_label_)
		# # plt.xlabel(self.name_label_X_, color=self.color_Y_label_)
		# plt.title(self.title_, color=self.title_color_)

		# # if self.upper_right.isChecked():
		# # 	plt.legend(loc='upper right')
		# # elif self.upper_left.isChecked():
		# # 	plt.legend(loc='upper left')
		# # elif self.lower_right.isChecked():
		# # 	plt.legend(loc='lower right')
		# # elif self.lower_left.isChecked():
		# # 	plt.legend(loc='lower left')
		# # else:
		# # 	plt.legend(loc='upper left')
		# plt.show()