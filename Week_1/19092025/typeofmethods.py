class Car:
    # Class attribute to track total cars
    total_cars = 0

    def __init__(self, make, model, mileage):
        self.make = make
        self.model = model
        self.mileage = mileage
        Car.total_cars += 1  # Increment total cars at each instantiation

    # Instance method
    def display_details(self):
        print(f"This is a {self.make} {self.model} with {self.mileage} km mileage.")

    # Class method factory
    @classmethod
    def from_dict(cls, car_data):
        return cls(car_data['make'], car_data['model'], car_data['mileage'])

    # Static method for conversion
    @staticmethod
    def convert_km_to_miles(kilometers):
        return kilometers * 0.621371


# Usage
car1 = Car("Honda", "Civic", 50000)
car2 = Car.from_dict({"make": "Ford", "model": "Figo", "mileage": 75000})

# Instance methods
car1.display_details()
car2.display_details()

# Static method
print(f"100 km is equal to {Car.convert_km_to_miles(100):.2f} miles.")

# Class attribute
print(f"Total cars created: {Car.total_cars}")
