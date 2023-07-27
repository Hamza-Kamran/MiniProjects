import tkinter
from tkinter import *
import backend



# def get_selected_row(event):
#     index = lb.curselection()
#     row = lb.get(index)
#     return row

def on_selection(event):
    index = lb.curselection()
    if index:
        ind, title, author, year, isbn = lb.get(index)
        t1.delete(0, END)
        t1.insert(0, title)
        t2.delete(0, END)
        t2.insert(0, author)
        t3.delete(0, END)
        t3.insert(0, isbn)
        t4.delete(0, END)
        t4.insert(0, year)


def view_all():
    lb.delete(0, END)
    all_books = backend.get_all()
    for index, book in enumerate(all_books):
        lb.insert(END, book)

def search_book():
    lb.delete(0, END)
    rows = backend.get_books(title_string.get(), author_string.get(), year_string.get(), isbn_string.get())
    for row in rows:
        lb.insert(END, row)

def insert_book():
    title = title_string.get()
    author = author_string.get()
    year = int(year_string.get())
    isbn = isbn_string.get()
    backend.insert(title, author, year, isbn)
    view_all()
    lb.select_set(END)
    lb.yview(END)


def update_book():
    id, title, author, year, isbn = lb.get(lb.curselection())
    new_title = title_string.get()
    new_author = author_string.get()
    new_year = year_string.get()
    new_isbn = isbn_string.get()
    backend.update(id, new_title, new_author, new_year, new_isbn)
    view_all()




def delete_entry():
    # row = lb.curselection()
    row = lb.get(lb.curselection())
    backend.delete_book(row[0])
    view_all()

def close():
    tk.destroy()

tk = Tk()

title_string = StringVar()
l1 = Label(tk, text="Title")
l1.grid(row=0, column=0)
t1 = Entry(tk, textvariable=title_string)
t1.grid(row=0, column=1)

author_string = StringVar()
l2 = Label(tk, text="Author")
l2.grid(row=0, column=2)
t2 = Entry(tk, textvariable=author_string)
t2.grid(row=0, column=3)


isbn_string = StringVar()
l3 = Label(tk, text="ISBN")
l3.grid(row=1, column=0)
t3 = Entry(tk, textvariable=isbn_string)
t3.grid(row=1, column=1)

year_string = StringVar()
l4 = Label(tk, text="Year")
l4.grid(row=1, column=2)
t4 = Entry(tk, textvariable=year_string)
t4.grid(row=1, column=3)


lb = Listbox(tk, width=35, height=6, selectmode=tkinter.SINGLE)
lb.grid(row=2, column=0, rowspan=6, columnspan=2)
sb = Scrollbar(tk)
sb.grid(row=2, column=2,rowspan=6)
lb.configure(yscrollcommand=sb.set)
sb.configure(command=lb.yview)
lb.bind('<<ListboxSelect>>', on_selection)


b1 = Button(tk, text="View All", width=15, command=view_all)
b1.grid(row=2, column=3)

b2 = Button(tk, text="Search Book", width=15, command=search_book)
b2.grid(row=3, column=3)

b3 = Button(tk, text="Add Book", width=15, command=insert_book)
b3.grid(row=4, column=3)

b4 = Button(tk, text="Update Book", width=15, command=update_book)
b4.grid(row=5, column=3)

b4 = Button(tk, text="Delete Book", width=15, command=delete_entry)
b4.grid(row=6, column=3)

b4 = Button(tk, text="Close", width=15, command=close)
b4.grid(row=7, column=3)

mainloop()
