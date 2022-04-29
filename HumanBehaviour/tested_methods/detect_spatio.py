
import cv2 as cv
import numpy as np
from PIL import Image
import os
from keras.layers import Conv3D,ConvLSTM2D,Conv3DTranspose
from keras.models import Sequential
import torch
from keras.models import load_model
def Spatio():

    """
    Sequential Model for the Spatio Temporal Autoencoder (STModel)
    :return:
    """

    STModel = Sequential()

    STModel.add(Conv3D(filters=128, kernel_size=(11, 11, 1), strides=(4, 4, 1), padding='valid', input_shape=(227, 227, 10, 1), activation='relu'))
    STModel.add(Conv3D(filters=64, kernel_size=(5, 5, 1), strides=(2, 2, 1), padding='valid', activation='relu'))

    STModel.add(ConvLSTM2D(filters=64, kernel_size=(3, 3), strides=1, padding='same', dropout=0.4, recurrent_dropout=0.3, return_sequences=True))
    STModel.add(ConvLSTM2D(filters=32, kernel_size=(3, 3), strides=1, padding='same', dropout=0.3, return_sequences=True))
    STModel.add(ConvLSTM2D(filters=64, kernel_size=(3, 3), strides=1, return_sequences=True, padding='same', dropout=0.5))

    STModel.add(Conv3DTranspose(filters=128,kernel_size=(5,5,1),strides=(2,2,1),padding='valid',activation='relu'))
    STModel.add(Conv3DTranspose(filters=1,kernel_size=(11,11,1),strides=(4,4,1),padding='valid',activation='relu'))


    STModel.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return STModel



def predict_pothole(path_to_image):

    # img = Image.fromarray(path_to_image)
    a = np.array(path_to_image,dtype=np.float32)
    a = a.reshape(-1,227,227,10)
    a=np.expand_dims(a,axis=4)
    n_bunch = np.expand_dims(a,expand_dims=0)

    print(n_bunch.shape)
    img_tensor = torch.from_numpy(a)
    # print(img_tensor.shape)
    # img = img.convert("L")
    img_cls = ["Normal", "Abnormal"]


    # if img.size != (64,64):
    # img = img.resize((64,64))
    # img = img.convert("RGB")
    

    
    # img_tensor = torch.reshape(img_tensor, (1,32*1024))

    
    model = load_model("model.h5")
    model_pred = model.predict(n_bunch)
    # model_pred.load_state_dict(torch.load("brhaviour8168.pth",map_location=torch.device("cpu")))
    print(model_pred.shape)
    # pred = model_pred(img_tensor).detach()
    # # print(pred)
    # pred = torch.nn.functional.softmax(pred,dim=1)
    # pred = np.array(pred[0])
    # pred = list(pred)
    # print(pred)

    # result_f = pred.index(max(pred))
    # print(result_f)
    
    # result = img_cls[result_f]
    
    # os.remove(path_to_image)
    
    # return result


