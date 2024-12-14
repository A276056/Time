from flask import Flask, render_template, request, jsonify
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
    app.run(debug=True)