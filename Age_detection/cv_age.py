import cv2 as cv
from detect import predict_age
import sys
a = sys.argv
face_cascade = cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_frontalface_default.xml')

font = cv.FONT_HERSHEY_SIMPLEX
import numpy as np
arr = [1]
arr_n = np.array(arr)
if "cam" in a:
    cap = cv.VideoCapture(0)
else:
    cap = cv.VideoCapture("demo.mp4")
while cap.isOpened():
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if type(faces) == type(arr_n):
        for (x, y, w, h) in faces:
            cv.rectangle(gray, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        
        data = predict_age(faces)
        # print(data[0][1])
        main_text = str(data)
        cv.putText(gray, 
                main_text, 
                (50, 50), 
                font, 1, 
                (0, 255, 255), 
                2, 
                cv.LINE_4)
        cv.imshow('frame', gray)
    else:
        main_text = "Detecting Face.."
        cv.putText(gray, main_text, (50, 50), font, 1, (0, 255, 255), 2, cv.LINE_4)
        cv.imshow("frame",gray)

    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()

