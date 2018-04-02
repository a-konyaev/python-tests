import time
from multiprocessing import Process


class MyProcess(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print("!!! hello ", self.name)


def f(name):
    print("hello ", name)
    time.sleep(1)


if __name__ == '__main__':
    # использование баазового класса
    # p = Process(target=f, args=("Max",))

    # использование своего класса
    p = MyProcess("Zorro")
    p.start()
    p.join()