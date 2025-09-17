# The final, well-structured class

class Employee:
    """
    Represents an employee with a name, ID, and salary.
    """

    # Solution 3: A proper constructor to ensure valid object creation.
    def __init__(self, employee_id, name, initial_salary):
        # Solution 1: Use "private" attributes (by convention with a leading underscore)
        # to encourage encapsulation and add validation logic.
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise ValueError("Employee ID must be a positive integer.")
        self._employee_id = employee_id

        if not name or not isinstance(name, str):
            raise ValueError("Employee name must be a non-empty string.")
        # Solution 2: Use clear, descriptive names.
        self._name = name

        # Use a setter method during initialization to ensure validation is applied.
        self.set_salary(initial_salary)

    # --- Public Methods (API) ---

    def get_employee_id(self):
        """Returns the employee's ID."""
        return self._employee_id

    def get_name(self):
        """Returns the employee's name."""
        return self._name

    def get_salary(self):
        """Returns the employee's current salary."""
        return self._salary

    def set_salary(self, new_salary):
        """Sets the employee's salary after validating it."""
        if not isinstance(new_salary, (int, float)) or new_salary < 0:
            raise ValueError("Salary cannot be negative.")
        self._salary = new_salary

    # Solution 4: Remove the magic number by accepting it as a parameter.
    def apply_raise(self, percentage):
        """Applies a raise to the salary based on a percentage."""
        if not 0 < percentage < 1:
            raise ValueError("Percentage must be a decimal between 0 and 1 (e.g., 0.05 for 5%).")
        
        new_salary = self._salary * (1 + percentage)
        self.set_salary(new_salary) # Re-use the setter to maintain validation

    # Solution 5: Use the __str__ method to provide a string representation.
    # This separates data from presentation.
    def __str__(self):
        """Returns a user-friendly string representation of the employee."""
        return f"ID: {self._employee_id}, Name: {self._name}, Salary: ${self._salary:,.2f}"

# --- Example Usage ---
try:
    # Object is created in a single, valid step.
    emp1 = Employee(102, "Abinash Mishra", 400000)

    # You can't directly set a negative salary. This will raise a ValueError.
    # emp1.set_salary(-1000) 

    emp1.apply_raise(0.05) # The purpose of 0.05 is now clear from the parameter name.

    # The code that USES the object decides what to do with the string.
    print(emp1) # The __str__ method is called automatically by print().

except ValueError as e:
    print(f"Error: {e}")