class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

    def __str__(self):
        return f"{self.name}={self.damage}"

    def __repr__(self):
        return self.__str__()


class Robot:
    """test Robot class"""
    count = 0

    def __new__(cls, *args, **kwargs):
        #print(f"__new__! cls = {cls}")
        obj = super().__new__(cls)
        return obj

    def __init__(self, name, weapons=None, power=0):
        #print("__init__!")
        Robot.count += 1

        self.name = name
        self.weapons = weapons or []
        self._power = power

    power = property()

    @power.setter
    def power(self, value):
        self._power = value if value >= 0 else 0

    @power.getter
    def power(self):
        return self._power

    @power.deleter
    def power(self):
        del self._power

    def __str__(self):
        return f"{self.name},{self._power}: {self.weapons}"

    def __repr__(self):
        return f"robot {self.name}"

    def __del__(self):
        Robot.count -= 1
        #print(f"robot {self.name} destroyed!")

    def add_weapon(self, weapon):
        self.weapons.append(weapon)
        #print(f"weapons updated: {self.weapons}")

    @classmethod
    def get_robocop(cls):
        return cls("Murphy")

    @staticmethod
    def print_count():
        print(f"Robots count: {Robot.count}")


if __name__ == "__main__":
    r = Robot("Nexus")
    r.add_weapon(Weapon("blaster", 30))
    r.add_weapon(Weapon("gun", 10))
    print(r)

    m = Robot.get_robocop()
    m.power = 321
    print(m)
    m.power = -321
    print(m)
    del m.power
    m.power = 10
    print(m)

    q = m.get_robocop()
    print(q)
    q.print_count()

    Robot.print_count()