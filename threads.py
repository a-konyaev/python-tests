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

# GIL - блокировка, которая используется только при переключении между тредами.
# процессы - выполняются полностью независимо!

# треды выполняются внутри одного общего процесса и соотв. на одном ядре процессора