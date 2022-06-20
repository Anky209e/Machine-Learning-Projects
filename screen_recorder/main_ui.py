# importing libraries
from tkinter import *
from PIL import Image, ImageTk, ImageGrab
import cv2
import numpy as np
import threading
import os
import datetime
import logging
import boto3
from botocore.exceptions import ClientError
import os
import pyperclip

print("Loading Credentials for AWS S3..")
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
if aws_secret_access_key is None or aws_access_key_id is None:
    print("Credentials not found!")
else:
    print("Credentials Loaded!")

# getting date and time
x = datetime.datetime.now()
dt = x.strftime("%c").replace(" ","_")
dt = dt.replace(":","_")+".avi"


p = ImageGrab.grab()
a, b = p.size
filename= dt

fourcc = cv2.VideoWriter_fourcc(*"XVID")
frame_rate = 10
out = cv2.VideoWriter() 

def screen_capturing():
    global capturing
    capturing = True
    while capturing:
        img = ImageGrab.grab()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)

# function for starting recording
def start_screen_capturing():

    if not out.isOpened():

        out.open(filename,fourcc, frame_rate,(a,b))
    print(' Recording started')
    label_top.config(text="Recording...")
    t1=threading.Thread(target=screen_capturing, daemon=True)
    t1.start()

# finction fot stopping and saving
def stop_screen_capturing(): 
    global capturing
    capturing = False
    
    label_top.config(text="Saved as - "+str(filename))
    print('Completed and saved as:',filename)
    label_mid.config(text="File is ready to be uploaded to cloud")
    out.release()

# function for pausing the recording
def pause_screen_capturing():
    global capturing
    capturing = False
    label_top.config(text="Paused")
    print("Paused")

# function for resuming recording
def resume_screen_capturing():
    global capturing
    capturing = True
    if not out.isOpened():
        out.open(filename,fourcc, frame_rate,(a,b))
    t1=threading.Thread(target=screen_capturing, daemon=True)
    t1.start()
    label_top.config(text="[Resumed]Recording..")
    print("Resumed")

# function for uploading a file to AWS S3 
def upload_file(file_name:str, bucket:str, object_name=None):

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)


    # Upload the file
    s3_client = boto3.client('s3',aws_access_key_id,aws_secret_access_key)

    try:
        print("Uploading")
        label_top.config(text="Uploading...")
        
        response = s3_client.upload_file(file_name, bucket, object_name,ExtraArgs={'ACL':'public-read'})
        print("Uploaded")
        link = "https://bucketweights.s3.ap-south-1.amazonaws.com/"+filename
        pyperclip.copy(link)
        print(link)
        label_top.config(text="[Uploaded]Link is copied to clipboard")
        label_mid.config(text="File is uploaded.")
    except ClientError as e:
        label_top.config(text="[Failed]"+str(e))
        logging.error(e)
        return False
    return True

#------------Dracula Colors-------------------#
black = "#282a36"
gray = "#44475a"
white = "#f8f8f2"
red = "#ff5555"
yellow = "#f1fa8c"
pink = "#ff79c6"
purple = "#bd93f9"
green = "#50fa7b"
orange = "#ffb86c"
cyan = "#8be9fd"
blue = "#6272a4"
#-----------------Fonts---------------------#
font_hel = ('Helvetica', 10 , ' bold ')
font_time = ('monospace', 10 , ' bold')

#---------Main GUI Code-----------------------#
root = Tk()
root.title("Screen Recorder")
root.geometry("600x400")
root.resizable(False,False)
root.config(bg=black)

# top status bar
label_top = Label(root,text="Press [Start Recording] to begin!",bg=gray,fg=yellow,font=font_time,height=2)
label_top.pack(fill=X)


label_mid = Label(root,text="Record and Upload to cloud",bg=black,fg=blue,font=('monospace', 15 , ' bold'),height=2)

label_mid.pack(fill=X)


# start recording button
start_cap = Button(root, text='Start Recording',width=25,height=3,bg=red,fg=white ,command=start_screen_capturing,font=font_hel,activebackground=yellow)
start_cap.pack()
start_cap.place(x=100,y=175)

# pause recording button
pause_cap  = Button(root,text="Pause",width=25,height=3,command=pause_screen_capturing,bg=cyan,fg=black,activebackground=yellow,font=font_hel)
pause_cap.pack()
pause_cap.place(x=0,y=250)

# resume recording button
resume_cap  = Button(root,text="Resume",width=25,height=3,command=resume_screen_capturing,bg=green,fg=black,activebackground=yellow,font=font_hel)
resume_cap.pack()
resume_cap.place(x=200,y=250)

# stop recording button
stop_cap = Button(root, text='Stop Recording',width=25,height=3, command=stop_screen_capturing,bg=orange,fg=black,activebackground=yellow,font=font_hel)
stop_cap.pack()
stop_cap.place(x=300,y=175)

# upload to cloud button
upload_cap = Button(root,text="Upload To Cloud",width=25,height=3, command=lambda: upload_file(filename,"bucketweights"),bg=blue,fg=black,activebackground=yellow,font=font_hel)
upload_cap.pack()
upload_cap.place(x=400,y=250)

# main window loop
root.mainloop()