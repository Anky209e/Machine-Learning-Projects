import streamlit as st
from PIL import Image
from split_channels import split_channels
import os

os.makedirs("uploads",exist_ok=True)

st.title("Image Color Channel Splitter")

def load_image(image_file):
    img = Image.open(image_file)
    img.save("uploads/temp.jpg")
    return img


image_file = st.file_uploader("Upload Image", type=["jpg","jpeg","JPG"])

if image_file is not None:
    file_details = {"filename":image_file.name, "filetype":image_file.type,"filesize":image_file.size}
    st.image(load_image(image_file),width=250,caption="Uploaded Image")

a = st.button("Split Channels")

if a:
    st.markdown("> Image Splitted in RGB")
    st.info("Every Image Consists of 3 Color Channels Red,Green and Blue.")

    split_channels("uploads/temp.jpg")

    st.image("results/result_img.png",caption="Splitted Color Channels")

    