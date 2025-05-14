# Проект: Frontend для подключение к Blockchain на Python: FrontChain

## Описание проекта
Проект представляет собой веб-приложение, написанное на Python с использованием Flask, для управления пользовательскими кошельками и взаимодействия с транзакциями. Приложение поддерживает авторизацию, регистрацию, отображение баланса кошелька, историю транзакций и их осуществление, а также предоставляет пользователю интерфейс для изменения темы на светлую или тёмную.

---

## Выполненные задачи
1. **Создание структуры приложения:**
   - Проект организован в соответствии с рекомендациями Flask. Статические файлы хранятся в папке `static`, а HTML-шаблоны — в папке `templates`.

2. **Разработка интерфейса:**
   - Реализован базовый HTML-шаблон `base.html` с подключаемыми скриптами и стилями.
   - Созданы пользовательские страницы для входа, регистрации, информации о кошельке и транзакциях.

3. **Темизация интерфейса:**
   - Добавлена поддержка переключения темы (светлая/тёмная) с помощью JavaScript. Выбор темы сохраняется в `localStorage`.

4. **AJAX-запросы:**
   - Реализовано динамическое обновление данных о балансе и транзакциях с использованием `fetch`.
   - Обработка данных о транзакциях, включая их форматирование и отображение в таблице Bootstrap.

5. **Регулярные обновления:**
   - Реализовано автоматическое обновление данных каждые 10 секунд.

6. **Обработка данных:**
   - Реализована логика парсинга транзакций с форматом вида `"SYSTEM -> ADDR_xxx: yyy"`.
   - Добавлен вывод в виде таблицы с нумерацией и детализацией.

---

## Структура проекта

```plaintext
project/
├── static/
│   ├── ajax.js        # Логика AJAX-запросов и обработки транзакций
│   ├── base.css       # Базовые стили приложения
│   ├── base.js        # Скрипт для правильного позиционирования footer'а
|   ├── copy.js        # Скрипт для копирования данных (при необходимости)
|   ├── logo.png       # Логотип для страниц
│   ├── theme.js       # Скрипт для управления темами
├── templates/
│   ├── about.html     # Страница "О приложении"
│   ├── base.html      # Базовый HTML-шаблон
│   ├── login.html     # Страница входа
│   ├── receive.html   # Страница получения данных (опционально)
│   ├── register.html  # Страница регистрации
│   ├── user.html      # Основной интерфейс пользователя
├── .gitignore         # Файл игнорирования для Git
├── app.py             # Основной файл приложения Flask
├── requirements.txt   # Список зависимостей Python
└── venv/              # Виртуальное окружение (может быть исключено из репозитория)
```

---

## Подробная документация

### 1. Настройка окружения
Перед запуском приложения необходимо установить зависимости:
```bash
pip install -r requirements.txt
```

### 2. Запуск приложения
Для запуска приложения выполните:
```bash
python main.py
```

### 3. Основные страницы
- `/login` — Страница входа в систему.
- `/register` — Страница регистрации нового пользователя.
- `/user` — Интерфейс пользователя с отображением баланса и транзакций.
- `/about` — Страница информации о приложении.

### 4. Функционал AJAX-запросов
- Обновление баланса:
  ```javascript
  fetch(`${host}/balance`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
  });
  ```
- Обновление транзакций:
  ```javascript
  fetch(`${host}/transactions/${walletAddress}`);
  ```

### 5. Логика смены темы
Смена темы реализована с сохранением состояния в `localStorage`:
```javascript
document.body.classList.toggle('dark-theme');
localStorage.setItem('theme', body.classList.contains('dark-theme') ? 'dark' : 'light');
```

### 6. Форматирование транзакций
Транзакции обрабатываются с использованием регулярного выражения:
```javascript
function parseTransaction(transactionString) {
    const regex = /^(.+) -> (.+): ([\d.]+)$/;
    const match = transactionString.match(regex);
    if (match) {
        return { sender: match[1], recipient: match[2], amount: match[3] };
    }
    return null;
}
```

### 7. Обновление таблицы транзакций
Форматирование транзакций для отображения в таблице:
```javascript
function updateTransactions(data) {
    const transactionsContainer = document.getElementById('transactions-container');
    transactionsContainer.innerHTML = '';

    if (data.transactions.length === 0) {
        const emptyMessage = document.createElement('p');
        emptyMessage.textContent = "История транзакций отсутствует.";
        transactionsContainer.appendChild(emptyMessage);
    } else {
        const table = document.createElement('table');
        table.className = 'table table-striped table-dark'; // Поддержка темы
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>#</th>
                <th>Отправитель</th>
                <th>Получатель</th>
                <th>Сумма (USD)</th>
            </tr>
        `;
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        data.transactions.forEach((transaction, index) => {
            const parsedTransaction = parseTransaction(transaction);
            if (parsedTransaction) {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${index + 1}</td>
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
}
```
---
## Журнал прогресса

---

## Возможные улучшения
1. **Реализация REST API для улучшения логики взаимодействия с сервером.**
2. **Поддержка мультиязычности интерфейса.**
3. **Страница с графиком цен и возможностью покупки и продажи криптовалюты.**
