import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
from main import main
from PIL import Image

def load_image(image_file):
    img = Image.open(image_file)
    img.save("data/word.png")
    return img

def run():
    word,prob = main()
    status = str(word)+"\nProbablity:"+str(prob)
    return word,prob

st.title("Handwriting Recognition")
st.write("***")

st.write("### Upload Image")



image_file = st.file_uploader("Upload Image of skin or face", type=["png","jpg","jpeg"])

predict_btl = st.button(label="Predict")

st.write("***")
if predict_btl:

    if image_file is not None:
        load_image(image_file)
        st.image(caption="Current Image",image="data/word.png")
        word , prob = run()
        st.write("## Word: ",word)
        st.write("## Probablity: ",prob)
    else:
        st.warning("No image to save")

# st.write("***")
# st.write("# Training Process")
# head_cont = """##
#  Handwritten Text Recognition (HTR) system implemented with TensorFlow (TF) and trained on the IAM off-line HTR dataset.
# The model takes **images of single words or text lines (multiple words) as input** and **outputs the recognized text**.
# 3/4 of the words from the validation-set are correctly recognized, and the character error rate is around 10%.
# """



# st.write(head_cont)
# st.image(caption="Example",image="doc/htr.png")

# st.write("# Integrate word beam search decoding")
# dec_cont = """  Words are constrained to those contained in a dictionary, but arbitrary non-word character strings (numbers, punctuation marks) can still be recognized.
# The following illustration shows a sample for which word beam search is able to recognize the correct text, while the other decoders fail."""

# st.write(dec_cont)
# st.image(caption="Decoder",image="doc/decoder_comparison.png")
