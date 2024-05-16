import requests
from requests_ntlm import HttpNtlmAuth
import os
from dotenv import load_dotenv
import json
from datetime import datetime


def request_info():
    load_dotenv()
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    url = os.getenv("URL")
    domain = os.getenv("DOMAIN")
    return url, username, password, domain


def request_get_data(url, username, password, domain):
    headers = {'accept': 'application/json', 'content-type': 'application/json;odata=verbose;charset=utf-8'}
    response = requests.get(url, headers=headers, auth=HttpNtlmAuth(f'{domain}\\{username}', password), verify=False)
    response_text = response.text
    response_status = response.status_code
    return response_text, response_status


def create_file_menu(content):
    with open("file.txt", "w", encoding="utf-8") as file:
        file.write(content)


def parsing_dict(request_response_text):
    request_response_dict = json.loads(request_response_text)  # Словарь по всему ответу
    menu_list = request_response_dict.get("value", "Отсутствует файл меню")  # Лист состоящий из словарей
    if menu_list == "Отсутствует файл меню":
        print(menu_list)
        return
    else:
        menu_string = json.dumps(menu_list)  # Строка
        menu_dict = json.loads(menu_string)
        not_found_error = "Не найдено значение в меню"
        append_list = []

        for i in range(len(menu_dict)):
            title = menu_dict[i]["Category"].get("Title", not_found_error)
            name_title = menu_dict[i]["subcategory"].get("Title", not_found_error)
            dish = menu_dict[i].get("dish", not_found_error)
            composition = menu_dict[i].get("composition", not_found_error)
            proteins = menu_dict[i].get("proteins", not_found_error)
            fats = menu_dict[i].get("fats", not_found_error)
            carb = menu_dict[i].get("Carb", not_found_error)
            kcal = menu_dict[i].get("Kcal", not_found_error)
            weight = menu_dict[i].get("weight", not_found_error)
            price = menu_dict[i].get("price", not_found_error)
            time = datetime.now()
            if int(kcal) <= 300:
                vegan = True
            else:
                vegan = False

            dish_dict = {
                "Меню": str(title),
                "Тип": str(name_title),
                "Блюдо": str(dish),
                "Состав": str(composition),
                "Белки": int(proteins),
                "Жиры": int(fats),
                "Углеводы": int(carb),
                "Ккал": int(kcal),
                "Вес": str(weight),
                "Цена": int(price),
                "Диетическое": bool(vegan),
                "Время": str(time)
            }

            append_list.append(dish_dict)
    return append_list


def main():
    request_parameters = request_info()
    request_answer = request_get_data(*request_parameters)
    request_status = request_answer[1]
    request_response_text = request_answer[0]

    if request_status == 200:
        print(parsing_dict(request_response_text))
        return
    elif request_status == 401:
        print("Пользователь неавторизован\n\n")
        return
    else:
        print("Неизвестный статус-код\n\n")
        return


main()
