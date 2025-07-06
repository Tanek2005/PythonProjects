from flask import Flask, render_template, redirect
import sqlite3
from recipt_functions import extract_pdf_text, image_to_text, query, query_values

text = image_to_text("receiptScan/pdfs/receipt.jpg")
data = query_values(text)

items = ",".join(data["items"]).replace("'", "''")
quantity = ",".join(data["quantity"]).replace("'", "''")
store_name = data["store_name"].replace("'", "''")
total_amount = data.get("total_amount")
date = data["date_of_transaction"].replace("'", "''")
user_id = 2

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT
)
""")

cursor.execute(f"""
INSERT OR IGNORE INTO users(id, username, password)
VALUES ({user_id}, 'testuser', 'testpassword')
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    items TEXT,
    quantity TEXT,
    store_name TEXT,
    total_amount TEXT,
    date TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

if total_amount is None or total_amount == "NULL":
    total_amount_value = "NULL"
else:
    total_amount_value = f"'{total_amount}'"

cursor.execute(f"""
INSERT INTO receipts (user_id, items, quantity, store_name, total_amount, date)
VALUES (
    {user_id},
    '{items}',
    '{quantity}',
    '{store_name}',
    {total_amount_value},
    '{date}'
)
""")

print("*******")
conn.commit()
conn.close()