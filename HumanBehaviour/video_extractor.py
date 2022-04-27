import cv2 as cv

import sys
a = sys.argv
import os


if "cam" in a:
    cap = cv.VideoCapture(0)
else:
    cap = cv.VideoCapture("videos/a8.mp4")


c= len(os.listdir("data/train/normal1"))+1
print(c)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2RGB)  
    # ret,thresh1 = cv.threshold(gray,200,255,cv.THRESH_BINARY)
    # edge = cv.Canny(gray,100,100)
    # contours, hierarchy = cv.findContours(edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    # cv.drawContours(gray, contours, -1, (0, 255, 0), 3)


    font = cv.FONT_HERSHEY_SIMPLEX

    gray = cv.resize(gray,(64,64))
    cv.imwrite("data/train/normal1"+"/"+str(c)+".jpg",gray)

    # print(data)


    cv.imshow('frame', gray)
    c+=1

    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()