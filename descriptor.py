# дескриптор переопределяет поведение при обращении к атрибуту
# получается, это те же гетеры и сетеры

from abc import ABCMeta, abstractclassmethod


class Descriptor:
    # instance - сюда будет передан obj
    # owner - сюда будет передан Class
    def __get__(self, instance, owner):
        print(f'get: instance={type(instance)}, owner={type(owner)}')

    def __set__(self, instance, value):
        print('set')

    def __delete__(self, instance):
        print('delete')

    @property
    def test(self):
        pass


class BaseClass(metaclass=ABCMeta):
    '''
    пример применения мета-класса (класс, который создает объекты других классов)
    '''

    @abstractclassmethod
    def abs_method(self):
        pass


class Class(BaseClass):
    attr = Descriptor()
    __slots__ = ['a1']

    def __init__(self):
        self.a1 = '111'

    def abs_method(self):
        '''необходимо реализовать абстрактный метод, иначе будет ошибка, правда в рантайме'''
        pass


obj = Class()
obj.attr
obj.attr = 10
del obj.attr

print(obj.a1)
del obj.a1

# вызывает исключение, если не закоментировать __slots__, т.к. в нем перечисляем ровно тот набор атрибутов,
# которые есть у класса, и выходить за рамки этого набора (добавлять новые) нельзя
#obj.a2 = 111

