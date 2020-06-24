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

