import unittest
from cars import Car
from unittest.mock import patch


class MyTestCase(unittest.TestCase):
    # вызывается перед каждым тестом
    def setUp(self):
        print('test setUp')
        self.car = Car("car.jpg", "toyota", 756.7, 4)

    # вызывается после каждого теста
    def tearDown(self):
        print('test tearDown')

    # def test_something(self):
    #     print('run test: test_something')
    #     self.assertEqual(True, True)

    def mocked_get_info(self):
        return "???"

    # заменяем метод get_info класса Car из модуля cars на свою заглушку
    @patch('cars.Car.get_info', mocked_get_info)
    def test_get_info(self):
        print('run test: test_get_info')
        self.assertEqual(self.car.get_info(), "???")


if __name__ == '__main__':
    unittest.main()
