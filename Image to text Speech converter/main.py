import os
import sys
from pymongo import MongoClient
from tkinter import *
from PIL import Image,ImageTk 

#---------MongoDB cluster address here----------------#

cluster = MongoClient('#---MongoDB address-here---#')
db = cluster["SiteData"]

system_name = os.system("uname")
#-----------Finding duplicayes for registration-----#
def find_id_pass():
    collection = db["id-pass-internship"]
    label1.configure(text="Checking Database..")
    email = userid.get()
    # password = passid.get()
    dic = {"_id":email}
    mydoc = collection.find(dic)
    
    a = [i for i in mydoc]
    print(a)
    if len(a) > 0:
        return True
    else:
        return False

#--------Confirming ID and PASS for login----------#
def find_for_verification():
    collection = db["id-pass-internship"]
    label1.configure(text="Checking Database..")
    email = userid.get()
    password = passid.get()
    dic = {"_id":email,"pass":password}
    mydoc = collection.find(dic)
    
    a = [i for i in mydoc]
    print(a)
    if len(a) > 0:
        return True
    else:
        return False


# function of submit button
def submit():
    collection = db["id-pass-internship"]
    ret = find_for_verification()
    label1.configure(text="Loggin In")
    if ret:
        print("Logged In")
        label1.configure(text="Successful")
        if system_name == "Linux":

            os.system("python3 converter.py")
        else:
            os.system("python converter.py")
    else:
        label1.configure(text="Wrong username or password.")
        print("Wrong username or password!")

def register():
    collection = db["id-pass-internship"]
    email = userid.get()
    password = passid.get()
    ret = find_id_pass()
    if len(email) >=4 and len(password) >= 5 and ret != True :
        dic = {"_id":email,"pass":password}
        collection.insert_one(dic)
        print("Registered")
        label1.configure(text="Registered")
    else:
        print("Password too short or already exist")
        label1.configure(text="Password is too short or already exists.")

root = Tk()
root.title("Login-Manager")
root.geometry("700x450")
root.resizable(0,0)
root.configure(bg="gray")

#----TK variables---#
userid = StringVar()
passid = StringVar()

# -----label-----
userlabel = Label(root,text="Username:",font=('monospace', 13 , ' bold '),bg="gray",fg="snow")
userlabel.pack()
userlabel.place(x=200,y=150)
passlabel = Label(root,text="Password:",font=('monospace', 13 , ' bold '),bg="gray",fg="snow")
passlabel.pack()
passlabel.place(x=200,y=200)

#----widget----
userentry = Entry(root,textvariable=userid)
userentry.pack(padx=20)
userentry.place(x=300,y=150)
passentry = Entry(root,textvariable=passid)
passentry.pack()
passentry.place(x=300,y=200)

# ---submit----
srchbtn = Button(root,text="Log In",command=submit,bg="green",height=2,width=7,font=('monospace', 10 , ' bold '))
srchbtn.pack()
srchbtn.place(x=275,y=250)
reghbtn = Button(root,text="Register",command=register,bg="orange",height=2,width=7,font=('monospace', 10 , ' bold '))
reghbtn.pack()
reghbtn.place(x=400,y=250)

# ---label for userinfo---
global label1
label1 = Label(root,text="Enter above details",font=('monospace', 10 , ' bold '),bg="gray",fg="snow")
label1.pack()
label1.place(x=275,y=325)

root.mainloop()



