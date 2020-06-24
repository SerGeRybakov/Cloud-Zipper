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
