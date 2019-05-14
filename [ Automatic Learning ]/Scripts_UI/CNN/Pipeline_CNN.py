import os, sys, PyQt5, os.path

from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PIL import Image
import matplotlib.image as mpimg

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.callbacks import EarlyStopping, ModelCheckpoint, Callback 
from keras.models import load_model

from sklearn.model_selection import train_test_split

from Scripts_UI._MainPage_.Main import Main_Page

from Scripts_UI.CNN.Page_2.Settings_CNN import *
from Scripts_UI.CNN.Page_1.Load_Images import *

#---------------------------------------------------------

class Pipeline():
    def __init__(self):
        super(Pipeline, self).__init__()
        
        self.parsing_data()
        self.define_model()
        self.training()

#---------------------------------------------------------

    def parsing_data(self):

        self.X_test = []
        self.X_train = []
        self.y_train = []
        self.y_test = []

        imgs,labels = Import_Image().stock_img()
        
        # Define data variables
        self.X_train_full = imgs
        self.y_train_full = labels
        self.X_train,self.X_test,self.y_train,self.y_test = train_test_split(self.X_train_full,self.y_train_full,test_size=0.2)
        
        # Convert list to array
        self.X_train = np.asarray(self.X_train)
        self.X_test = np.asarray(self.X_test)
        self.y_train = np.asarray(self.y_train)
        self.y_test = np.asarray(self.y_test)

    #---------------------------------------------------------

    def define_model(self):

        self.param = Set_Settings_CNN().stock_settings()

        self.model = Sequential()
        self.model.add(Conv2D(self.param[3], (3, 3), padding=self.param[13], input_shape=(self.param[0],self.param[1],self.param[2]), activation=self.param[8]))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(self.param[4], (3, 3), padding=self.param[13], activation=self.param[9]))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(self.param[5], (3, 3), padding=self.param[13], activation=self.param[10]))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        # the model so far outputs 3D feature maps (height, width, features)

        self.model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
        self.model.add(Dense(self.param[6], activation=self.param[11]))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(self.param[7], activation=self.param[12]))
        # COMPILE
        self.model.compile(loss='sparse_categorical_crossentropy',
                      optimizer=self.param[14],
                      metrics=[self.param[15]])
    #---------------------------------------------------------

    def training(self):

        self.filepath = Set_Settings_CNN().stock_filepath()
        
        self.callbacks = [EarlyStopping(monitor='val_acc', patience=4),
                     ModelCheckpoint(filepath=self.filepath +'/'+ self.param[18], monitor='val_acc', save_best_only=True)]

        # TRAINING

        self.History = self.model.fit(self.X_train, self.y_train,
                            validation_split= self.param[19],
                            batch_size = self.param[16],
                            callbacks = self.callbacks,
                            epochs= self.param[17],
                            verbose= self.param[20]
                           )
        return self.History

    #---------------------------------------------------------

    def plot_acc(self):
        plt.plot(self.History.history['acc'])
        plt.plot(self.History.history['val_acc'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('Epoch')
        plt.legend(['accuracy','Val_acc'],loc = 'lower right')
        plt.show()

    def plot_loss(self):
        plt.plot(self.History.history['loss'])
        plt.plot(self.History.history['val_loss'])
        plt.title('model Loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Loss','Val_Loss'])
        plt.show()

    def acc_values(self):
        global acc
        acc = self.History.history['acc'][0]
        return round(acc,2)

    def loss_values(self):
        global loss
        loss = self.History.history['loss'][0]
        return round(loss,2)


    #--------------------------------------------------------