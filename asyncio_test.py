import asyncio
import time


# тут используем декоратор и корутину asyncio.sleep
@asyncio.coroutine
def test():
    for i in range(3):
        print("test: iter %r" % i)
        yield from asyncio.sleep(1.0)


# это "современный" аналог test(), но здесь уже используем синтаксич. сахар от python3
async def test2():
    for i in range(3):
        print("test2: iter %r" % i)
        await asyncio.sleep(3.0)


# пример использования asyncio.Future (аналог cuncurrent.futures.Future)
async def slow(future):
    await asyncio.sleep(1.0)
    future.set_result("future is done!")


def sync_func():
    print("sync_func starting...")
    time.sleep(2)
    return "sync_func done!"


async def call_sync(loop=None):
    # run_in_executor - запускает переданную функцию в отдельном потоке, а не как корутину
    # (которые выполняются последовательно друг за другом, переключая контекс тогда, когда текущая корутина скажет await)
    future = loop.run_in_executor(None, sync_func)
    response = await future
    print("sync_func result: " + response)


loop = asyncio.get_event_loop()

#loop.run_until_complete(test())
#loop.run_until_complete(test2())

future = asyncio.Future()
# asyncio.ensure_future(slow(future))
# loop.run_until_complete(future)
# print(future.result())

# tasks = [loop.create_task(test()), loop.create_task(test2())]
# print("------1")
# loop.run_until_complete(asyncio.wait(tasks))
# print("------2")
# loop.run_until_complete(loop.create_task(test2()))
# print("------3")
# loop.run_until_complete(asyncio.gather(test(), test2()))

loop.run_until_complete(asyncio.gather(call_sync(loop=loop), test()))

loop.close()