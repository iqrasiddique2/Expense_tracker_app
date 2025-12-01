import sqlite3

def connect_db():
    conn=sqlite3.connect("expense.db")
    return conn

def setup_tables():
    conn=connect_db()
    cur=conn.cursor()


    cur.execute('''CREATE TABLE IF NOT EXISTS categories(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS expenses(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Amount REAL NOT NULL,
                Category_id INTEGER,
                date TEXT NOT NULL,
                note TEXT,
                FOREIGN KEY (Category_id) REFERENCES categories(Id))''')
    conn.commit()
    conn.close()
    print("Database and tables created successfully!!")

def insert_default_categories():
    conn=connect_db()
    cur=conn.cursor()

    default_categories=[ ("Food",),
        ("Travel",),
        ("Shopping",),
        ("Bills",),
        ("Groceries",),
        ("Medical",),
        ("Entertainment",),
        ("Education",),
        ("Savings",),
        ("Miscellaneous",)]
    
    cur.execute("SELECT COUNT(*) FROM categories")
    count=cur.fetchone()[0]

    if count==0:
        cur.executemany("INSERT INTO categories (Name) VALUES (?)",default_categories)
        conn.commit()
        print("Default categories inserted!!")
    else:
        print("Categories already exist!!")
    conn.close()