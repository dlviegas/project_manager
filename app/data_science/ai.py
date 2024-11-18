import google.generativeai as genai
from decouple import config
import re
import json
from app.utils.getDatabase import DatabaseConnection
from app.utils.getUserInfo import UsersConnection
from app.utils.createCards import Cards


class Chatbot:
    def __init__(self, user_id):
        genai.configure(api_key=config('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.user_id = user_id
        self.db = DatabaseConnection()


    def project_creator(self, text):
        prompt = f"Me ajude a criar um passo a passo para o seguinte problema: {text}. Para o passo a passo deetalhe em vários passos em alto nível. Coloque cada passo como um campo de json."

        response = self.model.generate_content(prompt)

        regex = re.findall("```json\n(.*?)```", response.text, re.DOTALL)[0]
        json_result = json.loads(regex)
        self.transform_card(json_result)


    def transform_card(self, json_result):
        inserter = []
        for j in json_result:
            inserter.append([j['title'],j['description'],self.user_id, 'To Do'])

        self.db.insert_many_todos(inserter)




