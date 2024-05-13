import requests 123
from requests_ntlm import HttpNtlmAuth
import xmltodict
import json
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
    response = requests.get(
        url, auth=HttpNtlmAuth(f"{domain}\\{username}", password), verify=False
    )
    response_text = response.text
    response_status = response.status_code
    return response_text, response_status


def convert_xml(response_text):
    dict_data = xmltodict.parse(response_text)
    json_data = json.dumps(dict_data)
    return json_data


def convertation_menu(json_data):
    json_data = json.loads(json_data)
    json_data = json_data["feed"]["entry"]
    append_list = []

    for entry in json_data:
        title = entry["link"][1]["m:inline"]["entry"]["content"]["m:properties"]["d:Title"]
        name_title = entry["link"][2]["m:inline"]["entry"]["content"]["m:properties"]["d:Title"]
        dish = entry["content"]["m:properties"]["d:dish"]
        composition = entry["content"]["m:properties"]["d:composition"]
        proteins = entry["content"]["m:properties"]["d:proteins"]
        fats = entry["content"]["m:properties"]["d:fats"]
        carb = entry["content"]["m:properties"]["d:Carb"]
        kcal = entry["content"]["m:properties"]["d:Kcal"]
        weight = entry["content"]["m:properties"]["d:weight"]
        price = entry["content"]["m:properties"]["d:price"]["#text"]

        dish_json = {
            "Меню": title,
            "Тип": name_title,
            "Блюдо": dish,
            "Состав": composition,
            "Белки": proteins,
            "Жиры": fats,
            "Углеводы": carb,
            "Ккал": kcal,
            "Вес": weight,
            "Цена": price,
        }

        append_list.append(dish_json)

    append_list = json.dumps(append_list, ensure_ascii=False)
    return append_list


def create_file_menu(content):
    with open("file.txt", "w", encoding="utf-8") as file:
        file.write(content)


def main():
    request_parametrs = init_user()
    response_menu = request_get_menu(*request_parametrs)

    if response_menu[1] == 200:
        json_data = convert_xml(response_menu[0])
        append_list = convertation_menu(json_data)
        create_file_menu(append_list)
        print("\n\nФайл подготовлен\n\n")
        return
    elif response_menu[1] == 401:
        create_file_menu("Не авторизован")
        print("\n\nФайл подготовлен, пользователь неавторизован\n\n")
        return
    else:
        create_file_menu(f"Неизвестный код: {response_menu[1]}")
        print("\n\nФайл подготовлен, но неизвестный статус-код\n\n")
        return


main()
