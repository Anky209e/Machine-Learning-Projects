print("Importing Libraries..")
import speech_recognition as sr
import pyttsx3
import datetime
import playsound
import os
from tkinter import *
import threading
from gtts import gTTS
import boto3
from botocore.exceptions import ClientError
import warnings
warnings.filterwarnings("ignore")
print("Libraries Loaded!")

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[32].id)

print("Loading Credentials...")
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
if aws_secret_access_key is None or aws_access_key_id is None:
    print("Credentials not found! You can't sent mails")
else:
    print("Credentials Loaded!")

def send_mail(sender,reciever,subject,content_text,content_html):
    SENDER = sender
    RECIPIENT = reciever

    # region
    AWS_REGION = "ap-south-1"
    SUBJECT = subject
    BODY_TEXT = content_text
    BODY_HTML = content_html
    CHARSET = "UTF-8"

    client = boto3.client('ses',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name=AWS_REGION)
    try:
    #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,)

# Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

# female audio engine
def speak_f(text):
    tts = gTTS(text=text,lang="en")
    filename = "temp.mp3"
    tts.save(filename)
    playsound.playsound(filename)

# male audio engine
def speak_m(audio):
    engine.say(audio)
    engine.runAndWait()

# wishme function wishes 
def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak_f("Good Morning")
    elif hour >= 12 and hour < 16:
        speak_f("Good afternoon")
    else:
        speak_f("Good Evening")

# taking audio command and convertng it to text string
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        status_bar.config(text="Listening..")
        r.pause_threshold = 1
        r.energy_threshold = 500
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognising..")
        status_bar.config(text="Recognising..")
        query = r.recognize_google(audio, language='en-in')
        print('You said ', query)
        info_bar.config(text=query)
        status_bar.config(text="Done")
        speak_f(query)

    except Exception as e:
        speak_f("did't get it")
        status_bar.config(text="Say that again please..")
        return None
    return query

# function gets all text and send to address
def record_and_send():
    sender_add = " "
    recv_add = userid.get()
    speak_f("What should be the subject for Email")
    subject = takecommand()
    speak_f("What should be the content")
    content_html = takecommand()
    content_text = " "
    if subject != None and content_html != None and len(recv_add) > 0:
        send_mail(sender=sender_add,reciever=recv_add,subject=subject,content_text=content_text,content_html=content_html)
        speak_f("Email sent succesfully")
    else:
        speak_f("oops looks like there was a issue lets try again")
        record_and_send()

def t_takecommand():
    a = threading.Thread(target=takecommand)
    a.start()

def thread_rec_send():
    t_rs = threading.Thread(target=record_and_send())
    t_rs.start()

root = Tk()

# tkinter variables
userid = StringVar()

#------Dracula Color theme--------#
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

# root window config
root.geometry("500x400")
root.title("Email Bot")
root.resizable(False,False)
root.config(bg=black)

# staus bar
status_bar = Label(root,text="Enter Email Below",bg=gray,fg=white)
status_bar.pack(fill=X)

# entry widget
userentry = Entry(root,textvariable=userid)
userentry.pack()
userentry.place(x=100,y=70,width=300,height=30)

# send button
send_btn = Button(root,text="Record and Send",command=thread_rec_send,width=25,height=2,bg=red,fg=white,activebackground=yellow,font=font_hel)
send_btn.pack()
send_btn.place(x=145,y=150)

# inforamtion bar
info_bar = Label(root,text="Written Email should be verified on AWS SES",bg=black,fg=yellow,font=font_hel)
info_bar.place(x=100,y=210)

# main window loop
root.mainloop()