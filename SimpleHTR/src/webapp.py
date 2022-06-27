import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
from main import main

def run():
    word,prob = main()
    status = str(word)+"\nProbablity:"+str(prob)
    return word,prob

st.title("Handwriting Recognition")
st.write("***")

st.write("### Write something")
canvas_result = st_canvas(
            fill_color="#eee",
            stroke_width=5,
            stroke_color="black",
            background_color="white",
            update_streamlit=False,
            height=200,
            width=400,
            drawing_mode="freedraw",
        )

predict_btl = st.button(label="Predict")

st.write("***")
if predict_btl:
    if canvas_result.image_data is not None:
        cv2.imwrite(f"data/word.png",  canvas_result.image_data)
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
