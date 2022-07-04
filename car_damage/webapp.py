from numpy import imag
import streamlit as st
import os
from PIL import Image
import prediction
st.set_page_config(page_title="Car Damage",page_icon="uploads/1.png")
st.write("# Car Damage detection CNN")

def load_image(image_file):
    img = Image.open(image_file)
    img.save("1.png")
    return img


st.write("### Upload image")
image_file = st.file_uploader("Upload Image of car", type=["png","jpg","jpeg"])


if image_file is not None:
    file_details = {"filename":image_file.name, "filetype":image_file.type,"filesize":image_file.size}
    # st.write(file_details)
    st.write("#### Car Image Uploaded")
    st.image(load_image(image_file),width=250)

a = st.button("Predict")

if a:
    result = prediction.real_time("1.png")
    st.write("#### Output: "+str(result))
    # st.write("#### Probablity: "+str(prob))
st.write("***")
