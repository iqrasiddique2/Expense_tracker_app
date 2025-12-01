from database import connect_db

def add_expense(Amount,category,date,note):
    conn=connect_db()
    cur=conn.cursor()

    cur.execute("SELECT Id FROM categories WHERE Name=?",(category,))
    result=cur.fetchone()

    if result is None:
        conn.close()
        raise ValueError("Invalid category selected")
    
    Category_id=result[0]

    cur.execute('''INSERT INTO expenses (Amount,Category_id,date,note) VALUES(?,?,?,?)''',(Amount,Category_id,date,note)
               )
    conn.commit()
    conn.close()

def fetch_all_expenses():
    conn=connect_db()
    cur=conn.cursor()

    cur.execute('''SELECT expenses.Id,expenses.Amount,
                   categories.Name,expenses.date,
                   expenses.note FROM expenses 
                   JOIN categories ON expenses.Category_id=categories.Id''')
    data=cur.fetchall()
    conn.close()
    return data

def delete_expense(expense_id):
    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM expenses WHERE Id = ?", (expense_id,))
        conn.commit()

        if cur.rowcount == 0:
            print("No expense found with that id.")
        else:
            print("Expense deleted successfully!")

    except Exception as e:
        print("Error deleting expense:", e)

    finally:
        conn.close()

def update_expense(expense_id, amount, category, date, note):
    conn=connect_db()
    cur=conn.cursor()

    cur.execute("SELECT Id FROM categories WHERE Name=?",(category,))
    result=cur.fetchone()

    if result is None:
        print("Category not found")
        conn.close()
        return
    
    category_id=result[0]

    cur.execute('''UPDATE expenses SET Amount=?,Category_id=?,date=?,note=? WHERE Id=?''',(amount,category_id,date,note,expense_id))
    conn.commit()
    conn.close()


def get_monthly_total():
    conn=connect_db()
    cur=conn.cursor()

    cur.execute("SELECT SUM(Amount) FROM expenses WHERE strftime('%m',date)=strftime('%m','now')")
    total=cur.fetchone()[0]
    conn.close()

    if total:
        return total
    else:
        return 0