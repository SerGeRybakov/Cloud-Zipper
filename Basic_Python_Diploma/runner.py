"""Модуль запускает работу всей программы"""

import json
import time
from datetime import datetime

import VK as vk
import YaDisk

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
Для вызова функций вводите следующие команды (без кавычек):

* Для работы с ВКонтакте:
    - "user" для заведения в программу ранее неизвестного пользователя ВКонтакте
    - "all_vk" для вывода списка id всех известных на данный момент пользователей
    - "len_vk" для вывода количества всех известных на данный момент пользователей
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
    - "zip" для скачивания и архивирования файла или папки, имеющихсамый большой размер, и загрузки архива обратно

Для завершения программы введите "exit".
==================================="""

    def _all_users_names():
        """Метод выводит имена всех уже известных пользователей ВКонтакте"""

        return [user.name for user in vk.users_list]

    def _split(string):
        """Метод создаёт срез из пользовательского ввода"""

        def _collection(obj_type):
            if obj_type == 'file':
                collection = ya.all_files
            elif obj_type == 'folder':
                collection = ya.all_folders
            else:
                raise TypeError("Введите file или folder")
            return collection

        def _slice(slice_string):
            s_s_s = slice_string.replace(']', '').split(':')
            if len(s_s_s) == 1:
                s_s_s[0] = int(s_s_s[0])
                s_s_s.append(s_s_s[0] + 1)
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
            if string[0].isdigit():
                string.replace('[', '').replace(']', '')
                return _slice(string)
            else:
                return _collection(string)

    def photos():
        """Метод загружает 5 последних фотографий из альбомов уже известного пользователя ВКонтакте
        на жесткий диск или на Яндекс.Диск"""

        for num, name in enumerate(_all_users_names()):
            print(str(num) + " " + name)
        user = vk.users_list[int(input("Укажите пользователя: "))]
        print('Для скачивания фотографий на жесткий диск введите "1"')
        print('Для загрузки фотографий на Яндекс.Диск введите "2"')
        print('Для скачивания фотографий на жесткий диск и загрузки фотографий на Яндекс.Диск введите "3"')
        methods = (1, 2, 3)
        method = int(input("Введите ответ: "))
        photos = user.get_photos()
        while method not in methods:
            print("Такая команда не предусмотрена")
            method = int(input("Введите ответ: "))
        if method == 1:
            user.download(photos)
            return "Фотографии успешно загружены на жесткий диск"
        elif method == 2:
            ya.upload(photos)
            ya.reload()
            return "Фотографии успешно загружены на Яндекс.Диск"
        elif method == 3:
            ya.upload(photos)
            user.download(photos)
            ya.reload()
            return "Фотографии успешно загружены на жесткий диск и на Яндекс.Диск"

    def mutual():
        """Метод выводит перечень общих друзей двух пользователей ВКонтакте"""

        _user1 = int(input("Укажите пользователя 1: "))
        _user2 = int(input("Укажите пользователя 2: "))
        return vk.users_list[_user1] & vk.users_list[_user2]

    def print_user_name():
        """Метод выводит имя уже известного пользователя ВКонтакте"""

        return vk.users_list[int(input("Укажите пользователя: "))].name

    def print_user_link():
        """Метод выводит ссылку на страницу уже известного пользователя ВКонтакте"""

        return vk.users_list[int(input("Укажите пользователя: "))]

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

        for num, dir in enumerate(print_all_objects()):
            print(num, dir)
        print("Для удаления объекта необходимо ввести его тип, а также его индекс или срез")
        print("Например: file[1], folder[3::-1]")
        string = input("Введите тип объекта для удаления, его индекс или срез: ")
        split = _split(string)
        collection, slice = split
        print(slice)
        return ya.delete(collection[slice[0]:slice[1]:slice[2]])

    def download():
        """Метод скачивает папку, файл с Яндекс.Диска на жесткий диск"""

        objects = input("Для скачивания объекта необходимо ввести его тип: ")
        if objects == "file":
            object = ya.all_files
        elif objects == "folder":
            object = ya.all_folders
        else:
            return "Такой тип объекта отсутствует. Попробуйте снова."
        for num, dir in enumerate(print_all_objects(objects)):
            print(num, dir)
        index = int(input("Введите индекс объекта для скачивания: "))
        return ya.download(object[index])

    def find_biggest():
        """Метод выводит имя файла или папки Яндекс.Диска, имеющих самый большой размер"""

        print("Для поиска самого большого объекта необходимо ввести его тип: file или folder")
        return ya.find_biggest(input("Введите тип объектa: "))

    def print_all_objects(obj_type=None):
        """Метод выводит на экран перечень всех файлов или папкок Яндекс.Диска"""

        if obj_type:
            return _split(obj_type)
        else:
            print("Для вывода всех папок или файлов необходимо ввести тип объектов: file или folder")
            return _split(input("Введите тип объектов: "))

    def top_10():
        """Метод выводит топ-10 файлов или папкок Яндекс.Диска, имеющих самый большой размер"""

        print("Для подборки самых больших объектов необходимо ввести их тип: file или folder")
        return ya.top10(input("Введите тип объектов: "))

    def upload(object=None):
        """Метод загружает папку, файл с жесткого диска или фотографии по url из ВКонтакте на Яндекс.Диск"""

        if object:
            obj = object
        else:
            obj = input("Введите имя папки или файла (без пути): ")
        return ya.upload(obj)

    def zipfile():
        """Метод скачивает с Яндекс.Диска файл или папку, имеющиесамый большой размер, архивирует их в формат zip
         и загружает архив обратно. Опционально можно удалить архивируемый объект."""

        print('Если после загрузки архива Вы хотите удалить архивируемый объект c Яндекс.Диска - введите "1"')
        print("В противном случае нажмите Enter")
        _del = input("Введите ответ: ")
        object = input('Введите тип объекта ("file" или "folder"): ')
        if _del == "1":
            big = ya.find_biggest(object)
            ya.download(big)
            _zip = ya.zip_file(big)
            ya.upload(_zip)
            ya.delete(big)
            return f'{big.name} успешно заархивирован и удалён с Яндекс.Диска'
        elif not _del:
            big = ya.find_biggest(object)
            ya.download(big)
            ya.upload(ya.zip_file(big))
            return f'\n{big.name.capitalize()} успешно заархивирован'
        else:
            return 'Такой команды не предусмотрено. Попробуйте снова'

    def user():
        """Метод задаёт нового пользователя ВКонтакте"""
        return vk.User(int(input("Введите id пользоваьтеля: ")))

    user_commands = {
        "user": user,
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
    print()
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
    access_token = input("Введите токен Яндекс.Диска (получить его можно тут - https://yandex.ru/dev/disk/poligon/): ")
    ya = YaDisk.YaDisk(access_token)
    give_command()
