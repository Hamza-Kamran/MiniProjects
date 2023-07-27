import sqlite3

def connect():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title text, author text, year integer, isbn text)")
    conn.commit()
    conn.close()

def get_all():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    lst = cur.fetchall()
    conn.close()
    return lst

def insert(title, author, year, isbn):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO books VALUES (NULL, ?, ?, ?, ?)", (title, author, year, isbn))
    conn.commit()
    conn.close()

def get_books(title="", author="", year="", isbn=""):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE title=? OR author=? OR year=? OR isbn=?", (title, author, year, isbn))
    books = cur.fetchall()
    conn.commit()
    conn.close()
    return books

def delete_book(id):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    conn.close()

def delete_table():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE books")
    conn.commit()
    conn.close()

def update(id, title, author, year, isbn):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("UPDATE books SET title=?, author=?, year=?, isbn=? WHERE id=?", (title, author, year, isbn, id))
    conn.commit()
    conn.close()

connect()
# insert("Hamza has arrived", "Hamza Kamran", 1995, 'BN34567875434567898765')
books = get_books(author="Hamza Kamran")
print(books)
print(get_all())
update(2, "My story", "Afnan Kamran", 2001, 'dsifhuidhsf')
print(get_all())
