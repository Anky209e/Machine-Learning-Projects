import torch
from torchvision.transforms import ToTensor
import torch.nn as nn
import numpy as np
from PIL import Image
import os
stats = ((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
def denormalize(images,means,stds):
    means = torch.tensor(means).reshape(1,3,1,1)
    stds = torch.tensor(stds).reshape(1,3,1,1)
    return images*stds+means


class ResNet9(nn.Module):
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

        self.linear = nn.Linear(512*2*2,40)

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

def predict(path_to_image):
    size = 64

    img = Image.fromarray(path_to_image)
    img_cls = ['applauding',
    'blowing_bubbles',
    'brushing_teeth',
    'cleaning_the_floor',
    'climbing',
    'cooking',
    'cutting_trees',
    'cutting_vegetables',
    'drinking',
    'feeding_a_horse',
    'fishing',
    'fixing_a_bike',
    'fixing_a_car',
    'gardening',
    'holding_an_umbrella',
    'jumping',
    'looking_through_a_microscope',
    'looking_through_a_telescope',
    'phoning',
    'playing_guitar',
    'playing_violin',
    'pouring_liquid',
    'pushing_a_cart',
    'reading',
    'riding_a_bike',
    'riding_a_horse',
    'rowing_a_boat',
    'running',
    'shooting_an_arrow',
    'smoking',
    'taking_photos',
    'texting_message',
    'throwing_frisby',
    'using_a_computer',
    'walking_the_dog',
    'washing_dishes',
    'watching_TV',
    'waving_hands',
    'writing_on_a_board',
    'writing_on_a_book']

    if img.size != (size,size):
        img = img.resize((size,size))
    
    transform = ToTensor()
    img_tensor = transform(img)
    img_tensor = img_tensor[:3]
    img_tensor = denormalize(img_tensor,*stats)
    
    img_tensor = torch.reshape(img_tensor, (1,3,size,size))

    model_pred = ResNet9(3,40)
    model_pred.load_state_dict(torch.load("weights/weight_29.pth",map_location=torch.device("cpu")))

    pred = model_pred(img_tensor).detach()
    pred = np.array(pred[0])
    pred = list(pred)
    # for i in range(len(img_cls)):
    #     pred[i] = round(pred[i]*100, 2)
    max_el = max(pred)

    index_cl = pred.index(max_el)
    result = img_cls[index_cl]
    # result.sort(key=lambda x:x[1], reverse=True)
    
    # os.remove(path_to_image)
    
    return result

if __name__ == "__main__":
    print(predict("data/test/phoning_test/phoning_001.jpg"))