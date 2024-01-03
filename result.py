#Made by Babzoonis15 ( group : TK-102 )
#boking app made by Babzoonis15
from flask import Flask, request, jsonify
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
from geopy.geocoders import Nominatim
import pycountry
import os
import sqlite3
import requests
from urllib3 import HTTPConnectionPool
import json
from test import calculate_chain_cuts
from itertools import combinations
import subprocess


app = Flask(__name__)


class HotelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Registration and Booking")
        self.root.configure(bg="orange")

        # Registration variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()

        # Booking variables
        self.location_var = tk.StringVar()
        self.check_in_date_var = tk.StringVar()

        # Authentication state
        self.logged_in = False
        self.current_user = None

        # Create tabs
        self.notebook = ttk.Notebook(root)
        self.registration_tab = ttk.Frame(self.notebook)
        self.booking_tab = ttk.Frame(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(self.registration_tab, text="Registration")
        self.notebook.add(self.booking_tab, text="Booking")
        self.notebook.pack(padx=10, pady=10)

        # Registration Form
        self.create_registration_form()

        # Booking Form
        self.create_booking_form()

        # Add choice buttons for Registration and Login

        ttk.Button(root, text="Login", command=self.login).pack(side=tk.LEFT)
        ttk.Button(root, text="Delete User", command=self.delete_user).pack(side=tk.RIGHT)  # Добавлен новый кнопка "Delete User"

        # Initialize with the registration form
        self.show_registration_form()

        # Create a database and table for users
        self.conn = self.create_database()

    def run_test2(self):
        try:
            # Выполняем test2.py с использованием subprocess
            subprocess.run(["python", "test2.py"])
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при запуске test2.py: {e}")

    def create_database(self):
        db_file = "users.db"

        if not os.path.exists(db_file):
            print(f"Creating database file: {db_file}")
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()

                # Создаем таблицу пользователей, если ее нет
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL
                    )
                ''')

                # Создаем таблицу администратора и устанавливаем пароль по умолчанию
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS admin (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        admin_password TEXT NOT NULL
                    )
                ''')
                default_admin_password = "YASHALAVA"  # Установите свой пароль
                cursor.execute('INSERT INTO admin (admin_password) VALUES (?)', (default_admin_password,))

                conn.commit()
                print("Database creation successful.")

            except Exception as e:
                print(f"Error creating database: {e}")
                return None

        else:
            print(f"Database file already exists: {db_file}")
            try:
                conn = sqlite3.connect(db_file)
                print("Connected to the existing database.")
                return conn

            except Exception as e:
                print(f"Error connecting to the existing database: {e}")
                return None

    def create_registration_form(self):
        frame_register = ttk.Frame(self.registration_tab)

        ttk.Label(frame_register, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        ttk.Entry(frame_register, textvariable=self.username_var).grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame_register, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        ttk.Entry(frame_register, textvariable=self.password_var, show="*").grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(frame_register, text="First Name:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        ttk.Entry(frame_register, textvariable=self.first_name_var).grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(frame_register, text="Last Name:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        ttk.Entry(frame_register, textvariable=self.last_name_var).grid(row=3, column=1, padx=10, pady=5)

        ttk.Button(frame_register, text="Register", command=self.register).grid(row=4, column=0, columnspan=2, pady=10)

        frame_register.pack(padx=20, pady=20)

    def create_booking_form(self):
        frame_booking = ttk.Frame(self.booking_tab)

        ttk.Label(frame_booking, text="Location:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        countries = [country.name for country in pycountry.countries]
        location_dropdown = ttk.Combobox(frame_booking, textvariable=self.location_var, values=countries)
        location_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        ttk.Label(frame_booking, text="Check-In Date:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        check_in_date_entry = DateEntry(frame_booking, textvariable=self.check_in_date_var)
        check_in_date_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        ttk.Button(frame_booking, text="Search", command=self.search).grid(row=2, column=0, columnspan=2, pady=10)

        frame_booking.pack(padx=20, pady=20)

    def search(self):
        if self.logged_in:
            selected_location = self.location_var.get()
            check_in_date = self.check_in_date_var.get()

            if not selected_location or not check_in_date:
                messagebox.showwarning("Warning", "Please fill in all fields.")
                return
            self.run_test2()

            geolocator = Nominatim(user_agent="booking_app")
            location_info = geolocator.geocode(selected_location)

            if location_info:
                city = location_info.address.split(",")[0]
                country = location_info.raw.get("address", {}).get("country")
                print(f"Search for {city}, {country} on {check_in_date}")

                pool = HTTPConnectionPool(host='127.0.0.1', port=5000, maxsize=10)
                url = 'http://localhost:5000/register'
                data = {'username': self.username_var.get(), 'password': self.password_var.get(), 'first_name': self.first_name_var.get(), 'last_name': self.last_name_var.get()}

                try:
                    response = requests.post(url, json=data)
                    # Далее обработка response
                except requests.exceptions.RequestException as e:
                    print(f"Error sending request to the server: {e}")
                    messagebox.showerror("Error", f"Registration failed: {e}")
                finally:
                    pool.close()

            else:
                print(f"Search for {selected_location} on {check_in_date}")

    def show_registration_form(self):
        self.notebook.select(self.registration_tab)

    def show_booking_form(self):
        self.notebook.select(self.booking_tab)

    def show_login_form(self):
        username = tk.simpledialog.askstring("Login", "Enter your username:")
        password = tk.simpledialog.askstring("Login", "Enter your password:")

        if self.validate_login(username, password):
            self.logged_in = True
            self.current_user = username
            self.show_booking_form()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

    def login(self):
        if self.logged_in:
            messagebox.showinfo("Already Logged In", "You are already logged in.")
        else:
            self.show_login_form()

    def validate_login(self, username, password):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM users
            WHERE username = ? AND password = ?
        ''', (username, password))

        user = cursor.fetchone()

        conn.close()

        return user is not None

    def register(self):
        # Получение значений из текстовых полей (или откуда-то еще)
        username = self.username_var.get()
        password = self.password_var.get()
        first_name = self.first_name_var.get()
        last_name = self.last_name_var.get()

        # Проверка наличия пользователя с таким именем
        if self.username_exists(username):
            messagebox.showerror("Error",
                                 "User with this username already exists. Please choose another username or login to an existing account.")
            return

        # Проверка наличия значений
        if not username or not password or not first_name or not last_name:
            messagebox.showerror("Error", "Please fill in all registration fields.")
            return

        # Создание словаря для передачи данных на сервер
        data = {'username': username, 'password': password, 'first_name': first_name, 'last_name': last_name}

        # Отправка запроса на сервер
        url = 'http://localhost:5000/register'

        try:
            response = requests.post(url, json=data)
            response_data = response.json()

            # Проверка успешности регистрации
            if response_data.get('success'):
                messagebox.showinfo("Registration", response_data['message'])
                self.insert_user_data(username, password, first_name, last_name)
                self.logged_in = True
                self.current_user = username
                self.show_booking_form()
            else:
                messagebox.showerror("Error", response_data['message'])

        except requests.exceptions.RequestException as e:
            print(f"Error sending request to the server: {e}")
            messagebox.showerror("Error", f"Registration failed: {e}")

    def insert_user_data(self, username, password, first_name, last_name): #That function need for insert new user into DataBase
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO users (username, password, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (username, password, first_name, last_name))

        conn.commit()
        conn.close()

    def delete_user(self): #With that function Admin can delet any user in my DataBase if he has Admin password
        if self.logged_in:
            # Ввод пароля администратора
            admin_password = tk.simpledialog.askstring("Admin Password", "Enter admin password:")
            self.root.update()  # Обновление главного окна
            if not admin_password:
                messagebox.showwarning("Admin Password", "Admin password is required.")
                return

            # Получение имени пользователя для удаления
            username_to_delete = tk.simpledialog.askstring("Delete User", "Enter username to delete:")
            self.root.update()  # Обновление главного окна

            if not username_to_delete:
                messagebox.showwarning("Delete User", "Please enter username to delete.")
                return

            # Отправка запроса на удаление пользователя
            url = f'http://localhost:5000/delete_user/{username_to_delete}'
            headers = {'Admin-Password': admin_password}

            try:
                response = requests.delete(url, headers=headers)
                response_data = response.json()

                if response.status_code == 200 and response_data.get('success'):
                    messagebox.showinfo("Delete User", response_data['message'])
                else:
                    messagebox.showerror("Delete User Failed", response_data['message'])

            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Delete user failed: {e}")

    def username_exists(self, username): # That function check exists username in my DataBase
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM users
            WHERE username = ?
        ''', (username,))

        user = cursor.fetchone()

        conn.close()

        return user is not None

#Run main part of code
if __name__ == "__main__":
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()