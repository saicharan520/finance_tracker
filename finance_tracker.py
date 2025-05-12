import sqlite3
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# === Logging setup ===
logging.basicConfig(filename='finance_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# === Database setup ===
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL
    )
''')
conn.commit()

# === Core functionality ===
def add_transaction(t_type, amount, category):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO transactions (type, amount, category, date) VALUES (?, ?, ?, ?)",
                   (t_type, amount, category, date))
    conn.commit()
    logging.info(f"{t_type.capitalize()} of {amount} for {category}")
    messagebox.showinfo("Success", f"{t_type.capitalize()} added successfully.")

def plot_report():
    cursor.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type")
    data = cursor.fetchall()

    if not data:
        messagebox.showwarning("No Data", "No transactions available for reporting.")
        return
        
    types = [row[0].capitalize() for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(5, 4))
    plt.bar(types, amounts, color=['green', 'red'])
    plt.title("Finance Summary")
    plt.ylabel("Amount")
    plt.grid(True)
    plt.show()

# === GUI functionality ===

def submit_income():
    try:
        amount = float(entry_amount.get())
        category = entry_category.get().strip()
        if not category:
            raise ValueError("Category is empty")
        add_transaction("income", amount, category)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid amount and category.")

def submit_expense():
    try:
        amount = float(entry_amount.get())
        category = entry_category.get().strip()
        if not category:
            raise ValueError("Category is empty")
        add_transaction("expense", amount, category)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid amount and category.")  

# === Build GUI ===
root = tk.Tk()
root.title("Finance Tracker")
root.geometry("300x200")

tk.Label(root, text="Amount:").grid(row=0, column=0, padx=10, pady=5)
entry_amount = tk.Entry(root)
entry_amount.grid(row=0, column=1)

tk.Label(root, text="Category:").grid(row=1, column=0, padx=10, pady=5)
entry_category = tk.Entry(root)
entry_category.grid(row=1, column=1)

tk.Button(root, text="Add Income", command=submit_income).grid(row=2, column=0, pady=10)
tk.Button(root, text="Add Expense", command=submit_expense).grid(row=2, column=1, pady=10)
tk.Button(root, text="Show Report", command=plot_report).grid(row=3, columnspan=2, pady=10)

root.mainloop()
conn.close()
