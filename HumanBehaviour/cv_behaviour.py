import cv2 as cv
from detect import predict_anomly
import sys
a = sys.argv
import time
# face_cascade = cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_frontalface_default.xml')


np_path = "f4.npy"
weights = "weights_hb/Human_behaviour_73.h5"
font = cv.FONT_HERSHEY_SIMPLEX
import numpy as np
arr = [1]
arr_n = np.array(arr)


def open_cam():
    data = predict_anomly(weights,np_path)

    frames_a = data[1]
    a = 1

    cap = cv.VideoCapture(0)
    v_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    print(v_count)
    while cap.isOpened():
        
        ret, frame = cap.read()
        

        if a in frames_a:
            # time.sleep(2)
            print(a)
            main_text = "Abnormal"
            cv.putText(frame, 
                    main_text, 
                    (50, 50), 
                    font, 1, 
                    (0, 255, 255), 
                    2, 
                    cv.LINE_4)
        else:
            main_text = "Normal"
            cv.putText(frame, 
                    main_text, 
                    (50, 50), 
                    font, 1, 
                    (0, 255, 255), 
                    2, 
                    cv.LINE_4)

        time.sleep(0.3)
            # cv.imshow('frame', frame)
        cv.imshow('frame', frame)
            
        a+=1
    



        
    # else:
    #     main_text = "Detecting Face.."
    #     cv.putText(frame, main_text, (50, 50), font, 1, (0, 255, 255), 2, cv.LINE_4)
    #     cv.imshow("frame",frame)

        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
cv.destroyAllWindows()

open_cam()