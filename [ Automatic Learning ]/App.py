import os, sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from IPython import *

from Scripts_UI._MainPage_.Main import Main_Page
from Scripts_UI._MainPage_._Auth_ import Auth_Page
from Scripts_UI.CNN.Page_2.Settings_CNN import *
from Scripts_UI.CNN.Page_2 import Settings_CNN

class main():

	def launchApp():

		app = QApplication(sys.argv)
		widget = Auth_Page.Auth() # Strt_App Class

		stream = QtCore.QFile("QSS/Style.qss") # Get Style file
		stream.open(QtCore.QIODevice.ReadOnly)
		widget.setStyleSheet(QtCore.QTextStream(stream).readAll()) # Set it
		
		sys.exit(app.exec_()) # Start App

	if __name__ == '__main__':
		try:
			os.remove(Settings_CNN.filepath_train + '/' + Settings_CNN.name_train_f + '/' + Settings_CNN.History)
		except AttributeError:
			pass

		launchApp()

#----------------------------------------------
### Changer le popup de Settings_CNN
#----------------------------------------------