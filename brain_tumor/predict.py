import tensorflow as tf
from tensorflow.keras.models import Model, load_model
import cv2
import imutils
import warnings
import os
import argparse
import sys



warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

print("Loading Model..")
best_model = load_model(filepath='cnn-parameters-improvement-23-0.91.model')
print("Model Loaded!")


def crop_brain_contour(image):

    print("Processing image..")
    # Convert the image to grayscale, and blur it slightly
    image = cv2.imread(image)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold the image, then perform a series of erosions +
    # dilations to remove any small regions of noise
    thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours in thresholded image, then grab the largest one
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    
    # Find the extreme points
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])
    
    # crop new image out of the original image using the four extreme points (left, right, top, bottom)
    new_image = image[extTop[1]:extBot[1], extLeft[0]:extRight[0]]  
    new_image = cv2.resize(new_image,(240,240))   

    return new_image

# Parsing image path
def check_tumor(IMG_PATH,THRESHOLD):

# pre-processing image 
    new_image = crop_brain_contour(IMG_PATH)
    new_image = new_image/255
    model_image = new_image.reshape(1,240,240,3)

    # predicting output
    out = best_model.predict(model_image)
    prob = out[0][0]*10

    # final conditions
    if prob >= THRESHOLD:
        print("**** Brain Tumor Detected ****")
        status = "Tumor Detected"
        print("**** Probablity:{} ****".format(round(prob*100,3)))
        
    else:
        print("**** No Tumor Detection ****")
        status = "No Tumor Detected"
        print("**** Probablity:{} ****".format(prob*100))
    return status,prob
