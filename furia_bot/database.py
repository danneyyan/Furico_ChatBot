# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            alerts_enabled INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def set_alert_status(user_id, username, status):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (user_id, username, alerts_enabled)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            alerts_enabled=excluded.alerts_enabled,
            username=excluded.username
    ''', (user_id, username, status))
    conn.commit()
    conn.close()

def get_alert_status(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT alerts_enabled FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] == 1 if result else False

def get_all_users_with_alerts():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT user_id FROM users WHERE alerts_enabled=1')
    results = c.fetchall()
    conn.close()
    return [row[0] for row in results]
