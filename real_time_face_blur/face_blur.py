import cv2 as cv
import numpy as np

from tkinter import filedialog
from tkinter import *

from PIL import Image,ImageTk
import os
import sys

from threading import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import warnings
warnings.filterwarnings('ignore')

face_cascade = cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_frontalface_default.xml')

tuple_t = ()
# creating window
win = Tk()
win.title("Real_time face blur")
win.resizable(False,False)

win.configure(bg="gray")
win.geometry("700x625")

#default image for camera
default_img = Image.open("images/main.jpg")
default_img  = default_img.resize((700,500))
img_default = ImageTk.PhotoImage(default_img)

# creating window frames
top_frame = Frame(win)
top_frame.pack()

bottom_frame = Frame(win)
bottom_frame.pack(side=BOTTOM,fill=Y)
bottom_frame.configure(bg="gray")

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
    ret = True
    while ret:
        ret,frame = cap.read()
        cam_img = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        face = face_cascade.detectMultiScale(cam_img,1.2,3)
        if type(face) == type(np.array([0])) :
            for (x,y,w,h) in face:
                img = cv.rectangle(cam_img,(x,y),(x+w,y+h),(0,0,255),2)
                img[y:y+h,x:x+w]=cv.medianBlur(img[y:y+h,x:x+w],35)
            status_l.configure(text="Face-detected",width=700)
        
        cv.imshow('faceblur',cam_img)
        key=cv.waitKey(1)

        if key==ord('q'):
            break

        # img = Image.fromarray(cam_img)
        
        # img = img.resize((700,500))

        # imgtk = ImageTk.PhotoImage(image = img)
        # # label.imgtk = imgtk

        # label.configure(image=imgtk)


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