import streamlit as st
from PIL import Image
from predict import check_tumor
st.title("Brain Tumor Detection using MRI")

def load_image(image_file):
    img = Image.open(image_file)
    img.save("uploads/1.png")
    return img


st.write("### Upload image")
image_file = st.file_uploader("Upload MRI Scan Image Here", type=["png","jpg","jpeg"])
threshold = st.select_slider("Choose a threshold",options=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.8,1.0],value=0.3)

if image_file is not None:
    file_details = {"filename":image_file.name, "filetype":image_file.type,"filesize":image_file.size}
    # st.write(file_details)
    st.write("#### MRI Scan Uploaded")
    st.image(load_image(image_file),width=250)

a = st.button("Predict")

if a:
    status,prob = check_tumor("uploads/1.png",threshold)
    prob = round(prob,3)
    st.write("## "+str(status))
    st.write("Actual Probablity:",prob)
    st.write("Threshold Selected:",threshold)