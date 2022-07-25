import streamlit as st
import os
from PIL import Image
from pymongo import MongoClient
cluster = MongoClient('#------------MongoDB address Here-------#')
db = cluster["findperson"]
st.title("Missing Persons Finder-User Panel")

os.makedirs("data/admin_data",exist_ok=True)
os.makedirs("data/user_data",exist_ok=True)

page = st.sidebar.radio(label="Menu",options=['Missing Persons','Report Sighting'])

def add_info(name,number,image_path):
    collection = db["user_data"]
    try:
        dic = {"_id":number,"name":name,"img_path":image_path}
        collection.insert_one(dic)
        print("Report Added")
        st.info(f"Report for {name} Added!")
    except:
        print("Error Encountered while Uploading Data to Cloud.")
        st.warning("There was an Issue Uploading Data.Make Sure This data don't exists already.")

def get_person_name(pnum):
    collection = db["admin_data"]
    query = {"_id":int(pnum)}
    data = collection.find_one(query)
    return data["name"]

def provide_data():
    collection = db["admin_data"]
    data = collection.find().sort("_id")
    persons = []
    for x in data:
        persons.append([x["_id"],x["name"]])
    
    return persons,data

def load_image(image_file,path_to_save):
    img = Image.open(image_file)
    img.save(path_to_save)
    return img

def process_inputs(name,image,number):
    name = name.split(" ")
    name = "_".join(name).lower()
    path = "data/user_data/"+str(name)
    image_path = path+"/"+"1.jpg"
    os.makedirs(path,exist_ok=True)
    img_ret = load_image(image,path_to_save=image_path)
    number = int(number)
    return name,img_ret,number,image_path

if page == "Missing Persons":
    st.markdown("> All Missing Persons Reported.")
    st.write("***")
    data_persons , data = provide_data()
    print(data_persons)
    a,b = st.columns(2)
    a.write("Phone Number")
    b.write("Name")
    for i in data_persons:
        a.write(i[0])
        b.write(i[1].capitalize())

if page == "Report Sighting":
    st.markdown("> Report Sighting of Person")
    st.write("***")
    number = st.text_input(label="Enter Phone Number",value=123456789)
    
    person_image = st.file_uploader("Upload Sighting Image Here", type=["jpg","jpeg"])

    upload = st.button(label="Upload")

    if upload:
        name = get_person_name(number)
        name,img_ret,number,image_path = process_inputs(name,person_image,number)
        add_info(name,number,image_path)






