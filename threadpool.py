import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


def f(a):
    time.sleep(1)
    return f"[{threading.current_thread().name}] {a} ** {a} = {a ** a}"


with ThreadPoolExecutor(max_workers=3) as pool:
    results = [pool.submit(f, i) for i in range(10)]

    for future in as_completed(results):
        print(future.result())