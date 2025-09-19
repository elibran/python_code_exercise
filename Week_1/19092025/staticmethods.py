class MathUtils:
    # Static method for mathematical operations
    @staticmethod
    def add(x, y):
        return x + y

    @staticmethod
    def is_positive(num):
        return num > 0

# Call directly on the class
result = MathUtils.add(5, 10)  # Output: 15
print(f"Result is: {result}")
print(f"Is 10 positive? {MathUtils.is_positive(10)}")
