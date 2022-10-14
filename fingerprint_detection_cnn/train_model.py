
from cProfile import label
import torch, gc
import os

import torch.nn as nn
import numpy as np
import torch.nn.functional as F
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
import torchvision.transforms as tt

import matplotlib.pyplot as plt



def denormalize(images,means,stds):
    means = torch.tensor(means).reshape(1,3,1,1)
    stds = torch.tensor(stds).reshape(1,3,1,1)
    return images*stds+means


def get_default_device():
    """Pick GPU if available, else CPU"""
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')
    
def to_device(data, device):
    """Move tensor(s) to chosen device"""
    if isinstance(data, (list,tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)

class DeviceDataLoader():
    """Wrap a dataloader to move data to a device"""
    def __init__(self, dl, device):
        self.dl = dl
        self.device = device
        
    def __iter__(self):
        """Yield a batch of data after moving it to device"""
        for b in self.dl: 
            yield to_device(b, self.device)

    def __len__(self):
        """Number of batches"""
        return len(self.dl)

def plot_all(history):
    print("Saving Graph")
    fig = plt.figure(1)
    accuracies = [x['val_acc'] for x in history]
    loss = [x['val_loss'] for x in history]
    lr = [x['lrs'] for x in history]
    plt.plot(accuracies,label = "Accuracy")
    plt.plot(loss,label="Loss")
    plt.plot(lr,label="Learning Rate")
    plt.xlabel('epoch')
    plt.ylabel('parameters')
    plt.savefig("images/main.png")




def accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == labels).item() / len(preds))

class ImageClassificationBase(nn.Module):
    def training_step(self, batch):
        images, labels = batch 
        out = self(images)                  # Generate predictions
        loss = F.cross_entropy(out, labels) # Calculate loss
        return loss
    
    def validation_step(self, batch):
        images, labels = batch 
        out = self(images)                    # Generate predictions
        loss = F.cross_entropy(out, labels)   # Calculate loss
        acc = accuracy(out, labels)           # Calculate accuracy
        return {'val_loss': loss.detach(), 'val_acc': acc}
        
    def validation_epoch_end(self, outputs):
        batch_losses = [x['val_loss'] for x in outputs]
        epoch_loss = torch.stack(batch_losses).mean()   # Combine losses
        batch_accs = [x['val_acc'] for x in outputs]
        epoch_acc = torch.stack(batch_accs).mean()      # Combine accuracies
        # saving model above 85% accuracy
        return {'val_loss': epoch_loss.item(), 'val_acc': epoch_acc.item()}
    
    def epoch_end(self, epoch, result):
        print("Epoch [{}], last_lr: {:.5f}, train_loss: {:.4f}, val_loss: {:.4f}, val_acc: {:.4f}".format(
            epoch, result['lrs'][-1], result['train_loss'], result['val_loss'], result['val_acc']))


class ResNet9(ImageClassificationBase):
    def __init__(self, in_channels, num_classes):
        super().__init__()
        self.norm15 = nn.BatchNorm2d(15)
        self.norm30 = nn.BatchNorm2d(30)
        self.norm60 = nn.BatchNorm2d(60)
        self.norm120 = nn.BatchNorm2d(120)
        self.norm200 = nn.BatchNorm2d(200)
        self.norm300 = nn.BatchNorm2d(300)
        self.norm360 = nn.BatchNorm2d(360)
        self.norm512 = nn.BatchNorm2d(512)
        #--------------------
        self.conv15 = nn.Conv2d(3,15,kernel_size=3,stride=1,padding=1)#15x64x64
        self.conv30 = nn.Conv2d(15,30,kernel_size=3,stride=1,padding=1)#30x64x64
        self.conv60 = nn.Conv2d(30,60,kernel_size=3,stride=2,padding=1)#60x32x32

        self.res60 = nn.Conv2d(60,60,kernel_size=3,stride=1,padding=1)
        #---------------
        self.conv120a = nn.Conv2d(60,60,kernel_size=3,stride=1,padding=1)
        #------------
        self.conv200 = nn.Conv2d(60,200,kernel_size=3,stride=1,padding=1)#200x32x32
        self.conv200a = nn.Conv2d(200,200,kernel_size=3,stride=2,padding=1)#200x16x16
        

        self.res200 = nn.Conv2d(200,200,kernel_size=3,stride=1,padding=1)
        #------------------
        self.conv300 = nn.Conv2d(200,200,kernel_size=3,stride=1,padding=1)
        self.conv360 = nn.Conv2d(200,360,kernel_size=3,stride=1,padding=1)#360x16x16
        self.conv512 = nn.Conv2d(360,512,kernel_size=3,stride=1,padding=1)#512x16x16

        

        #===========================#
        self.pool = nn.MaxPool2d(2,2)
        self.avgpool = nn.AvgPool2d(2,2)
        self.flat = nn.Flatten()

        self.linear = nn.Linear(512*2*2,2)

    def forward(self,xb):
      out = torch.relu(self.norm15(self.conv15(xb)))#15x64x64

      out = torch.relu(self.norm30(self.conv30(out)))#30x64x64

      out = torch.relu(self.norm60(self.conv60(out)))#60x32x32

      x = self.res60(out)#120x32x32

      out = torch.relu(self.conv120a(out)+x)

      out = torch.relu(self.norm200(self.conv200(out)))

      out = torch.relu(self.conv200a(out))

      

      x = self.res200(out)

      out = torch.relu(self.conv300(out)+x)

      out = torch.relu(self.norm360(self.conv360(out)))

      out = torch.relu(self.norm512(self.conv512(out)))

      out = self.avgpool(out)#512x8x8
      out = self.avgpool(out)#512 4 4
      out = self.avgpool(out)#512 2 2
      
      out = self.flat(out)
      out = self.linear(out)

      return out






from tqdm import tqdm

def validate_results(path_to_validation_data):
    val_ds = ImageFolder(path_to_validation_data,test_tfms)
    val_dl = DataLoader(val_ds,batch_size=32,shuffle=True,num_workers=3,pin_memory=True)
    model = ResNet9(3,2)
    model.load_state_dict(torch.load("weights/fingerprint_final.pth"))
    results = evaluate(model,val_dl)
    return results
@torch.no_grad()
def evaluate(model, val_loader):
    model.eval()
    outputs = [model.validation_step(batch) for batch in val_loader]
    return model.validation_epoch_end(outputs)

def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']

def fit_one_cycle(epochs, max_lr, model, train_loader, val_loader, 
                  weight_decay=0, grad_clip=None, opt_func=torch.optim.SGD):
    torch.cuda.empty_cache()
    history = []
    
    # Set up cutom optimizer with weight decay
    optimizer = opt_func(model.parameters(), max_lr, weight_decay=weight_decay)
    # Set up one-cycle learning rate scheduler
    sched = torch.optim.lr_scheduler.OneCycleLR(optimizer, max_lr, epochs=epochs, 
                                                steps_per_epoch=len(train_loader))
    
    for epoch in range(epochs):
        # Training Phase 
        model.train()
        train_losses = []
        lrs = []
        for batch in tqdm(train_loader):
            loss = model.training_step(batch)
            train_losses.append(loss)
            loss.backward()
            
            # Gradient clipping
            if grad_clip: 
                nn.utils.clip_grad_value_(model.parameters(), grad_clip)
            
            optimizer.step()
            optimizer.zero_grad()
            
            # Record & update learning rate
            lrs.append(get_lr(optimizer))
            sched.step()
        
        # Validation phase
        result = evaluate(model, val_loader)
        result['train_loss'] = torch.stack(train_losses).mean().item()
        result['lrs'] = lrs
        model.epoch_end(epoch, result)
        history.append(result)
    return history

if __name__=="__main__":
    stats = ((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    
    train_tfms = tt.Compose([
                        tt.RandomHorizontalFlip(),
                        tt.RandomVerticalFlip(),
                        tt.RandomRotation(30),
                        tt.RandomAdjustSharpness(1.3),
                        tt.ToTensor(),
                        tt.Normalize(*stats,inplace=True)
                        ])
    test_tfms = tt.Compose([tt.ToTensor(),tt.Normalize(*stats)])

    train_ds = ImageFolder('data/train',train_tfms)
    test_ds = ImageFolder('data/test',test_tfms)


    print(f"Classes: {train_ds.classes}")


    batch_size = 24

    train_dl = DataLoader(train_ds,batch_size,shuffle=True,num_workers=3,pin_memory=True)
    test_dl = DataLoader(test_ds,batch_size*2,num_workers=3,pin_memory=True)
    device = get_default_device()

    print(f"Using: {device}")

    train_dl = DeviceDataLoader(train_dl, device)
    test_dl = DeviceDataLoader(test_dl, device)

    model = to_device(ResNet9(3,2),device)

    model_det = f"""
    --------------------------------
    {model}
    --------------------------------
    """
    print(model_det)

    epochs = 20
    max_lr = 0.0001
    grad_clip = 0.1
    weight_decay = 1e-5
    opt_func = torch.optim.Adam

    details = f"""
    ------------------
    |   Details      |
    ------------------
    Epochs: {epochs}
    Max Learning Rate: {max_lr}
    Grad Clip: {grad_clip}
    Decay: {weight_decay}
    Optimizer: Adam
    -------------------
    """
    print(details)

    ret_data = fit_one_cycle(epochs,max_lr,model,train_dl,test_dl,weight_decay,grad_clip,opt_func)

    os.makedirs("weights",exist_ok=True)
    print("Saving Weights...")
    torch.save(model.state_dict(),"weights/fingerprint_final.pth")


    print("Validating Results...")
    final_res = validate_results("data/test")

    final_cont = f"""
    ==========================
            Results
    ==========================
    Trained for {epochs} epochs using {device}.
    Final Loss on Validation set: {round(final_res["val_loss"],3)}
    Final Accuracy on Validation set: {round(final_res["val_acc"]*100,3)}%
    ==========================
    """
    print(final_cont)
    import json


    os.makedirs("images",exist_ok=True)



    plot_all(ret_data)

    with open('info.json', 'w') as outfile:
        json.dump(final_res, outfile)



