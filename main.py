import google.generativeai as genai
from decouple import config
import re
import json

genai.configure(api_key=config('GEMINI_API_KEY'))
def print_hi():
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Me ajude a criar um passo a passo para o seguinte problema: Tenho que criar um webcrawler para um site, desenvolver um banco de dados para colocar as informações desse site e criar um dashboard com as informações que eu coletei. Para o passo a passo deetalhe em vários passos em alto nível. Coloque cada passo como um campo de json.")
    regex = re.findall("```json\n(.*?)```", response.text, re.DOTALL)[0]
    json_result = json.loads(regex)
    return response.text

def dummy(text):
    regex = re.findall("```json\n(.*?)```", text, re.DOTALL)[0]

    return regex.group(1)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    result = print_hi()

    result_json = dummy(result)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
