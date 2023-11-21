import streamlit as st
from datetime import datetime
import requests
import pandas as pd
API_URL = "http://app-fastapi-server-1:8000/member"


def create_member(member_information):
    response = requests.post(API_URL, json=member_information)
    return response

def get_members():
    response = requests.get(API_URL)
    return response

def get_member(id):
    response = requests.get(API_URL+"/"+id)
    return response

def update_member(id, member_information):
    response = requests.put(API_URL+"/"+id, json=member_information)
    return response

def delete_member(id):
    response = requests.delete(API_URL+"/"+id)
    return response

def success_page(data):
    st.balloons()
    st.markdown("# Thank you for information")
    st.json(data)

def error_page(response):
    st.error('Error', icon="🚨")
    st.markdown("## Please check your information")
    st.markdown("### Error Message")
    st.json(response)

def register_page():
    st.title("Register Member")

    with st.form(key="member"):
        member_name: str = st.text_input("NAME", max_chars=15)
        member_birthDate = st.date_input("BirthDate", min_value= datetime(1900,1,1))
        member_role = st.radio("Role", ("admin", "student"))

        member_information = {"name": member_name, "birthDate": member_birthDate.strftime("%Y-%m-%dT00:00:00"), "role": member_role}
        submit_button = st.form_submit_button(label="Register!")

    if submit_button:
        response = create_member(member_information)
        if response.status_code == 201:
            success_page(response.json()['data'])
        else:
            error_page(response.json())

def list_members_page():
    st.title("Members")
    response = get_members()
    df = pd.DataFrame(response.json()['data'])
    if (df.empty):
        st.markdown("No Members... :(")
    else:
        df['birthDate'] = pd.to_datetime(df['birthDate']).dt.strftime('%Y-%m-%d')
        st.dataframe(df, hide_index=True)

def manage_members_page():
    if (len(user_list) == 0):
        st.title("Manage Members")
        st.markdown("No Members... :(")
        st.stop()
    member = st.sidebar.selectbox("Member",  [user[1] for user in user_list])
    id = [user[0] for user in user_list if user[1] == member][0]
    response = get_member(id)
    member_information = response.json()['data']
    st.title("Manage Member: "+ member_information['name'])
    with st.form(key="member"):
        member_name: str = st.text_input("NAME", value=member_information['name'], max_chars=15)
        member_birthDate = st.date_input("BirthDate", value=datetime.strptime(member_information['birthDate'], '%Y-%m-%dT00:00:00'), min_value= datetime(1900,1,1))
        member_role = st.radio("Role", ("admin", "student"), index=0 if member_information['role'] == "admin" else 1)
        member_information = {"name": member_name, "birthDate": member_birthDate.strftime("%Y-%m-%dT00:00:00"), "role": member_role}
        st.markdown(
        """
        <style>
        div[data-testid="column"]:nth-of-type(2)
        {
            text-align: end;
        } 
        </style>
        """,unsafe_allow_html=True
        )
        col1, col2 = st.columns([1,1])
        with col1:
            submit_button = st.form_submit_button(label="Update")
        with col2:
            delete_button = st.form_submit_button(label="Delete", type="primary")

    if submit_button:
        response = update_member(id, member_information)
        if response.status_code == 200:
            success_page(response.json()['data'])
        else:
            error_page(response.json())

    if delete_button:
        response = delete_member(id)
        if response.status_code == 200:
            st.success("Deleted!", icon="🗑️")
            st.experimental_rerun()
        else:
            error_page(response.json())


response = get_members()
user_list = response.json()['data']
user_list = [(item["id"], item["name"]) for item in response.json()['data']]

page = st.sidebar.selectbox("DevKor!", ["REGISTER NEW MEMBER", "SEE MEMBERS", "MANAGE MEMBERS"])


if page == "REGISTER NEW MEMBER":
    register_page()

if page == "SEE MEMBERS":
    list_members_page()

if page == "MANAGE MEMBERS":
    manage_members_page() 