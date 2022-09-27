import streamlit as st
from email_utils import is_spam,get_email_type
import imaplib
import email
import json

st.title("Email Dashboard")

with open('creds.json','r') as json_file:
    print("Loading Credentials..")
    data = json.load(json_file)  

try:
    #credentials
    username =data["mail"]
    #generated app password
    app_password= data["auth_key"]
except:
    print("Credentials Error")

gmail_host= 'imap.gmail.com'

#set connection
mail = imaplib.IMAP4_SSL(gmail_host)

#login
mail.login(username, app_password)

#select inbox
mail.select("INBOX")

query = st.text_input(label="Email Query")
num_emails = int(st.number_input(label="Number of Emails to Check",min_value=0))
proceed = st.button(label="Check")


def get_mails(query,total_mails):
    state, selected_mails = mail.search(None, f'(FROM "{query}")')
    mails_present = selected_mails[0].split()

    if total_mails > len(mails_present):
        total_mails = 1
    st.write(f"> {len(mails_present)} Emails related to {query} found.")
    for i in range(0,total_mails):
        state, data = mail.fetch(mails_present[i] , '(RFC822)')
        state, bytes_data = data[0]
        email_message = email.message_from_bytes(bytes_data)
        subject = email_message["subject"]
        spam_ = is_spam(subject)
        spam_cont = "Its not a Spam Email"
        if spam_:
            spam_cont = "It is a Spam Email"
        type_email  = get_email_type(subject)
        to = email_message["to"]
        from_ = email_message["from"]
        date_ = email_message["date"]
        st.write("***")
        subject_cont = f"## Subject: {subject}"
        to_cont = f"#### To: {to}"
        from_cont = f"#### From: {from_}"
        date_cont = f"**{date_}**"
        st.markdown(subject_cont)
        st.markdown(to_cont)
        st.markdown(from_cont)
        st.markdown(date_cont)
        st.markdown(f"Status: {spam_cont}")
        st.markdown(f"Type: {type_email}")
        

if proceed:
    get_mails(query,num_emails)

    
