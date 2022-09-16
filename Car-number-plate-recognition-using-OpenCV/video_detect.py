import cv2 as cv
import numpy as np
import time
import argparse
import pytesseract
from data_check import find_data
parser  = argparse.ArgumentParser()

parser.add_argument("--video",type=str,required=True,help="Video Path")
parser.add_argument("--slow",type=bool,default=False,help="If you want to slow down video use this flag.")

args = parser.parse_args()
print("Loading FASTRCNN Trained Cascade...")
carPlatesCascade = cv.CascadeClassifier('haarcascades/haarcascade_russian_plate_number.xml')
font = cv.FONT_HERSHEY_SIMPLEX


# org
org = (50, 50)

slow = args.slow
# fontScale
fontScale = 1
   
# Blue color in BGR
color = (255, 255, 0)

# Line thickness of 2 px
thickness = 2

def show_frames():
    numbers = []
    prev_frame_time = 0
 
    # used to record the time at which we processed current frame
    new_frame_time = 0
    cap = cv.VideoCapture(args.video)
    ret = True
    while ret:
        ret,frame = cap.read()

        if not ret:
            break

        

        new_frame_time = time.time()

        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time

        fps = int(fps)

        
        cam_img = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        print(f'FPS: {str(fps)}')
        cv.putText(cam_img, f'FPS: {str(fps)}', (20, 100), font, 1, (100, 255, 0), 3, cv.LINE_AA)
        face = carPlatesCascade.detectMultiScale(cam_img,1.2,3)
        if type(face) == type(np.array([0])) :
            for (x,y,w,h) in face:
                img = cv.rectangle(cam_img,(x,y),(x+w,y+h),(0,255,255),2)
                plate_image = img[y:y+h,x:x+w]
                cv.imwrite("test.jpg",plate_image)
                text = pytesseract.image_to_string(plate_image, lang='eng')
                if text:
                    text = str(text).upper()
                    numbers.append(text[:-1])
                print(f'Plate Number: {text}')
                img = cv.putText(img, f'number {text}', org, font, 
                   fontScale, color, thickness, cv.LINE_AA)
                # img[y:y+h,x:x+w]=cv.medianBlur(img[y:y+h,x:x+w],35)
        
        cv.imshow('Number Plate Detection',cam_img)
        if slow:
            time.sleep(0.1)
        key=cv.waitKey(1)

        if key==ord('q'):
            break
    print(numbers)
    plate_data = find_data(numbers)
    if plate_data is not None:
        print(plate_data)
    else:
        print(f"Cannot Find Plate with numbers:\n{numbers}")
    

show_frames()