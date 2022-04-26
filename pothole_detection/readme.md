## Pothole Detection using Deep neural networks and OpenCV
#### Data is gathered from randmo sites.
## Data Preprocessing
### 1) Thresholding
### 2) Finding Edges
### 3) Resizing
## FInal data batch used for training
![Data](images/batch.png)

## Model Used
### I Created a custom ResNet model using pytorch
![Model](images/model.png)
## Training Process
#### Accuracy
![Accuracy Image](images/acuu.png)
#### Loss
![Loss Image](images/loss.png)
#### Learning rate decay
![Lr](images/lr.png)
# Implementing in OpenCV
![Gif](images/output.gif)
# Run on your desktop
```
pip install opencv-python
pip install torch torchvision pillow matplotlib
python3 cv_pothole.py cam
```
##### Note: use cam for using your own camera else it will use a default video.
