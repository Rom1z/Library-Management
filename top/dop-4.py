import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import csv

# Подключение к базе данных MySQL
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Замените на ваше имя пользователя
        password="",  # Замените на ваш пароль
        database="library"
    )
    return conn

# Функция для добавления книги в базу данных
def add_book(title, author, isbn, year, genre):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO books (title, author, isbn, year, genre) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (title, author, isbn, year, genre))
    conn.commit()
    conn.close()

# Функция для удаления книги по ID
def delete_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM books WHERE id = %s"
    cursor.execute(query, (book_id,))
    conn.commit()
    conn.close()

# Функция для редактирования информации о книге
def edit_book(book_id, title, author, isbn, year, genre):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE books SET title = %s, author = %s, isbn = %s, year = %s, genre = %s WHERE id = %s"
    cursor.execute(query, (title, author, isbn, year, genre, book_id))
    conn.commit()
    conn.close()

# Функция для поиска книги по названию, автору или ISBN
def search_books(search_term):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s"
    cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
    books = cursor.fetchall()
    conn.close()
    return books

# Функция для получения всех книг из базы данных
def get_all_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

# Функция для экспорта данных в CSV
def export_to_csv():
    books = get_all_books()
    with open('books.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Title", "Author", "ISBN", "Year", "Genre"])
        for book in books:
            writer.writerow(book)
    messagebox.showinfo("Экспорт", "Данные успешно экспортированы в файл books.csv")

# Класс интерфейса приложения
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление библиотекой")
        self.root.geometry("1000x900")
        self.root.config(bg="#f0f0f0")  # Установка фона окна

        # Заголовок
        self.header_label = tk.Label(self.root, text="Управление библиотекой", font=("Helvetica", 20, "bold"), bg="#4CAF50", fg="white", pady=10)
        self.header_label.pack(fill="x")

        # Поля для добавления/редактирования книги
        self.title_label = tk.Label(self.root, text="Название книги:", bg="#f0f0f0", font=("Arial", 12))
        self.title_label.pack(pady=5)
        self.title_entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.title_entry.pack(pady=5)

        self.author_label = tk.Label(self.root, text="Автор:", bg="#f0f0f0", font=("Arial", 12))
        self.author_label.pack(pady=5)
        self.author_entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.author_entry.pack(pady=5)

        self.isbn_label = tk.Label(self.root, text="ISBN:", bg="#f0f0f0", font=("Arial", 12))
        self.isbn_label.pack(pady=5)
        self.isbn_entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.isbn_entry.pack(pady=5)

        self.year_label = tk.Label(self.root, text="Год издания:", bg="#f0f0f0", font=("Arial", 12))
        self.year_label.pack(pady=5)
        self.year_entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.year_entry.pack(pady=5)

        self.genre_label = tk.Label(self.root, text="Жанр:", bg="#f0f0f0", font=("Arial", 12))
        self.genre_label.pack(pady=5)
        self.genre_entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.genre_entry.pack(pady=5)

        # Кнопки для действий
        self.add_button = tk.Button(self.root, text="Добавить книгу", command=self.add_book, bg="#4CAF50", fg="white", font=("Arial", 12), relief="raised")
        self.add_button.pack(pady=10, fill="x", padx=50)

        self.edit_button = tk.Button(self.root, text="Редактировать книгу", command=self.edit_book, bg="#FFC107", fg="black", font=("Arial", 12), relief="raised")
        self.edit_button.pack(pady=10, fill="x", padx=50)

        self.delete_button = tk.Button(self.root, text="Удалить книгу", command=self.delete_book, bg="#F44336", fg="white", font=("Arial", 12), relief="raised")
        self.delete_button.pack(pady=10, fill="x", padx=50)

        self.export_button = tk.Button(self.root, text="Экспортировать данные в CSV", command=export_to_csv, bg="#2196F3", fg="white", font=("Arial", 12), relief="raised")
        self.export_button.pack(pady=10, fill="x", padx=50)

        # Поле для поиска
        self.search_label = tk.Label(self.root, text="Поиск книги:", bg="#f0f0f0", font=("Arial", 12))
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(self.root, text="Поиск", command=self.search_books, bg="#8BC34A", fg="white", font=("Arial", 12), relief="raised")
        self.search_button.pack(pady=10)

        # Таблица для отображения книг
        self.tree = ttk.Treeview(self.root, columns=("ID", "Title", "Author", "ISBN", "Year", "Genre"), show="headings", height=8)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Year", text="Год")
        self.tree.heading("Genre", text="Жанр")
        self.tree.pack(pady=20)

        # Отображение всех книг при запуске
        self.show_books()

    # Функция для добавления книги
    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        isbn = self.isbn_entry.get()
        year = self.year_entry.get()
        genre = self.genre_entry.get()

        if not title or not author or not isbn or not year or not genre:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        # Проверка уникальности ISBN
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE isbn = %s", (isbn,))
        existing_book = cursor.fetchone()
        conn.close()

        if existing_book:
            messagebox.showerror("Ошибка", "Книга с таким ISBN уже существует!")
            return

        add_book(title, author, isbn, year, genre)
        self.show_books()

    # Функция для редактирования книги
    def edit_book(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите книгу для редактирования!")
            return

        book_id = self.tree.item(selected_item, "values")[0]
        title = self.title_entry.get()
        author = self.author_entry.get()
        isbn = self.isbn_entry.get()
        year = self.year_entry.get()
        genre = self.genre_entry.get()

        if not title or not author or not isbn or not year or not genre:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        edit_book(book_id, title, author, isbn, year, genre)
        self.show_books()

    # Функция для удаления книги
    def delete_book(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите книгу для удаления!")
            return

        book_id = self.tree.item(selected_item, "values")[0]
        delete_book(book_id)
        self.show_books()

    # Функция для поиска книг
    def search_books(self):
        search_term = self.search_entry.get()
        books = search_books(search_term)
        self.update_book_list(books)

    # Функция для отображения всех книг
    def show_books(self):
        books = get_all_books()
        self.update_book_list(books)

    # Функция для обновления списка книг в Treeview
    def update_book_list(self, books):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for book in books:
            self.tree.insert("", "end", values=book)


# Создание главного окна
root = tk.Tk()
app = LibraryApp(root)
root.mainloop()
