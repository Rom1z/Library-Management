import mysql.connector
import tkinter as tk
from tkinter import messagebox, simpledialog


# Функция подключения к базе данных
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Укажите ваш пароль
        database="phonebook_app"
    )


# Функция добавления нового контакта
def add_contact(first_name, last_name, phone, email, address):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO contacts (first_name, last_name, phone, email, address) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (first_name, last_name, phone, email, address))
    conn.commit()
    cursor.close()
    conn.close()


# Функция получения всех контактов или поиска по запросу
def get_contacts(search_term=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if search_term:
        query = "SELECT * FROM contacts WHERE first_name LIKE %s OR last_name LIKE %s OR phone LIKE %s"
        search_term = f"%{search_term}%"
        cursor.execute(query, (search_term, search_term, search_term))
    else:
        query = "SELECT * FROM contacts"
        cursor.execute(query)
    contacts = cursor.fetchall()
    cursor.close()
    conn.close()
    return contacts


# Функция редактирования контакта
def edit_contact(contact_id, first_name, last_name, phone, email, address):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE contacts SET first_name = %s, last_name = %s, phone = %s, email = %s, address = %s WHERE id = %s"
    cursor.execute(query, (first_name, last_name, phone, email, address, contact_id))
    conn.commit()
    cursor.close()
    conn.close()


# Функция удаления контакта
def delete_contact(contact_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM contacts WHERE id = %s"
    cursor.execute(query, (contact_id,))
    conn.commit()
    cursor.close()
    conn.close()


# Класс интерфейса приложения PhonebookApp
class PhonebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Телефонный справочник")

        # Поле поиска
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()
        self.search_button = tk.Button(self.root, text="Поиск", command=self.search_contacts)
        self.search_button.pack()

        # Список контактов
        self.contacts_listbox = tk.Listbox(self.root, width=50, height=15, selectmode=tk.SINGLE)
        self.contacts_listbox.pack()

        # Кнопки управления
        self.add_button = tk.Button(self.root, text="Добавить контакт", command=self.open_add_contact_form)
        self.add_button.pack()
        self.edit_button = tk.Button(self.root, text="Редактировать контакт", command=self.open_edit_contact_form)
        self.edit_button.pack()
        self.delete_button = tk.Button(self.root, text="Удалить контакт", command=self.delete_selected_contact)
        self.delete_button.pack()

        self.show_contacts()

    # Функция отображения контактов
    def show_contacts(self, search_term=None):
        self.contacts_listbox.delete(0, tk.END)
        contacts = get_contacts(search_term)
        for contact in contacts:
            self.contacts_listbox.insert(tk.END, f"{contact['first_name']} {contact['last_name']} - {contact['phone']}")

    # Форма добавления нового контакта
    def open_add_contact_form(self):
        add_contact_window = tk.Toplevel(self.root)
        add_contact_window.title("Добавить контакт")

        # Поля для ввода данных
        tk.Label(add_contact_window, text="Имя:").pack()
        first_name_entry = tk.Entry(add_contact_window)
        first_name_entry.pack()

        tk.Label(add_contact_window, text="Фамилия:").pack()
        last_name_entry = tk.Entry(add_contact_window)
        last_name_entry.pack()

        tk.Label(add_contact_window, text="Телефон:").pack()
        phone_entry = tk.Entry(add_contact_window)
        phone_entry.pack()

        tk.Label(add_contact_window, text="Email:").pack()
        email_entry = tk.Entry(add_contact_window)
        email_entry.pack()

        tk.Label(add_contact_window, text="Адрес:").pack()
        address_entry = tk.Entry(add_contact_window)
        address_entry.pack()

        def add_contact_action():
            add_contact(first_name_entry.get(), last_name_entry.get(), phone_entry.get(), email_entry.get(),
                        address_entry.get())
            self.show_contacts()
            add_contact_window.destroy()

        add_button = tk.Button(add_contact_window, text="Добавить", command=add_contact_action)
        add_button.pack()

    # Функция поиска контактов
    def search_contacts(self):
        search_term = self.search_entry.get()
        self.show_contacts(search_term)

    # Форма редактирования выбранного контакта
    def open_edit_contact_form(self):
        selected = self.contacts_listbox.curselection()
        if selected:
            contact_index = selected[0]
            contact_text = self.contacts_listbox.get(contact_index).split(" - ")[0]
            first_name, last_name = contact_text.split()

            contacts = get_contacts()
            contact = next((c for c in contacts if c['first_name'] == first_name and c['last_name'] == last_name), None)
            if contact:
                edit_contact_window = tk.Toplevel(self.root)
                edit_contact_window.title("Редактировать контакт")

                # Поля для редактирования
                tk.Label(edit_contact_window, text="Имя:").pack()
                first_name_entry = tk.Entry(edit_contact_window)
                first_name_entry.insert(0, contact['first_name'])
                first_name_entry.pack()

                tk.Label(edit_contact_window, text="Фамилия:").pack()
                last_name_entry = tk.Entry(edit_contact_window)
                last_name_entry.insert(0, contact['last_name'])
                last_name_entry.pack()

                tk.Label(edit_contact_window, text="Телефон:").pack()
                phone_entry = tk.Entry(edit_contact_window)
                phone_entry.insert(0, contact['phone'])
                phone_entry.pack()

                tk.Label(edit_contact_window, text="Email:").pack()
                email_entry = tk.Entry(edit_contact_window)
                email_entry.insert(0, contact['email'])
                email_entry.pack()

                tk.Label(edit_contact_window, text="Адрес:").pack()
                address_entry = tk.Entry(edit_contact_window)
                address_entry.insert(0, contact['address'])
                address_entry.pack()

                def edit_contact_action():
                    edit_contact(contact['id'], first_name_entry.get(), last_name_entry.get(), phone_entry.get(),
                                 email_entry.get(), address_entry.get())
                    self.show_contacts()
                    edit_contact_window.destroy()

                edit_button = tk.Button(edit_contact_window, text="Сохранить изменения", command=edit_contact_action)
                edit_button.pack()
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите контакт")

    # Удаление выбранного контакта
    def delete_selected_contact(self):
        selected = self.contacts_listbox.curselection()
        if selected:
            contact_index = selected[0]
            contact_text = self.contacts_listbox.get(contact_index).split(" - ")[0]
            first_name, last_name = contact_text.split()

            contacts = get_contacts()
            contact = next((c for c in contacts if c['first_name'] == first_name and c['last_name'] == last_name), None)
            if contact:
                delete_contact(contact['id'])
                self.show_contacts()
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите контакт")


# Запуск приложения
root = tk.Tk()
app = PhonebookApp(root)
root.mainloop()
