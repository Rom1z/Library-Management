import mysql.connector
import tkinter as tk
from tkinter import messagebox, simpledialog

# Подключение к базе данных MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="todo_app"
    )

# Функция для добавления задачи
def add_task(task, priority, deadline):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO tasks (task, priority, deadline, status) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (task, priority, deadline, False))
    conn.commit()
    cursor.close()
    conn.close()

# Функция для получения задач
def get_tasks(status=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if status is None:
        query = "SELECT * FROM tasks"
        cursor.execute(query)
    else:
        query = "SELECT * FROM tasks WHERE status = %s"
        cursor.execute(query, (status,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks

# Функция для обновления статуса задачи
def update_task_status(task_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE tasks SET status = %s WHERE id = %s"
    cursor.execute(query, (status, task_id))
    conn.commit()
    cursor.close()
    conn.close()

# Функция для редактирования задачи
def edit_task(task_id, new_task, new_priority, new_deadline):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE tasks SET task = %s, priority = %s, deadline = %s WHERE id = %s"
    cursor.execute(query, (new_task, new_priority, new_deadline, task_id))
    conn.commit()
    cursor.close()
    conn.close()

# Функция для удаления задачи
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM tasks WHERE id = %s"
    cursor.execute(query, (task_id,))
    conn.commit()
    cursor.close()
    conn.close()

# Основной класс приложения
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Список дел")
        self.tasks_listbox = tk.Listbox(self.root, width=50, height=15, selectmode=tk.SINGLE)
        self.tasks_listbox.pack()

        self.add_button = tk.Button(self.root, text="Добавить задачу", command=self.open_add_task_form)
        self.add_button.pack()

        self.complete_button = tk.Button(self.root, text="Отметить как выполненное", command=self.mark_task_completed)
        self.complete_button.pack()

        self.delete_button = tk.Button(self.root, text="Удалить задачу", command=self.delete_selected_task)
        self.delete_button.pack()

        self.filter_var = tk.StringVar()
        self.filter_var.set("все")
        self.filter_menu = tk.OptionMenu(self.root, self.filter_var, "все", "выполненные", "невыполненные", command=self.filter_tasks)
        self.filter_menu.pack()

        self.show_tasks()

    def show_tasks(self, status_filter=None):
        self.tasks_listbox.delete(0, tk.END)
        if status_filter == "выполненные":
            tasks = get_tasks(status=True)
        elif status_filter == "невыполненные":
            tasks = get_tasks(status=False)
        else:
            tasks = get_tasks()
        for task in tasks:
            status = "✅" if task['status'] else "❌"
            self.tasks_listbox.insert(tk.END, f"{status} {task['task']} - Приоритет: {task['priority']} - Дедлайн: {task['deadline']}")

    def open_add_task_form(self):
        add_task_window = tk.Toplevel(self.root)
        add_task_window.title("Добавить задачу")

        tk.Label(add_task_window, text="Задача:").pack()
        task_entry = tk.Entry(add_task_window)
        task_entry.pack()

        tk.Label(add_task_window, text="Приоритет:").pack()
        priority_entry = tk.Entry(add_task_window)
        priority_entry.pack()

        tk.Label(add_task_window, text="Дедлайн (YYYY-MM-DD):").pack()
        deadline_entry = tk.Entry(add_task_window)
        deadline_entry.pack()

        def add_task_action():
            task = task_entry.get()
            priority = priority_entry.get()
            deadline = deadline_entry.get()
            add_task(task, priority, deadline)
            self.show_tasks()
            add_task_window.destroy()

        add_button = tk.Button(add_task_window, text="Добавить", command=add_task_action)
        add_button.pack()

    def mark_task_completed(self):
        selected = self.tasks_listbox.curselection()
        if selected:
            task_index = selected[0]
            task_text = self.tasks_listbox.get(task_index)
            task_id = int(task_text.split()[1])  # предполагается, что ID задачи хранится в начале
            update_task_status(task_id, True)
            self.show_tasks(self.filter_var.get())
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите задачу")

    def delete_selected_task(self):
        selected = self.tasks_listbox.curselection()
        if selected:
            task_index = selected[0]
            task_text = self.tasks_listbox.get(task_index)
            task_id = int(task_text.split()[1])  # предполагается, что ID задачи хранится в начале
            delete_task(task_id)
            self.show_tasks(self.filter_var.get())
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите задачу")

    def filter_tasks(self, selection):
        self.show_tasks(selection)

# Запуск приложения
root = tk.Tk()
app = ToDoApp(root)
root.mainloop()
