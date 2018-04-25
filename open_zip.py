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


def run_single_process(folder, file_name, pwd_len, pwd_first_symbol, pwd_proxy):
    pid = os.getpid()

    za = ZipArch(folder, file_name)
    pg = PasswordGenerator(pwd_len)

    for pwd in pg.go_over_passwords(pwd_first_symbol):
        # print(pid, pwd)

        is_valid = za.check_pwd(pwd)
        if is_valid:
            stop_event.set()
            pwd_proxy.value = pwd
            return pwd

        if stop_event.is_set():
            return

    return


def run_multi_process(folder, file_name, pwd_len, process_count):
    manager = multiprocessing.Manager()
    pwd_proxy = manager.Value('password', '')
    # check_count = manager.Value('check_count', 0, lock=True)

    # first_symbols = PasswordGenerator.get_shuffled_symbols()
    first_symbols = PasswordGenerator.symbols

    # pool = multiprocessing.Pool(processes=process_count)

    # for first_symbol in first_symbols:
    #     pool.apply_async(run_single_process, (folder, file_name, pwd_len, first_symbol, pwd_proxy))

    index = 0
    while True:
        chunk = first_symbols[index:index + process_count]
        if len(chunk) == 0:
            break

        print('process: ', chunk)
        index += process_count

        processes = [multiprocessing.Process(
            target=run_single_process,
            args=(folder, file_name, pwd_len, first_symbol, pwd_proxy,))
            for first_symbol in chunk]

        for p in processes:
            p.start()

        for p in processes:
            p.join()


    # pool.close()
    # pool.join()

    return pwd_proxy.value


def main():
    folder = r'c:\.my\1'
    pwd_len = 6
    # file_name = f'test{pwd_len}.zip'
    file_name = 't.zip'

    time_start = time.time()

    found_password = run_multi_process(folder, file_name, pwd_len, process_count=8)

    print('password = ', found_password)
    print(f"time elapsed: {int(time.time() - time_start)} sec")


if __name__ == '__main__':
    main()
