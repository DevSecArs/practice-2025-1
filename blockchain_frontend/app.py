from flask import Flask, render_template, request, redirect, url_for, flash
import qrcode
import io
import base64
from flask import send_file

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Replace with a secure key

# Dummy data for demonstration purposes
users = {
    "user": {"password": "user123", "role": "user", "wallet": "1A2B3C4D5E6F7G8H9I0J"}
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = users.get(username)
        if user and user['password'] == password:
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/user', methods=['GET', 'POST'])
def user_dashboard():
    balance = 500.00  # Example data
    wallet_address = users['user']['wallet']
    transactions = [  # Example data
        {"id": "1", "status": "Success", "amount": -50, "timestamp": "2025-05-04T10:00:00Z"},
        {"id": "2", "status": "Success", "amount": 150, "timestamp": "2025-05-04T15:00:00Z"}
    ]

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'send':
            recipient = request.form.get('recipient')
            amount = request.form.get('amount')
            if recipient and amount:
                flash(f'Successfully sent {amount} to {recipient}.', 'success')
            else:
                flash('Please provide both recipient and amount.', 'danger')

    return render_template('user.html', balance=balance, transactions=transactions, wallet_address=wallet_address)

@app.route('/user/receive')
def receive():
    wallet_address = users['user']['wallet']
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(wallet_address)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    encoded_qr = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return render_template('receive.html', wallet_address=wallet_address, qr_code=encoded_qr)

@app.route('/logout')
def logout():
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
