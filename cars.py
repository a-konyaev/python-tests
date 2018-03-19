import os.path


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
        return f"""
car_type = {self.car_type}; 
photo_file_name = {self.photo_file_name} (ext = {self.get_photo_file_ext()}); 
brand = {self.brand};
carrying = {self.carrying}"""


class Truck(BaseCar):
    def __init__(self, photo_file_name, brand, carrying, body_spec):
        super().__init__("truck", photo_file_name, brand, carrying)
        if len(body_spec) == 0:
            self.body_length = 0.0
            self.body_width = 0.0
            self.body_height = 0.0
        else:
            specs = body_spec.split('x')
            self.body_length = float(specs[0])
            self.body_width = float(specs[1])
            self.body_height = float(specs[2])

    def get_body_volume(self):
        """объем кузова в метрах кубических"""
        return self.body_length * self.body_width * self.body_height

    def get_info(self):
        return BaseCar.get_info(self) + \
               f""";
length x width x height = [{self.body_length} x {self.body_width} x {self.body_height}]"""


class Car(BaseCar):
    def __init__(self, photo_file_name, brand, carrying, passenger_seats_count):
        super().__init__("car", photo_file_name, brand, carrying)

        if passenger_seats_count < 1:
            raise ValueError("passenger_seats_count must be >= 1")
        self.passenger_seats_count = passenger_seats_count


class SpecMachine(BaseCar):
    def __init__(self, photo_file_name, brand, carrying, extra):
        super().__init__("spec_machine", photo_file_name, brand, carrying)
        self.extra = extra

    def get_info(self):
        return BaseCar.get_info(self) + \
               f""";
extra = '{self.extra}'"""


if __name__ == "__main__":
    car = Car("car.jpg", "toyota", 800, 4)
    print(car.get_info())

    truck = Truck("truck.jpg", "KAMAZ-5490-001-T5", 6000, "6.13x3x3.78")
    print(truck.get_info())

    sm = SpecMachine("tractor.jpg", "JCB", 1500, "супер-трактор!")
    print(sm.get_info())