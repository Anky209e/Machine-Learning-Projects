import cv2 as cv
from detect import predict_pothole
import sys
a = sys.argv

xml_data = cv.CascadeClassifier('XML-data.xml')  

if "cam" in a:
    cap = cv.VideoCapture(0)
else:
    cap = cv.VideoCapture("Potholes live.mp4")



while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2RGB)  
    ret,thresh1 = cv.threshold(gray,200,255,cv.THRESH_BINARY)
    edge = cv.Canny(thresh1,100,100)
    contours, hierarchy = cv.findContours(edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    cv.drawContours(gray, contours, -1, (0, 255, 0), 3)

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

