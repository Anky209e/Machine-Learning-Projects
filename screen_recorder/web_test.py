
from distutils.command.upload import upload
from PIL import Image,ImageGrab
import cv2
import numpy as np
import threading
import os
import streamlit as st
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

st.title("Web client for Screen Recorder")
st.write("***")
# getting date and time
x = datetime.datetime.now()
dt = x.strftime("%c").replace(" ","_")
dt = dt.replace(":","_")+".avi"

p = ImageGrab.grab()
a, b = p.size
filename= st.text_input("Enter Filename(.avi)",value="default_recording.avi")
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

def start_screen_capturing():

    if not out.isOpened():

        out.open(filename,fourcc, frame_rate,(1920,1080))
    print(' Recording started')
    t1=threading.Thread(target=screen_capturing, daemon=True)
    t1.start()

def stop_screen_capturing():
    global capturing
    capturing = False
    out.release()
    print('Completed and saved as:',filename)

def pause_screen_capturing():
    global capturing
    capturing = False
    print("Paused")

def resume_screen_capturing():
    global capturing
    capturing = True
    if not out.isOpened():
        out.open(filename,fourcc, frame_rate,(1920,1080))
    t1=threading.Thread(target=screen_capturing, daemon=True)
    t1.start()
    print("Resumed")

def upload_file(file_name:str, bucket:str, object_name=None):

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3',aws_access_key_id,aws_secret_access_key)

    try:
        print("Uploading")
        response = s3_client.upload_file(file_name, bucket, object_name,ExtraArgs={'ACL':'public-read'})
        print("Uploaded")
        link = "https://bucketweights.s3.ap-south-1.amazonaws.com/"+filename
        pyperclip.copy(link)
        print(link)

    except ClientError as e:

        logging.error(e)
        return False
    return True
a,b,c,d,e = st.columns(5)

record = a.button("Record")
pause = b.button("Pause")
resume = c.button("Resume")
stop = d.button("Stop")
upload_btn = e.button("Upload")


if record:
    
    start_screen_capturing()
    st.write("## Started")
if pause:
    pause_screen_capturing()
    st.write("Paused")

if resume:
    resume_screen_capturing()
    st.write("Resumed")

if stop:
    stop_screen_capturing()
    st.write("Recording saved")

if upload_btn:
    upload_file(filename,"bucketweights")

    

    

