import streamlit as st
import sqlite3
import pandas as pd

#DB
conn=sqlite3.connect("book.db")
cursor=conn.cursor()
conn.execute('''
CREATE TABLE IF NOT EXISTS BOOKS(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    TITLE TEXT NOT NULL,
    author TEXT,
    genre TEXT
)
''')
conn.commit()
conn.close()

#CRUD
def add_book(title, author, genre):
    conn = sqlite3.connect("book.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books(title,author,genre) VALUES(?,?,?)",
        (title, author, genre)
    )
    conn.commit()
    conn.close()

    st.write(f"Book [{title}] added")

def list_books():
    conn = sqlite3.connect("book.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    conn.close()

    if not books:
        st.write("No book")
        return
    st.write("Book List")
    for book in books:
        st.write(f"{book[0]}. {book[1]} (author:{book[2]}, genre:{book[3]})")
        
def update_book(book_id,new_title,new_author,new_genre):
    conn=sqlite3.connect('book.db')
    cursor=conn.cursor()
    cursor.execute("UPDATE books SET title=?,author=?,genre=? WHERE id=?",
                   (new_title,new_author,new_genre,book_id))            
    conn.commit()
    conn.close()
    st.write(f"Book ID {book_id} updated successfully")

def delete_book(book_id):
    conn=sqlite3.connect("book.db")
    cursor=conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=?",(book_id,))
    conn.commit()
    conn.close()
    st.write(f"Book ID {book_id} deleted successfully")


#UI
st.title("📚 Book Manager")
st.caption("本の追加・一覧表示・更新・削除ができる簡易管理アプリ")

keyword = st.text_input("Search")
if keyword.strip():
    conn = sqlite3.connect("book.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM books WHERE title LIKE ?",
        ('%' + keyword + '%',)
    )
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["ID","Title","Author","Genre"])
    st.dataframe(df)
    conn.close()

menu = st.selectbox(
    "Choose menu",
    ["Add Book", "Book List", "Update Book", "Delete Book"]
)

if menu == "Add Book":
    title = st.text_input("Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    if st.button("Add"):
     if title.strip():
        add_book(title,author,genre)
        st.success("Book added")
     else:
        st.warning("Title required")

elif menu == "Book List":
    list_books()

elif menu == "Update Book":
    book_id = st.number_input("Book ID")
    new_title = st.text_input("New Title")
    new_author = st.text_input("New Author")
    new_genre = st.text_input("New Genre")

    if st.button("Update"):
        update_book(book_id,new_title,new_author,new_genre)
        st.success("Book updated")

elif menu == "Delete Book":
    book_id = st.number_input("Book ID:")
    if st.button("Delete"):
        delete_book(book_id)
        st.success("Book deleted")
else:
    st.write("Please choose a menu")
