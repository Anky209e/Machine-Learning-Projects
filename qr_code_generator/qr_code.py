import pyqrcode
import argparse
import cv2

parser = argparse.ArgumentParser()

parser.add_argument("--url",type=str,required=True,help="Url or text for which you want to generate Qr.")
parser.add_argument("--output",type=str,required=True,help="Path to save qr code image [png]")

args = parser.parse_args()

url = args.url
image_path = args.output

qr = pyqrcode.create(url)

qr.png(image_path,scale=6)

img = cv2.imread(image_path)

cv2.imshow(url,img)
cv2.waitKey(0)
cv2.destroyAllWindows()