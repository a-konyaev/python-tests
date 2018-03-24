class Pet:
    #x = 2
    def __init__(self, name=None):
        self.name = name


# класс-примесь
class Loud:
    x = 3
    def say_loud(self):
        return f"{self.breed}  {self.name}: WAW! WAW! WAW!"


class Dog(Pet):
    #x = 1
    def __init__(self, name, breed=None):
        super().__init__(name)
        self.breed = breed
        # private attribute (name mangling)
        self.__weight = 50

    def say(self):
        return f"{self.name}: waw!"


# множественное наследование
class LoudDog(Dog, Loud):
    #x = 0
    def print_weight(self):
        print(f"weight = {self.__weight}")


class ExDog(Dog, Loud):
    def __init__(self, name):
        super(Dog, self).__init__(name)
        self.breed = "taksa"


class PetExport:
    def export(self, pet):
        raise NotImplementedError


class ExportJson(PetExport):
    def export(self, pet):
        pass


class ExportXml(PetExport):
    def export(self, pet):
        return "<dog/>"


class ExportDog(Dog):
    def __init__(self, name, breed=None, exporter=None):
        super().__init__(name, breed)
        self._exporter = exporter or ExportJson()
        if not isinstance(self._exporter, PetExport):
            raise ValueError("wrong exporter", exporter)

    def export(self):
        return self._exporter.export(self)


if __name__ == "__main__":
    d = ExportDog("Барбос", "Ягдтерьер", exporter=ExportXml())
    print(d.export())

    print(issubclass(Dog, object))

    #dog = LoudDog("Beethoven", "St. Bernard")
    #print(dog.say())
    #print(dog.say_loud())

    #print(f"issubclass(Dog, Pet) = {issubclass(Dog, Pet)}; isinstance(dog, Pet) = {isinstance(dog, Pet)}")

    # method resolution order
    #print(LoudDog.__mro__)
    #print(dog.x)

    #ex = ExDog("Zhuchka")
    #print(ex.say_loud())

    #print(dog.__dict__)
    #dog.print_weight()