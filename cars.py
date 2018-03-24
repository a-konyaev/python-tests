import os.path
import csv


class BaseCar:
    # region car_type

    car_type = property()

    @car_type.setter
    def car_type(self, value):
        """vlue must be one of: car, truck, spec_machine"""
        if value not in ["car", "truck", "spec_machine"]:
            raise ValueError(f"car_type have wrong value: {value}; value must be one of [car, truck, spec_machine]")

        self._car_type = value

    @car_type.getter
    def car_type(self):
        return self._car_type

    # endregion

    # region photo_file_name, photo_file_name_ext

    photo_file_name = property()

    @photo_file_name.setter
    def photo_file_name(self, value):
        try:
            self._photo_file_name = value
            self._photo_file_name_ext = os.path.splitext(value)[1]
        except:
            raise ValueError(f"photo_file_name is wrong file name: {value}; it has not extension")

    @photo_file_name.getter
    def photo_file_name(self):
        return self._photo_file_name

    def get_photo_file_ext(self):
        return self._photo_file_name_ext

    # endregion

    def __init__(self, car_type, photo_file_name, brand, carrying):
        self.car_type = car_type
        self.photo_file_name = photo_file_name
        self.brand = brand
        if carrying <= 0:
            raise ValueError(f"car carrying must be more zero: {carrying}")
        self.carrying = carrying

    def get_info(self):
        return f"car_type = {self.car_type}; \
photo_file_name = {self.photo_file_name} (ext = {self.get_photo_file_ext()}); \
brand = {self.brand}; \
carrying = {self.carrying}"


class Truck(BaseCar):
    def __init__(self, photo_file_name, brand, carrying, body_whl):
        super().__init__("truck", photo_file_name, brand, carrying)
        if len(body_whl) == 0:
            self.body_length = 0.0
            self.body_width = 0.0
            self.body_height = 0.0
        else:
            specs = body_whl.split('x')
            self.body_length = float(specs[0])
            self.body_width = float(specs[1])
            self.body_height = float(specs[2])

    def get_body_volume(self):
        """объем кузова в метрах кубических"""
        return self.body_length * self.body_width * self.body_height

    def get_info(self):
        return BaseCar.get_info(self) + \
               f";length x width x height = [{self.body_length} x {self.body_width} x {self.body_height}]; \
volume = {self.get_body_volume()}"


class Car(BaseCar):
    def __init__(self, photo_file_name, brand, carrying, passenger_seats_count):
        super().__init__("car", photo_file_name, brand, carrying)

        if passenger_seats_count < 1:
            raise ValueError("passenger_seats_count must be >= 1")
        self.passenger_seats_count = passenger_seats_count

    def get_info(self):
        return BaseCar.get_info(self) + f"; passenger_seats_count = {self.passenger_seats_count}"


class SpecMachine(BaseCar):
    def __init__(self, photo_file_name, brand, carrying, extra):
        super().__init__("spec_machine", photo_file_name, brand, carrying)
        self.extra = extra

    def get_info(self):
        return BaseCar.get_info(self) + f"; extra = '{self.extra}'"


def get_car_list(csv_filename):
    """
        parse csv with columns:
        car_type;brand;passenger_seats_count;photo_file_name;body_whl;carrying;extra

    :param csv_filename: имя файла
    :return: список автомобилей
    """
    car_list = []

    with open(csv_filename, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            #print(row)

            if len(row) == 0:
                continue

            try:
                car_type = row[0]
                brand = row[1]
                passenger_seats_count = row[2]
                photo_file_name = row[3]
                body_whl = row[4]
                carrying = float(row[5])
                extra = row[6]

                if car_type == "car":
                    car = Car(photo_file_name=photo_file_name, brand=brand, carrying=carrying,
                              passenger_seats_count=int(passenger_seats_count))

                elif car_type == "truck":
                    car = Truck(photo_file_name=photo_file_name, brand=brand, carrying=carrying,
                                body_whl=body_whl)

                elif car_type == "spec_machine":
                    car = SpecMachine(photo_file_name=photo_file_name, brand=brand, carrying=carrying,
                                      extra=extra)

                else:
                    continue

                #print(f"Parse result: {car.get_info()}\n")
                car_list.append(car)

            except Exception as err:
                #print(err)
                #print("\n")
                continue

    return car_list


if __name__ == "__main__":
    # car = Car("car.jpg", "toyota", 756.7, 4)
    # print(car.get_info())
    # print(car.car_type, car.brand, car.photo_file_name, car.carrying, car.passenger_seats_count)
    #
    # truck = Truck("truck.jpg", "KAMAZ-5490-001-T5", 6000, "6.13x3x3.78")
    # print(truck.get_info())
    # print(truck.car_type, truck.brand, truck.photo_file_name, truck.carrying, truck.body_width, truck.body_height, truck.body_length)
    #
    # truck0 = Truck("0.jpg", "0", 1, "")
    # print(truck0.get_info())
    #
    # sm = SpecMachine("tractor.jpg", "JCB", 1500, "супер-трактор!")
    # print(sm.get_info())
    # print(sm.car_type, sm.brand, sm.photo_file_name, sm.carrying, sm.extra)

    for car in get_car_list("coursera_week3_cars.csv"):
        print(car.get_info())