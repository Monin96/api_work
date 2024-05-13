import requests
from requests_ntlm import HttpNtlmAuth
import json
import xmltodict
import os
from dotenv import load_dotenv

def init_user():
    load_dotenv()
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    url = os.getenv("URL")
    domain = os.getenv("DOMAIN")
    return url, username, password, domain


def request_get_menu(url, username, password, domain): 
    response = requests.get(url, auth=HttpNtlmAuth(f'{domain}\\{username}', password), verify=False)# Заменить на один запрос
    response_text = response.text
    response_status = response.status_code
    return response_text, response_status
 
         
def convert_xml(response_text): 
    dict_data = xmltodict.parse(response_text[0]) 
    json_data = json.dumps(dict_data)
    return json_data 

def dict_get(json_data): 
    json_data = json.loads(json_data) 
    i = json_data.get("d:dish")
    print(i)
    return 

def main():
    request_parametrs = init_user()
    response_menu = request_get_menu(*request_parametrs)
    json_data = convert_xml(response_menu)
    dict_get(json_data)
    return

main()