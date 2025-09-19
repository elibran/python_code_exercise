class Calculator:
    # This single method can act like add(a, b) or add(a, b, c)
    def add(self, a, b, c=0):
        return a + b + c

# Usage demonstration
calc = Calculator()
# Calling it in two "forms"
print(f"Two args: {calc.add(5, 10)}")        # Output: Two args: 15
print(f"Three args: {calc.add(5, 10, 20)}")  # Output: Three args: 35
