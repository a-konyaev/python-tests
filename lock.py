import threading


# мьютексы
a = threading.RLock()
b = threading.RLock()
m = threading.RLock

# условная переменная (чтобы сипользовать wait и notify)
cond = threading.Condition(m)

def foo():
    # критическая секция через with
    with m:
        pass

    # получение блокировок вручную
    try:
        a.acquire()
        b.acquire()
    finally:
        a.release()
        b.release()


