"""
DRY_Complied.py
DRY-compliant: extract validation into a single, authoritative place.
"""
def validateContactInfo(email: str, phone: str) -> None:
    if not email or "@" not in email:
        raise ValueError("Invalid email format.")
    if not phone or len(phone) != 10:
        raise ValueError("Invalid phone number format.")

class CustomerService:
    def createCustomer(self, name: str, email: str, phone: str) -> None:
        validateContactInfo(email, phone)  # ✅ single source of truth
        print(f"Creating customer: {name}")
        # ... database logic

    def updateCustomer(self, customerId: int, email: str, phone: str) -> None:
        validateContactInfo(email, phone)  # ✅ single source of truth
        print(f"Updating customer: {customerId}")
        # ... database logic

# Optional: shared util module could hold validateContactInfo for use across services.

if __name__ == "__main__":
    svc = CustomerService()
    svc.createCustomer("Charlie", "charlie@example.com", "1112223333")
    svc.updateCustomer(7, "dana@example.com", "4445556666")
