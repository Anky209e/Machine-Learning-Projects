import streamlit as st
import os
from PIL import Image
from pymongo import MongoClient
from image_similarity_api import get_distance
cluster = MongoClient('#------------MongoDB address Here-------#')
db = cluster["findperson"]
st.title("Missing Persons Finder-Admin Panel")

os.makedirs("data/admin_data",exist_ok=True)
os.makedirs("data/user_data",exist_ok=True)


def register(name,number,image_path):
    collection = db["admin_data"]
    try:
        dic = {"_id":number,"name":name,"img_path":image_path}
        collection.insert_one(dic)
        print("Report Added")
        st.info(f"Report for {name} Added!")
    except:
        print("Error Happened while Uploading Data to Cloud.")
        st.warning("There was an Issue Uploading Data.Make Sure This data don't exists already.")


def provide_admin_data():
    collection = db["admin_data"]
    data = collection.find().sort("_id")
    persons = []
    for x in data:
        persons.append([x["name"],x["img_path"]])
    
    return persons

def provide_user_data():
    collection = db["user_data"]
    data = collection.find().sort("_id")
    persons = []
    for x in data:
        persons.append([x["name"],x["img_path"]])
    
    return persons

def load_image(image_file,path_to_save):
    img = Image.open(image_file)
    img.save(path_to_save)
    return img

def process_inputs(name,image,number):
    name = name.split(" ")
    name = "_".join(name).lower()
    path = "data/admin_data/"+str(name)
    image_path = path+"/"+"1.jpeg"
    os.makedirs(path,exist_ok=True)
    img_ret = load_image(image,path_to_save=image_path)
    number = int(number)
    return name,img_ret,number,image_path

page = st.sidebar.radio(label="Menu",options=['Report Missing Person','Reports from Users'])

if page == "Report Missing Person":

    st.markdown("> Report a Missing Person")
    person_name = st.text_input(label="Name")
    person_image = st.file_uploader("Upload Missing Person Image Here", type=["jpg","jpeg"])
    contact_number = st.number_input(label="Phone Number",value=9823892893)
    report = st.button(label="Report")
    if report:
        
        name,img_ret,number,image_path = process_inputs(person_name,person_image,contact_number)
        
        register(name,number,image_path)
        st.image(img_ret)



if page == "Reports from Users":

    st.markdown("> Data Recieved from Users")
    
    admin_data_present = os.listdir("data/admin_data")
    user_data_present = os.listdir("data/user_data")

    if len(admin_data_present) and len(user_data_present) > 0:

        admin_data = provide_admin_data()
        user_data = provide_user_data()
        main_dic = {}
        print(admin_data)
        for i in range(0,len(admin_data)-1):
            name_show = admin_data[i][0]
            img_score = get_distance(admin_data[i][1],user_data[i][1])
            print(admin_data[i][1],user_data[i][1])
            print(img_score)
            name_show = name_show.split("_")
            name_show = " ".join(name_show).capitalize()
            cont = f"Name: {name_show},Image Distance: {img_score}"
            st.markdown("## "+cont)





