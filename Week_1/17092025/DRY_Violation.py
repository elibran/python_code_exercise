"""
DRY_Violation.py
Deliberate DRY violation: repeated validation logic in both methods.
"""
class CustomerService:
    def createCustomer(self, name: str, email: str, phone: str) -> None:
        # Repeated validation block (❌)
        if not email or "@" not in email:
            raise ValueError("Invalid email format.")
        if not phone or len(phone) != 10:
            raise ValueError("Invalid phone number format.")
        print(f"Creating customer: {name}")
        # ... database logic to save new customer

    def updateCustomer(self, customerId: int, email: str, phone: str) -> None:
        # Repeated validation block (❌)
        if not email or "@" not in email:
            raise ValueError("Invalid email format.")
        if not phone or len(phone) != 10:
            raise ValueError("Invalid phone number format.")
        print(f"Updating customer: {customerId}")
        # ... database logic to update customer

if __name__ == "__main__":
    svc = CustomerService()
    svc.createCustomer("Alice", "alice@example.com", "1234567890")
    svc.updateCustomer(42, "bob@example.com", "0987654321")
