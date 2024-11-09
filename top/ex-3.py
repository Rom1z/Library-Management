import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import matplotlib.pyplot as plt


# Подключение к базе данных MySQL
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Замените на ваше имя пользователя
        password="",  # Замените на ваш пароль
        database="expense_tracker"
    )
    return conn


# Функция добавления новой транзакции
def add_transaction(amount, category, date, description, t_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO transactions (amount, category, date, description, type) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (amount, category, date, description, t_type))
    conn.commit()
    conn.close()


# Функция получения всех транзакций или фильтрации по дате и категории
def get_transactions(filter_type=None, filter_category=None, filter_date=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []
    if filter_type:
        query += " AND type = %s"
        params.append(filter_type)
    if filter_category:
        query += " AND category = %s"
        params.append(filter_category)
    if filter_date:
        query += " AND date = %s"
        params.append(filter_date)
    cursor.execute(query, params)
    transactions = cursor.fetchall()
    conn.close()
    return transactions


# Функция вычисления баланса
def calculate_balance():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Доход'")
    income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Расход'")
    expense = cursor.fetchone()[0] or 0
    conn.close()
    return income - expense


# Функция отображения статистики по категориям
def show_category_statistics():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type = 'Расход' GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    categories = [item[0] for item in data]
    amounts = [item[1] for item in data]

    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
    plt.title("Расходы по категориям")
    plt.show()


# Класс интерфейса приложения ExpenseTrackerApp
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Учёт расходов")
        self.root.geometry("1300x900")
        self.root.config(bg="#F4F4F4")

        # Поля для добавления новой транзакции
        self.amount_label = tk.Label(self.root, text="Сумма", bg="#F4F4F4", font=("Helvetica", 12))
        self.amount_label.pack(pady=5)
        self.amount_entry = tk.Entry(self.root, font=("Helvetica", 12), bd=2)
        self.amount_entry.pack(pady=5)

        self.category_label = tk.Label(self.root, text="Категория", bg="#F4F4F4", font=("Helvetica", 12))
        self.category_label.pack(pady=5)
        self.category_entry = tk.Entry(self.root, font=("Helvetica", 12), bd=2)
        self.category_entry.pack(pady=5)

        self.date_label = tk.Label(self.root, text="Дата", bg="#F4F4F4", font=("Helvetica", 12))
        self.date_label.pack(pady=5)
        self.date_entry = tk.Entry(self.root, font=("Helvetica", 12), bd=2)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.pack(pady=5)

        self.description_label = tk.Label(self.root, text="Описание", bg="#F4F4F4", font=("Helvetica", 12))
        self.description_label.pack(pady=5)
        self.description_entry = tk.Entry(self.root, font=("Helvetica", 12), bd=2)
        self.description_entry.pack(pady=5)

        self.type_var = tk.StringVar(value="Расход")
        self.income_radio = tk.Radiobutton(self.root, text="Доход", variable=self.type_var, value="Доход", bg="#F4F4F4",
                                           font=("Helvetica", 12))
        self.income_radio.pack(pady=5)
        self.expense_radio = tk.Radiobutton(self.root, text="Расход", variable=self.type_var, value="Расход",
                                            bg="#F4F4F4", font=("Helvetica", 12))
        self.expense_radio.pack(pady=5)

        add_button = tk.Button(self.root, text="Добавить транзакцию", command=self.add_transaction, bg="#4CAF50",
                               fg="white", font=("Helvetica", 12), relief="solid")
        add_button.pack(pady=10)

        # Список транзакций
        self.transactions_tree = ttk.Treeview(self.root,
                                              columns=("ID", "Amount", "Category", "Date", "Description", "Type"),
                                              show="headings")
        self.transactions_tree.heading("ID", text="ID")
        self.transactions_tree.heading("Amount", text="Сумма")
        self.transactions_tree.heading("Category", text="Категория")
        self.transactions_tree.heading("Date", text="Дата")
        self.transactions_tree.heading("Description", text="Описание")
        self.transactions_tree.heading("Type", text="Тип")
        self.transactions_tree.pack(pady=10)

        self.show_transactions()

        # Поля для отображения баланса и фильтрации
        self.balance_label = tk.Label(self.root, text=f"Текущий баланс: {calculate_balance()}", bg="#F4F4F4",
                                      font=("Helvetica", 14))
        self.balance_label.pack(pady=10)

        filter_button = tk.Button(self.root, text="Фильтр", command=self.show_transactions, bg="#2196F3", fg="white",
                                  font=("Helvetica", 12), relief="solid")
        filter_button.pack(pady=5)

        stats_button = tk.Button(self.root, text="Статистика по категориям", command=show_category_statistics,
                                 bg="#FF9800", fg="white", font=("Helvetica", 12), relief="solid")
        stats_button.pack(pady=5)

    # Функция добавления новой транзакции
    def add_transaction(self):
        amount = float(self.amount_entry.get())
        category = self.category_entry.get()
        date = self.date_entry.get()
        description = self.description_entry.get()
        t_type = self.type_var.get()

        add_transaction(amount, category, date, description, t_type)
        self.show_transactions()
        self.balance_label.config(text=f"Текущий баланс: {calculate_balance()}")

    # Функция отображения транзакций
    def show_transactions(self):
        for i in self.transactions_tree.get_children():
            self.transactions_tree.delete(i)
        transactions = get_transactions()
        for transaction in transactions:
            self.transactions_tree.insert("", tk.END, values=transaction)


# Запуск приложения
root = tk.Tk()
app = ExpenseTrackerApp(root)
root.mainloop()
