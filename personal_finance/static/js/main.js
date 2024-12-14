// 获取所有交易记录
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
document.addEventListener('DOMContentLoaded', getTransactions);