# пример того, как одновременно обрабатывать несколько запросов без потоков и тредов
# т.е. неблокирующий ввод/вывод или мультиплексирование ввода/вывода

# вместо select.epoll-ов можно использовать современные фреймворки, которые все это скрывают внутри, например:
# Tornado - использует внутри generators api
# Asyncio - современный и mainstream-овый, идея реализации внутри, как у Tornado, но лучше

import socket
import select


sock = socket.socket()
sock.bind(("", 10001))
sock.listen()

conn1, addr1 = sock.accept()
conn2, addr2 = sock.accept()

# переводим соединения в неблокирующий режим.
# это равносильно тому, как если бы мы сказали conn.settimeout(0), чтобы вызов conn.recv не блокировался,
# даже если данных еще нет
conn1.setblocking(0)
conn2.setblocking(0)

# работает только в линуксе, в винде ругается
epoll = select.epoll()

# подписываемся на события записи и чтения для файловых дескрипторов, которые соотв. соединениям
epoll.register(conn1.fileno(), select.EPOLLIN | select.EPOLLOUT)
epoll.register(conn2.fileno(), select.EPOLLIN | select.EPOLLOUT)

conn_map = {
    conn1.fileno(): conn1,
    conn2.fileno(): conn2,
}

# цикл обработки событий
while True:
    events = epoll.poll(1)
    for fileno, event in events:
        if event & select.EPOLLIN:
            data = conn_map[fileno].recv(1024)
            print(data.decode())
        elif event & select.EPOLLOUT:
            conn_map[fileno].send(b"Hi! I an server!")