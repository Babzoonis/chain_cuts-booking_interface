from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Создадим таблицы, если их нет
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_password TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO users (username, password, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (username, password, first_name, last_name))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'User registered successfully'}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'Registration failed: {e}'}), 500

@app.route('/delete_user/<username>', methods=['DELETE'])
def delete_user(username):
    # Проверка пароля администратора
    admin_password = request.headers.get('Admin-Password')
    print(admin_password)
    if not admin_password:
        return jsonify({'success': False, 'message': 'Admin password is required'}), 401

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        # Проверка правильности пароля администратора
        cursor.execute('''
            SELECT * FROM admin
            WHERE admin_password = ?
        ''', (admin_password,))

        admin = cursor.fetchone()
        if not admin:
            return jsonify({'success': False, 'message': 'Incorrect admin password'}), 401

        # Удаление пользователя
        cursor.execute('''
            DELETE FROM users
            WHERE username = ?
        ''', (username,))

        conn.commit()

        return jsonify({'success': True, 'message': 'User deleted successfully'}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error deleting user: {e}'}), 500

    finally:
        conn.close()

@app.route('/get_users', methods=['GET'])
def get_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        # Получение списка всех пользователей
        cursor.execute('''
            SELECT * FROM users
        ''')

        users = cursor.fetchall()

        return jsonify({'success': True, 'users': users}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error getting users: {e}'}), 500

    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
# получение данных пользователей "http://127.0.0.1:5000/get_users"