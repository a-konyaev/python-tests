import socket
import threading


# без контекст. менеджера
# sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# sock.bind(("127.0.0.1", 10001))
# sock.listen(socket.SOMAXCONN)
#
# conn, addr = sock.accept()
# while True:
#     data = conn.recv(1024)
#     if not data:
#         break
#
#     print("receive: ", data.decode())
#
# conn.close()
# sock.close()

def process_request(conn, addr):
    print("connected client: ", addr)

    # если в сокет не поступит данных в течение 5 сек, то будет ошибка
    conn.settimeout(5)

    with conn:
        while True:
            data = None
            try:
                data = conn.recv(1024)
            except:
                print("timeout!")
                break

            if not data:
                break

            print("receive: ", data.decode())


# с использованием контекст. менеджера
with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
    sock.bind(("127.0.0.1", 10001))
    sock.listen(socket.SOMAXCONN)

    while True:
        # accept можно было бы запускать в нескольких отдельных процессах, чтобы повысить производительность
        conn, addr = sock.accept()

        # обработка запроса в треде
        th = threading.Thread(target=process_request, args=(conn, addr))
        th.start()

