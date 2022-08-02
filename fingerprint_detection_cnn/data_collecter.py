import cv2
import os
import numpy as np
from PIL import Image

# Creating Folders for collecting Data




# num_images = 40


# train = False

# fing1 = False

def collect_data(train:bool,fing1:bool,num_images:int):


    print("Collekting Data")
    cap = cv2.VideoCapture(1)

    for i in range(num_images):
        ret,img = cap.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # img = remove_small_pixel(img)

        cv2.imshow("main",img)
        img_resized = cv2.resize(img,(64,64))
        if fing1 and train:   
            filename = f"data/train/fing1/{i}.jpg" 
        elif fing1 and not train:
            filename = f"data/test/fing1/{i}.jpg"
        elif not fing1 and train:
            filename = f"data/train/fing2/{i}.jpg" 
        else:
            filename = f"data/test/fing2/{i}.jpg" 

        cv2.imwrite(filename,img_resized)
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()