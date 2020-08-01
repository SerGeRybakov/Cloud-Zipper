"""Домашнее задание к лекции 7.«Открытие и чтение файла, запись в файл»
Необходимо написать программу для кулинарной книги.

Список рецептов должен храниться в отдельном файле в следующем формате:

Название блюда
Количество ингредиентов в блюде
Название ингредиента | Количество | Единица измерения
Название ингредиента | Количество | Единица измерения
...
Пример(файл в папке files):

Омлет
3
Яйцо | 2 | шт
Молоко | 100 | мл
Помидор | 2 | шт

Утка по-пекински
4
Утка | 1 | шт
Вода | 2 | л
Мед | 3 | ст.л
Соевый соус | 60 | мл

Запеченный картофель
3
Картофель | 1 | кг
Чеснок | 3 | зубч
Сыр гауда | 100 | г

Фахитос
5
Говядина | 500 | г
Перец сладкий | 1 | шт
Лаваш | 2 | шт
Винный уксус | 1 | ст.л
Помидор | 2 | шт
В одном файле может быть произвольное количество блюд.
Читать список рецептов из этого файла.
Соблюдайте кодстайл, разбивайте новую логику на функции и не используйте глобальных переменных.

Задача №1
Должен получится следующий словарь

cook_book = {
  'Омлет': [
    {'ingredient_name': 'Яйцо', 'quantity': 2, 'measure': 'шт.'},
    {'ingredient_name': 'Молоко', 'quantity': 100, 'measure': 'мл'},
    {'ingredient_name': 'Помидор', 'quantity': 2, 'measure': 'шт'}
    ],
  'Утка по-пекински': [
    {'ingredient_name': 'Утка', 'quantity': 1, 'measure': 'шт'},
    {'ingredient_name': 'Вода', 'quantity': 2, 'measure': 'л'},
    {'ingredient_name': 'Мед', 'quantity': 3, 'measure': 'ст.л'},
    {'ingredient_name': 'Соевый соус', 'quantity': 60, 'measure': 'мл'}
    ],
  'Запеченный картофель': [
    {'ingredient_name': 'Картофель', 'quantity': 1, 'measure': 'кг'},
    {'ingredient_name': 'Чеснок', 'quantity': 3, 'measure': 'зубч'},
    {'ingredient_name': 'Сыр гауда', 'quantity': 100, 'measure': 'г'},
    ]
  }
  
Задача №2
Нужно написать функцию, которая на вход принимает список блюд из cook_book и количество персон для кого мы будем готовить

get_shop_list_by_dishes(dishes, person_count)
На выходе мы должны получить словарь с названием ингредиентов и его количества для блюда. Например, для такого вызова

get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2)
Должен быть следующий результат:

{
  'Картофель': {'measure': 'кг', 'quantity': 2},
  'Молоко': {'measure': 'мл', 'quantity': 200},
  'Помидор': {'measure': 'шт', 'quantity': 4},
  'Сыр гауда': {'measure': 'г', 'quantity': 200},
  'Яйцо': {'measure': 'шт', 'quantity': 4},
  'Чеснок': {'measure': 'зубч', 'quantity': 6}
}
Обратите внимание, что ингредиенты могут повторяться"""


from pprint import pprint


def cookbook():
    cook_book = {}
    with open("recipes.txt", encoding="utf8") as f:
        dishes = {}
        while True:
            dish = f.readline().strip()
            if not dish:
                break
            ingredients_quantity = int(f.readline().strip())
            ingredients_list = []
            for i in range(ingredients_quantity):
                ingredients = f.readline().strip().split(" | ")
                ingredient_dict = {}
                for y in range(len(ingredients)):
                    ingredient_dict['ingredient_name'] = ingredients[0]
                    ingredient_dict['quantity'] = int(ingredients[1])
                    ingredient_dict['measure'] = ingredients[2]
                ingredients_list.append(ingredient_dict)
            f.readline().strip()
            dishes[dish] = ingredients_list
        cook_book.update(dishes)
    pprint(cook_book)
    return cook_book


def get_shop_list_by_dishes(dishes, person_count, cook_book):
    shop_list = {}
    for dish in dishes:
        for dic in (cook_book[dish]):
            tmp = {}
            if dic['measure'] == "г" and dic['quantity'] * person_count // 1000 >= 1:
                tmp["measure"] = "кг"
                if dic['ingredient_name'] not in shop_list.keys():
                    tmp["quantity"] = dic['quantity'] * person_count / 1000
                else:
                    tmp["quantity"] = shop_list[dic['ingredient_name']]['quantity'] + dic[
                        'quantity'] * person_count / 1000
            else:
                tmp["measure"] = dic['measure']
                if dic['ingredient_name'] not in shop_list.keys():
                    tmp["quantity"] = dic['quantity'] * person_count
                else:
                    tmp["quantity"] = shop_list[dic['ingredient_name']]['quantity'] + dic['quantity'] * person_count

            shop_list[dic['ingredient_name']] = tmp
    return shop_list


def main(cook_book):
    dish_names = cook_book.keys()
    commands = {}
    for num in enumerate(dish_names):
        commands[num[0]] = num[1]
    print()
    print("==========================")
    print("Меню:")
    print("--------------------------")
    print("Код", "-", "Наименование блюда", sep="\t")
    for key in commands.keys():
        print(key, "-", commands[key], sep="\t")
    print("==========================")
    print()

    dish = input("Для выбора блюд введите соответствующие коды через пробел: ")
    dish_lst = dish.strip().split()
    dishes = []
    for number in dish_lst:
        number = int(number)
        dishes.append(commands[number])
    persons = int(input("Введите количество гостей: "))
    shop_list = get_shop_list_by_dishes(dishes, persons, cook_book)
    return shop_list


pprint(main(cookbook()))
