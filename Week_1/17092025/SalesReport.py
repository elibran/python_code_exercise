class SalesReport:
    def __init__(self, user):
        self.user = user
        self.db_connection = "mysql://user:pass@localhost/sales"
        self.data = []

    def generate(self):
        print(f"Connecting to {self.db_connection}...")
        # Simulating a DB query
        raw_data = [
            {"item": "Laptop", "quantity": 2, "price": 1200},
            {"item": "Mouse", "quantity": 5, "price": 25},
        ]
        
        total_revenue = sum(d["quantity"] * d["price"] for d in raw_data)
        self.data = raw_data
        
        report_content = f"Sales Report for {self.user}\n"
        for item in self.data:
            report_content += f"- Item: {item['item']}, Revenue: ${item['quantity'] * item['price']}\n"
        report_content += f"Total Revenue: ${total_revenue}"

        return report_content

    def export_to_json(self):
        raw_data = [{"item": "Laptop", "quantity": 2, "price": 1200}, {"item": "Mouse", "quantity": 5, "price": 25}]
        total_revenue = sum(d["quantity"] * d["price"] for d in raw_data)
        
        return {"user": self.user, "total_revenue": total_revenue, "items": raw_data}

    def get_raw_data(self):
        return self.data

# --- Example Usage ---
report = SalesReport("admin_user")
print(report.generate())

raw_data_ref = report.get_raw_data()
raw_data_ref.clear()
