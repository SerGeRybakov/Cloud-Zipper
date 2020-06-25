yard_list = []
birds = []
animals = []


class AllAnimals:
    food = ""
    voice = ""

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        yard_list.append(self)
        if issubclass(Bird, AllAnimals):
            birds.append(self)
        if issubclass(Animal, AllAnimals):
            animals.append(self)

    def feed(self):
        feed = self.food
        return feed

    def give_voice(self):
        say_smth = self.voice
        return say_smth


class Bird(AllAnimals):
    food = ("трава", "семена", "червяки")


class EggBird(Bird):
    eggs = True

    def take_eggs(self):
        take = self.eggs
        return take


class Goose(EggBird):
    voice = ("Га-га-га", "Шшшшшшш")
    food = "семена"


class Chicken(EggBird):
    voice = "Ко-ко-ко"
    food = ("червяки", "семена")


class Cock(Bird):
    voice = ("Ко-ко-ко", "Ку-ка-ре-ку")
    food = ("червяки", "семена")


class Duck(EggBird):
    voice = "Кря-кря"


class Animal(AllAnimals):
    food = "трава"


class MilkAnimal(Animal):
    milk = True

    def to_milk(self):
        milk_ = self.milk
        return milk_


class WoolAnimal(Animal):
    wool = True

    def cut_wool(self):
        cut = self.wool
        return cut


class Cow(MilkAnimal):
    voice = "Му-у-у"


class Sheep(WoolAnimal):
    voice = "Ме-е-е"


class Goat(MilkAnimal):
    voice = "Бе-е-е"


def max_weight():
    pet = ""
    max_weight = 0
    for pet_ in yard_list:
        if max_weight < pet_.weight:
            max_weight = pet_.weight
            pet = pet_
    print(f"Больше всех весит {pet.name} - {max_weight} кг")
    print()


def feeding():
    print("КОРМИМ ВСЕХ")
    for pet_ in yard_list:
        if type(pet_.voice) == tuple:
            print(pet_.name, pet_.feed(), pet_.give_voice()[0])
        else:
            print(pet_.name, pet_.feed(), pet_.give_voice())
    print()


def taking_eggs():
    print("СОБИРАЕМ ЯЙЦА")
    for bird in birds:
        if isinstance(bird, EggBird):
            if type(bird.voice) == tuple:
                print(bird.name, bird.take_eggs(), bird.give_voice()[1])
            else:
                print(bird.name, bird.take_eggs(), bird.give_voice())
        else:
            pass
    print()


def milking():
    print("ВРЕМЯ ДОЙКИ")
    for animal in animals:
        if isinstance(animal, MilkAnimal):
            print(animal.name, animal.to_milk(), animal.give_voice())
    print()


def cutting():
    print("ВРЕМЯ СТРИЖКИ")
    for animal in animals:
        if isinstance(animal, WoolAnimal):
            print(animal.name, animal.cut_wool(), animal.give_voice())
    print()


def morning():
    print(f"Петух {cock0.name} кричит: '{cock0.give_voice()[1]}!!!'")
    print()


goose0 = Goose("Серый", 3)
goose1 = Goose("Белый", 3)

duck0 = Duck("Кряква", 2)

hen0 = Chicken("Кококо", 1.5)

cock0 = Cock("Кукареку", 2)

cow0 = Cow("Манька", 150)

sheep0 = Sheep("Барашек", 25)
sheep1 = Sheep("Кудрявый", 30)

goat0 = Goat("Рога", 31)
goat1 = Goat("Копыта", 35)

morning()
milking()
taking_eggs()
feeding()
cutting()
max_weight()
