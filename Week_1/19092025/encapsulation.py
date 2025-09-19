class Student:
    def __init__(self, name, marks):
        self.name = name
        # Initialize marks using the setter to apply validation from the start
        self._marks = 0  # Start with a safe default
        self.set_marks(marks) # Call the setter

    def get_marks(self):
        """Returns the student's marks."""
        return self._marks

    def set_marks(self, new_marks):
        """Sets the student's marks only if they are between 0 and 100."""
        if 0 <= new_marks <= 100:
            self._marks = new_marks
            print(f"{self.name}'s marks have been updated to {self._marks}.")
        else:
            print(f"Error: Invalid marks. {new_marks} is not between 0 and 100.")

# --- Testing the Student class ---
student1 = Student("Priya", 85)
print(f"Initial marks: {student1.get_marks()}")

# Try to set valid marks
student1.set_marks(92)
print(f"Current marks: {student1.get_marks()}")

# Try to set invalid marks (too high)
student1.set_marks(105)
print(f"Current marks are still: {student1.get_marks()}")

# Try to set invalid marks (too low)
student1.set_marks(-10)
print(f"Current marks are still: {student1.get_marks()}")