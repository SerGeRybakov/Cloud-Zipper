"""Задание 5. *(Необязательное) Напишите код для преобразования произвольного списка
вида ['2018-01-01', 'yandex', 'cpc', 100] (он может быть любой длины)
в словарь {'2018-01-01': {'yandex': {'cpc': 100}}}"""

lst = ['2018-01-01', 'yandex', 'cpc', 100]
dic = {lst[-2]: lst[-1]}
for item in lst[-3::-1]:
    dic = {item: dic}
print(dic)

def create_dict(cust_dict, cust_list):
    if len(cust_list) > 2:
        cust_dict[cust_list[0]] = dict()
        create_dict(cust_dict[cust_list[0]], cust_list[1:])

    elif len(cust_list) == 2:
        cust_dict[cust_list[0]] = cust_list[1]
        cust_list = None


complicated_dict = dict()
create_dict(complicated_dict, lst)
print(complicated_dict)



