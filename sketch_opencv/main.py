
import cv2

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--img",required=True,type=str,help="Image Path")
parser.add_argument("--show",default=False,type=bool,help="Add this tag if you also want to see image")
parser.add_argument("--out",type=str,default="output.jpeg",help="Name for file in which Sketch to be saved")

args = parser.parse_args()

image_name =  args.img
show = args.show
filename_out = args.out

img = cv2.imread(image_name,1)

img_invert = cv2.bitwise_not(img)
img_smoothing = cv2.GaussianBlur(img_invert,(21,21),sigmaX=0,sigmaY=0)

def dodgeV2(x,y):
    return cv2.divide(x,255-y,scale=256)


final_img = dodgeV2(img,img_smoothing)

cv2.imwrite(filename_out,final_img)

if show:
    cv2.imshow("Sketch",final_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

