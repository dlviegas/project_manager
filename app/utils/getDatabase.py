
import streamlit as st
import datetime
import psycopg2
from bson.objectid import ObjectId
from decouple import config
import os


class DatabaseConnection:
    def __init__(self):
        self.database = 'test.db'
        self.db_user = config('DB_USER')
        self.db_pwd = config('DB_PASSWORD')
        self.db_host = config('DB_HOST')
        self.db_port = config('DB_PORT')
        self.db_name = config('DB_NAME')
    
    # @st.cache_resource
    def init_connection(self):
        return psycopg2.connect(f"dbname={self.db_name} user={self.db_user} password={self.db_pwd} host={self.db_host} port={self.db_port}")


    def get_data(self, user_id):
        conn = self.init_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT title, description, id, user_id, status from projectmanager.todo where user_id={user_id}")
        cards = cur.fetchall()
        if cards:
            items = [{
                        'title': row[0],
                        'description': row[1],
                        'card_id': row[2],
                        'user_id': row[3],
                        'status': row[4]
                      } for row in cards]

        else:
            items = []
        cur.close()
        conn.close()
        return items

    def insert_todo(self, todo):
        conn = self.init_connection()
        cur = conn.cursor()

        cur.execute(f"""INSERT INTO projectmanager.todo
                            (title, description, user_id, status)
                        VALUES 
                            ('{todo['title']}', '{todo['description']}', '{todo['user_id']}', '{todo['status']}')""")

        conn.commit()
        cur.close()
        conn.close()

    def insert_many_todos(self, todo:list):
        conn = self.init_connection()
        cur = conn.cursor()

        cur.executemany(f"""INSERT INTO projectmanager.todo
                                    (title, description, user_id, status)
                                VALUES 
                                    (%s, %s, %s, %s)""", todo)
        conn.commit()
        cur.close()
        conn.close()

    def update_todo(self, id, old_value, new_value):
        conn = self.init_connection()
        cur = conn.cursor()

        cur.execute(f"""
                    UPDATE projectmanager.todo
                    SET {old_value} = '{new_value}'
                    WHERE id = {id}
                    """)

        conn.commit()
        cur.close()
        conn.close()
        st.rerun()
    
    def count_tasks(self, filter, id):
        conn = self.init_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT count(1) FROM projectmanager.todo WHERE user_id = id")
        count = cur.fetchall()[0][0]
        if count > 1:
            return f":grey[{count} tasks]"
        elif count == 1:
            return f":grey[{count} task]"
        else:
            return ""
    
    def delete_task(self, id):
        conn = self.init_connection()
        cur = conn.cursor()
        cur.execute(f"DELETE FROM projectmanager.todo WHERE id = {id}")
        conn.commit()
        cur.close()
        conn.close()
        st.rerun()
