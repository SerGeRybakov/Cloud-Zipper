import itertools

""" Задание 2. Выведите на экран все уникальные гео-ID из значений словаря ids. Т. е. список вида [213, 15, 54, 119, 98, 35] """

ids = {'user1': [213, 213, 213, 15, 213],
       'user2': [54, 54, 119, 119, 119],
       'user3': [213, 98, 98, 35]}
vals = []

## первое решение
# for lst in ids.values():
#     for num in lst:
#         vals.append(num)
# print(list(set(vals)))

## вариант с extend
# for lst in ids.values():
#     vals.extend(lst)
# print(list(set(vals)))

## вариант с itertools.chain
# vals = list(set(itertools.chain(*ids.values())))
# print(vals)

## вариант с itertools.chain.from_iterable
# vals = list(set(itertools.chain.from_iterable(ids.values())))
# print(vals)

# вариант "как вывести точно такой же список как из задания"
# for lst in ids.values():
#     vals.extend(set(lst))
# vals.pop()
# print(vals)
