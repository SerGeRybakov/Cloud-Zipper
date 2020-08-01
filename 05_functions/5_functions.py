"""Домашнее задание к лекции 5.«Функции — использование встроенных и создание собственных»
Я работаю секретарем и мне постоянно приходят различные документы. Я должен быть очень внимателен чтобы не потерять ни один документ. Каталог документов хранится в следующем виде:

      documents = [
        {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
        {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
        {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
      ]
Перечень полок, на которых находятся документы хранится в следующем виде:

      directories = {
        '1': ['2207 876234', '11-2', '5455 028765'],
        '2': ['10006'],
        '3': []
      }
Задача №1
Необходимо реализовать пользовательские команды, которые будут выполнять следующие функции:

p – people – команда, которая спросит номер документа и выведет имя человека, которому он принадлежит;
s – shelf – команда, которая спросит номер документа и выведет номер полки, на которой он находится;
Правильно обработайте ситуации, когда пользователь будет вводить несуществующий документ.
l– list – команда, которая выведет список всех документов в формате passport "2207 876234" "Василий Гупкин";
a – add – команда, которая добавит новый документ в каталог и в перечень полок, спросив его номер, тип, имя владельца и номер полки, на котором он будет храниться. Корректно обработайте ситуацию, когда пользователь будет пытаться добавить документ на несуществующую полку.
Внимание: p, s, l, a - это пользовательские команды, а не названия функций. Функции должны иметь выразительное название, передающие её действие.

Задача №2. Дополнительная (не обязательная)
d – delete – команда, которая спросит номер документа и удалит его из каталога и из перечня полок. Предусмотрите сценарий, когда пользователь вводит несуществующий документ;
m – move – команда, которая спросит номер документа и целевую полку и переместит его с текущей полки на целевую. Корректно обработайте кейсы, когда пользователь пытается переместить несуществующий документ или переместить документ на несуществующую полку;
as – add shelf – команда, которая спросит номер новой полки и добавит ее в перечень. Предусмотрите случай, когда пользователь добавляет полку, которая уже существует.;"""


documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

directories = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006'],
    '3': []
}


def check_doc_num():
    def docs_list():
        doc_list = []
        for i in directories.values():
            for y in i:
                doc_list.extend(i)
        return set(doc_list)

    doc_list = docs_list()
    doc_num = None

    while doc_num not in doc_list:
        doc_num = input("Введите корректный номер документа: ")
    return doc_num


def person():
    doc_number = check_doc_num()
    for dic in documents:
        if doc_number in dic.values():
            return dic["name"]
    return "Информация о владельце/составителе документа отсутствует"


def shelf():
    doc_number = check_doc_num()
    for shelf_num, document_num in directories.items():
        if doc_number in document_num:
            return shelf_num


def lst():
    docs = []
    for dic in documents:
        a = ""
        for keys in dic.keys():
            a = a + '"' + str(dic[keys]) + '"' + ' '
        docs.append(a)
    return docs


def add():
    def add_dic(doc_t, doc_n, pers):
        dic = {}
        dic["type"] = doc_t.strip()
        dic["number"] = doc_n.strip()
        dic["name"] = pers.strip()
        documents.append(dic)
        return documents[documents.index(dic)]

    def add_sh(doc_n, shelf_n):
        if shelf_num not in directories.keys():
            add_shelf(shelf_num, doc_number)
            return directories[shelf_num]
        else:
            for keys in directories.keys():
                value_lst = directories[shelf_num]
                value_lst.append(doc_number)
                return directories[shelf_num]

    doc_type = input("Введите тип документа: ")
    doc_number = input("Введите номер документа: ")
    person = input("Введите владельца/составителя документа: ")
    shelf_num = input("Введите номер полки: ")

    new_dic = add_dic(doc_type, doc_number, person)
    shelved_doc = add_sh(doc_number, shelf_num)
    return new_dic, shelved_doc


def delete():
    doc_number = check_doc_num()

    for dic in documents:
        if doc_number in dic.values():
            documents.remove(dic)
    for keys, values in directories.items():
        if doc_number in values:
            value_lst = directories[keys]
            value_lst.remove(doc_number)

    return f"\nДокумент успешно удалён.\n\n{documents}\n{directories}\n"


def move():
    def del_number(doc_num):
        for keys, values in directories.items():
            if doc_num in values:
                value_lst = directories[keys]
                value_lst.remove(doc_num)
                directories[keys] = value_lst
            else:
                continue
            return keys, directories[keys]

    def create_number(shelf_num, doc_num):
        if shelf_num not in directories.keys():
            add_shelf(shelf_num, doc_num)
            return directories[shelf_num]
        else:
            for keys in directories.keys():
                value_lst = directories[shelf_num]
                value_lst.append(doc_num)
                return directories[shelf_num]

    doc_number = check_doc_num()
    shelf_number = input("Введите номер целевой полки: ")
    delete = del_number(doc_number)
    create = create_number(shelf_number, doc_number)
    print(documents)
    print(directories)
    return f"\nДокумент успешно перемещён c полки {delete[0]} ({delete[1]}) на полку {shelf_number} ({create})\n"


def add_shelf(shelf_num=None, key=None):
    shelves = []
    for num in directories.keys():
        shelves.append(num)

    if shelf_num and key:
        directories[shelf_num] = [key]
    else:
        shelf_num = input("Введите номер полки: ")
        if shelf_num not in shelves:
            directories[shelf_num] = []
            print(f"Полка с номером {shelf_num} успешно создана!\n")
        else:
            print(f"Полка с номером {shelf_num} уже существует!\n")
        print(directories)
        return directories
    print(directories)


def main():
    """
1) Функция person() выводит имя человека, имеющего/составившего документ с определенным номером
2) Функция shelf() выводит номер полки, на которой лежит документ, имеющий определенный номер.
3) Функция lst() выводит список всех документов в формате: "Тип документа" "Номер документа" "Владелец/составитель документа"
4) Функция add() добавляет новый документ в каталог и на целевую полку. Если целевая полка в момент перемещения отсутствует, то она будет автоматически создана.
5) Функция delete() удаляет документ из каталога и с соответствующей полки по его номеру.
6) Функция move() перемещает документ с текущей полки на целевую по номеру документа и номеру целевой полки. Если целевая полка в момент перемещения отсутствует, то она будет автоматически создана.
7) Функция add_shelf() добавляет новую полку в перечень полок.

Для вызова функций введите следующие команды (без кавычек):
    - "p" для person(),
    - "s" для shelf(),
    - "l" для lst(),
    - "a" для add(),
    - "d" для delete(),
    - "m" для move(),
    - "as" для add_shelf().
Для повторного вывода справки введите "help."
Для завершения программы введите "exit"."""

    user_commands = {
        "p": person,
        "s": shelf,
        "l": lst,
        "a": add,
        "d": delete,
        "m": move,
        "as": add_shelf,
        "help": None,
        "exit": None
    }

    command = None
    print(main.__doc__)
    print()

    while command != "exit":
        command = None
        while command not in user_commands.keys():
            command = input("Введите команду: ")
        else:
            if command == "help":
                print(main.__doc__)
                print()
            elif command == "exit":
                print()
                print("Работа программы завершена")
                break
            else:
                print(user_commands[command]())
                print()


main()
