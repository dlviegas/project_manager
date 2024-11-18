import streamlit as st
import datetime
import hmac
from sqlalchemy import select, table, MetaData, sql
from app.utils.getDatabase import DatabaseConnection

database = DatabaseConnection()

class UsersConnection:
    def __init__(self):
        self.conn = database.init_connection()
    def user_email_exists(self, email):

        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM projectmanager.user where user = '{email}'")
        user_info = cur.fetchall()
        cur.close()
        if user_info:
            st.error('Email is already registered')
            return True
        else:
            return False

    def insert_user(self, user):
        cur = self.conn.cursor()
        cur.execute(f"INSERT INTO projectmanager.user (username, password, email, modified_at)"
                    f"                      values ('{user['name']}', '{user['password']}', '{user['email']}', current_timestamp)")
        self.conn.commit()

        cur.close()