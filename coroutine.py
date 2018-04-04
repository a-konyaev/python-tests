# пример генератора
def my_range(max_count):
    count = 0
    while count < max_count:
        yield count
        count += 1


# пример сопрограммы (тот же генератор, но он не производит значениия, а потребляет их):

# суть yield в том, что она как бы хибирнейтит (а стеке) состояние метода/функции (корутины),
# в котором yield был вызван, до тех пор, пока не будет возобновлено выполнение корутины путем вызова метода send
def grep(pattern):
    print("grep start...")
    while True:
        try:
            # тут yield используем для чтения! см. ниже вызов метода send
            line = yield
            if pattern in line:
                print(line)
        except RuntimeError as ex:
            print("catch error: ", ex)
        except GeneratorExit:
            print("grep stop")
            break


# корутина-обертка, которая возвращает внутреннюю корутину
def grep_outer(pattern):
    g = grep(pattern)
    yield from g


for i in my_range(3):
    print(i)

# g = grep("python")
# next(g)
# g.send("ggg")
# g.send("!! python &&&")
# g.throw(RuntimeError, "send error to coroutine")
# g.close()
#g.send("send to closed coroutine")     # вызовет исключение StopIteration

g2 = grep_outer("2")
# особенность: в корутину "2-ого уровня" сперва надо заслать None, иначе ошибка
g2.send(None)   # или вот так: next(g2)
g2.send("123")