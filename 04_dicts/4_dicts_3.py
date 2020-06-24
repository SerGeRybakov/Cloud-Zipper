""" Задание 3. Дан список поисковых запросов. Получить распределение количества слов в них.
Т. е. поисковых запросов из одного слова - 5%, из двух - 7%, из трех - 3% и т.д.queries """


queries = [
    'смотреть сериалы онлайн',
    'новости спорта',
    'афиша кино',
    'курс доллара',
    'сериалы этим летом',
    'курс по питону',
    'сериалы про спорт',
]

## Первое решение
# query_1 = 0
# query_2 = 0
# query_3 = 0
# len_counter = 0
# for query in queries:
#     query = query.split()
#     if len(query) == 3:
#         query_3 += 1
#         len_counter += len(query)
#     elif len(query) == 2:
#         query_2 += 1
#         len_counter += len(query)
#     else:
#         query_1 += 1
#         len_counter += len(query)
# print(f'Поисковых запросов из одного слова - {round(query_1/len(queries)*100, 2)}%, из двух - {round(query_2/len(queries)*100, 2)}%, из трех - {round(query_3/len(queries)*100, 2)}%')

# Вариант со словарём
dic = {}
counter = 0
for query in queries:
    query = query.split()
    dic.setdefault(len(query))
    if dic[len(query)] is None:
        dic[len(query)] = 1
    else:
        counter = dic[len(query)] + 1
        dic[len(query)] = counter
for keys, values in dic.items():
    dic[keys] = round(values / len(queries)*100, 2)
queries_amount = []
queries_amount.extend(dic.keys())
queries_amount = list(set(queries_amount))
queries_amount.sort()
for amounts in queries_amount:
    if amounts % 10 == 1 and amounts % 100 != 11:
        print(f"Поисковых запросов из {amounts} слова - {dic[amounts]}%")
    else:
        print(f"Поисковых запросов из {amounts} слов - {dic[amounts]}%")


## С collections.Counter пока не смог самостоятельно разобраться.
