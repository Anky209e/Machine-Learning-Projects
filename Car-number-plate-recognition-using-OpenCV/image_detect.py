import cv2
import numpy as np
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--img",type=str,required=True,help="Path of image you want to use")

args = parser.parse_args()
faceCascade = cv2.CascadeClassifier('haarcascades/haarcascade_russian_plate_number.xml')

img = cv2.imread(args.imgq)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(gray,scaleFactor=1.2,
    minNeighbors = 5, minSize=(25,25))

for (x,y,w,h) in faces:
    cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
    plate = gray[y: y+h, x:x+w]
    plate = cv2.blur(plate,ksize=(20,20))
    # put the blurred plate into the original image
    gray[y: y+h, x:x+w] = plate

cv2.imshow('plates',gray)
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()