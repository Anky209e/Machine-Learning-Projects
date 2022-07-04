from numpy import imag
import streamlit as st
import os
from PIL import Image
from predict_disease_normal import predict
st.set_page_config(page_title="Skin Disease",page_icon="uploads/1.png")
st.write("# Skin Disease CNN")

def load_image(image_file):
    img = Image.open(image_file)
    img.save("uploads/1.png")
    return img


st.write("### Upload image")
image_file = st.file_uploader("Upload Image of skin or face", type=["png","jpg","jpeg"])


if image_file is not None:
    file_details = {"filename":image_file.name, "filetype":image_file.type,"filesize":image_file.size}
    # st.write(file_details)
    st.write("#### Skin image uploaded")
    st.image(load_image(image_file),width=250)




a = st.button("Predict")

if a:
    result,prob = predict("uploads/1.png")
    
    st.write("#### Disease: "+str(result))
    st.write("#### Probablity: "+str(prob))
st.write("***")
st.write("## About Model")
st.write("##### This is a custom RESNET model created using two residual blocks.")
st.image("images/model.png",caption="Model Image")
st.write("***")

st.write("## Dataset used")
st.write("##### We used two dataset for this model on with two skin disease *Acne* and *Eczema* and celebrity face dataset for normal skin.")
st.write("##### We used technique of Data Augmentaion for increasing dataset size..")
st.image("images/batch.png",caption="Batch of data")

st.write("***")
st.write("## Training Process")
st.write("##### This model was trained for 30 epochs and reached max accuracy of *82.3%*.")
st.image("images/train.png",caption="Training process")

st.write("#### Loss vs Epocs")
st.image("images/loss.png",caption="Loss graph")

st.write("### Accuracy vc Epoch")
st.image("images/accuracy.png",caption="Accuracy graph")

st.write("### Learning rate vs Epoch")
st.image("images/lr.png",caption="Learning Rate")

st.write("***")
st.write("## Tools Used")
st.write("### Libraries")
st.write("-Pytorch")
st.write("-StreamLit")
st.write("### Optimizer")
st.write("-ADAM")
    