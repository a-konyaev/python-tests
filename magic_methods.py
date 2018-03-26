class User:
    def __init__(self, name):
        self.name = name

    def __call__(self, func):
        print("call: " + str(func))
        return func

    def get_name(self):
        return {
            'name': self.name
        }

    def __del__(self):
        print("destroy User: " + str(id(self)))

    def __str__(self):
        return "Name is " + self.name

    def __eq__(self, other):
        if other is None:
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __getattr__(self, item):
        return "Attribute not found: " + str(item)

    def __getattribute__(self, item):
        print(f"get attribute: {item}")
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        print(f"try to set attr {key} to value = {value}")
        object.__setattr__(self, key, value)

    def __delattr__(self, item):
        print(f"delete attr: {item}")
        object.__delattr__(self, item)
# u = User('test')
# print(u.get_name())
# print(u)
#
# u2 = User('test')
# print(f"u == u2 is {u == u2}")
#
# u_map = {user: user.name for user in [u, u2]}
# print(u_map)
#
# print("test assess to attributes:")
# print(u.email)
# u.email = "a@a.aa"
# print(u.email)
# del u.email
# print(u.email)
#
# @u
# def q():
#     pass


class Singleton:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__init__(cls)

        return cls.instance

    def __del__(self):
        print("destroy Singleton: " + str(id(self)))
# a = Singleton()
# b = Singleton()
# print(a is b)
# del a
# del b
# del Singleton.instance


class MyMap:
    def __init__(self):
        self.map = {}
        self.current = 0

    def __getitem__(self, item):
        return self.map[item]

    def __setitem__(self, key, value):
        self.map[key] = value

    def __iter__(self):
        return self

    def __next__(self):
        l = list(self.map.keys())
        if self.current >= len(l):
            raise StopIteration

        res = l[self.current]
        self.current += 1
        return f"{res}={self.map[res]}"


m = MyMap()
m[1] = 'a'
m[2] = 'b'
m[3] = 'c'
m[3] = 'd'
print(m[1])

for i in m:
    print(i)




