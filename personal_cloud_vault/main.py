import boto3
from botocore.exceptions import ClientError
import os
import streamlit as st
os.makedirs("uploads",exist_ok=True)


def load_from_env():
    print("Loading Credentials for AWS S3..")
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    if aws_secret_access_key is None or aws_access_key_id is None:
        print("Credentials not found!")
    else:
        print("Credentials Loaded!")



s3_client = boto3.client('s3')

# Your bucket name where you want to upload all of your files
BUCKET_NAME = "your_bucket_name"

response = s3_client.list_objects(Bucket=BUCKET_NAME)

st.set_page_config(page_title='Cloud Vault',page_icon="assets/favicon.ico")

# Getting and sorting data from S3 bucket
def get_data(response):
    main_ar = []
    total_size = 0
    for i in response['Contents']:

        name = i['Key']
        size = int(i['Size'])*(1e-6)
        storage_class = i['StorageClass']
        raw_date_time = str(i['LastModified'])[:-6]
        date_time = raw_date_time.split(" ")
        date = date_time[0]
        time = date_time[1]

        total_size+=size
        stats = """
        -----------
        FileName: {}
        FileSize: {} MB
        StorageClass: {}
        Date: {}
        Time: {}
        ------------
        """.format(name,round(size,2),storage_class,date,time)

        main_ar.append({"Name":name,"Size(MB)":round(size,2),"Last Modified":date,"Time":time,"Storage Class":storage_class})
        print(stats)
    
    return main_ar,len(main_ar),total_size


# Uploading file to S3 bucket
def upload_file(file_name, bucket:str, object_name=None):

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        print("Uploading")

        response = s3_client.upload_file(file_name, bucket, object_name,ExtraArgs={'ACL':'public-read'})
        print("Uploaded")

    except ClientError as e:
        st.warning(e)
        return False

    st.success("File Uploaded to cloud")
    return True

# Saving file locally in uploads folder to keep track
def save_uploadedfile(uploadedfile):
     with open(os.path.join("uploads",uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.info("Saved File:{} to uploads".format(uploadedfile.name))

# Deleting file from S3 Bucket
def delete_file(key):
    try:
        stats = s3_client.delete_object(Bucket = BUCKET_NAME,Key = str(key))
    except:
        return False
    return True


my_page = st.sidebar.radio('Options', ['Upload Document', 'View All Documents','Download Documents','Delete Documents'])


if my_page == "Upload Document":
    st.title("Encrypted Documents Cloud Vault")
    st.write("***")
    st.write("### Encrypt And Upload To Cloud")

    
    filename = st.file_uploader(label="Upload File",accept_multiple_files=False)
    a,b = st.columns(2)
    
    cloud_upload = a.button("Upload File")
    save_locally = b.checkbox(label="Save Locally",value=True)

    if cloud_upload:
        if save_locally:
            save_uploadedfile(filename)
        path_to_file = "uploads/"+str(filename.name)
        upload_file(path_to_file,BUCKET_NAME)




elif my_page == "View All Documents":
    st.title("Encrypted Documents Cloud Vault")
    st.write("***")
    data,file_num,file_size = get_data(response=response)
    a,b = st.columns(2)

    a.metric(label="Total Storage Used",value= str(round(file_size,2))+" MB")
    b.metric(label="Total Number of Files Uploaded",value=file_num)

    st.write("***")
    st.write("### All Uploaded Documents")
    
    st.table(data=data)

elif my_page == "Download Documents":
    st.title("Encrypted Documents Cloud Vault")
    st.write("***")

    st.write("### Download Files")

    data,file_num,file_size = get_data(response=response)

    for i in data:
        link_name = i['Name']
        print(link_name)

        link = "https://bucketweights.s3.ap-south-1.amazonaws.com/"+str(link_name)

        content = """ [{}]({})""".format(link_name,link)

        st.write(content)

elif my_page =="Delete Documents":
    st.title("Encrypted Documents Cloud Vault")
    st.write("***")
    st.warning("Warning! You cannot download file after deleting.")

    key = st.text_input(label="Enter Filename you want to delete.")

    delete_final = st.button(label="Delete")
    if delete_final:

        if_deleted = delete_file(key=key)

        if if_deleted:
            st.success("{} Deleted Successfully!".format(key))
        else:
            st.info("There was some error deleting file")
            st.write("> Make sure entered filename is correct and file exists.")

