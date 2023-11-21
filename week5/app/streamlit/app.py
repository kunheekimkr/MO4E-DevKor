import streamlit as st
from datetime import datetime
import requests
import pandas as pd

page = st.sidebar.selectbox("DevKor!", ["REGISTER NEW MEMBER", "SEE MEMBERS"])

API_URL = "http://localhost:8000/member"


def update_page(response):
    st.balloons()
    st.markdown("# Thank you for information")
    st.json(response)

def error_page(response):
    st.error('Error', icon="🚨")
    st.markdown("## Please check your information")
    st.markdown("### Error Message")
    st.json(response)


def create_member(member_information):
    response = requests.post(API_URL, json=member_information)
    return response

if page == "REGISTER NEW MEMBER":
    st.title("Register Member")

    with st.form(key="member"):
        member_name: str = st.text_input("NAME", max_chars=15)
        member_birthDate = st.date_input("BirthDate", min_value= datetime(1900,1,1))
        member_role = st.radio("Role", ("admin", "student"))

        member_information = {"name": member_name, "birthDate": member_birthDate.strftime("%Y-%m-%dT00:00:00"), "role": member_role}
        submit_button = st.form_submit_button(label="Send")

    if submit_button:
        response = create_member(member_information)
        if response.status_code == 201:
            update_page(response.json()['data'])
        else:
            error_page(response.json())

if page == "SEE MEMBERS":
    st.title("Members")
    response = requests.get(API_URL)
    df = pd.DataFrame(response.json()['data'])
    if (df.empty):
        st.markdown("No Members... :(")
    else:
        df['birthDate'] = pd.to_datetime(df['birthDate']).dt.strftime('%Y-%m-%d')
        st.dataframe(df, hide_index=True)