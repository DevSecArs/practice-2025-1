from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import qrcode
import io
import base64

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Нужно заменить на свой ключ

API_BASE_URL = "http://localhost:8000"  # URL вашего сервера с блокчейном

@app.route('/')
def home():
    if "username" in session:
        return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Запрос к API для логина
        response = requests.post(f"{API_BASE_URL}/login", json={"username": username, "password": password})
        if response.status_code == 200:
            data = response.json()
            session['username'] = username
            session['password'] = password
            session['wallet_address'] = data['address']
            flash('Вход успешный!', 'success')
            return redirect(url_for('user_dashboard'))
        elif response.status_code == 401:
            flash('Неправильный логин или пароль.', 'danger')
        else:
            flash('Непредвиденная ошибка.', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Пароли не совпадают.', 'danger')
        else:
            response = requests.post(f"{API_BASE_URL}/register", json={"username": username, "password": password})
            if response.status_code == 201:
                flash('Регистрация успешна! Войдите, чтобы войти в кошелёк.', 'success')
                return redirect(url_for('login'))
            elif response.status_code == 400:
                flash('Пользователь уже существует.', 'danger')
            
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/user', methods=['GET', 'POST'])
def user_dashboard():
    if "username" not in session:
        flash('Войдите, чтобы попасть в кошелёк.', 'warning')
        return redirect(url_for('login'))

    username = session['username']
    password = session['password']
    wallet_address = session['wallet_address']

    # Получение баланса и транзакций
    balance_response = requests.post(f"{API_BASE_URL}/balance", json={"username": username, "password": password})
    transactions_response = requests.get(f"{API_BASE_URL}/transactions/{wallet_address}")

    if balance_response.status_code == 200:
        balance = balance_response.json().get('balance', 0)
    else:
        balance = 0
        flash("Невозможно загрузить данные о балансе.", "danger")

    if transactions_response.status_code == 200:
        transactions = transactions_response.json().get('transactions', [])
    else:
        transactions = []
        flash("Невозможно загрузить данные о транзакциях.", "danger")

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'send':
            recipient = request.form.get('recipient')
            amount = request.form.get('amount')
            if recipient and amount:
                transaction_response = requests.post(f"{API_BASE_URL}/transaction", json={
                    "sender_username": username,
                    "sender_password": password,
                    "sender_address": wallet_address,
                    "recipient_address": recipient,
                    "amount": float(amount)
                })
                if transaction_response.status_code == 201:
                    flash('Транзакция прошла успешно!', 'success')
                elif transaction_response.status_code == 401:
                    flash('Транзакция не осуществилась. Необходимо пройти аутентификацию.', 'warning')
                    return redirect(url_for('login'))
                else:
                    flash('Транзакция не осуществилась. Недостаточно средств.', 'danger')
            else:
                flash('Транзакция не осуществилась. Проверьте баланс или попробуйте позже.', 'danger')
            return redirect(url_for('user_dashboard'))
        if action == 'borrow':
            amount = request.form.get('amount')
            if amount:
                transaction_response = requests.post(f"{API_BASE_URL}/credit", json={
                    "recipient_address": wallet_address,
                    "amount": float(amount)
                })
                if transaction_response.status_code == 201:
                    flash('Кредит оформлен успешно!', 'success')
                else:
                    flash('Неудалось получить кредит. Попробуйте позже.', 'danger')
                return redirect(url_for('user_dashboard'))

    return render_template('user.html', balance=balance, transactions=transactions, wallet_address=wallet_address, username=username, password=password)

@app.route('/user/receive')
def receive():
    if "username" not in session:
        flash('Войдите, чтобы попасть в кошелёк.', 'warning')
        return redirect(url_for('login'))

    wallet_address = session['wallet_address']
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(wallet_address)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Кодируем изображение в base64 для отображения на веб-странице
    encoded_qr = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render_template('receive.html', wallet_address=wallet_address, qr_code=encoded_qr)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Вы успешно вышли из аккаунта.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
