""" Мы делаем MVP dating-сервиса, и у нас есть список парней и девушек (их число может варьироваться):

boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard']
girls = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']

Выдвигаем гипотезу: лучшие рекомендации мы получим, если просто отсортируем имена по алфавиту и познакомим людей 
с одинаковыми индексами после сортировки! "Познакомить" пары нам поможет функция zip, а в цикле распакуем zip-объект 
и выведем информацию в виде:

Идеальные пары:
Alex и Emma
Arthur и Kate
John и Kira
Peter и Liza
Richard и Trisha
Внимание! Если количество людей в списках будет не совпадать, то мы никого знакомить не будет и выведем пользователю 
предупреждение, что кто-то может остаться без пары!"""


boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard']
girls = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha', 'Masha']
boys.sort()
girls.sort()

if len(boys) < len(girls):
    print("Кто-то из парней останется без пары.")
elif len(boys) > len(girls):
    print("Кто-то из девушек останется без пары.")
else:
    print("Идеальные пары:")
    for boy, girl in zip(boys, girls):
        print(f'{boy} и {girl}')

