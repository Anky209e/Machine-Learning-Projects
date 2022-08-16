import streamlit as st
import random
from pymongo import MongoClient

cluster = MongoClient('#---MOngoDB address Here---#')
db = cluster["learning_outcomes"]
my_page = st.sidebar.radio('Menu', ['Check Question', 'Reported Question','All Data'])

st.title("Learning outcome analysis")
st.write("***")
def provide_data(database_name):
    collection = db[database_name]
    data = collection.find().sort("_id")
    products = []
    for x in data:
        products.append((x["question"]))
    
    return products


def report_question(question):
    collection = db["reported"]
    query = {"question":question}
    collection.insert_one(query)
    print("Reported question")

def all_question(question):
    collection = db["all_questions"]
    query = {"question":question}
    collection.insert_one(query)
    print("Added question to database.")

def inputs():

    question = st.text_input(label="Enter Question")
    question = str(question)
    school = st.selectbox(label="Student's Education Level",options=['High-School','University'])
    if school == "High-School":
        school = 0
    else:
        school = 1
    
    gender = st.selectbox(label="Gender",options=['Male','Female'])
    if gender == "Male":
        gender = 0
    else:
        gender = 1
    
    first_col1,first_col2 = st.columns(2)
    st.write("***")

    age = first_col1.number_input(label="Age",step=2,min_value=5,max_value=103)
    age = int(age)

    address = first_col2.selectbox(label="Living Area",options=['Urban','Rural'])
    if address == "Urban":
        address = 0
    else:
        address = 1
    
    famsize = st.selectbox(label="Famliy Size",options=['Less than 3','Greater than 3'])
    if famsize == "Less than 3":
        famsize = 0
    else:
        famsize = 1

    Pstatus = st.selectbox(label="Parent living together",options=['Yes','No'])
    if Pstatus == "Yes":
        Pstatus = 0
    else:
        Pstatus = 1

    st.write("***")
    col1,col2 = st.columns(2)
    Medu = col1.selectbox(label="Mother's Education Level",options=['None','Primary Education','5th to 9th Grade','Secondary Education','Higher Education'])
    if Medu == "None":
        Medu = 0
    elif Medu == "Primary Education":
        Medu = 1
    elif Medu == "5th to 9th Grade":
        Medu = 2
    elif Medu == "Secondary Education":
        Medu = 3
    else:
        Medu = 4
    
    Fedu = col2.selectbox(label="Father's Education Level",options=['None','Primary Education','5th to 9th Grade','Secondary Education','Higher Education'])
    if Fedu == "None":
        Fedu = 0
    elif Fedu == "Primary Education":
        Fedu = 1
    elif Fedu == "5th to 9th Grade":
        Fedu = 2
    elif Fedu == "Secondary Education":
        Fedu = 3
    else:
        Fedu = 4

    Mjob = random.randint(0, 4)
    Fjob = random.randint(0, 4)
    reason = random.randint(0, 4)
    guardian = st.selectbox(label="Gaurdian",options=['Mother','Father','Other'])
    if guardian == "Mother":
        guardian = 0
    elif guardian == "Father":
        guardian = 1
    else:
        guardian = 2

    studytime = st.selectbox(label="Study Time",options=['Less than 2hr','2-5hr','5-10hr','Greater than 10hr'])
    if studytime == "Less than 2hr":
        studytime = 1
    elif studytime == "2-5hr":
        studytime = 2
    elif studytime == "5-10hr":
        studytime = 3
    else:
        studytime = 4
    
    freetime = st.select_slider(label="Free time after school (hr)",options=[1,2,3,4,5])
    freetime = int(freetime)

    st.write("***")
    traveltime = st.selectbox(label="Travel Time",options=['Less Than 15 min','15-30min','30min-1hr','Greater than 1hr'])
    if traveltime == "Less Than 15 min":
        traveltime = 1
    elif traveltime == "15-30min":
        traveltime = 2
    elif traveltime == "30min-1hr":
        traveltime = 3
    else:
        traveltime = 4
    
    third_col1,third_col2 = st.columns(2)
    failures = third_col1.select_slider(label="Number of failures",options=[1,2,3,4])
    failures = int(failures)
    absences = third_col2.select_slider(label="Range of absences in school",options=[1,2,3,4,5])
    absences = int(absences)
    schoolsup = random.randint(0, 1)
    famsup = 0 if schoolsup==1 else 1
    paid = col1.selectbox(label="Taking extra classes",options=["Yes","No"])
    if paid == "Yes":
        paid = 1
    else:
        paid = 0

    activities = col2.selectbox(label="Involved in sports activities?",options=['Yes','No'])
    if activities == "Yes":
        activities = 1
    else:
        activities = 0

    nursery = random.randint(0, 1)
    othcol1,othcol2 = st.columns(2)
    higher = othcol1.selectbox(label="Plan to take higher education",options=['Yes','No'])
    if higher == "Yes":
        higher = 1
    else:
        higher = 0

    internet = othcol2.selectbox(label="Internet access",options=['Yes','No'])
    if internet == "Yes":
        internet = 1
    else:
        internet = 0
    
    romantic = random.randint(0, 1)
    famrel = random.randint(1, 5)
    second_col1,second_col2 = st.columns(2)

    goout = second_col1.select_slider(label="Time spend with friends (hr)",options=[1,2,3,4,5])
    goout = int(goout)
    Dalc = 0
    health = second_col2.select_slider(label="Current health status (good to bad)",options=[1,2,3,4,5])
    health = int(health)
    Walc = st.selectbox(label="Habit of alcohol consumption",options=['Yes','No'])
    if Walc == "Yes":
        Walc = 1
    else:
        Walc = 0

    all_data_dic = {"school":school,"gender":gender,"age":age,"address":address,"famsize":famsize,"Pstatus":Pstatus,"Medu":Medu,"Fedu":Fedu,"Mjob":Mjob,"Fjob":Fjob,"reason":reason,"guardian":guardian,"studytime":studytime,"traveltime":traveltime,"failures":failures,"schoolsup":schoolsup,"famsup":famsup,"paid":paid,"activities":activities,"nursery":nursery,"higher":higher,"internet":internet,"romantic":romantic,"famrel":famrel,"freetime":freetime,"goout":goout,"Dalc":Dalc,"Walc":Walc,"health":health,"absences":absences}
    all_data_arr = [school, gender, age, address, famsize, Pstatus, Medu, Fedu, Mjob, Fjob, reason, guardian, studytime, traveltime, failures, schoolsup, famsup, paid, activities, nursery, higher, internet, romantic, famrel, freetime, goout, Dalc, Walc, health, absences]

    return question,all_data_dic,all_data_arr


if my_page == "Check Question":

    question,dic,arr = inputs()
    arr = [arr]
    a = st.button(label="Submit")
    from predict import take_from_web
    if a :
        if question:
            all_question(question)
            outputs,msg,acc=take_from_web(question,arr)
            if msg == "Yes":
                st.write("## The student can solve the question.")
                
            else:
                report_question(question)
                st.write("## The student can not solve the question.")
                st.warning("Reporting question to admin.")
            st.write("### Parameters of question:")
            for out in outputs:
                st.write(out)
        else:
            st.warning(" Please enter a question.")
elif my_page == "Reported Question":
    st.title("Reported Questions")
    r_questions = provide_data("reported")
    for i in r_questions:
        st.write(i)
    

elif my_page == "All Data":
    st.title("All Data")
    r_questions = provide_data("all_questions")
    for i in r_questions:
        st.write(i)



