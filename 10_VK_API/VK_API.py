from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import requests
import json
import datetime
import time
import random

users_list = []

now = int(time.mktime(datetime.datetime.now().timetuple()))


class VKAPIAuth:
    ACCESS_TOKEN = ""

    def __init__(self, login=None, password=None):
        self.AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
        self.oath_params = {
            'client_id': 3116505,
            'scope': "users,friends",
            'display': 'page',
            'response_type': 'token',
            'v': '5.120',
        }
        self.ACCESS_TOKEN = ""
        self.login = login
        self.password = password
        with open("access_token.json") as f:
            access_key_dic = json.load(f)
        if access_key_dic["expires_in"] > now:
            self.ACCESS_TOKEN = access_key_dic["access_token"]
            self.expires_in = access_key_dic["expires_in"]
            print(f"\nТокен пользователя действителен в течение {int((self.expires_in - now) / 3600)} ч.\n")
        else:
            self.get_token = self.authorize()
            if "access_token" in self.get_token:
                self.ACCESS_TOKEN = self.get_token.split("access_token=")[1].split("&")[0]
                self.expires_in = int(int(self.get_token.split("expires_in=")[1].split("&")[0]) / 3600)
                access_key_dic["access_token"] = self.ACCESS_TOKEN
                access_key_dic["granted"] = now
                access_key_dic["expires_in"] = now + self.expires_in * 3600
                with open("access_token.json", "w", encoding="utf-8") as f:
                    json.dump(access_key_dic, f)
                print(f"\nТокен пользователя выдан со сроком действия {self.expires_in} ч.\n")
            else:
                print("\nЧто-то пошло не так.")
                print(self.get_token)

    def authorize(self):
        print("\nПолучаем токен пользователя")
        # собираем ссылку для авторизации
        url = requests.get(self.AUTHORIZE_URL, params=self.oath_params).url

        # параметры запуска Selenium
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(port=443, chrome_options=options)

        # процесс авторизации
        driver.get(url)
        login = driver.find_element_by_xpath('//*[@id="login_submit"]/div/div/input[6]')
        ActionChains(driver).move_to_element(login).click().perform()

        login.send_keys(self.login)

        password = driver.find_element_by_xpath(
            '//*[@id="login_submit"]/div/div/input[7]')
        ActionChains(driver).move_to_element(password).click().perform()

        password.send_keys(self.password)

        enter = driver.find_element_by_xpath(
            '//*[@id="install_allow"]')
        ActionChains(driver).move_to_element(enter).click().perform()

        # получаем ключ доступа из новой ссылки
        url = driver.current_url

        if "access_token" not in url:
            enter = driver.find_element_by_xpath(
                '//*[@id="oauth_wrap_content"]/div[3]/div/div[1]/button[1]')
            ActionChains(driver).move_to_element(enter).click().perform()

        url = driver.current_url
        page = driver.page_source
        driver.close()
        driver.quit()

        if "access_token" in url:
            return url
        else:
            return page


class User:
    def __init__(self, _id: int):
        self.id = _id
        self.URL = 'https://vk.com/id'
        self.API_URL = 'https://api.vk.com/method/'
        self.params = {
            'access_token': auth.ACCESS_TOKEN,
            # 'access_token': '18d41ffaaa5261e8eaf2bdc9d005498b9f61fe7fae75a6f9798caa79513202597f4c1ea912f6ce7c835bc',
            'v': '5.120'
        }
        self.methods = {
            'users': {'get': 'users.get?'},
            'friends': {'get': 'friends.get?',
                        'areFriends': 'friends.areFriends?',
                        'getMutual': 'friends.getMutual?',
                        },

        }

        if not users_list:
            users_list.append(self)
        else:
            id_list = []
            for _user in users_list:
                id_list.append(_user.id)
            id_list = list(set(id_list))
            if self.id not in id_list:
                users_list.append(self)

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return self.URL + str(self.id)

    def __and__(self, other):
        return self.mutual_friends(other.id)

    def user(self, ids=None):
        if ids:
            user_params = {"user_ids": ids}
        else:
            user_params = {"user_ids": self.id}
        user_params.update(self.params)
        if ids:
            if 0 < len(ids) <= 10:
                user_id = requests.get(self.API_URL + self.methods['users']['get'],
                                       params=user_params).json()['response'][0]
                return user_id
            else:
                user_ids = requests.get(self.API_URL + self.methods['users']['get'],
                                        params=user_params).json()['response']
                return user_ids
        else:
            user_id = requests.get(self.API_URL + self.methods['users']['get'],
                                   params=user_params).json()['response'][0]

            user_name = user_id['first_name'] + ' ' + user_id['last_name']
            return user_name

    def mutual_friends(self, friend):
        mutual_friends_params = {
            'source_uid': self.id,
            'target_uid': friend,
        }
        mutual_friends_params.update(self.params)
        ids_list = requests.get(user1.API_URL + self.methods['friends']['getMutual'],
                                params=mutual_friends_params).json()['response']

        ids_str = ''
        friends_list = [User(_id) for _id in ids_list]
        for _id in ids_list:
            if not ids_str:
                ids_str = ids_str + str(_id)
            else:
                ids_str = ids_str + "," + str(_id)
        mut_friends_names = self.user(ids_str)
        mut_friends_names_list = []
        for _name in mut_friends_names:
            name = _name['first_name'] + ' ' + _name['last_name']
            mut_friends_names_list.append(name)
        print(f'{self.user()} и {User(friend).user()} имеют {len(mut_friends_names_list)} общих друзей:')
        print(*mut_friends_names_list, sep=", ")
        print(f'Все они являются сущностями и хранятся в списке "users_list" '
              f'(также как {user0.user()} и {user1.user()}).')
        print(f'А вот список ссылок на их профили. ')
        print(*friends_list, sep="\t")
        print()


def check_token():
    with open("access_token.json") as file:
        access_key_dict = json.load(file)
    if access_key_dict['expires_in'] <= now:
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Для работы программы необходимо ввести данные для авторизации в Вашей учётной записи ВКонтакте.\n")
        print("Данные запрашиваются только в случае необходимости получения валидного ключа доступа от ВКонтакте.\n")
        print("Вводимые учётные данные нигде не сохраняются, не передаются никуда, кроме сервиса ВКонтакте и "
              "используются только во время работы программы.")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!")
        auth_ = VKAPIAuth(login=input("\nВведите логин (номер телефона/e-mail): "), password=input("Введите пароль: "))
        return auth_
    else:
        auth_ = VKAPIAuth()
        return auth_


def intro():
    print(f"Сейчас в списке сущностей класса USER имеются следующие id: {users_list}.\n")
    print(f"Первый в списке у нас {user0.user()}.")
    print(user0, '\n')

    print(f"Второй - конечно же {user1.user()}. Куда ж без него...")
    print(user1, '\n')
    time.sleep(1)
    print("Давайте посмотрим, есть ли у них общие друзья?")
    user0 & user1
    number = random.randint(2, len(users_list) - 1)
    print(f"И сейчас в списке сущностей класса USER уже {len(users_list)} id: {users_list}.\n")
    time.sleep(1)
    print(f"Давайте узнаем, кто в нашем списке значится, например, под номером {number+1}?")
    print(f"И это - {users_list[number].user()}, {users_list[number]}!\n")

    print("Отлично!\nТеперь вы можете сами вводить команды.")
    print("Не забывайте заглядывать в users_list ради интереса.\n")


def give_command():
    """===================================
Вы можете найти общих друзей у любых пользователей, находящихся в списке пользователей "users_list".
В функциях, требующих указания пользователя(-ей), необходимо указать индекс в списке пользователей "users_list".
Так как отсчёт индекса проще всего вести с единицы, а не с нуля, то так и считайте.

Для вызова функций введите следующие команды (без кавычек):
- "mut" для поиска общих друзей,
- "name" для вывода имени пользователя,
- "link" для lst(),
- "all" для add(),
- "len" для вывода количества уже известных нам пользователей,

Для завершения программы введите "exit".
==================================="""

    def mutual():
        return users_list[int(input("Укажите пользователя 1: "))-1] & \
               users_list[int(input("Укажите пользователя 2: "))-1]

    def print_user_name():
        # return print(users_list[int(input("Укажите пользователя: "))-1].user())
        return users_list[int(input("Укажите пользователя: ")) - 1].user()

    def print_user_link():
        # return print(users_list[int(input("Укажите пользователя: ")) - 1])
        return users_list[int(input("Укажите пользователя: "))-1]

    def print_all_users():
        # return print(users_list)
        return users_list

    def print_len_users():
        # return print(len(users_list))
        return len(users_list)

    user_commands = {
        "mut": mutual,
        "name": print_user_name,
        "link": print_user_link,
        "all": print_all_users,
        "len": print_len_users,
        "exit": None
    }

    command = None
    print(give_command.__doc__)
    print()

    while command != "exit":
        command = None
        while command not in user_commands.keys():
            command = input("Введите команду: ")
        else:
            if command == "exit":
                print()
                print("Работа программы завершена")
                break
            else:
                print(user_commands[command]())
                print()


if __name__ == '__main__':
    auth = check_token()
    user0 = User(273251945)
    user1 = User(271138000)
    intro()
    give_command()
