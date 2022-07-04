from tkinter import *
from PIL import Image, ImageGrab
canvas_width = 100
canvas_height = 150
from main import main
import threading
def paint( event ):
   python_green = "#ffffff"
   x1, y1 = ( event.x - 1 ), ( event.y - 1 )
   x2, y2 = ( event.x + 1 ), ( event.y + 1 )
   w.create_oval( x1, y1, x2, y2, fill = python_green )
# thats it you can use any image and name it word.
def run():
    word,prob = main()
    status = str(word)+"\nProbablity:"+str(prob)
    message.configure(text=status)
    return word,prob

def thread_run():
    a = threading.Thread(target=run)
    a.start()

master = Tk()
master.geometry("400x200")
master.configure(bg="gray")
def getter():
    x=master.winfo_rootx()+w.winfo_x()
    y=master.winfo_rooty()+w.winfo_y()
    x1=x+w.winfo_width()
    y1=y+w.winfo_height()
    ImageGrab.grab().crop((x,y,x1,y1)).save("data/word.png")
    print("Image_saved")

master.title( "Handwriting to real" )
w = Canvas(master, width=canvas_width, height=canvas_height,bg="snow")

w.pack(expand = YES, fill = BOTH)
w.bind( "<B1-Motion>", paint )

message = Label( master, text = "Press and Drag the mouse to draw",bg="gray",fg="snow" )
message.pack()

save_img = Button(master,text="Save Image",command=getter,height=2,width=7)
save_img.pack(side=LEFT)
# save_img.place(x=50,y=150)

run_btn = Button(master,text="Run",command=thread_run,height=2,width=7)
run_btn.pack(side=RIGHT)
# run_btn.place(x=500,y=150)




    
mainloop()