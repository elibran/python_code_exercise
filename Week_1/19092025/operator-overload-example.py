class Point:
    """Represents a point in 2D space."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """Defines the behavior for the '+' operator for Point objects."""
        # Creates a new Point object by adding the coordinates of two points
        return Point(self.x + other.x, self.y + other.y)

    def __str__(self):
        """Defines how the object should be represented as a string."""
        # This is called by functions like print() or str()
        return f"Point({self.x}, {self.y})"


# --- Usage Example ---

# Create two Point objects
p1 = Point(1, 2)
p2 = Point(3, 4)

# Use the overloaded '+' operator.
# Behind the scenes, this calls p1.__add__(p2)
p3 = p1 + p2

# Print the points.
# This calls the __str__() method for each object.
print(p1)
print(p2)
print(p3)

# Expected Output:
# Point(1, 2)
# Point(3, 4)
# Point(4, 6)