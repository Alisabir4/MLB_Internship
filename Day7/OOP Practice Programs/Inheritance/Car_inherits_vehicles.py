# This program show how inherit 


class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def start(self):
        print(f"{self.brand} is starting.")


class Car(Vehicle):
    def drive(self):
        print(f"{self.brand} is driving.")


car = Car("Toyota")

print(car.brand)   # Inherited attribute
car.start()        # Inherited method
car.drive()        # Child method