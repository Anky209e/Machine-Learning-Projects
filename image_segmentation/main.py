import torch

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--img",type=str,required=True,help="Image path or link")

args = parser.parse_args()

image_path = args.img

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom

# Images
img = image_path  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)

# Results
results.print()
results.show() 
results.save()