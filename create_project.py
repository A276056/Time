import os
import json

# 项目结构配置
project_structure = {
    'name': 'personal_finance',
    'directories': [
        'static/css',
        'static/js',
        'templates'
    ],
    'files': {
        'README.md': '''# 个人记账本项目

这是一个简单的个人记账本应用，用于展示前后端协作的基本原理。

## 功能特点
- 添加收支记录（金额、类型、备注、日期）
- 查看所有收支记录
- 显示总收入和支出统计

## 技术栈
- 前端：HTML + CSS + JavaScript
- 后端：Python (Flask)
- 数据库：SQLite

## 项目结构
- `static/`: 存放静态文件（CSS、JavaScript）
- `templates/`: 存放 HTML 模板
- `app.py`: Flask 后端应用主文件
- `database.py`: 数据库操作相关代码''',

        'app.py': '''from flask import Flask, render_template, request, jsonify
from database import init_db, add_transaction, get_all_transactions

app = Flask(__name__)

# 初始化数据库
init_db()

@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html')

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """获取所有交易记录"""
    transactions = get_all_transactions()
    return jsonify([{
        'id': t[0],
        'amount': t[1],
        'type': t[2],
        'note': t[3],
        'date': t[4]
    } for t in transactions])

@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    """创建新的交易记录"""
    data = request.json
    add_transaction(data['amount'], data['type'], data['note'])
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)''',

        'database.py': '''import sqlite3
from datetime import datetime

def init_db():
    """初始化数据库，创建表结构"""
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    # 创建收支记录表
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            note TEXT,
            date TEXT NOT NULL
        )
    """)
    
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
    return transactions''',

        'view_data.py': '''import sqlite3

def view_all_data():
    # 连接数据库
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    # 执行查询
    c.execute('SELECT * FROM transactions')
    data = c.fetchall()
    
    # 打印表头
    print("\\n记账本所有记录：")
    print("ID  |  金额  |  类型  |  备注  |  日期时间")
    print("-" * 60)
    
    # 打印每条记录
    for row in data:
        print(f"{row[0]:<4} | {row[1]:<6} | {row[2]:<4} | {row[3]:<6} | {row[4]}")
    
    # 计算统计信息
    c.execute('SELECT SUM(amount) FROM transactions WHERE type="收入"')
    total_income = c.fetchone()[0] or 0
    
    c.execute('SELECT SUM(amount) FROM transactions WHERE type="支出"')
    total_expense = c.fetchone()[0] or 0
    
    print("\\n统计信��：")
    print(f"总收入：{total_income}")
    print(f"总支出：{total_expense}")
    print(f"结余：{total_income - total_expense}")
    
    conn.close()

if __name__ == '__main__':
    view_all_data()''',

        'static/css/style.css': '''/* 基础样式 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    background-color: #f4f4f4;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

/* 表单样式 */
.add-form {
    background: white;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.form-group {
    display: flex;
    gap: 10px;
    margin-top: 10px;
}

input, select, button {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

button {
    background: #4CAF50;
    color: white;
    border: none;
    cursor: pointer;
}

button:hover {
    background: #45a049;
}

/* 统计信息样式 */
.statistics {
    display: flex;
    gap: 20px;
    margin: 20px 0;
}

.stat-item {
    background: white;
    padding: 15px;
    border-radius: 8px;
    flex: 1;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* 交易记录列表样式 */
.transaction-item {
    background: white;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.income {
    color: #4CAF50;
}

.expense {
    color: #f44336;
}''',

        'static/js/main.js': '''// 获取所有交易记录
async function getTransactions() {
    const response = await fetch('/api/transactions');
    const transactions = await response.json();
    displayTransactions(transactions);
    updateStatistics(transactions);
}

// 添加新交易记录
async function addTransaction() {
    const amount = document.getElementById('amount').value;
    const type = document.getElementById('type').value;
    const note = document.getElementById('note').value;

    if (!amount || !type) {
        alert('请填写金额和类型！');
        return;
    }

    const response = await fetch('/api/transactions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ amount, type, note })
    });

    if (response.ok) {
        // 清空表单
        document.getElementById('amount').value = '';
        document.getElementById('note').value = '';
        
        // 重新加载数据
        getTransactions();
    }
}

// 显示交易记录列表
function displayTransactions(transactions) {
    const list = document.getElementById('transaction-list');
    list.innerHTML = '';

    transactions.forEach(t => {
        const div = document.createElement('div');
        div.className = `transaction-item ${t.type === '收入' ? 'income' : 'expense'}`;
        div.innerHTML = `
            <div>
                <strong>${t.type}</strong>
                <span>${t.note}</span>
            </div>
            <div>
                <span>${t.type === '收入' ? '+' : '-'}${Math.abs(t.amount)}</span>
                <small>${t.date}</small>
            </div>
        `;
        list.appendChild(div);
    });
}

// 更新统计信息
function updateStatistics(transactions) {
    const income = transactions
        .filter(t => t.type === '收入')
        .reduce((sum, t) => sum + parseFloat(t.amount), 0);
    
    const expense = transactions
        .filter(t => t.type === '支出')
        .reduce((sum, t) => sum + parseFloat(t.amount), 0);

    document.getElementById('total-income').textContent = income.toFixed(2);
    document.getElementById('total-expense').textContent = expense.toFixed(2);
}

// 页面加载时获取数据
document.addEventListener('DOMContentLoaded', getTransactions);''',

        'templates/index.html': '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>个人记账本</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <h1>个人记账本</h1>
        
        <!-- 添加记录表单 -->
        <div class="add-form">
            <h2>添加记录</h2>
            <div class="form-group">
                <input type="number" id="amount" placeholder="金额" step="0.01">
                <select id="type">
                    <option value="收入">收入</option>
                    <option value="支出">支出</option>
                </select>
                <input type="text" id="note" placeholder="备注">
                <button onclick="addTransaction()">添加</button>
            </div>
        </div>

        <!-- 统计信息 -->
        <div class="statistics">
            <div class="stat-item">
                <span>总收入：</span>
                <span id="total-income">0</span>
            </div>
            <div class="stat-item">
                <span>总支出：</span>
                <span id="total-expense">0</span>
            </div>
        </div>

        <!-- 记录列表 -->
        <div class="transactions">
            <h2>收支记录</h2>
            <div id="transaction-list"></div>
        </div>
    </div>
    <script src="/static/js/main.js"></script>
</body>
</html>'''
    }
}

def create_project():
    """创建项目结构"""
    # 创建项目根目录
    root_dir = project_structure['name']
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    
    # 创建子目录
    for directory in project_structure['directories']:
        dir_path = os.path.join(root_dir, directory)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    
    # 创建文件
    for file_path, content in project_structure['files'].items():
        full_path = os.path.join(root_dir, file_path)
        # 确保文件所在的目录存在
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        # 写入文件内容
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"项目 {root_dir} 创建成功！")
    print("\n目录结构：")
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

if __name__ == '__main__':
    create_project() 