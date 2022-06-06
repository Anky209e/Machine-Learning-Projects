import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from collections import OrderedDict
import tkinter.ttk as ttk
from tkinter import *
from sklearn.neighbors import KNeighborsClassifier
from tkinter.filedialog import askopenfilename
from sklearn.model_selection import train_test_split
from sklearn import linear_model

def Submit():
    print("Submit")

   

def StartTest():
    filename = input_filename.get()
    X_test = pd.read_csv(filename)

    Cost1 = X_test['CostCultivation'].values
    Cost2 = X_test['CostCultivation2'].values
    Product = X_test['Production'].values
    Yield = X_test['Yield'].values
    RainF = X_test['RainFall Annual'].values
    Cost_Len = len(Cost1)
    Pre_Prc = []
    VGAP = 80
    for i in range(0,Cost_Len):
        X1 = Cost1[i]
        X2 = Cost2[i]
        X3 = Product[i]
        X4 = Yield[i]
        X5 = RainF[i]
        Pce = ((M1*X1)+(M2*X2)+(M3*X3)+(M4*X4)+(M5*X5)+M)
        Pre_Prc.append(Pce)

    #print(Pre_Prc)
    
    for i in range(0,Cost_Len):
        Ar = X_test.loc[i, 'State']
        Cp = X_test.loc[i, 'Crop']
        ProD = X_test.loc[i, 'Production']
        Yi = X_test.loc[i, 'Yield']
        
        Pr = Pre_Prc[i]
        SLNO = str(i+1)
        VGAP += 50
        
        Temp_Arr = []
        State_Condition = ''
        DF = pd.read_csv("Subsidy.csv")
        Data_Size = DF['State'].values
        Data_Len = len(Data_Size)
        for A in range(0, Data_Len):
            State_Name = DF.loc[A, 'State']
            State_Crop = DF.loc[A, 'Crop']
            State_Price = float(DF.loc[A, 'Price'])
            if Cp == State_Crop:
                Bal = State_Price - Pr
                if Bal >= 0:
                    Temp_Arr.append(State_Price)

        for A in range(0, Data_Len):
            State_Name = DF.loc[A, 'State']
            State_Crop = DF.loc[A, 'Crop']
            State_Price = float(DF.loc[A, 'Price'])
            if len(Temp_Arr)!=0:
                Min_Value = min(Temp_Arr)
                if Cp == State_Crop:
                    if Min_Value == State_Price:
                        print("State "+str(State_Name)+" Price "+str(State_Price))            
                        State_Price = float("{0:.2f}".format(State_Price))
                        State_Condition = State_Name +"\t ( Price "+str(State_Price)+" )"
        Pce_Float = float(Pr)              
        Pce_Float = float("{0:.2f}".format(Pce_Float))
        Pr = str(Pce_Float)

        
        
        widget = Label(Main2, text=SLNO, fg='black', bg='white',anchor = NW,padx=7)
        Main2.create_window(350, VGAP, window=widget)
        
        widget = Label(Main2, text=Ar, fg='black', bg='white',anchor = NW,padx=7)
        Main2.create_window(450, VGAP, window=widget)

        widget = Label(Main2, text=Cp, fg='black', bg='white',anchor = NW,padx=7)
        Main2.create_window(550, VGAP, window=widget)

        widget = Label(Main2, text=Pr, fg='black', bg='white',anchor = NW,padx=7)
        Main2.create_window(750, VGAP, window=widget)

        widget = Label(Main2, text=State_Condition, fg='black', bg='white',anchor = NW,padx=7)
        Main2.create_window(950, VGAP, window=widget)

        
        
    Main2.configure(scrollregion=Main2.bbox("all"))
        
    
   
  

def SelectInput():
    filename = askopenfilename()
    input_filename_entry.set(filename)

win = Tk()
knn = KNeighborsClassifier()
myvar = StringVar()
win.state("normal")
win.title("Subsidy Rate Prediction For Agricultural Crop")
width_px = win.winfo_screenwidth()
height_px = win.winfo_screenheight()

input_filename_entry = StringVar()

df = pd.read_csv("Subsidy.csv")
reg = linear_model.LinearRegression()



reg.fit(df[['CostCultivation','CostCultivation2','Production','Yield','RainFall Annual']],df.Price)
Coff = reg.coef_

Inter = reg.intercept_
M1 = Coff[0]
M2 = Coff[1]
M3 = Coff[2]
M4 = Coff[3]
M5 = Coff[4]
M = Inter
label = Label(win, text = "Subsidy Rate Prediction For Agricultural Crop",fg='white', bg='grey',pady=24)
label.config(font=("Serif bold", 28))
label.pack(side='top', fill='x')

FrameBIG = Frame(win) #Creating Framework
Main = Canvas(FrameBIG,background="#f2f2f2", height = 200,width = width_px)
#Inside Canvas Frame
widget = Label(Main, text="Select Input File : ", fg='black', bg='#f2f2f2',anchor = NW,padx=7)
widget.config(font=("Serif bold", 15))
Main.create_window(200, 60, window=widget)

input_filename = Entry(Main, width=60,bd =5, bg='white', fg='black', textvariable=input_filename_entry)
input_filename.config(font=("Serif", 12))
Main.create_window(600, 60, window=input_filename)

widget = Button(Main, text="Choose Input CSV",bg='gray',fg='white',width=20, command=SelectInput)
widget.config(font=("Serif bold", 9))
Main.create_window(1050, 60, window=widget)

widget = Button(Main, text="Start Test",width=20,bg='green',fg='white', command=StartTest)
widget.config(font=("Serif bold", 15))
Main.create_window(600, 150, window=widget)

Main.pack(side = TOP, anchor = NW,fill="x")

Main2 = Canvas(FrameBIG,background="white", height = 300,width = width_px)
Main2.configure(scrollregion=Main.bbox("all"))

scroll = Scrollbar(FrameBIG ,orient="vertical", command=Main2.yview)
scrollX = Scrollbar(FrameBIG ,orient="horizontal", command=Main2.xview)
Main2.configure(yscrollcommand=scroll.set)
Main2.configure(xscrollcommand=scrollX.set)

widget = Label(Main2, text="SL.No", fg='black', bg='white',anchor = NW,padx=7)
widget.config(font=("Serif bold", 10))
Main2.create_window(350, 80, window=widget)

widget = Label(Main2, text="Area", fg='black', bg='white',anchor = NW,padx=7)
widget.config(font=("Serif bold", 10))
Main2.create_window(450, 80, window=widget)


widget = Label(Main2, text="Crop", fg='black', bg='white',anchor = NW,padx=7)
widget.config(font=("Serif bold", 10))
Main2.create_window(550, 80, window=widget)


widget = Label(Main2, text="Price", fg='black', bg='white',anchor = NW,padx=7)
widget.config(font=("Serif bold", 10))
Main2.create_window(750, 80, window=widget)

widget = Label(Main2, text="Recommended State", fg='black', bg='white',anchor = NW,padx=7)
widget.config(font=("Serif bold", 10))
Main2.create_window(950, 80, window=widget)

scroll.pack(side="right", fill="y")
scrollX.pack(side="bottom", fill="x")
Main2.pack(side = BOTTOM, anchor = NW,fill="x")


FrameBIG.pack(anchor = W, fill = "x")


win.mainloop()