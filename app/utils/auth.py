import streamlit as st
from utils.getDatabase import DatabaseConnection
from utils.getUserInfo import UsersConnection
import argon2

database = DatabaseConnection()
users = UsersConnection()

class Auth():
    def __init__(self):
        self.conn = database.init_connection()

    def form_selection(self):
        st.title("Log in or create an account")
        login, signup = st.columns(2)
        with login:
            login_butt = st.button("Log In", use_container_width=True)
            if login_butt:
                st.session_state.form = 'login_form'
                st.rerun()
        with signup:
            sign_up = st.button("Sign Up", use_container_width=True)
            if sign_up:
                st.session_state.form = 'signup_form'
                st.rerun()

    def hashed_password(self,password):
        argon2Hasher = argon2.PasswordHasher(
            time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16)
        hash = argon2Hasher.hash(password)
        return hash

    def verify_password(self,password, hashed):
        argon2Hasher = argon2.PasswordHasher(
            time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16)
        try:
            verified = argon2Hasher.verify(hashed, password)
            st.write(verified)
            return verified
        except:
            return False

    def login(self, email, password):
        cur = self.conn.cursor()
        cur.execute(f"SELECT id, email, password, username FROM projectmanager.user where email='{email}'")
        user_info = cur.fetchall()

        if user_info:
            user_info = {'id': user_info[0][0], 'email': user_info[0][1], 'password': user_info[0][2], 'name': user_info[0][3]}
            verify = self.verify_password(password, user_info['password'])
            if verify:
                st.session_state['user'] = True
                st.session_state['user_id'] = user_info['id']
                st.session_state['username'] = user_info['name']
                del user_info['password']
                st.rerun()
            elif verify == False:
                st.session_state['user'] = False
                st.error("😕 Incorrect password")
        else:
            st.session_state['user'] = False
            st.error("😕 User not known")
        return st.session_state['user']

    def logout(self):
        logout = st.sidebar.button(label='Log Out')
        if logout:
            st.session_state.username = ''
            st.session_state.user = ''
            st.session_state.form = ''
            st.rerun()

    def login_form(self):
        with st.form(key='login_user', clear_on_submit=True):
            st.title("Hey there! Welcome back!")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submit_user_login = st.form_submit_button("Log In",use_container_width=True)
            if submit_user_login:
                user_id = self.login(email, password)

    def signup_form(self):
        with st.form(key='create_user', clear_on_submit=True):
            st.title("Hey there! Welcome!")
            name = st.text_input("Name", key="create_name")
            email = st.text_input("Email", key="create_email")
            password = st.text_input("Password", type="password", key="create_password")
            submit_user = st.form_submit_button("Sign Up",use_container_width=True)
            if submit_user:
                if '' in [name, email, password]:
                    st.error("All fields are required, please fill out the form!")
                else:
                    test_email = users.user_email_exists(email)
                    if test_email == False:
                        hashed_password = self.hashed_password(password)
                        user = {
                            "name": name,
                            "email": email.lower(),
                            "password": hashed_password,
                        }
                        user_id = users.insert_user(user)
                        st.success('You have successfully registered!')
                        st.success(f"You are logged in as {name.title()}")
                        user_id = self.login(email, password)

