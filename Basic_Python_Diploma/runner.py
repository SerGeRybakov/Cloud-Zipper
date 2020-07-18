import VK as vk
import YaDisk
import json
from datetime import datetime
import time

from tqdm import tqdm

now = int(time.mktime(datetime.now().timetuple()))

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
        auth_ = vk.VKAPIAuth(login=input("\nВведите логин (номер телефона/e-mail): "), password=input("Введите пароль: "))
        return auth_
    else:
        auth_ = vk.VKAPIAuth()
        vk.VKAPIAuth.ACCESS_TOKEN = access_key_dict['access_token']
        return auth_


def give_command():
    """===================================
Вы можете найти общих друзей у любых пользователей, находящихся в списке пользователей "users_list".
В функциях, требующих указания пользователя(-ей), необходимо указать индекс в списке пользователей "users_list".
Так как отсчёт индекса проще всего вести с единицы, а не с нуля, то так и считайте.

Для вызова функций введите следующие команды (без кавычек):
- "mut" для поиска общих друзей,
- "name" для вывода имени пользователя,
- "link" для вывода ссылки на профиль пользователя,
- "all" для вывода  списка id всех известных нам пользователей,
- "len" для вывода количества всех известных нам пользователей,

Для завершения программы введите "exit".
==================================="""

    def photos():
        print_all_users()
        ya.upload(vk.users_list[int(input("Укажите пользователя: ")) - 1].get_photos())
        return ya.reload()

    def mutual():
        return vk.users_list[int(input("Укажите пользователя 1: "))-1] & \
               vk.users_list[int(input("Укажите пользователя 2: "))-1]

    def print_user_name():
        return vk.users_list[int(input("Укажите пользователя: ")) - 1].name

    def print_user_link():
        return vk.users_list[int(input("Укажите пользователя: "))-1]

    def print_all_users():
        return vk.users_list

    def print_len_users():
        return len(vk.users_list)

    user_commands = {
        "pic": photos,
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

    user0 = vk.User(273251945)
    user1 = vk.User(271138000)


    access_token = input("Введите токен Яндекс.Диска: ")

    ya = YaDisk.YaDisk(access_token)
    user0 & user1

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

    # arch_file = ya.zip_file(biggest_file)
    # print(arch_file)
    # arch_folder = ya.zip_file(biggest_folder)
    # print(arch_folder)

    # ya.create_folder("test")
    # print(ya.upload("271138000"))
    # print(ya.upload("test1.txt"))

    # give_command()

