
class ProblematicEmployee:
    name = ""
    employee_id = 0
    sal = 0.0

    def give_raise(self):
        self.sal = self.sal * 1.05

    def print_details_to_console(self):
        print(f"ID: {self.employee_id}, Name: {self.name}, Salary: {self.sal}") # type: ignore

# --- Example Usage ---
emp = ProblematicEmployee()

# We have to set data manually after creating the object
emp.name = "Abinash Mishra"
emp.employee_id = 101
emp.sal = -50000

emp.print_details_to_console()