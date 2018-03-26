# про использование with
import time

class open_file:
    def __init__(self, filename, mode):
        print("init...")
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        print("enter...")
        self.file = open(self.filename, self.mode)
        self.time = time.time()
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"exit...: exc_type={exc_type}, exc_val={exc_val}, exc_tb={exc_tb}")
        self.file.close()

        if exc_type is ZeroDivisionError:
            print("suppress ZeroDivisionError")

        print(f"elapsed time = {time.time() - self.time}")
        return True


fm = open_file('tmp.txt', 'w')
print(type(fm))
with fm as f:
    f.write("test context manager")
    time.sleep(0.12345)
    i = 1/0
    f.write("after 1/0 - не запишется, т.к. все равно произойдет выход")
