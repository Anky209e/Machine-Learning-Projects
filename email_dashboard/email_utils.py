import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
import pickle

filename = 'weights/nlp_model.pkl'
clf = pickle.load(open(filename, 'rb'))
cv=pickle.load(open('weights/tranform.pkl','rb'))

FILE = "weights/data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

def get_email_type(message):
    features = ["Social","Buisness","Advertisement"]
    sentence = tokenize(message)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    
    return features[predicted.item()]

def is_spam(message):
    data = [message]
    vect = cv.transform(data).toarray()
    my_prediction = clf.predict(vect)
    
    return my_prediction[0]