import asyncio


async def echo_client(message, loop):
    reader, writer = await asyncio.open_connection("127.0.0.1", 10001, loop=loop)

    print("send: %r" % message)
    writer.write(message.encode())
    writer.close()


loop = asyncio.get_event_loop()
msg = "hi asyncio!!!"
loop.run_until_complete(echo_client(msg, loop))
loop.close()