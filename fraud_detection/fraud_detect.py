import torch
import torch.nn as nn
import numpy as np


class LogisticRegression(nn.Module):
    def __init__(self,no_of_features):
        super(LogisticRegression, self).__init__()
        self.linear1 = nn.Linear(no_of_features,10)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(10,1)
        self.sigmoid = nn.Sigmoid()
        

    def forward(self, targets_train ):
        out = self.linear1(targets_train)
        out  = self.relu(out)
        out = self.linear2(out)
        out = self.sigmoid(out)
        
        return out

model = LogisticRegression(no_of_features=4)


def predict_value(inputs):
    if len(inputs)==4:
        inputs = np.array(inputs)
        inputs = torch.from_numpy(inputs.astype(np.float32))
        main_model = torch.load("credit_card_4-1.pth")
        pred = main_model(inputs)
        value = pred.item()
        if value < 0.5:
            return "No Fraud"
        else:
            return "Fraud Detected"
    else:
        return "SOme errors in input found!!"

