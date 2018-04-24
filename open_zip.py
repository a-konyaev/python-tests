import time
from zipfile36 import ZipFile
from itertools import product
import random
import math
import os
import multiprocessing
import concurrent.futures


class ZipArch:
    def __init__(self, folder, file_name):
        self.file_path = os.path.join(folder, file_name)
        self.zip_file = ZipFile(self.file_path)
        self.zip_first_item = self.zip_file.namelist()[0]

    def __del__(self):
        self.zip_file.close()

    def check_pwd(self, pwd):
        try:
            with self.zip_file.open(self.zip_first_item, "r", pwd=pwd.encode()) as f:
                f.read1(1)
            return True
        except Exception as ex:
            return False


class PasswordGenerator:
    symbols = [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
              [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    # [chr(i) for i in range(ord('а'), ord('я')+1)] +\
    # [chr(i) for i in range(ord('А'), ord('Я')+1)]
    # [chr(i) for i in range(ord('0'), ord('9')+1)]

    def __init__(self, pwd_len):
        self.pwd_len = pwd_len

    @staticmethod
    def get_shuffled_symbols():
        symbols_copy = PasswordGenerator.symbols.copy()
        random.shuffle(symbols_copy, random=lambda: float(math.modf(time.time())[0]))
        return symbols_copy

    def go_over_passwords(self, pwd_first_symbol=None):
        if pwd_first_symbol:
            for second_part_tuple in product(PasswordGenerator.symbols, repeat=self.pwd_len - 1):
                yield pwd_first_symbol + ''.join(second_part_tuple)
        else:
            for second_part_tuple in product(PasswordGenerator.symbols, repeat=self.pwd_len):
                yield ''.join(second_part_tuple)


stop_event = multiprocessing.Event()


def run_single_process(folder, file_name, pwd_len, pwd_first_symbol=None):
    za = ZipArch(folder, file_name)
    pg = PasswordGenerator(pwd_len)

    for pwd in pg.go_over_passwords(pwd_first_symbol):
        print(pwd)
        is_valid = za.check_pwd(pwd)
        if is_valid:
            stop_event.set()
            return pwd

        if stop_event.is_set():
            return

    return


def run_multi_process(folder, file_name, pwd_len):
    manager = multiprocessing.Manager()
    manager.Value('password', '')

    shuffled_symbols = PasswordGenerator.get_shuffled_symbols()

    pool = multiprocessing.Pool(processes=4)
    results = [pool.apply_async(run_single_process, (folder, file_name, pwd_len, first_symbol))
               for first_symbol in shuffled_symbols]
    pool.close()
    pool.join()


def run_fork():
    pid = os.fork()
    if pid == 0:
        # child process
        while True:
            print(f"child pid = {os.getpid()}; time = {time.time()}");
            time.sleep(3)
    else:
        # parent process
        print(f"parent pid = {os.getpid()}, fork = {pid}")
        os.wait()


def main():
    folder = r'c:\.my\1'
    file_name = 'test3.zip'
    time_start = time.time()

    # found_password = run_single_process(folder, file_name, 3)
    found_password = run_multi_process(folder, file_name, 3)

    print('password = ', found_password)
    print(f"time elapsed: {int(time.time() - time_start)} sec")


if __name__ == '__main__':
    main()
