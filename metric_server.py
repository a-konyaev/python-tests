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
import asyncio
import re
import time


match_put = re.compile('^put (\S+) (\S+)( (\d+))?$')
match_get = re.compile('^get (\S+|\*)$')

answer_ok = "ok\n\n"
metric_dict = {}


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
        try:
            m = match_put.match(data)
            if m:
                key = m.group(1)
                value = float(m.group(2))
                ts = m.group(4)
                ts = int(time.time()) if ts is None else int(ts)
                res = ClientServerProtocol._process_put(key, value, ts)
                return res

            m = match_get.match(data)
            if m:
                res = ClientServerProtocol._process_get(m.group(1))
                return res

            return ClientServerProtocol._get_error("wrong command")

        except Exception as ex:
            return ClientServerProtocol._get_error("process data failed: ", ex)

    @staticmethod
    def _process_put(key, value, ts):
        print(f'put: key=[{key}]; value=[{value}]; ts=[{ts}]')

        if key not in metric_dict:
            metric_dict[key] = [(ts, value)]
        else:
            value_list = metric_dict[key]
            value_list = ClientServerProtocol._append_value_in_list(value_list, value, ts)
            metric_dict[key] = value_list

        print("metric_dict updated: ", metric_dict)

        return answer_ok

    @staticmethod
    def _append_value_in_list(value_list, value, ts):
        for index, item in enumerate(value_list):
            if item[0] == ts:
                value_list[index] = (ts, value)
                return value_list

        value_list.append((ts, value))
        return sorted(value_list, key=lambda pair: pair[0])

    @staticmethod
    def _process_get(key):
        print(f'get: key=[{key}]')
        answer = 'ok\n'

        if key == '*':
            for item_key, value_list in metric_dict.items():
                answer += ClientServerProtocol._value_list_to_text(item_key, value_list)

        elif key in metric_dict:
            value_list = metric_dict[key]
            answer += ClientServerProtocol._value_list_to_text(key, value_list)

        return answer + '\n'

    @staticmethod
    def _value_list_to_text(key, value_list):
        res = ''
        for pair in value_list:
            val = pair[1]
            ts = pair[0]
            res += f"{key} {val} {ts}\n"
        return res

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


# if __name__ == "__main__":
#     run_server("127.0.0.1", 8888)
