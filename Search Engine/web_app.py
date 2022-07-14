import streamlit as st
import os
import json

st.set_page_config(page_title="Search Engine")
st.write("# Search Engine Using Python")

query = st.text_input(label="Search Here")


a = st.button(label="Search")
if a:
    st.write("***")

    os.system("python3 search_engines_cli.py -p 2 -e google -q "+query+" -o json")




    with open("search_engines/search_results/output.json", 'r') as f:
        data = json.load(f)
    for i in range(0,10):
        hostname = data["results"]["Google"][i]["title"]
        link = data["results"]["Google"][i]["link"]
        text = data["results"]["Google"][i]["text"]
        print(link)
        link_mark = "["+str(hostname)+"]"+"("+str(link)+")"
        st.write(hostname)
        st.write(link)
        st.write(text)
        st.write("***")