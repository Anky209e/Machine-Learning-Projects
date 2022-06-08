from tensorflow.keras import preprocessing, layers, models, callbacks 
import pandas as pd  # Data analysis & manipulation
import numpy as np  
import cv2
import warnings
warnings.filterwarnings("ignore")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
print("Loading Model...")
best_model = models.load_model("car_damage_classifier.h5")
print("Model Loaded...")

def real_time(current_frame):
    img = cv2.imread(current_frame)
    grayClone = cv2.cvtColor(np.float32(img),cv2.COLOR_BGR2GRAY)
    #print(img.shape)
    img = cv2.resize(grayClone, (300, 300))
    
    img = img/255 #rescalinng
    pred_img =img.copy()
    prob = best_model.predict(img.reshape(-1,300,300,1))
    print(prob[0])
    # prob=np.argmax(prob,axis=1)
    # print(prob)
    if (prob>0.5):
        return "All good"
    else:
        return "Damaged"

