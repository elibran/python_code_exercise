def calculate_score(data, index):
    """
    Safely calculates and returns a student's score percentage.
    Handles several potential runtime exceptions.
    """
    try:
        # --- Risky code block ---
        student = data[index]
        marks = student["marks_scored"]
        total = student["total_marks"]
        
        percentage = (marks / total) * 100
        
        return f"Student {student['name']} scored {percentage:.2f}%."

    except IndexError:
        return f"Error: Invalid index {index}. No student record found."
    
    except KeyError as e:
        # The 'as e' part captures the exception object, which is useful for logging.
        return f"Error: Missing key in student record: {e}."
        
    except ZeroDivisionError:
        student_name = data[index].get("name", "Unknown") # Safely get the name
        return f"Error: Total marks for {student_name} is zero. Cannot calculate percentage."
        
    except TypeError:
        student_name = data[index].get("name", "Unknown")
        return f"Error: Invalid data type for marks for {student_name}. Please use numbers."
        
    except Exception as e:
        # A general catch-all for any other unexpected errors.
        return f"An unexpected error occurred: {e}"

# --- Data and Testing ---
student_data = [
    {"name": "Arun", "marks_scored": 87, "total_marks": 100},
    {"name": "Bina", "marks_scored": 90, "total_marks": 0},
    {"name": "Chloe", "marks_scored": "sixty", "total_marks": 100},
    {"name": "David", "marks_scored": 75}
]

print(f"Test 1: {calculate_score(student_data, 0)}")
print(f"Test 2: {calculate_score(student_data, 1)}")
print(f"Test 3: {calculate_score(student_data, 2)}")
print(f"Test 4: {calculate_score(student_data, 3)}")
print(f"Test 5: {calculate_score(student_data, 4)}")