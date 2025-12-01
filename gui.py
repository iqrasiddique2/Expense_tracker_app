import customtkinter as ctk
from Expense_operations import add_expense, fetch_all_expenses, delete_expense, update_expense, get_monthly_total
from charts import show_bar_chart,show_pie_chart
import tkinter as tk
from tkinter import ttk
import sqlite3

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Expense Tracker App")
app.geometry("900x550")

main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True)

left_frame = ctk.CTkFrame(main_frame, width=300, corner_radius=10)
left_frame.pack(side="left", fill="y", padx=10, pady=10)

right_frame = ctk.CTkFrame(main_frame, corner_radius=10)
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

form_title = ctk.CTkLabel(left_frame, text="Add Expense", font=("Arial", 20, "bold"))
form_title.pack(pady=(10, 30))

amount_label = ctk.CTkLabel(left_frame, text="Amount:")
amount_label.pack(anchor="w", padx=10)

amount_entry = ctk.CTkEntry(left_frame, placeholder_text="Enter amount")
amount_entry.pack(fill="x", padx=10, pady=5)

category_label = ctk.CTkLabel(left_frame, text="Category:")
category_label.pack(anchor="w", padx=10)

def fetch_categories():
    conn = sqlite3.connect("expense.db")
    cur = conn.cursor()
    cur.execute("SELECT Name FROM categories")
    data = []
    for row in cur.fetchall():
        data.append(row[0])
    conn.close()
    return data

category_options = fetch_categories()

category_dropdown = ctk.CTkOptionMenu(left_frame, values=category_options)
category_dropdown.pack(fill="x", padx=10, pady=5)

date_label = ctk.CTkLabel(left_frame, text="Date (YYYY-MM-DD):")
date_label.pack(anchor="w", padx=10)

date_entry = ctk.CTkEntry(left_frame, placeholder_text="2025-11-20")
date_entry.pack(fill="x", padx=10, pady=5)

note_label = ctk.CTkLabel(left_frame, text="Note:")
note_label.pack(anchor="w", padx=10)

note_entry = ctk.CTkEntry(left_frame, placeholder_text="Optional")
note_entry.pack(fill="x", padx=10, pady=5)

def handle_add_expense():
    amount = amount_entry.get()
    category = category_dropdown.get()
    date = date_entry.get()
    note = note_entry.get()

    amount = amount.strip()
    if amount == "":
        return
    try:
        amount_val = float(amount)
    except:
        return

    add_expense(amount_val, category, date, note)

    amount_entry.delete(0, "end")
    date_entry.delete(0, "end")
    note_entry.delete(0, "end")

    load_expense_into_table()
    update_monthly_total()

add_button = ctk.CTkButton(left_frame, text="Add Expense", command=handle_add_expense)
add_button.pack(pady=20)

columns = ("ID", "Amount", "Category", "Date", "Note")

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", font=("Arial", 12), rowheight=30)
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

tree = ttk.Treeview(right_frame, columns=columns, show="headings")

tree.heading("ID", text="ID")
tree.heading("Amount", text="Amount")
tree.heading("Category", text="Category")
tree.heading("Date", text="Date")
tree.heading("Note", text="Note")

tree.column("ID", width=50, anchor="center")
tree.column("Amount", width=100, anchor="center")
tree.column("Category", width=130, anchor="center")
tree.column("Date", width=130, anchor="center")
tree.column("Note", width=250, anchor="center")

tree.pack(fill="both", expand=True, padx=10, pady=10)

def load_expense_into_table():
    for row in tree.get_children():
        tree.delete(row)

    expenses = fetch_all_expenses()

    for expense in expenses:
        tree.insert("", tk.END, values=expense)

def delete_selected_expense():
    selected_item = tree.selection()
    if not selected_item:
        return

    values = tree.item(selected_item)["values"]
    expense_id = values[0]
    delete_expense(expense_id)

    load_expense_into_table()
    update_monthly_total()

delete_button = ctk.CTkButton(left_frame, text="Delete Expense", fg_color="red", command=delete_selected_expense)
delete_button.pack(pady=10)

selected_expense_id = None

def on_row_select(event):
    global selected_expense_id
    selected = tree.selection()
    if not selected:
        return

    values = tree.item(selected)["values"]
    selected_expense_id = values[0]

    amount_entry.delete(0, "end")
    amount_entry.insert(0, values[1])

    category_dropdown.set(values[2])

    date_entry.delete(0, "end")
    date_entry.insert(0, values[3])

    note_entry.delete(0, "end")
    note_entry.insert(0, values[4])

tree.bind("<<TreeviewSelect>>", on_row_select)

def update_selected_expense():
    global selected_expense_id

    if selected_expense_id is None:
        return

    amount = amount_entry.get()
    category = category_dropdown.get()
    date = date_entry.get()
    note = note_entry.get()

    try:
        amount_val = float(amount)
    except:
        return

    update_expense(selected_expense_id, amount_val, category, date, note)

    load_expense_into_table()
    update_monthly_total()

update_button = ctk.CTkButton(left_frame, text="Update Expense", command=update_selected_expense)
update_button.pack(pady=10)

total_label = ctk.CTkLabel(left_frame, text="Total this month: ₹0", font=("Arial", 14, "bold"))
total_label.pack(pady=10)

def update_monthly_total():
    total = get_monthly_total()
    total_label.configure(text=f"Total this month: ₹{total}")

load_expense_into_table()
update_monthly_total()



# chartsbutton
chart_btn1 = ctk.CTkButton(left_frame, text="Category Pie Chart", command=show_pie_chart)
chart_btn1.pack(pady=10)

chart_btn2 = ctk.CTkButton(left_frame, text="Monthly Bar Chart", command=show_bar_chart)
chart_btn2.pack(pady=10)

def start_app():
    app.mainloop()
