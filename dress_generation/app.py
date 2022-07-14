import streamlit as st
import os
from PIL import Image
st.set_page_config(page_title="Dress Gan",page_icon="test/1.png")
st.write("# Dress Generation Gan")

def load_image(image_file):
    img = Image.open(image_file)
    img.save("test/1.png")
    return img

def load_mask(image_file):
    img = Image.open(image_file)
    img.save("cihp_test_mask/1.png")
    return img

st.write("### Upload image")
image_file = st.file_uploader("Upload Image of person", type=["png","jpg","jpeg"])
st.write("### Upload Mask")
image_mask = st.file_uploader("Upload Image for mask", type=["png","jpg","jpeg"],key="asdawd")

if image_file is not None:
    file_details = {"filename":image_file.name, "filetype":image_file.type,"filesize":image_file.size}
    # st.write(file_details)
    st.write("#### Person image uploaded")
    st.image(load_image(image_file),width=250)
if image_mask is not None:
    file_details = {"filename":image_mask.name, "filetype":image_mask.type,"filesize":image_mask.size}
    st.write("#### Mask uploaded")
    st.image(load_mask(image_mask),width=250)



a = st.button("Generate New Dress")
st.write("### Generated dress image.")
st.image("results/deepfashion_smis/test_latest/images/1.png")
st.write("### Uploaded image.")
st.image("test/1.png")
if a:
    os.system("./deepfashion.sh")
    st.write("#### Just generated image.")
    st.image("results/deepfashion_smis/test_latest/images/1.png")
    