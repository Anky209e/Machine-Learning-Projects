import cv2 as cv
from detect import predict_pothole

import sys

a = sys.argv
import numpy as np



full_body = cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_fullbody.xml')   
arr = []
arr_n = np.array(arr)

if "cam" in a:
    cap = cv.VideoCapture(0)
else:
    cap = cv.VideoCapture("f1.mp4")



while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2RGB)  
    body = full_body.detectMultiScale(gray, 1.1, 4)
    ret,thresh1 = cv.threshold(gray,200,255,cv.THRESH_BINARY)
    edge = cv.Canny(gray,100,100)
    
    for (x, y, w, h) in body:
        cv.rectangle(gray, (x, y), (x+w, y+h), (0, 200, 0), 2)



    font = cv.FONT_HERSHEY_SIMPLEX

    edge = cv.resize(edge,(64,64))
    data = predict_pothole(edge)
    # print(data)
    main_text = str(data)
    cv.putText(gray, 
            main_text, 
            (50, 50), 
            font, 1, 
            (255,0,0), 
            2, 
            cv.LINE_4)
    cv.imshow('frame', gray)

    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()

