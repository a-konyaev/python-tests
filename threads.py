from threading import Thread


class MyThread(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print("!!! hello ", self.name)


def f(name):
    print("thread: ", name)


#th = Thread(target=f, args=("111",))
th = MyThread("222")
th.start()
th.join()