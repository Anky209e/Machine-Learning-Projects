#importing the Libraries
from gtts import gTTS          
import PIL              
import gtts                   
import pytesseract           
from tkinter import filedialog 
from tkinter import *
from PIL import Image,ImageTk  
import pyperclip
import speech_recognition as sr
import moviepy.editor as mp
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
print("All Libraries Imported")
#defining the Window
r = sr.Recognizer()
window = Tk()
window.geometry('1280x800')
window.resizable(0, 0)
window.title("Text Recognition System for Visually Impaired")
image=Image.open("space-background-6.jpg")
photo=ImageTk.PhotoImage(image)
lab=Label(image=photo,bg='#8fb5c2') 
lab.pack()

#Defining the Labels
message = Label(window, text="Text Recognition System for Visually Impaired" ,bg="#000000"  ,fg="white"  ,width=55  ,height=1,font=('Helvetica', 25, 'italic bold '))
message.place(x=60, y=10)
message = Label(window, text="" ,bg="white"  ,fg="black"  , justify=LEFT, width=60  ,height=23, wraplength=960,activebackground = "yellow" ,font=('times', 20 , ' bold ')) 
message.place(x=70, y=80)
lbl2 = Label(window, text="Enter the text :",width=13  ,fg="white"  ,bg="#00008B"    ,height=1 ,font=('Helvetica', 12 , ' bold '))  # #000000
lbl2.place(x=80, y=720)
txt2 = Entry(window,width=40  ,bg="white" ,fg="black",font=('Helvetica', 20 , ' bold '))
txt2.place(x=230, y=720)


def Picture_to_Text():
    window.filename =  filedialog.askopenfilename()
    img= PIL.Image.open(window.filename)      
    result= pytesseract.image_to_string(img) 
    res = "***Successfully Converted to Text***\n" + result
    pyperclip.copy(res)
    message.configure(text= res)
    if(result==""):
        res = "Oops, No Text Recognized"
        message.configure(text= res)

def Picture_to_Speech():
    window.filename =  filedialog.askopenfilename()
    img= PIL.Image.open(window.filename)     
    result= pytesseract.image_to_string(img)  
    if(result==""):
        res = "Oops, No Text Recognized"
        message.configure(text= res)   
    res= gTTS(result)                #Internet required
    window.filename =  filedialog.asksaveasfilename()
    res.save(window.filename+ '.mp3') 
    res = "Audio Saved Successfully"
    message.configure(text= res)  

def Text_to_Speech(): 
    textInp= (txt2.get())
    res= gTTS(textInp)
    window.filename =  filedialog.asksaveasfilename()
    res.save(window.filename+ '.mp3')
    res = "Audio Saved Successfully"
    message.configure(text= res)

def Speech_to_Text():
    # try:
    #     with sr.Microphone() as source:
    #         message.configure(text="Listening.....")
    #         r.adjust_for_ambient_noise(source, duration=0.2)
    #         audio = r.listen(source)
    #         Text = r.recognize_google(audio)
    #         res = "You said: "+Text
    #         message.configure(text=res)
    #         # with open("audio.wav", "wb") as f:
    #         #     f.write(audio.get_wav_data())
    # except sr.RequestError as e:
    #     print("Could not request results; {0}".format(e))
         
    # except sr.UnknownValueError:
    #     print("unknown error occured")
    freq = 44100
  
    duration = 5
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
    sd.wait()
    wv.write("recording.wav", recording, freq, sampwidth=2)
    with sr.AudioFile("recording.wav") as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        message.configure(text = text)
        
def Video_to_Text():
    window.filename =  filedialog.askopenfilename()
    my_clip = mp.VideoFileClip(window.filename)
    my_clip.audio.write_audiofile(r"output.wav")
    with sr.AudioFile("output.wav") as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        #wrapper = textwrap.TextWrapper(width=50)
        #Text = wrapper.wrap(text=text)
        message.configure(text = text) 
    
    
#Defining the buttons
pictext = Button(window, text="Picture_to_Text", command=Picture_to_Text  ,fg="red"  ,bg="white"  ,width=20  ,height=3, activebackground = "yellow" ,font=('Helvetica', 10 , ' bold '))
pictext.place(x=1100, y=170)

picspeech = Button(window, text="Picture_to_Speech", command=Picture_to_Speech  ,fg="red"  ,bg="white"  ,width=20  ,height=3, activebackground = "yellow" ,font=('Helvetica', 10 , ' bold '))
picspeech.place(x=1100, y=230)

textspeech = Button(window, text="Text_to_Speech", command=Text_to_Speech  ,fg="red"  ,bg="white"  ,width=20  ,height=3, activebackground = "yellow" ,font=('Helvetica', 10 , ' bold '))
textspeech.place(x=1100, y=290)

audiospeech = Button(window, text='Speech to Text', command=Speech_to_Text, fg="red"  ,bg="white"  ,width=20  ,height=3, activebackground = "yellow" ,font=('Helvetica', 10 , ' bold '))
audiospeech.place(x=1100, y=350)

videotext = Button(window, text='Video Transcript', command=Video_to_Text, fg="red"  ,bg="white"  ,width=20  ,height=3, activebackground = "yellow" ,font=('Helvetica', 10 , ' bold '))
videotext.place(x=1100, y=410)

quitWindow = Button(window, text="QUIT", command=window.destroy  ,fg="red"  ,bg="white"  ,width=17  ,height=2, activebackground = "yellow" ,font=('Helvetica', 10 , ' bold '))
quitWindow.place(x=1100, y=600)

window.mainloop()
