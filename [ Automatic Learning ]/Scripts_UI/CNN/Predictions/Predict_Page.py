class Predict(QMainWindow):
 
	def __init__(self):
		super(Predict, self).__init__()
		loadUi('UI/Predict_Page.ui', self) # Load UI File

		self.graph_acc.clicked.connect(self.plot_acc)
		self.graph_loss.clicked.connect(self.plot_loss)

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
						temp_img = mpimg.imread(path + '/' + folders[0][i] + '/' + f)
						resize_img = cv2.resize(temp_img, dsize=(self.img_x_resize, self.img_y_resize), interpolation=cv2.INTER_CUBIC)
						imgs.append(resize_img)
				i += 1
		self.hide()
		self.window = Settings_CNN.Set_Settings_CNN()

		Main_Page.Main_Page.style(self)

		return imgs