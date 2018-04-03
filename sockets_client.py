import socket
import time


# sock = socket.socket()
# sock.connect(("127.0.0.1", 10001))
#
# # or shorted:
# #sock = socket.create_connection(("127.0.0.1", 10001))
#
#
# sock.sendall(b"hi! " + str(time.time()).encode())
# sock.close()

try:
    # в create_connection параметр 5 (сек) - это таймаут на подключение к серверу
    with socket.create_connection(("127.0.0.1", 10001), 5) as sock:
        # таймаут на чтение
        sock.settimeout(2)

        #time.sleep(6)

        try:
            sock.sendall(b"hi!!! " + str(time.time()).encode())
        except socket.timeout:
            print("send data timeout")
        except socket.error as ex:
            print("send data error: ", ex)

except socket.error as ex:
    print("connection timeout: ", ex)