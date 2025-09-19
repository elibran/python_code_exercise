class Shape:
    """A generic shape that serves as a base class."""
    def area(self):
        """Prints a message indicating the area is not defined."""
        print("I am a generic shape. I don't have an area.")


class Square(Shape):
    """A square that inherits from Shape and calculates its area."""
    def __init__(self, side):
        self.side = side

    # Overriding the parent's area method
    def area(self):
        """Calculates and prints the area of the square."""
        print(f"The area of the square is {self.side * self.side}.")


class Circle(Shape):
    """A circle that inherits from Shape and calculates its area."""
    def __init__(self, radius):
        self.radius = radius
        
    # Overriding the parent's area method
    def area(self):
        """Calculates and prints the area of the circle."""
        print(f"The area of the circle is {3.14 * self.radius ** 2}.")


# --- Polymorphism in action! ---

# Create a list containing objects of different, but related, classes
shapes = [Square(5), Circle(10)]

# Loop through the list and call the same .area() method on each object.
# Each object will respond with its own specific behavior.
for shape in shapes:
    shape.area()