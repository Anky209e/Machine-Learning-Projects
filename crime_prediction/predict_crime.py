import pandas as pd
import numpy as np
import torch
import torch.nn as nn


def softmax(x):
    return (np.exp(x)/np.exp(x).sum())



class LogisticRegression(nn.Module):
    def __init__(self,no_of_features):
        super(LogisticRegression, self).__init__()
        self.linear1 = nn.Linear(no_of_features,10)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(10,6)
        

    def forward(self, targets_train ):
        out = self.linear1(targets_train)
        out  = self.relu(out)
        out = self.linear2(out)
        # out = self.relu(out)
        
        return out

model = LogisticRegression(no_of_features=11)

model.load_state_dict(torch.load('model/final_crime_lats.pth'))

def predict(arr):
    main_tensor = torch.from_numpy(arr.astype(np.float32))
    preds_all = model(main_tensor)
    softmax_pred = softmax(preds_all.detach().numpy())*100
    
    
    final_dict = {'act379':round(softmax_pred[0],2),'act13':round(softmax_pred[1],2),'act279':round(softmax_pred[2],2),'act323':round(softmax_pred[3],2),'act363':round(softmax_pred[4],2),'act302':round(softmax_pred[5],2)}
    
    print(final_dict)
    
    return softmax_pred,final_dict