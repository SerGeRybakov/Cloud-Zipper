""" Модуль определяет порядок авторизации и дальнейшей работы с сервисом vk.com"""
import json
import os
import time
from datetime import datetime

import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from tqdm import tqdm

users_list = []

now = int(time.mktime(datetime.now().timetuple()))


class VKAPIAuth:
    """ Класс предназначен для авторизации на сервисе vk.com"""
    ACCESS_TOKEN = ""

    def __init__(self, login=None, password=None):
        self.AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
        self.oath_params = {
            'client_id': 3116505,
            'scope': "users,friends,photos",
            'display': 'page',
            'response_type': 'token',
            'v': '5.120',
        }

        self.login = login
        self.password = password
        with open("access_token.json") as file:
            access_key_dic = json.load(file)
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
                with open("access_token.json", "w", encoding="utf-8") as file:
                    json.dump(access_key_dic, file)
                print(f"\nТокен пользователя выдан со сроком действия {self.expires_in} ч.\n")
            else:
                print("\nЧто-то пошло не так.")
                print(self.get_token)

    def authorize(self):
        """Метод получает токен пользователя"""
        print("\nПолучаем токен пользователя")
        # собираем ссылку для авторизации
        url = requests.get(self.AUTHORIZE_URL, params=self.oath_params).url

        # параметры запуска Selenium
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(port=443, chrome_options=options)

        # процесс авторизации
        driver.get(url)
        login = driver.find_element(By.XPATH, '//*[@id="login_submit"]/div/div/input[6]')
        ActionChains(driver).move_to_element(login).click().perform()

        login.send_keys(self.login)

        password = driver.find_element(By.XPATH, '//*[@id="login_submit"]/div/div/input[7]')
        ActionChains(driver).move_to_element(password).click().perform()

        password.send_keys(self.password)

        enter = driver.find_element(By.XPATH, '//*[@id="install_allow"]')
        ActionChains(driver).move_to_element(enter).click().perform()

        # получаем ключ доступа из новой ссылки
        url = driver.current_url

        if "access_token" not in url:
            enter = driver.find_element(By.XPATH, '//*[@id="oauth_wrap_content"]/div[3]/div/div[1]/button[1]')
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
    """Класс определяет методы работы с сервисами vk.com"""

    def __init__(self, _id: int):
        self.id = _id
        self.URL = 'https://vk.com/id'
        self.API_URL = 'https://api.vk.com/method/'
        self.params = {
            'access_token': VKAPIAuth.ACCESS_TOKEN,
            'v': '5.120'
        }
        self.methods = {
            'users': {'get': 'users.get?'},
            'friends': {'get': 'friends.get?',
                        'areFriends': 'friends.areFriends?',
                        'getMutual': 'friends.getMutual?',
                        },
            'photos': {'get': 'photos.get?',
                       'get_albums': 'photos.getAlbums?'},
        }
        user_params = {"user_ids": self.id}
        user_params.update(self.params)
        # print(requests.get(self.API_URL + self.methods['users']['get'],
        #              params=user_params).json())
        resp = requests.get(self.API_URL + self.methods['users']['get'],
                            params=user_params).json()['response'][0]
        self.name = resp['first_name'] + ' ' + resp['last_name']
        if not users_list:
            users_list.append(self)
        else:
            id_list = {_user.id for _user in users_list}
            if self.id not in id_list:
                users_list.append(self)

    # noinspection Pylint
    def __repr__(self):
        return str(self.id)

    # noinspection Pylint
    def __str__(self):
        return self.URL + str(self.id)

    # noinspection Pylint
    def __and__(self, other):
        return self.mutual_friends(other.id)

    def mutual_friends(self, friend):
        """Метод получает список общих друзей двух пользователей"""
        mutual_friends_params = {
            'source_uid': self.id,
            'target_uid': friend,
        }
        mutual_friends_params.update(self.params)
        ids_list = requests.get(self.API_URL + self.methods['friends']['getMutual'],
                                params=mutual_friends_params).json()['response']
        time.sleep(1)
        friends_list = tqdm((User(_id).name for _id in ids_list),
                            total=len(ids_list),
                            desc="Получение имён общих друзей")
        time.sleep(1)
        print(f'\n{self.name} и {User(friend).name} имеют {len(friends_list)} общих друзей:')
        print(*friends_list, sep=", ", end="\n\n")

    def get_photos(self):
        """Метод получает ссылки на 5 последних по дате загрузки фотографий из различных альбомов пользователя"""

        def get_albums():
            param = {"owner_id": self.id}
            param.update(self.params)
            response = requests.get(self.API_URL + self.methods['photos']['get_albums'],
                                    params=param).json()['response']['items']
            albums = {num: {album["title"]: album["id"]} for num, album in enumerate(response, start=1)}
            try:
                last_key = max(albums.keys()) + 1
                albums[last_key] = {"Фото профиля": "profile"}
                return albums
            except ValueError:
                albums[0] = {"Фото профиля": "profile"}
                return albums

        albums = get_albums()

        print("Фото из какого альбома Вы хотите загрузить?")
        for keys, values in albums.items():
            for key in values.keys():
                print(f'{keys}: "{key}"')
        album_number = albums[int(input("Введите номер альбома: "))]
        album_id = (album_number[key] for key in album_number.keys())

        param = {"album_id": album_id, "photo_sizes": "1", 'extended': 1, "owner_id": self.id}
        param.update(self.params)
        photos_list = requests.get(self.API_URL + self.methods['photos']['get'],
                                   params=param).json()['response']['items'][-5:]

        photos_info = []
        for photo in photos_list:
            info = {
                "file_name": str(photo['likes']['count']) + "_" + str(
                    datetime.fromtimestamp(photo['date']).date()) + ".jpg",
                "size": photo['sizes'][-1]['type']
            }
            photos_info.append(info)
        with open("downloaded_vk_photos.json", "w") as file:
            json.dump(photos_info, file)

        url_list = [(photo['sizes'][-1]['url'], photo['likes']['count'], photo['date']) for photo in photos_list]
        return url_list, self.name

    @staticmethod
    def download(urls_list):
        """Метод скачивает на жесткий диск фотографии пользователя"""
        tuples, name = urls_list
        target_folder = os.path.join('downloads', name)
        os.makedirs(target_folder, exist_ok=True)
        target_folder = os.path.abspath(target_folder)
        for url, likes, date in tqdm(tuples):
            file_to_download = requests.get(url)
            with open(os.path.join(target_folder, str(likes) + "_" + str(datetime.fromtimestamp(date).date()) + ".jpg"),
                      'wb') as file:
                file.write(file_to_download.content)
        return target_folder.split(os.path.sep)[-1]
