import streamlit as st
from fraud_detect import predict_value
import torch.nn as nn
from aws_ses import send_mail
st.title("Sikeee")


class LogisticRegression(nn.Module):
    def __init__(self,no_of_features):
        super(LogisticRegression, self).__init__()
        self.linear1 = nn.Linear(no_of_features,10)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(10,1)
        self.sigmoid = nn.Sigmoid()
        

    def forward(self, targets_train ):
        out = self.linear1(targets_train)
        out  = self.relu(out)
        out = self.linear2(out)
        out = self.sigmoid(out)
        
        return out

model = LogisticRegression(no_of_features=4)

total_amount = st.number_input("Total Amount")
old_balance = st.number_input("Old Amout")

new_balance = st.number_input("New Balance")
final_old = st.number_input("Final Amount")

a,b= st.columns(2)
check = a.button("Check for fraud")
send = b.button("Alert Using Email")

if check:
    ins = [total_amount,old_balance,new_balance,final_old]
    result = predict_value(ins)

    st.write(result)

if send:
    ins = [total_amount,old_balance,new_balance,final_old]
    result = predict_value(ins)
    print("Sending...")
    sender_address = "warrior.prince652002@gmail.com"
    rec_add = "nasaankit01@gmail.com"

    subject = result

    cont_text = "AWS EMail"
    cont_html = f"""

    <h1>Hey! We just Scanned for Fraud Detection in Database</h1>
    <h3>Status:{result}</h3>
    <p>This message is sent by AWS SES,Please do not reply.</p>
    
    """

    send_mail(sender_address,rec_add,subject,cont_text,cont_html)
