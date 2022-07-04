
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import time
import pyjokes
import ctypes
import subprocess
import playsound
from gtts import gTTS
import warnings
warnings.filterwarnings("ignore")



engine = pyttsx3.init()
voices = engine.getProperty("voices")

engine.setProperty('voice', voices[0].id)

def speak(text):
    tts = gTTS(text=text,lang="en")
    filename = "temp.mp3"
    tts.save(filename)
    playsound.playsound(filename)


def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        print("Good Morning sir")
        speak("Good Morning sir")
        
    elif hour >= 12 and hour < 16:
        print("Good afternoon sir")
        speak("Good afternoon sir")
        
    else:
        print("Good Evening, sir")
        speak("Good Evening, sir")
    print("I am your virtual assistant.How may I help you?")
    speak("I am your virtual assistant  how may i help you")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..")
        r.pause_threshold = 1
        r.energy_threshold = 500
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognising..")
        query = r.recognize_google(audio, language='en-in')
        print('You said: ', query)
    except Exception as e:
        # print(e)
        return "no"
    return query


def run_jarvis():

    wishme()
    while True:
        speak("Whats the order")
        query = takecommand().lower()

        if 'wikipedia' in query:
            try:
                speak('Searching Wikipedia sir')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to wikipedia")
                print(results)
                speak(results)
            except:
                speak("Sorry I cant find that page")

        elif 'youtube' in query:
            speak("opening youtube")
            webbrowser.open("Youtube.com")
            time.sleep(5)

        elif 'the time' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is{strtime}")
            time.sleep(5)

        elif 'notepad' in query:
            try:
                print("opening notepad...")
                speak("opening notepad sir")
                np_path = r'C:\Windows\system32\notepad.exe'
                os.startfile(np_path)
            except:
                speak("I cant open notepad")
            
        elif 'paint' in query:
            try:
                print("opening Paint ...")
                speak("opening MS paint sir")
                paint_path = r'C:\Windows\system32\mspaint.exe'
                os.startfile(paint_path)
                time.sleep(5)
            except:
                speak("I cant open paint")

        elif 'snip'in query:
            try:
                print("opening SnippingTool....")
                speak("opening SnippingTool sir")
                sni_path = r'C:\Windows\system32\SnippingTool.exe'
                os.startfile(sni_path)
                time.sleep(5)
            except:
                speak("I cant open any tool for that")

        elif 'powershell' in query:
            try:
                print("opening powershell...")
                speak("opening powershell sir")
                pows_path = r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
                os.startfile(pows_path)
                time.sleep(5)
            except:
                speak("I dont think you have permission for that")

        elif 'calculator' in query:
            try:
                print("opening calculator...")
                speak("opening calculater sir")
                cal_path = r'C:\Windows\System32\calc.exe'
                os.startfile(cal_path)
                time.sleep(5)
            except:
                speak("oh no i cant open calculator you have to solve it on paper")

        elif 'task manager' in query:
            try:
                print("opening task manager....")
                speak("opening task manager sir")
                man_path = r'C:\Windows\system32\Taskmgr.exe'
                os.startfile(man_path)
                time.sleep(5)
            except:
                speak(" I Cant open it")
            
        elif 'joke' in query:
            try:
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)
            except:
                speak("I dont have any jokes at the moment")

        elif 'search' in query:
            try:
                query = query.replace("search", "")
                query = query.replace("play", "")
                webbrowser.open(query)
            except:
                speak("I cant open webbrowser")

        elif 'lock window' in query:
            try:
                speak("locking the device")
                ctypes.windll.user32.LockWorkStation()
            except:
                speak(" No I wont")

        elif 'shutdown' in query:
            try:
                speak("Hold On a Sec ! Your system is on its way to shut down")
                subprocess.call('shutdown / p /f')
            except:
                speak(" oh No I cant it will kill me")

        elif "where is" in query:
            try:
                query = query.replace("where is", "")
                location = query
                speak("you asked me to Locate")
                speak(location)
                webbrowser.open(
                    "https://www.google.nl / maps / place/" + location + "")
            except:
                speak("I dont know where that is")

        elif "restart" in query:
            try:
                subprocess.call(["shutdown", "/r"])
            except:
                speak("No I cant")

        elif "hibernate" in query or "sleep" in query:
            try:
                speak("Hibernating")
                subprocess.call("shutdown / h")
            except:
                speak("Oops looks like there is a issue")

        elif "log off" in query or "sign out" in query:
            try:
                speak("Make sure all the application are closed before sign-out")
                time.sleep(5)
                subprocess.call(["shutdown", "/l"])
            except:
                speak(" Oh no I cant do it")
        
        elif "who am i" in query:
            speak("If you talk then definately your human.")
        elif "why you came to world" in query:
            speak("It's a secret")
        elif 'is love' in query:
            speak("I am not a smart man but I know what love is")
        elif "who are you" in query:
            speak("I am your virtual assistant created.")

        elif 'reason for you' in query:
            speak("I am just a mere project")

        elif 'stop' in query:
            speak("I am going sir bye and thanks for using me see you later")
            print("Call me if you need any help")
            break

        else:
            speak("sorry i was not able to get that")

if __name__=="__main__":

    art = """
    
    ####################################
    #                                  #
    #                                  #
    #           Virtual AI             #
    #            Assistant             #
    #                                  #
    #                                  #
    #----------------------------------#
    #                                  #
    #**********************************#
    #            Python 3.10           #
    #                                  #
    ####################################
    
    """
    print(art)
    cont = """
    Enter the number:
    1) Start Assistant
    2) Exit
    """
    userinput = int(input(cont))

    if userinput == 1:
        print("Welcome to Virtual assistant!")
        run_jarvis()
    elif userinput == 2:
        import sys
        sys.exit()
    else:
        print("Please enter correct number!")
    