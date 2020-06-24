yard_list = []


class Bird:
    feet = 2
    wings = 2
    feather = True
    movement = ("walk", "fly")
    eggs = True
    food = ("grass", "seeds", "worms")

    def __init__(self, name, weight):
        yard_list.append(self)

    def feed_birds(self):
        pass

    def take_eggs(self):
        self.take = self.eggs
        return self.take

    def give_voice(self):
        pass


class Goose(Bird):
    movement = ("walk", "fly", "swim")
    voice = ("Га-га-га", "Шшшшшшш")
    food = "seeds"

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        yard_list.append(self)

    def feed(self):
        feed = self.food
        return feed

    def give_voice(self):
        self.say_smth = self.voice
        return self.say_smth

    def take_eggs(self):
        super().take_eggs()

    @property
    def get_weight(self):
        return self.weight


class Chicken(Bird):
    movement = ("walk", "fly", "jump", "run")
    voice = ("Ко-ко-ко")
    food = ("worms", "seeds")

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        yard_list.append(self)

    def feed(self):
        self.feed = self.food
        return self.feed

    def give_voice(self):
        self.say_smth = self.voice
        return self.say_smth

    def take_eggs(self):
        super().take_eggs()

    @property
    def get_weight(self):
        return self.weight


class Duck(Bird):
    movement = ("walk", "fly", "swim", "run")
    voice = ("Кря-кря")
    food = ("grass", "seeds", "worms")

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        yard_list.append(self)

    def feed(self):
        super().feed_birds()
        self.feed = self.food
        return self.feed

    def give_voice(self):
        self.say_smth = self.voice
        return self.say_smth

    def take_eggs(self):
        super().take_eggs()

    @property
    def get_weight(self):
        return self.weight


class Animal:
    feet = 4
    wool = True
    movement = ("walk", "run")
    milk = True
    food = "grass"

    def __init__(self, name, weight):
        yard_list.append(self)

    def feed_animals(self):
        self.feed = self.food
        return self.feed

    def give_voice(self):
        pass


class Cow(Animal):
    voice = "Му-у-у"
    wool = False

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        yard_list.append(self)

    def feed(self):
        super().feed_animals()

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

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        yard_list.append(self)

    def feed(self):
        super().feed_animals()

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
    movement = ("walk", "jump", "run")
    voice = "Бе-е-е"

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        yard_list.append(self)

    def feed(self):
        super().feed_animals()

    def give_voice(self):
        self.say_smth = self.voice
        return self.say_smth

    def to_milk(self):
        self.milk_ = self.milk
        return self.milk_

    @property
    def get_weight(self):
        return self.weight


goose0 = Goose("Серый", 3)
goose1 = Goose("Белый", 3)

duck0 = Duck("Кряква", 2)

hen0 = Chicken("Кококо", 1.5)
hen1 = Chicken("Кукареку", 2)
hen1.voice = ("Ко-ко-ко", "Ку-ка-ре-ку")

cow0 = Cow("Манька", 150)

sheep0 = Sheep("Барашек", 25)
sheep1 = Sheep("Кудрявый", 30)

goat0 = Goat("Рога", 31)
goat1 = Goat("Копыта", 35)

# yard_list = [goose1, goose0, cow0, goat1, goat0, sheep1, sheep0, hen0, hen1, duck0]
pet = ""
max_weight = 0
for pet_ in yard_list:
    if max_weight < pet_.get_weight:
        max_weight = pet_.get_weight
        pet = pet_
print(max_weight, pet.name)
