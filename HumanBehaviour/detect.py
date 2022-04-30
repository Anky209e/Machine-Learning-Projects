from keras.callbacks import ModelCheckpoint, EarlyStopping
import numpy as np
import keras
from keras.layers import Conv3D,ConvLSTM2D,Conv3DTranspose
from keras.models import Sequential
import numpy as np
import glob
import os
import cv2 as cv
threshold=0.00052

def loadModel():


    STModel = Sequential()

    STModel.add(Conv3D(filters=128, kernel_size=(11, 11, 1), strides=(4, 4, 1), padding='valid', input_shape=(227, 227, 10, 1), activation='relu'))
    STModel.add(Conv3D(filters=64, kernel_size=(5, 5, 1), strides=(2, 2, 1), padding='valid', activation='relu'))

    STModel.add(ConvLSTM2D(filters=64, kernel_size=(3, 3), strides=1, padding='same', dropout=0.4, recurrent_dropout=0.3, return_sequences=True))
    STModel.add(ConvLSTM2D(filters=64, kernel_size=(3, 3), strides=1, return_sequences=True, padding='same', dropout=0.5))

    STModel.add(Conv3DTranspose(filters=128,kernel_size=(5,5,1),strides=(2,2,1),padding='valid',activation='relu'))
    STModel.add(Conv3DTranspose(filters=1,kernel_size=(11,11,1),strides=(4,4,1),padding='valid',activation='relu'))


    STModel.compile(optimizer='SGD', loss='mse', metrics=['loss'])

    return STModel


from keras.models import load_model
import numpy as np
def mean_squared(x1, x2):
    difference = x1 - x2
    a,b,c,d,e = difference.shape
    n_samples = a*b*c*d*e
    sq_diff = difference ** 2
    Sum = sq_diff.sum()
    dist = np.sqrt(Sum)
    mean_dist = dist / n_samples
    return mean_dist

def predict_anomly(weights_path,path_to_npy_processed_video_file):
    model=load_model(weights_path)

    X_test=np.load(path_to_npy_processed_video_file)
    frames=X_test.shape[2]

    Anomality  = False

    frames=frames-frames%10

    X_test=X_test[:,:,:frames]
    X_test=X_test.reshape(-1,227,227,10)
    X_test=np.expand_dims(X_test,axis=4)
    a_frames = []
    for number,bunch in enumerate(X_test):
        n_bunch=np.expand_dims(bunch,axis=0)
        reconstructed_bunch=model.predict(n_bunch)
        loss=mean_squared(n_bunch,reconstructed_bunch)
        print(loss)
        if loss>threshold:
            print("Anomalous frames @ {}".format(number))
            a_frames.append(number)
            Anomality = True
        else:
            continue

    if len(a_frames) > 0:
        return (Anomality,a_frames)
    else:
        a = []
        return (Anomality,a)
