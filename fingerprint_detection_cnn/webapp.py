import streamlit as st
import json
from predict_fing import predict 
import os
from PIL import Image


st.title("Fingerprint Recognition Using CNN")
st.write("> *Collect Fingerprint Data*")
a = 0
train = False
thumb = False
os.makedirs("data/train/fing1",exist_ok=True)
os.makedirs("data/test/fing1",exist_ok=True)

os.makedirs("data/train/fing2",exist_ok=True)
os.makedirs("data/test/fing2",exist_ok=True)
os.makedirs("uploads",exist_ok=True)

def load_image(image_file):
    img = Image.open(image_file)
    img.save("uploads/image.jpg")
    return img

page = st.sidebar.selectbox("Menu",options=["Train","Infrence"])

if page == "Train":

    type_class = st.radio("Select any Class first",options=["Thumb","Finger"])
    type_data = st.selectbox("Select Set",options=["Train","Test"])

    model = """

    ResNet9(
    - (norm15): BatchNorm2d(15, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
    - (norm30): BatchNorm2d(30, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
    - (norm60): BatchNorm2d(60, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
    - (norm120): BatchNorm2d(120, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
    - (norm200): BatchNorm2d(200, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
    - (norm300): BatchNorm2d(300, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
    - (norm360): BatchNorm2d(360, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
    - (norm512): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
    - (conv15): Conv2d(3, 15, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
    - (conv30): Conv2d(15, 30, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
    - (conv60): Conv2d(30, 60, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))
    - (res60): Conv2d(60, 60, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
    - (conv120a): Conv2d(60, 60, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
    - (conv200): Conv2d(60, 200, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
    - (conv200a): Conv2d(200, 200, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))
    - (res200): Conv2d(200, 200, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
    - (conv300): Conv2d(200, 200, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
    - (conv360): Conv2d(200, 360, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
    - (conv512): Conv2d(360, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
    - (pool): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
    - (avgpool): AvgPool2d(kernel_size=2, stride=2, padding=0)
    - (flat): Flatten(start_dim=1, end_dim=-1)
    - (linear): Linear(in_features=2048, out_features=2, bias=True)
    )

    """



    st.write("***")

    collect = st.button("Collect")
    train = False
    fing1 = True



    if collect:
        if type_class == "Thumb" and type_data == "Train":
            a +=1
            os.system("python utils/train_c1.py")
        elif type_class == "Finger" and type_data == "Train":
            a+=1
            os.system("python utils/train_c2.py")

        elif type_class == "Thumb" and type_data == "Test":
            a+=1
            os.system("python utils/test_c1.py")
        elif type_class == "Finger" and type_data == "Test":
            a+=1
            os.system("python utils/test_c2.py")

        else:
            st.info("Using Default Setting")
        

    data_dir1 = len(os.listdir("data/test/fing1"))
    data_dir2 = len(os.listdir("data/test/fing2"))
    data_dir3 = len(os.listdir("data/train/fing1"))
    data_dir4 = len(os.listdir("data/train/fing2"))
    print(data_dir1,data_dir2,data_dir3,data_dir4)

    if data_dir1 > 0 and data_dir2 > 0 and data_dir3 > 0 and data_dir4 > 0:
        st.balloons()
        train = st.button("Train")
        st.info("Data is Collected you can start Training now!")
    else:
        st.warning("Please Collect Data First.You Cannot Train Model Without Collecting Data")

    if train:
        st.info("Watch Console for Training Process!")
        os.system("python train_model.py")
        st.snow()
        st.info("Training Finished")

        with open('info.json') as f:
            data = json.load(f)

        cont = f"""
        Trained for 20 epochs.
        - Final Loss on Validation set: {round(data["val_loss"],3)}
        - Final Accuracy on Validation set: {round(data["val_acc"]*100,3)}%
        """

        st.write(cont)

        st.write(model)

        st.image("images/main.png",caption="Result Graph")

if page == "Infrence":
    st.markdown("Test Your Fingerprint")

    conts = os.listdir("weights")

    if len(conts)> 0 :
        st.info("Model is Trained You can Test Now!")
        img_file_buffer = st.camera_input("Take a picture")
        if img_file_buffer is not None:
            st.image(load_image(img_file_buffer))

            results = predict("uploads/image.jpg")

            if results[0][0] == "Thumb":
                st.balloons()
                st.info("Fingerprint Matched")
            else:
                st.snow()
                st.warning("Fingerprint Not Matched")

    
    else:
        st.info("Please Train Your Model Before Testing!")
        