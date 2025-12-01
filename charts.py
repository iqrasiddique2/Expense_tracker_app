import matplotlib.pyplot as plt
from Expense_operations import connect_db

def show_pie_chart():
    conn=connect_db()
    cur=conn.cursor()

    cur.execute('''SELECT categories.Name,SUM(expenses.Amount) FROM expenses
                JOIN categories ON expenses.Category_id=categories.Id
                GROUP BY categories.Name''')
    
    data=cur.fetchall()
    conn.close()


    categories=[]
    amounts=[]

    for row in data:
        categories.append(row[0])
        amounts.append(row[1])

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title("Expenses by Category")
    plt.show()

def show_bar_chart():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT strftime('%m', date) AS month, SUM(amount)
        FROM expenses
        GROUP BY month
    """)

    data = cur.fetchall()
    conn.close()

    months = [row[0] for row in data]
    totals = [row[1] for row in data]

    plt.figure(figsize=(6, 5))
    plt.bar(months, totals)
    plt.title("Monthly Expense Summary")
    plt.xlabel("Month (01-12)")
    plt.ylabel("Total Amount")
    plt.show()
