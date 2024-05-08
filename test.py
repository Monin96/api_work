import requests
from requests_ntlm import HttpNtlmAuth
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
    response_text = requests.get(url, auth=HttpNtlmAuth(f'{domain}\\{username}', password), verify=False)
    return response_text.status_code, response_text.text

def main():
    request_info = init_user()
    result = request_get_menu(*request_info)
    print(result)

main()
