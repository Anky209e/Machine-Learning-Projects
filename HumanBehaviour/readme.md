# Human Behaviour classification
### Implemented with spatial diffrence Learning.(New)
![Paper](1701.01546.pdf)
## Dataset
### I Used the Avenue Datset.
### Processing
#### 1) Took every one frame after skipping one.
#### 2) Grayscaled and resized to 227x227

## Model Used
### I created a custom resnet model using pytorch
![Model](images/model.png)
### LSTM Layer
![lstm](images/lstm.png)
### Training
#### ACC was 73% with 30 epochs.
![train](images/train.png)
## Run on your own Desktop
#### Open .ipynb notebook and run predict_anomly function
