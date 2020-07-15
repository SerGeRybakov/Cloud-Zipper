from datetime import datetime
import json
import os
import time
from pprint import pprint

import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import runner

users_list = []

now = int(time.mktime(datetime.now().timetuple()))


class VKAPIAuth:
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
    def __init__(self, _id: int, token: str):
        self.id = _id
        self.URL = 'https://vk.com/id'
        self.API_URL = 'https://api.vk.com/method/'
        self.params = {
            'access_token': token,
            'v': '5.120'
        }
        self.methods = {
            'users': {'get': 'users.get?'},
            'friends': {'get': 'friends.get?',
                        'areFriends': 'friends.areFriends?',
                        'getMutual': 'friends.getMutual?',
                        },
            'photos': {'get': 'photos.get?',
                       'areFriends': 'friends.areFriends?',
                       'getMutual': 'friends.getMutual?',
                       },

        }

        if not users_list:
            users_list.append(self)
        else:
            id_list = {_user.id for _user in users_list}
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
        ids_list = requests.get(self.API_URL + self.methods['friends']['getMutual'],
                                params=mutual_friends_params).json()['response']

        ids_str = ''
        friends_list = [User(_id) for _id in ids_list]
        for _id in ids_list:
            if not ids_str:
                ids_str += str(_id)
            else:
                ids_str = ids_str + "," + str(_id)
        mut_friends_names = self.user(ids_str)
        mut_friends_names_list = []
        for _name in mut_friends_names:
            name = _name['first_name'] + ' ' + _name['last_name']
            mut_friends_names_list.append(name)
        print(f'{self.user()} и {User(friend).user()} имеют {len(mut_friends_names_list)} общих друзей:')
        print(*mut_friends_names_list, sep=", ")
        print(f'Все они являются сущностями и хранятся в списке "users_list".')
        print(f'А вот список ссылок на их профили. ')
        print(*friends_list, sep="\t")
        print()

    def get_photos(self):
        param = {"album_id": "profile", "photo_sizes": "w", "type": "z", 'extended': 1, "owner_id": self.id}
        param.update(self.params)
        photos_list = requests.get(self.API_URL + self.methods['photos']['get'],
                                   params=param).json()['response']["items"][-5:]
        # pprint(photos_list)
        url_list = [(photo["sizes"][-1]['url'], photo['likes']["count"], photo["date"]) for photo in photos_list]
        return url_list, self.user()


    def download(self, item):
        target_folder = 'downloads'
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)
        target_folder = os.path.join(target_folder, str(self.id))
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)
        target_folder = os.path.abspath(target_folder)
        file_to_download = requests.get(item["sizes"][-1]['url'])
        with open(os.path.join(target_folder,
                               str(item['likes']["count"]) + "_" +
                               str(datetime.fromtimestamp(item["date"]).date()) + ".jpg"),
                  'wb') as f:
            f.write(file_to_download.content)
        print(os.path.basename(target_folder))
        return target_folder.split(os.path.sep)[-1]
