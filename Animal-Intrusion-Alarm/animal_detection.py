import numpy as np
import time
import cv2
import os
import numpy as np
from playsound import playsound
import threading
from aws_ses import send_mail

def alert():
    threading.Thread(target=playsound, args=('alarm.wav',), daemon=True).start()

already_sent = False
def notify(data):
    global already_sent

    # Senders Address (Should be verified with AWS SES service)
    SENDER_ADDRESS = ""

    # Reciv. address (Should be verified with AWS SES service)
    RECIEVER_ADDRESS = ""

    sub = "A "+data+" is detected."
    text = "Warning from System"
    html_content = """
    <h1>A {} is detected in Animal Detection system.</h1>
    <h4>This mail is sent using AWS SES.Please do not reply to this.</h4>

    <a href="https://modelsmith.info">Learn more about ML</a>
    """.format(data)

    send_mail(sender=SENDER_ADDRESS,reciever=RECIEVER_ADDRESS,subject=sub,content_text=text,content_html=html_content)
    already_sent = True
    print("Sent")







args = {"confidence":0.5, "threshold":0.3}
flag = False

labelsPath = "./yolo-coco/coco.names"
LABELS = open(labelsPath).read().strip().split("\n")
final_classes = ['bird', 'cat', 'dog', 'sheep', 'horse', 'cow', 'elephant', 'zebra', 'bear', 'giraffe']

np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

weightsPath = os.path.abspath("./yolo-coco/yolov3.weights")
configPath = os.path.abspath("./yolo-coco/yolov3.cfg")

# print(configPath, "\n", weightsPath)

net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

vs = cv2.VideoCapture(0)
writer = None
(W, H) = (None, None)

flag=True
num_counter = 0
while True:
    print("Detection Count: "+str(num_counter),end="\r")
    # read the next frame from the file
    (grabbed, frame) = vs.read()
    
    # if the frame was not grabbed, then we have reached the end
    # of the stream
    if not grabbed:
        break

    # if the frame dimensions are empty, grab them
    if W is None or H is None:
        (H, W) = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
        swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()

    # initialize our lists of detected bounding boxes, confidences,
    # and class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability)
            # of the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > args["confidence"]:
                # scale the bounding box coordinates back relative to
                # the size of the image, keeping in mind that YOLO
                # actually returns the center (x, y)-coordinates of
                # the bounding box followed by the boxes' width and
                # height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top
                # and and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates,
                # confidences, and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping
    # bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
        args["threshold"])


    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            
            if(LABELS[classIDs[i]] in final_classes):
                # playsound('alarm.wav')
                if(flag):
                    alert()
                    flag=False
                
                    
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]],
                    confidences[i])
                if not already_sent or cv2.waitKey(33) == ord('a') or (num_counter % 100 == 0):
                    notify(LABELS[classIDs[i]])
                else:
                    print("Email is already sent!",end="\r")
                    print("Press A to send it again.(not recommended)",end="\r")
                num_counter +=1
                
                cv2.putText(frame, text, (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    else:
        flag=True

    cv2.imshow("Animal Detector", frame) 

    if cv2.waitKey(1) == ord('q'):
        break

# release the webcam and destroy all active windows
vs.release()
cv2.destroyAllWindows()


