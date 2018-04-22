import time
from zipfile36 import ZipFile
from itertools import product
import random
import math
import os
import multiprocessing
import concurrent.futures


folder = r'c:\Users\user\Desktop\github\1'
zip_file_name = 'file.zip'
# zip_file_name = 'test3.zip'
zip_file = None
first_zip_item = ''

symbols = [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
          [chr(i) for i in range(ord('A'), ord('Z') + 1)]
# [chr(i) for i in range(ord('а'), ord('я')+1)] +\
# [chr(i) for i in range(ord('А'), ord('Я')+1)]
# [chr(i) for i in range(ord('0'), ord('9')+1)]
pwd_len = 3

stop_event = multiprocessing.Event()


def get_shuffle_symbol_list():
    symbols_copy = symbols.copy()
    rand = lambda: float(math.modf(time.time())[0])
    random.shuffle(symbols_copy, random=rand)
    return symbols_copy


def check_pwd(pwd):
    try:
        with zip_file.open(first_zip_item, "r", pwd=pwd.encode()) as f:
            f.read1(1)
        return True
    except Exception as ex:
        return False


def sort_out_pwd(pwd_first_part):
    # print(f"start process: pid={os.getpid()}")

    for second_part_tuple in product(symbols, repeat=pwd_len - 1):
        pwd = pwd_first_part + ''.join(second_part_tuple)
        print(pwd)
        is_valid = check_pwd(pwd)
        if is_valid:
            print('Password found: ', pwd)
            stop_event.set()
            return pwd

        if stop_event.is_set():
            return None

    return None


if __name__ == '__main__':
    shuffle_symbols = get_shuffle_symbol_list()

    zip_file_path = os.path.join(folder, zip_file_name)
    zip_file = ZipFile(zip_file_path)
    first_zip_item = zip_file.namelist()[0]

    time_start = time.time()
    results = []

    zip_file.close()

    time_elapsed = time.time() - time_start
    print("time elapsed: ", time_elapsed)

    # if pwd_founded:
    #     print("!!! password found: ", pwd_founded)
    # else:
    #     print("password now found :(")