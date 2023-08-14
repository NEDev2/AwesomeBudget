document.getElementById("addExpenseForm").onsubmit = async function (e) {
    e.preventDefault();

    const amount = document.getElementById("amount").value;
    const title = document.getElementById("title").value;

    const response = await fetch("/spend_money", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ amount, title })
    });

    const data = await response.json();
    const statusElement = document.getElementById("expenseStatus");
    statusElement.innerText = data.message + " Category: " + data.category;

    setTimeout(() => {
        statusElement.innerText = '';
    }, 5000);
}

async function getCurrentMoney() {
    const response = await fetch("/current_money");
    const data = await response.json();
    document.getElementById("currentMoney").innerText = "Current Money: " + data.current_money;
}

async function getMoneySpentThisMonth() {
    const response = await fetch("/money_spent_this_month");
    const data = await response.json();
    document.getElementById("moneySpent").innerText = "Money Spent This Month: " + data.money_spent_this_month;
}

async function getAllExpenses() {
    const response = await fetch("/expenses");
    const expenses = await response.json();

    const expenseList = document.getElementById("expenseList");
    expenseList.innerHTML = "";

    expenses.forEach(expense => {
        const listItem = document.createElement("li");
        listItem.innerText = `${expense.title} - ${expense.amount} (Category: ${expense.category})`;
        expenseList.appendChild(listItem);
    });
}

function toggleDarkMode() {
    const bodyElement = document.body;
    if (bodyElement.classList.contains('dark-mode')) {
        bodyElement.classList.remove('dark-mode');
        document.getElementById('darkModeToggle').innerText = '🌙 Dark Mode';
    } else {
        bodyElement.classList.add('dark-mode');
        document.getElementById('darkModeToggle').innerText = '☀️ Light Mode';
    }
}
