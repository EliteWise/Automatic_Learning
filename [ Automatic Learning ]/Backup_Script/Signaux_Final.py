import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import sklearn
import sys
import tensorflow as tf
from tensorflow import keras
import time
import matplotlib.cm as cm
import matplotlib.image as mpimg
from sklearn.model_selection import train_test_split

from PIL import Image

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.models import load_model
import datetime
import progressbar
from time import sleep
import threading
from IPython.display import clear_output

# Import others files.py
import Graphics, Settings_CNN

def resize_images(num_folder, num_frame, i, input_folders, type_folder):
    
    global X_train_full, train_labels, test_labels, X_test, X_train, y_test, y_train
    
    X_train_full = []
    train_labels = []
    test_labels = []

    X_test = []
    X_train = []

    y_test = []
    y_train = []
    
    pan = pd.read_csv('Desktop/Signaux/'+str(type_folder)+'/000'+format(num_folder,"02d")+'/GT-000'+format(num_frame,"02d")+'.csv', sep=';')
    for x in range(len(pan)):
        img = Image.open('Desktop/Signaux/'+str(type_folder)+'/000'+format(num_frame,"02d")+'/'+str(pan['Filename'].iloc[i]))
        new_img = img.resize((56,56))
        new_img.save('Desktop/Signaux/'+str(type_folder)+'/000'+format(num_frame,"02d")+'/'+str(pan['Filename'].iloc[i]), "PPM", optimize=True)
        i += 1
        if i == len(pan):
            num_frame += 1
            num_folder += 1
            i = 0
            x = 0
            if num_frame == input_folders:
                print('-=-=- Resizing Done -=-=-')
            else:
                if len(os.listdir('Desktop/Signaux/Test/000'+format(num_folder,"02d"))) == 1 and (type_folder == 'Test'):
                    num_frame += 1
                    num_folder += 1
                    resize_images(num_folder, num_frame, i, input_folders, type_folder)
                else:
                    resize_images(num_folder, num_frame, i, input_folders, type_folder)

def append_images(num_folder, num_frame, i, input_folders, type_folder, X_type, labels):
    pan = pd.read_csv('Desktop/Signaux/'+str(type_folder)+'/000'+format(num_folder,"02d")+'/GT-000'+format(num_frame,"02d")+'.csv', sep=';')
    for x in range(len(pan)):
        X_type.append(mpimg.imread('Desktop/Signaux/'+str(type_folder)+'/000'+format(num_frame,"02d")+'/'+str(pan['Filename'].iloc[i])))
        labels.append(pan['ClassId'].iloc[i]) # Get Labels
        i += 1
        if i == len(pan):
            num_frame += 1
            num_folder += 1
            i = 0
            x = 0
            if num_frame == input_folders and X_type == X_train_full:
                append_images.X_train_final = np.asarray(X_type) # List to Array
                append_images.labels_X_train_full = np.asarray(labels) # Define X_train labels + to array
                print('Len:', len(append_images.X_train_final), '| Type:', type(append_images.X_train_final), '| X_train_full Shape:', np.shape(append_images.X_train_final), '| Labels Shape:', np.shape(append_images.labels_X_train_full))
                
            elif num_frame == input_folders and X_type == X_test:
                append_images.X_test_final = np.asarray(X_type) # List to Array
                append_images.labels_X_test = np.asarray(labels) # Define X_test labels + to array
                print('Len:', len(append_images.X_test_final), '| Type:', type(append_images.X_test_final), '| X_test Shape:', np.shape(append_images.X_test_final), '| Labels Shape:', np.shape(append_images.labels_X_test))
                
            else:
                if len(os.listdir('Desktop/Signaux/Test/000'+format(num_folder,"02d"))) == 1 and (type_folder == 'Test'):
                    num_frame += 1
                    num_folder += 1
                    append_images(num_folder, num_frame, i, input_folders, type_folder, X_type, labels)
                else:
                    append_images(num_folder, num_frame, i, input_folders, type_folder, X_type, labels)


def parsing_data():
    # Set global variables
    global X_test, X_train
    global y_train,y_test
    
    # Define data variables
    y_train_full = append_images.labels_X_train_full
    X_train,X_test,y_train,y_test = train_test_split(X_train_full,y_train_full,test_size=0.2)
    
    # Convert list to array
    X_train = np.asarray(X_train)
    X_test = np.asarray(X_test)
    y_train = np.asarray(y_train)
    y_test = np.asarray(y_test)



def define_model(shape_input, n_1, n_2, n_3, n_4, n_5, a_1, a_2, a_3, a_4, a_5, optimizer, metrics):
    global model

    model = Sequential()
    model.add(Conv2D(n_1, (3, 3), padding='same', input_shape=shape_input, activation=a_1))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(n_2, (3, 3), padding='same', activation=a_2))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(n_3, (2, 2), padding='same', activation=a_3))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # the model so far outputs 3D feature maps (height, width, features)

    model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
    model.add(Dense(n_4, activation=a_4))
    model.add(Dropout(0.5))
    model.add(Dense(n_5, activation=a_5))
    # COMPILE
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=optimizer,
                  metrics=[metrics])
    
    # output
    return model.summary()



def training(valid_split, b_size, epochs, verbose, filepath, name):

    global History

    callbacks = [EarlyStopping(monitor='val_acc', patience=4),
                 ModelCheckpoint(filepath=filepath + name, monitor='val_acc', save_best_only=True)]

    # TRAINING
    History = model.fit(X_train, y_train,
                        validation_split=valid_split,
                        batch_size = b_size,
                        callbacks = callbacks,
                        epochs=epochs,
                        verbose=verbose
                       )

    model.save_weights(filepath + '-weights')  # always save your weights after training or during training



def plot():
    plt.plot(History.history['acc'])
    plt.plot(History.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('Epoch')
    plt.legend(['accuracy','Val_acc'],loc = 'lower right')
    plt.show()

    plt.plot(History.history['loss'])
    plt.plot(History.history['val_loss'])
    plt.title('model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Loss','Val_Loss'])
    plt.show()



# Evaluate the Model loaded
def evaluation(filepath, name):
    model_opti = load_model(filepath + name)
    print(model_opti.evaluate(X_test, y_test))



def final_function():
    
    # Resize Train & Test images
    resize_images(0,0,0,1,'Train');
    resize_images(0,0,0,1,'Test');
    
    # Append Train & Test images
    append_images(0,0,0,1,'Train',X_train_full, train_labels);
    append_images(0,0,0,1,'Test',X_test, test_labels);
    
    # Define + Convert
    parsing_data();
    
    # Model  | (input shape)
    define_model((56, 56, 3));
    
    # Training Model | (validation split, batch size, epochs, verbose, filepath)
    training(0.1, 32, 100, 0, 'C:/Users/Dell/Desktop/Signaux - App/Best_Models/', Graphics.name);
    
    # Accuracy Plot + Loss Plot
    plot();
    
    # Load Best Model + Evaluate it
    evaluation();


# Run Pipeline
#final_function();

def function_graphics():
    # # Training Model | (validation split, batch size, epochs, verbose, filepath)
    # training(0.1, 32, 100, 0, 'C:/Users/Dell/Desktop/Signaux - App/Best_Models/', Graphics_UI.name_model.text());

    # Load Best Model + Evaluate it
    evaluation('C:/Users/Dell/Desktop/Signaux - App/Best_Models/', Graphics.name);

    # # Accuracy Plot + Loss Plot
    # plot();

def launch_model():
    define_model((Settings_CNN.img_x, Settings_CNN.img_y, Settings_CNN.img_dim), Settings_CNN.n_1, Settings_CNN.n_2, Settings_CNN.n_3, Settings_CNN.n_4, Settings_CNN.n_5, Settings_CNN.a_1, Settings_CNN.a_2, Settings_CNN.a_3, Settings_CNN.a_4, Settings_CNN.a_5, Settings_CNN.optimizer, Settings_CNN.metrics);




