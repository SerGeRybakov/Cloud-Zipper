""" Задание 4. Дана статистика рекламных каналов по объемам продаж.
Напишите скрипт, который возвращает название канала с максимальным объемом.
Т.е. в данном примере скрипт должен возвращать 'yandex'. """

stats = {'facebook': 55, 'yandex': 120, 'vk': 115, 'google': 99, 'email': 42, 'ok': 98}

## Первое решение
# sells_volume = 0
# for nets, sells in stats.items():
#     if sells_volume < sells:
#         sells_volume = sells
# for net, sells in stats.items():
#     if sells_volume == sells:
#         print(net)

## Второй вариант через max
# sells_volume = max(stats.values())
# for net, sells in stats.items():
#     if sells_volume == sells:
#         print(net)


## Третий вариант с трюком через zip
# print(max(zip(stats.keys(), stats.values()))[0])
