import cv2
import torch
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--source",type=str,required=True,help="Video Path or Camera Source")
print("Checking Video Source..")
args = parser.parse_args()

image_path = args.source
# cameras = [0,1,2,3,4,5]
try: 
    vid = cv2.VideoCapture(int(image_path))
except:
    print("Video File Found")
    vid = cv2.VideoCapture(image_path)
try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
except:
    print("OOPS! Looks like you are not connected to internet.")

print("Starting Video.\nPress 'q' on keyboard to close OPENCV window.")
while True:  
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
  
    # Display the resulting frame
    # cv2.imshow('frame', frame)
    results = model(frame)
    # results.render()
    cv2.imshow("Video Segmentation",results.render()[0])
    # break
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()