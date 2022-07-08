import streamlit as st
import os
from bing_image_downloader import downloader




st.title("Image Scraper")

st.write("***")
a,b = st.columns(2)

query = a.text_input(label="Enter query")



limit = int(b.number_input(label="Number of images you want to download",min_value=1,max_value=1000,step=1,value=5))

adult_filter = a.checkbox(label="Adult Filter",value=True)

force_replace = b.checkbox(label="Force Replace",value=False)

timeout = st.number_input(label="Timeout interval",value=60)

verbose = st.checkbox(label="Show Logs",value=True)

downloadButton = st.button(label="Download")

if downloadButton:

    a = downloader.download(query, limit=limit, output_dir="dataset", adult_filter_off=adult_filter, force_replace=force_replace, timeout=timeout, verbose=verbose)
    
    images_name = os.listdir("dataset/"+query)
    st.write("***")
    st.write("> Downloaded Images")
    for i in images_name:
        img_path = "dataset/"+query+"/"+str(i)
        st.image(img_path)
