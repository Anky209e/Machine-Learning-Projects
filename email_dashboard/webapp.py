import streamlit as st
from email_utils import is_spam,get_email_type
st.title("Email Sorter")

email = st.text_area(label="Enter Email Here")

a = st.button(label="Check")

if a:
    spam = is_spam(email)
    mail_type = get_email_type(email)

    st.write(spam)
    st.write(mail_type)
