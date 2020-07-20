"""Модуль запускает работу всей программы"""

import json
import time
from datetime import datetime

from Basic_Python_Diploma import VK as vk
from Basic_Python_Diploma import YaDisk

now = int(time.mktime(datetime.now().timetuple()))


def check_token():
    """Модуль проверяет наличие и действительность токена пользователя vk.com"""
    with open("access_token.json") as file:
        access_key_dict = json.load(file)
    if access_key_dict['expires_in'] <= now:
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Для работы программы необходимо ввести данные для авторизации в Вашей учётной записи ВКонтакте.\n")
        print("Данные запрашиваются только в случае необходимости получения валидного ключа доступа от ВКонтакте.\n")
        print("Вводимые учётные данные нигде не сохраняются, не передаются никуда, кроме сервиса ВКонтакте")
        print("и используются только во время работы программы.")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!")
        auth_ = vk.VKAPIAuth(login=input("\nВведите логин (номер телефона/e-mail): "),
                             password=input("Введите пароль: "))
        vk.VKAPIAuth.ACCESS_TOKEN = auth_.ACCESS_TOKEN
        return auth_
    else:
        auth_ = vk.VKAPIAuth()
        vk.VKAPIAuth.ACCESS_TOKEN = access_key_dict['access_token']
        return auth_


def give_command():
    """===================================
Вы можете найти общих друзей у любых пользователей, находящихся в списке пользователей "users_list".
В функциях, требующих указания пользователя(-ей), необходимо указать индекс в списке пользователей "users_list".

Отсчёт индексов ведётся с ЕДИНИЦЫ!!!

Для вызова функций введите следующие команды (без кавычек):

* Для работы с ВКонтакте:
    - "all_vk" для вывода  списка id всех известных нам пользователей
    - "len_vk" для вывода количества всех известных нам пользователей
    - "link" для вывода ссылки на профиль пользователя
    - "mut" для поиска общих друзей
    - "name" для вывода имени пользователя
    - "pic" для скачивания фотографий

* Для работы с Яндекс.Диском:
    - "all" для вывода на экран всех файлов или папок Яндекс.Диска
    - "mkdir" для создании папки на Яндекс.Диске вручную
    - "del" для удаления папок или файлов на Яндекс.Диске
    - "down" для скачивания папки или файла с Яндекс.Диска на жёсткий диск
    - "big" для вывода файла или папки на Яндекс.Диске, имеющих самый большой размер
    - "top" для вывода топ-10 файлов или папок на Яндекс.Диске, имеющих самый большой размер
    - "up" для загрузки на Яндекс.Диск файла или папки с жесткого диска
    - "zip" для архивации файла или папки на жёстком диске и его дальнейшей загрузки на Яндекс.Диск

Для завершения программы введите "exit".
==================================="""

    def _split(string):
        def _collection(obj_type):
            if obj_type == 'file':
                collection = ya.all_files
            elif obj_type == 'folder':
                collection = ya.all_folders
            else:
                raise TypeError("Введите file или folder")
            return collection

        def _slice(slice_string):
            s_s_s = slice_string.replace('[', '').split(':')
            if len(s_s_s) == 1:
                s_s_s[0] = int(s_s_s[0])
                for _i in range(2):
                    s_s_s.append(None)
            elif len(s_s_s) == 2:
                for i in range(len(s_s_s)):
                    try:
                        s_s_s[i] = int(s_s_s[i])
                    except ValueError:
                        s_s_s[i] = None
                s_s_s.append(None)
            else:
                for i in range(len(s_s_s)):
                    try:
                        s_s_s[i] = int(s_s_s[i])
                    except ValueError:
                        s_s_s[i] = None

            return s_s_s

        try:
            collection, s_s_s = string.split("[")
            collection = _collection(collection)
            s_s_s = _slice(s_s_s)
            return collection, s_s_s
        except ValueError:
            return _collection(string)

    def photos():
        """Метод загружает 5 последних фотографий из альбомов уже известного пользователя ВКонтакте
        на жесткий диск или на Яндекс.Диск"""
        print_all_users()
        ya.upload(vk.users_list[int(input("Укажите пользователя: ")) - 1].get_photos())
        ya.reload()
        return

    def mutual():
        """Метод выводит перечень общих друзей двух пользователей ВКонтакте"""
        user1 = int(input("Укажите пользователя 1: ")) - 1
        user2 = int(input("Укажите пользователя 2: ")) - 1
        return vk.users_list[user1] & vk.users_list[user2]

    def print_user_name():
        """Метод выводит имя уже известного пользователя ВКонтакте"""
        return vk.users_list[int(input("Укажите пользователя: ")) - 1].name

    def print_user_link():
        """Метод выводит ссылку на страницу уже известного пользователя ВКонтакте"""
        return vk.users_list[int(input("Укажите пользователя: ")) - 1]

    def print_all_users():
        """Метод выводит id уже известных пользователей ВКонтакте"""
        return vk.users_list

    def print_len_users():
        """Метод выводит количество уже известных пользователей ВКонтакте"""
        return len(vk.users_list)

    def create_folder():
        """Метод создаёт папку на Яндекс.Диске"""
        return ya.create_folder(input("Введите имя папки (без пути): "))

    def delete():
        """Метод удаляет папку, файл или группу папок или файлов на Яндекс.Диске"""
        print("Для удаления объекта необходимо ввести его тип, а также его индекс или срез")
        print("Например: file[1], folder[3::-1]")
        string = input("Введите тип объекта для удаления, его индекс или срез: ")
        split = _split(string)
        collection, slice = split
        return ya.delete(collection[slice[0]:slice[1]:slice[2]])

    def download():
        """Метод скачивает папку, файл или группу папок или файлов с Яндекс.Диска на жесткий диск"""
        print(print_all_objects('file'))

        print("Для скачивания объекта необходимо ввести его тип, а также его индекс или срез")
        print("Например: file[1], folder[3::-1]")
        string = input("Введите тип объекта для скачивания, его индекс или срез: ")
        split = _split(string)
        collection, slice = split
        return ya.download(collection[slice[0]:slice[1]:slice[2]])

    def find_biggest():
        """Метод выводит имя файла или папки Яндекс.Диска, имеющих самый большой размер"""
        print("Для поиска самого большого объекта необходимо ввести его тип: file или folder")
        return ya.find_biggest(input("Введите тип объектa: "))

    def print_all_objects():
        print("Для вывода всех папок или файлов необходимо ввести тип объектов: file или folder")
        return _split(input("Введите тип объектов: "))

    def top_10():
        """Метод выводит топ-10 файлов или папкок Яндекс.Диска, имеющих самый большой размер"""
        print("Для подборки самых больших объектов необходимо ввести их тип: file или folder")
        return ya.top10(input("Введите тип объектов: "))

    def upload():
        """Метод загружает папку, файл с жесткого диска или фотографии по url из ВКонтакте на Яндекс.Диск"""
        pass

    def zipfile():
        """Метод архивирует файл или папку в формат zip"""
        pass

    user_commands = {
        "pic": photos,
        "mut": mutual,
        "name": print_user_name,
        "link": print_user_link,
        "all_vk": print_all_users,
        "len_vk": print_len_users,
        "mkdir": create_folder,
        "del": delete,
        "down": download,
        "big": find_biggest,
        "all": print_all_objects,
        "top": top_10,
        "up": upload,
        "zip": zipfile,
        "help": None,
        "exit": None
    }

    command = None
    print(give_command.__doc__)
    print()

    while command != "exit":
        command = None
        while command not in user_commands.keys():
            print('Для вывода описания команд введите "help".')
            command = input("Введите команду: ").lower().strip()
        else:
            if command == "exit":
                print()
                print("Работа программы завершена")
                break
            elif command == "help":
                print()
                print(give_command.__doc__)
                print()
            else:
                print(user_commands[command]())
                print()


if __name__ == '__main__':
    auth = check_token()

    user0 = vk.User(273251945)
    user1 = vk.User(271138000)
    access_token = input("Введите токен Яндекс.Диска: ")
    ya = YaDisk.YaDisk(access_token)

    # time.sleep(1)
    # user0.get_photos()
    # user0 & user1

    # vk.users_list[8].download(vk.users_list[8].get_photos())
    # ya.upload(vk.users_list[8].get_photos())

    # ya.upload(user1.get_photos())
    # ya.upload("test")

    # ya.reload()

    # ya.print_all("file")
    # ya.print_all("folder")

    # print(ya.all_files[14].path)

    # print(ya.delete(ya.all_files[13:]))
    # print(ya.delete(ya.all_folders[int(input("Введите индекс папки для удаления: "))]))

    # ya.top10('file')
    # ya.top10('folder')
    #
    # biggest_file = ya.find_biggest('file')
    # biggest_folder = ya.find_biggest('folder')
    # print(biggest_file)
    # print(biggest_folder)

    # ya.download(biggest_file)
    # ya.download(biggest_folder)
    #
    # arch_file = ya.zip_file(biggest_file)
    # print(arch_file)
    # arch_folder = ya.zip_file(biggest_folder)
    # print(arch_folder)

    # ya.create_folder("test")
    # print(ya.upload("271138000"))
    # print(ya.upload("test1.txt"))

    give_command()
