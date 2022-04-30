import os
import config
from PIL import Image
from tqdm import tqdm
import numpy as np
import pandas as pd
from annoy import AnnoyIndex
from tqdm import tqdm
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
import tensorflow as tf
import matplotlib.pyplot as plt

class LoadData:
    def __init__(self):
        pass
    def from_folder(self,folder_list:list):
        self.folder_list = folder_list
        image_path = []
        for folder in self.folder_list:
            for path in os.listdir(folder):
                image_path.append(os.path.join(folder,path))
        return image_path 

class FeatureExtractor:
    def __init__(self):

        # Use VGG-16 as the architecture and ImageNet for the weight
        base_model = VGG16(weights='vgg16_weights_tf_dim_ordering_tf_kernels.h5')
        # Customize the model to return features from fully-connected layer

        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
    def extract(self, img):

        # processing Images

        img = img.resize((224, 224))

        # Convert the image color space

        img = img.convert('RGB')
        # Reformat the image

        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Extract Features

        feature = self.model.predict(x)[0]
        return feature / np.linalg.norm(feature)

    def get_feature(self,image_data:list):
        self.image_data = image_data 
        features = []
        for img_path in tqdm(self.image_data):
            # Extract Features
            try:
                feature = self.extract(img=Image.open(img_path))
                features.append(feature)
            except:
                features.append(None)
                continue
        return features

class Index:

    def __init__(self,image_list:list):
        self.image_list = image_list
        if 'data_files_saved' not in os.listdir():
            os.makedirs("data_files_saved")
        self.FE = FeatureExtractor()
    
    def start_feature_extraction(self):
        image_data = pd.DataFrame()
        image_data['images_paths'] = self.image_list
        f_data = self.FE.get_feature(self.image_list)
        image_data['features']  = f_data
        image_data = image_data.dropna().reset_index(drop=True)
        image_data.to_pickle(config.image_data_with_features_pkl)
        print("Image Meta Information Saved: [data_files_saved/image_data_features.pkl]")
        return image_data
    
    def start_indexing(self,image_data):
        self.image_data = image_data
        f = len(image_data['features'][0])

        ## Using euclidean loss and knn
        
        t = AnnoyIndex(f, 'euclidean')
        for i,v in tqdm(zip(self.image_data.index,image_data['features'])):
            t.add_item(i, v)
        t.build(100) # 100 trees
        print("Saved the File:"+"[data_files_saved/image_features_vectors.ann]")
        t.save(config.image_features_vectors_ann)
    
    def Start(self):
        if len(os.listdir("data_files_saved/"))==0:
            data = self.start_feature_extraction()
            self.start_indexing(data)
        else:
            print("Features are Already saved want To extract again.[yes/no]?")
            flag  = str(input())
            if flag.lower() == 'yes':
                data = self.start_feature_extraction()
                self.start_indexing(data)
            else:
                print("Data is already present please just search.")
                print(os.listdir("data_files_saved/"))

class SearchImage:
    def __init__(self):
        self.image_data = pd.read_pickle(config.image_data_with_features_pkl)
        self.f = len(self.image_data['features'][0])
    def search_by_vector(self,v,n:int):
        self.v = v # Feature Vector
        self.n = n # number of output 
        u = AnnoyIndex(self.f, 'euclidean')
        u.load(config.image_features_vectors_ann) 
        # Finding 10 nearest neighbours
        index_list = u.get_nns_by_vector(self.v, self.n) 
        return dict(zip(index_list,self.image_data.iloc[index_list]['images_paths'].to_list()))
    
    def get_query_vector(self,image_path:str):
        self.image_path = image_path
        img = Image.open(self.image_path)
        fe = FeatureExtractor()
        query_vector = fe.extract(img)
        return query_vector
    
    def show_similar_images(self,image_path:str):
        self.image_path = image_path
        query_vector = self.get_query_vector(self.image_path)
        img_list = list(self.search_by_vector(query_vector,16).values())
        
        axes=[]
        fig=plt.figure(figsize=(20,15))
        for a in range(4*4):
            axes.append(fig.add_subplot(4, 4, a+1))  
            plt.axis('off')
            plt.imshow(Image.open(img_list[a]))
        fig.tight_layout()
        fig.suptitle('Similar Images Found', fontsize=22)
        plt.show(fig)
    
    def get_similar_images(self,image_path:str,number_of_images:int):
        self.image_path = image_path
        self.number_of_images = number_of_images
        query_vector = self.get_query_vector(self.image_path)
        img_dict = self.search_by_vector(query_vector,self.number_of_images)
        return img_dict