import sqlite3

conn = sqlite3.connect("banking.db")
cur = conn.cursor()

cur.execute("SELECT * FROM customers;")
print(cur.fetchall())

cur.execute("SELECT * FROM bank_accounts;")
print(cur.fetchall())
