from turtle import width
import cv2 as cv
import numpy as np
import keras
from tkinter import filedialog
from tkinter import *
from keras.models import load_model
from keras.layers import Conv3D,ConvLSTM2D,Conv3DTranspose
from keras.models import Sequential
import glob
from PIL import Image,ImageTk
import os
import sys
from threading import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import warnings
warnings.filterwarnings('ignore')
full_body = cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_fullbody.xml')
weapons = cv.CascadeClassifier("tools/cascade.xml")
face_cascade = cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_frontalface_default.xml')

# creating window
win = Tk()
win.resizable(False,False)

print("Loading Model..")
model = load_model("model.h5")
print("||Model Loaded||")

win.configure(bg="gray")
win.geometry("700x625")

#default image for camera
default_img = Image.open("images/main_cam.jpg")
default_img  = default_img.resize((700,500))
img_default = ImageTk.PhotoImage(default_img)

# creating window frames
top_frame = Frame(win)
top_frame.pack()

bottom_frame = Frame(win)
bottom_frame.pack(side=BOTTOM,fill=Y)
bottom_frame.configure(bg="gray")

def threshold(val):
    val = float(val)
    th = val/10000
    return th
# scale
scale = Scale(top_frame,from_=0,to=100,orient=HORIZONTAL,command=threshold)
scale.pack(side=BOTTOM,fill=Y)
scale.configure(length=625)
scale.set(10)

label =Label(top_frame,image=img_default)
label.pack()

threshol_l = Label(top_frame,text="Threshold value")
threshol_l.pack(side=TOP,fill=Y)

status_l = Label(bottom_frame,text="Status of video")
status_l.pack(side=BOTTOM)
status_l.configure(width=700)

def browse_file():
    global filename_path
    global cap
    filename_path = filedialog.askopenfilename()
    cap = cv.VideoCapture(filename_path)
    
cap = cv.VideoCapture(0)  

# mean squared error #
def mean_squared(x1, x2):
    difference = x1 - x2
    a,b,c,d,e = difference.shape
    n_samples = a*b*c*d*e
    sq_diff = difference ** 2
    Sum = sq_diff.sum()
    dist = np.sqrt(Sum)
    mean_dist = dist / n_samples
    return mean_dist

def stop():
    sys.exit()

# nomralize images
def normalize(img):
    img = (img-img.mean())/(img.std())
    return img

# frame shaping
def frame_shaper(np_img):
    frames = np_img.shape[2]
    np_img = np_img[:,:,:frames]
    np_img = np_img.reshape(227,227,1,1)
    return np_img

def gray_scale(frame):
    gray=0.2989*frame[:,:,0]+0.5870*frame[:,:,1]+0.1140*frame[:,:,2]
    return gray

'''
Function for opening camera and processing image.
To size 227X227X1X10
Process it through model which will give us a frame and then calculate MSE between real frame and Predicted frame.
'''
def show_frames():
    frame_number = 0
    imagedump=[]
    # Loop to get first 10 frames to determine rest video for abnormal or normal behavior
    for i in range(10):
        # reading frame
        ret,frame = cap.read()

        cam_img = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        draw_bd = cv.resize(cam_img,(227,227))
        bodies = full_body.detectMultiScale(cam_img, 1.2, 3) 
        guns = weapons.detectMultiScale(cam_img, 1.2, 3) 
        face = face_cascade.detectMultiScale(cam_img,1.2,3)
        if type(bodies) == type(np.array([0])) :
            for (x,y,w,h) in bodies:
                image_text_s = cv.rectangle(cam_img, (x, y), (x + w, y + h), (36,255,12), 1)
                cv.putText(image_text_s, "Focus", (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 1)

        if type(face) == type(np.array([0])) :
            for (x,y,w,h) in face:
                cv.rectangle(cam_img,(x,y),(x+w,y+h),(0,255,255),2)
        img = Image.fromarray(cam_img)
        img = img.resize((700,500))

        #resizing image
        resized_image = cv.resize(cam_img,(227,227),interpolation=cv.INTER_LINEAR_EXACT)
        gray = gray_scale(resized_image)
        normed_img = normalize(gray)
        imagedump.append(normed_img)

        imgtk = ImageTk.PhotoImage(image = img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
    
    imagedump = np.array(imagedump)
    imagedump.resize(227,227,10)
    imagedump=np.expand_dims(imagedump,axis=0)
    imagedump = np.expand_dims(imagedump,axis=4)

    predicted_image = model.predict(imagedump)
    loss = mean_squared(imagedump,predicted_image)
    print(loss)
    th = threshold(float(scale.get()))
    print_val = "Threshold_value:"+str(th)
    threshol_l.configure(text=print_val)
    if loss > th:
        status_l.configure(text="Abnormal",width=700)
        status = "abnormal"
        print("Abnormal",end="\r")
    else:
        status_l.configure(text="Normal",width=700)
        status = "normal"
        print("Normal",end="\r")
    label.after(20, show_frames)


def thread_show_frames():
    t1 = Thread(target=show_frames)
    t1.start()

#button for opening Video
b2 = Button(bottom_frame,text="Open a Video",command=browse_file,bg="skyblue1",fg="black")
b2.pack(side=LEFT)
b2.configure(width=35,height=40)
b3 = Button(bottom_frame,text="Force Stop",command=stop,bg="red",fg="snow")
b3.pack(side=LEFT)
b3.configure(width=20,height=40)
# Button for opening Camera
b1 = Button(bottom_frame,text="Camera/Start",command=thread_show_frames,bg="green",fg="snow")
b1.pack(side=RIGHT)
b1.configure(width=35,height=40)
    
win.mainloop()