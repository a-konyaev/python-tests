"""
Формат взаимодействия клиента и сервера:

"Передать метрику"
    запрос клиента:
        put <key> <value> <timestamp>\n
    успешный ответ сервера:
        ok\n\n

"Получить значение метрик"
    запрос клиента:
        get <key>\n
    Успешный ответ от сервера:
        ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n
    Если ни одна метрика не удовлетворяет условиям поиска, то вернется ответ:
        ok\n\n

При нарушении формата сервер возвращает ошибку:
    error\nwrong command\n\n
"""
import threading
import asyncio
import re

match_put = re.compile('^put (\S+) (\S+)( (\d+))?$')
match_get = re.compile('^get (\S+|\*)$')


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        print("client connected: ", transport._extra['peername'])
        self.transport = transport

    def data_received(self, data):
        data = data.decode()
        print(f"data received: {data}".replace('\n', '\\n'))
        resp = ClientServerProtocol._process_data(data)
        print(f"answer: {resp}".replace('\n', '\\n'))
        self.transport.write(resp.encode())

    @staticmethod
    def _process_data(data):
        m = match_put.match(data)
        if m:
            print(f'match put: key=[{m.group(1)}]; value=[{m.group(2)}]; ts=[{m.group(4)}]')
            return "ok\n\n"

        m = match_get.match(data)
        if m:
            print(f'match get: key=[{m.group(1)}]')
            return "ok\n\n"

        return ClientServerProtocol._get_error("wrong command")

    @staticmethod
    def _get_error(msg):
        return f"error\n{msg}\n\n"


def run_server(host, port):
    print("server starting...")
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)

    server = loop.run_until_complete(coro)
    print("server started")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    print("server stopping...")
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
    print("server stopped")


if __name__ == "__main__":
    run_server("127.0.0.1", 8888)
