height = int(input("Введите рост "))
age = int(input("Введите возраст "))
children = int(input("Введите количество детей "))
invalid = input("Наличие инвалидности или заболеваний, препятствующих прохождению службы (при отстутствии не заполнять): ")

if age >= 18:
    if invalid or children > 1:
        print("Не годен")
    else:
        if height < 170:
            print("Танковые войска")
        elif height < 180:
            print("Десантные войска")
        elif height < 190:
            print("Мотострелковые войска")
        else:
            print("Флот")
else:
    print("Не подлежит призыву")