import time
import socket


class ClientError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Client:

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        print(f"init: {host}:{port}; timeout={self.timeout}")
        self._init_connection()

    def __del__(self):
        self._close_connection()
        print("destructed")

    def _init_connection(self):
        try:
            self.sock = None
            print("connecting to server...", end='')
            self.sock = socket.create_connection((self.host, self.port), self.timeout)
            print("done")
        except Exception as ex:
            raise ClientError(f"cannot connect to server: {ex}") from ex

    def _close_connection(self):
        if self.sock:
            print("connection closing...", end='')
            self.sock.close()
            print("done")

    def _send(self, command):
        print(f"sending: {command}")
        self.sock.sendall((command + '\n').encode())

        answer = ''
        while True:
            try:
                data = self.sock.recv(1024)
            except Exception as ex:
                raise ClientError("socket read error" + ex) from ex

            if not data:
                break

            answer += data.decode()
            if answer.endswith('\n\n'):
                break

        return answer

    def put(self, key, value, timestamp=None):
        try:
            print(f"put: {key}; {value}; timeout={timestamp}")
            command = self._create_put_command(key, value, timestamp)
            answer = self._send(command)
            print("put answer: ", answer)
        except Exception as ex:
            print("put error: ", ex)
            raise ClientError("put failed") from ex

    @staticmethod
    def _create_put_command(key, value, timestamp=None):
        timestamp = str(int(time.time())) if timestamp is None else timestamp
        return f"put {key} {float(value)} {timestamp}"

    def get(self, key):
        try:
            print(f"get: {key}")
            command = self._create_get_command(key)
            answer = self._send(command)
            print("get answer: ", answer)
            res = self._parse_get_answer(answer)
            return res
        except Exception as ex:
            print("get error: ", ex)
            raise ClientError("get failed") from ex

    @staticmethod
    def _create_get_command(key):
        return f"get {key}"

    def getKey(item):
        return item[0]

    @staticmethod
    def _parse_get_answer(answer):
        if answer.startswith('error'):
            err_msg = answer.split('\n')[1]
            raise ClientError("server return error: ", err_msg)

        if not answer.startswith('ok'):
            raise ClientError("server wrong answer: ", answer)

        body = answer.lstrip('ok\n').rstrip('\n')
        if len(body) == 0:
            return {}

        metrics = body.split('\n')
        if len(metrics) == 0:
            return {}

        res = {}
        for m in metrics:
            m_items = m.split(' ')
            key = m_items[0]
            val = float(m_items[1])
            ts = int(m_items[2])
            if key not in res:
                res[key] = [(ts, val)]
            else:
                l = res[key]
                l.append((ts, val))
                res[key] = sorted(l, key=lambda pair: pair[0])

        return res


# if __name__ == "__main__":
#     try:
#         client = Client("127.0.0.1", 8888, timeout=5)
#
#         client.put("palm.cpu", 0.5, timestamp=1150864247)
#         client.put("palm.cpu", 2.0, timestamp=1150864248)
#         client.put("palm.cpu", 0.5, timestamp=1150864248)
#
#         client.put("eardrum.cpu", 3, timestamp=1150864250)
#         client.put("eardrum.cpu", 4, timestamp=1150864251)
#         client.put("eardrum.memory", 4200000)
#
#         print(client.get("*"))
#     except Exception as err:
#         print('\n', err)
