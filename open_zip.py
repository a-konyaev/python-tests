import time
from zipfile36 import ZipFile
from itertools import product
import random
import math
import os
import multiprocessing
import concurrent.futures


folder = r'c:\.my\1'
zip_file_name = 't.zip'
# zip_file_name = 'test3.zip'

first_zip_item = ''
symbols = [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
          [chr(i) for i in range(ord('A'), ord('Z') + 1)]
# [chr(i) for i in range(ord('а'), ord('я')+1)] +\
# [chr(i) for i in range(ord('А'), ord('Я')+1)]
# [chr(i) for i in range(ord('0'), ord('9')+1)]
pwd_len = 6
# stop_event = multiprocessing.Event()


def get_shuffle_symbol_list():
    shuffle_symbols = symbols.copy()
    rand = lambda: float(math.modf(time.time())[0])
    random.shuffle(shuffle_symbols, random=rand)
    return shuffle_symbols


def check_pwd(zip_file, pwd):
    try:
        with zip_file.open(first_zip_item, "r", pwd=pwd.encode()) as f:
            f.read1(1)
        return True
    except:
        return False


def sort_out_pwd(zip_file, pwd_first_part, check_pwd_func):
    print(f"start process: pid={os.getpid()}")

    for second_part_tuple in product(symbols, repeat=pwd_len - 1):
        pwd = pwd_first_part + ''.join(second_part_tuple)
        print(pwd)
        is_valid = check_pwd_func(zip_file, pwd)
        if is_valid:
            print('Password found: ', pwd)
            # stop_event.set()
            return pwd

        # if stop_event.is_set():
        #     return None

    return None


if __name__ == '__main__':
    time_start = time.time()
    zip_file_path = os.path.join(folder, zip_file_name)
    shuffle_symbols = get_shuffle_symbol_list()

    results = []

    zf = ZipFile(zip_file_path)
    first_zip_item = zf.namelist()[0]

    # pp = multiprocessing.Pool(processes=1)
    # results = [pp.apply_async(sort_out_pwd, (zf, first_symbol, check_pwd, stop_event))
    #            for first_symbol in shuffle_symbols]
    #
    # stop_event.wait()
    #
    # pp.close()
    # pp.join()

    executor = concurrent.futures.ProcessPoolExecutor(max_workers=1)
    futures = [
        executor.submit(sort_out_pwd, zf, first_symbol, check_pwd)
        for first_symbol in shuffle_symbols
    ]

    zf.close()

    time_elapsed = time.time() - time_start
    print("time elapsed: ", time_elapsed)

    # if pwd_founded:
    #     print("!!! password found: ", pwd_founded)
    # else:
    #     print("password now found :(")


# !!! делать через форк-и