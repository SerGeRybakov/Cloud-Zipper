""" Задание №3
Разработать приложение для определения знака зодиака по дате рождения.
Пример:

Введите месяц: март
Введите число: 6

Вывод:
Рыбы"""


month = input("Укажите первые три буквы месяца (например: янв) ")
date = int(input("Укажите день "))

if (month == "мар" and 21 <= date <= 31) or (month == "апр" and 1 <= date <= 20):
    print("Овен (21 марта – 20 апреля)")
elif (month == "апр" and 21 <= date <= 30) or (month == "май" and 1 <= date <= 21):
    print("Телец (21 апреля – 21 мая)")
elif (month == "май" and 22 <= date <= 31) or (month == "июн" and 1 <= date <= 21):
    print("Близнецы (22 мая – 21 июня)")
elif (month == "июн" and 22 <= date <= 30) or (month == "июл" and 1 <= date <= 22):
    print("Рак (22 июня – 22 июля)")
elif (month == "июл" and 23 <= date <= 31) or (month == "авг" and 1 <= date <= 23):
    print("Лев (23 июля – 23 августа)")
elif (month == "авг" and 24 <= date <= 31) or (month == "сен" and 1 <= date <= 23):
    print("Дева (24 августа – 23 сентября)")
elif (month == "сен" and 24 <= date <= 30) or (month == "окт" and 1 <= date <= 23):
    print("Весы (24 сентября – 23 октября)")
elif (month == "окт" and 24 <= date <= 31) or (month == "ноя" and 1 <= date <= 22):
    print("Скорпион (24 октября – 22 ноября)")
elif (month == "ноя" and 23 <= date <= 30) or (month == "дек" and 1 <= date <= 21):
    print("Стрелец (23 ноября – 21 декабря)")
elif (month == "дек" and 22 <= date <= 31) or (month == "янв" and 1 <= date <= 20):
    print("Козерог (22 декабря – 20 января)")
elif (month == "янв" and 21 <= date <= 31) or (month == "фев" and 1 <= date <= 18):
    print("Водолей (21 января – 18 февраля)")
elif (month == "фев" and 19 <= date <= 29) or (month == "мар" and 1 <= date <= 20):
    print("Рыбы (19 февраля – 20 марта)")
else:
    print("Такого числа в календаре не существует")
