import sqlite3
from datetime import datetime

def init_db():
    """初始化数据库，创建表结构"""
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    # 创建收支记录表
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            note TEXT,
            date TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def add_transaction(amount, type, note):
    """添加一条收支记录"""
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO transactions (amount, type, note, date) VALUES (?, ?, ?, ?)',
             (amount, type, note, date))
    
    conn.commit()
    conn.close()

def get_all_transactions():
    """获取所有收支记录"""
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM transactions ORDER BY date DESC')
    transactions = c.execute('SELECT * FROM transactions ORDER BY date DESC').fetchall()
    
    conn.close()
    return transactions 