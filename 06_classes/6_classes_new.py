yard_list = []
birds = []
animals = []


class Bird:
    feet = 2
    wings = 2
    feather = True
    movement = ("ходит", "летает")
    eggs = True
    food = ("трава", "семена", "червяки")

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        yard_list.append(self)
        birds.append(self)

    def feed_birds(self):
        self.feed = self.food
        return self.feed

    def take_eggs(self):
        self.take = self.eggs
        return self.take

    def give_voice(self):
        pass


class Goose(Bird):
    movement = ("ходит", "летает", "плавает")
    voice = ("Га-га-га", "Шшшшшшш")
    food = "семена"

    def __init__(self, name, weight):
        super().__init__(name, weight)

    def feed(self):
        feed = self.food
        return feed

    def give_voice(self):
        self.say_smth = self.voice
        return self.say_smth

    def take_eggs(self):
        eggs = super().take_eggs()
        return eggs

    @property
    def get_weight(self):
        return self.weight


class Chicken(Bird):
    movement = ("ходит", "летает", "прыгает", "бегает")
    voice = ("Ко-ко-ко")
    food = ("червяки", "семена")

    def __init__(self, name, weight):
        super().__init__(name, weight)

    def feed(self):
        self.feed = self.food
        return self.feed

    def give_voice(self):
        self.say_smth = self.voice
        return self.say_smth

    def take_eggs(self):
        eggs = super().take_eggs()
        return eggs

    @property
    def get_weight(self):
        return self.weight


class Duck(Bird):
    movement = ("ходит", "летает", "прыгает", "бегает")
    voice = ("Кря-кря")

    def __init__(self, name, weight):
        super().__init__(name, weight)

    def feed(self):
        food = super().feed_birds()
        return food

    def give_voice(self):
        self.say_smth = self.voice
        return self.say_smth

    def take_eggs(self):
        eggs = super().take_eggs()
        return eggs

    @property
    def get_weight(self):
        return self.weight


class Animal:
    feet = 4
    wool = True
    movement = ("ходит", "бегает")
    milk = True
    food = "трава"

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        yard_list.append(self)
        animals.append(self)

    def feed_animals(self):
        self.feed = self.food
        return self.feed

    def give_voice(self):
        pass


class Cow(Animal):
    voice = "Му-у-у"
    wool = False

    def __init__(self, name, weight):
        super().__init__(name, weight)

    def feed(self):
        food = super().feed_animals()
        return food

    def give_voice(self):
        self.say_smth = self.voice
        return self.say_smth

    def to_milk(self):
        self.milk_ = self.milk
        return self.milk_

    @property
    def get_weight(self):
        return self.weight


class Sheep(Animal):
    voice = "Ме-е-е"
    milk = False

    def __init__(self, name, weight):
        super().__init__(name, weight)

    def feed(self):
        food = super().feed_animals()
        return food

    def give_voice(self):
        self.say_smth = self.voice
        return self.say_smth

    def cut_wool(self):
        self.cut = self.wool
        return self.cut

    @property
    def get_weight(self):
        return self.weight


class Goat(Animal):
    movement = ("ходит", "прыгает", "бегает")
    voice = "Бе-е-е"
    wool = False

    def __init__(self, name, weight):
        super().__init__(name, weight)

    def feed(self):
        food = super().feed_animals()
        return food

    def give_voice(self):
        self.say_smth = self.voice
        return self.say_smth

    def to_milk(self):
        self.milk_ = self.milk
        return self.milk_

    @property
    def get_weight(self):
        return self.weight


def max_weight():
    pet = ""
    max_weight = 0
    for pet_ in yard_list:
        if max_weight < pet_.get_weight:
            max_weight = pet_.get_weight
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
        if bird.eggs is True:
            if type(bird.voice) == tuple:
                print(bird.name, bird.take_eggs(), bird.give_voice()[1])
            else:
                print(bird.name, bird.take_eggs(), bird.give_voice())
    print()


def milking():
    print("ВРЕМЯ ДОЙКИ")
    for animal in animals:
        if animal.milk is True:
            print(animal.name, animal.to_milk(), animal.give_voice())
    print()


def cutting():
    print("ВРЕМЯ СТРИЖКИ")
    for animal in animals:
        if animal.wool is True:
            print(animal.name, animal.cut_wool(), animal.give_voice())
    print()


goose0 = Goose("Серый", 3)
goose1 = Goose("Белый", 3)

duck0 = Duck("Кряква", 2)

hen0 = Chicken("Кококо", 1.5)
hen1 = Chicken("Кукареку", 2)
hen1.voice = ("Ко-ко-ко", "Ку-ка-ре-ку")
hen1.eggs = False

cow0 = Cow("Манька", 150)

sheep0 = Sheep("Барашек", 25)
sheep1 = Sheep("Кудрявый", 30)

goat0 = Goat("Рога", 31)
goat1 = Goat("Копыта", 35)


milking()
taking_eggs()
feeding()
cutting()
max_weight()



