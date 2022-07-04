import cv2 as cv
import numpy as np
from weapon_detection import weapon_find
from tkinter import filedialog
from tkinter import *
from predict_activity import predict
import glob
from PIL import Image,ImageTk
import os
import sys
from threading import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import warnings
warnings.filterwarnings('ignore')
full_body = cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_fullbody.xml')

face_cascade = cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_frontalface_default.xml')

# creating window
win = Tk()
win.title("HB-Detector")
win.resizable(False,False)

win.configure(bg="gray")
win.geometry("700x625")

#default image for camera
default_img = Image.open("images/model.png")
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


label =Label(top_frame,image=img_default)
label.pack()



status_l = Label(bottom_frame,text="Status of video")
status_l.pack(side=BOTTOM)
status_l.configure(width=700)

def browse_file():
    global filename_path
    global cap
    filename_path = filedialog.askopenfilename()
    cap = cv.VideoCapture(filename_path)
    
cap = cv.VideoCapture(0)  

def stop():
    sys.exit()

def show_frames():
    frame_number = 0
    while True:
        # reading frame
        ret,frame = cap.read()
        indexes,boxes = weapon_find(frame)
        print(indexes,boxes)

        cam_img = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        draw_bd = cv.resize(cam_img,(227,227))
        bodies = full_body.detectMultiScale(cam_img, 1.2, 3) 

        face = face_cascade.detectMultiScale(cam_img,1.2,3)
        if type(bodies) == type(np.array([0])) :
            for (x,y,w,h) in bodies:
                image_text_s = cv.rectangle(cam_img, (x, y), (x + w, y + h), (36,255,12), 2)
                cv.putText(image_text_s, "Focus", (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

        if type(face) == type(np.array([0])) :
            for (x,y,w,h) in face:
                cv.rectangle(cam_img,(x,y),(x+w,y+h),(0,255,255),2)
        
        predicted_image = predict(frame)
    
        print(predicted_image)
        font = cv.FONT_HERSHEY_PLAIN
        if indexes == 0:
            status_l.configure(text="Weapon detected-Abnormal",width=700)
            
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    data = "weapon"
                    color = (0,244,0)
                    cv.rectangle(cam_img, (x, y), (x + w, y + h), color, 2)
                    cv.putText(cam_img, data, (x, y + 30), font, 3, color, 3)

        else:
            status_l.configure(text=str(predicted_image)+"-normal",width=700)
            status = "normal"
            print("Normal",end="\r")
        
        img = Image.fromarray(cam_img)
        
        img = img.resize((700,500))

        imgtk = ImageTk.PhotoImage(image = img)
        label.imgtk = imgtk
        label.configure(image=imgtk)


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