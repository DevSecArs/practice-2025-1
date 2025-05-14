const host = "http://localhost:8000"; // Хост сервера API

function updateBalance(username, password) {
    fetch(`${host}/balance`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, password: password })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Ошибка при обновлении баланса");
            }
            return response.json();
        })
        .then(data => {
            if (data.balance !== undefined) {
                document.getElementById('wallet-balance').textContent = `${data.balance} USD`;
            } else {
                console.error("Не удалось получить баланс.");
            }
        })
        .catch(error => console.error("Ошибка:", error));
}

function parseTransaction(transactionString) {
    const regex = /^(.+) -> (.+): ([\d.]+)$/; // Регулярное выражение для разбора строки
    const match = transactionString.match(regex);

    if (match) {
        return {
            sender: match[1].trim(),
            recipient: match[2].trim(),
            amount: match[3].trim()
        };
    }
    console.error(`Не удалось разобрать транзакцию: ${transactionString}`);
    return null;
}

function updateTransactions(walletAddress) {
    fetch(`${host}/transactions/${walletAddress}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Ошибка при обновлении транзакций");
            }
            return response.json();
        })
        .then(data => {
            const transactionsContainer = document.getElementById('transactions-container');
            transactionsContainer.innerHTML = ''; // Очистить содержимое контейнера

            if (data.transactions && Array.isArray(data.transactions)) {
                if (data.transactions.length === 0) {
                    const emptyMessage = document.createElement('p');
                    emptyMessage.textContent = "История транзакций отсутствует.";
                    transactionsContainer.appendChild(emptyMessage);
                } else {
                    const table = document.createElement('table');
                    table.className = "table table-striped";

                    if (document.body.classList.contains('dark-theme')) {
                        table.classList.add('table-dark');
                    }

                    const thead = document.createElement('thead');
                    thead.innerHTML = `
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">Отправитель</th>
                            <th scope="col">Получатель</th>
                            <th scope="col">Количество (USD)</th>
                        </tr>
                    `;
                    table.appendChild(thead);

                    const tbody = document.createElement('tbody');

                    const reversedTransactions = [...data.transactions].reverse();
                    reversedTransactions.forEach((transaction, index) => {
                        const parsedTransaction = parseTransaction(transaction);
                        if (parsedTransaction) {
                            const row = document.createElement('tr');
                            row.innerHTML = `
                                <th scope="row">${index + 1}</th>
                                <td>${parsedTransaction.sender}</td>
                                <td>${parsedTransaction.recipient}</td>
                                <td>${parsedTransaction.amount}</td>
                            `;
                            tbody.appendChild(row);
                        }
                    });

                    table.appendChild(tbody);
                    transactionsContainer.appendChild(table);
                }
            } else {
                console.error("Не удалось получить список транзакций.");
            }
        })
        .catch(error => console.error("Ошибка:", error));
}

// Обновление каждые 10 секунд
function startUpdating(username, password, walletAddress) {
    updateBalance(username, password);
    updateTransactions(walletAddress);

    setInterval(() => {
        updateBalance(username, password);
        updateTransactions(walletAddress);
    }, 10000);
}
