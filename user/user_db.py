import sqlite3

def create_table():
    """Створює таблицю для збереження інформації про користувачів."""
    conn = sqlite3.connect('data/data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            user_name TEXT,
            user_first_name TEXT,
            phone INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, user_name, user_first_name):
    """Додає дані про користувача до бази даних, якщо його ще немає в базі."""
    conn = sqlite3.connect('data/data.db')
    cursor = conn.cursor()
    # Перевіряємо, чи існує користувач з таким chat_id в базі даних
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    existing_user = cursor.fetchone()
    if existing_user is None:
        # Якщо користувача з таким chat_id ще немає в базі, додаємо його
        cursor.execute('''
            INSERT INTO users (user_id, user_name, user_first_name)
            VALUES (?, ?, ?)
        ''', (user_id, user_name, user_first_name))
        conn.commit()
    conn.close()
    
def add_phone_number_to_user(user_id, phone_number):
    """Додає номер телефону користувача до запису у базі даних."""
    conn = sqlite3.connect('data/data.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET phone = ?
        WHERE user_id = ?
    ''', (phone_number, user_id))
    conn.commit()
    conn.close()
    
def add_name_to_user(user_id, user_real_name):
    """Додає ым'я користувача до запису у базі даних."""
    conn = sqlite3.connect('data/data.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET real_name = ?
        WHERE user_id = ?
    ''', (user_real_name, user_id))
    conn.commit()
    conn.close()
    
def create_table_orders():
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        real_name TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        items TEXT NOT NULL,
        total_price REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    
def save_order(order):
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        real_name TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        items TEXT NOT NULL,
        total_price REAL NOT NULL
    )
    """)
    conn.commit()

    cursor.execute("""
    INSERT INTO orders (username, real_name, phone_number, items, total_price) VALUES (?, ?, ?, ?, ?)
    """, (order['username'], order['real_name'], order['phone_number'], order['items'], order['total_price']))
    conn.commit()

    conn.close()