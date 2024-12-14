import sqlite3

def view_all_data():
    # 连接数据库
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    # 执行查询
    c.execute('SELECT * FROM transactions')
    data = c.fetchall()
    
    # 打印表头
    print("\n记账本所有记录：")
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
    
    print("\n统计信息：")
    print(f"总收入：{total_income}")
    print(f"总支出：{total_expense}")
    print(f"结余：{total_income - total_expense}")
    
    conn.close()

if __name__ == '__main__':
    view_all_data() 