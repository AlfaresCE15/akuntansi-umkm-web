
from flask import Flask, render_template_string, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.secret_key = 'rahasia_umkm_key'

# Simulasi database pengguna dan transaksi
users = {}
user_transactions = {}

HTML_LOGIN = """
<!DOCTYPE html>
<html><head><title>Login</title></head><body>
<h2>Login Akun</h2>
<form method="post">
  Username: <input name="username"><br>
  Password: <input type="password" name="password"><br>
  <button type="submit">Login</button>
</form>
<p>Belum punya akun? <a href="/register">Daftar di sini</a></p>
</body></html>
"""

HTML_REGISTER = """
<!DOCTYPE html>
<html><head><title>Daftar</title></head><body>
<h2>Registrasi Akun</h2>
<form method="post">
  Username: <input name="username"><br>
  Password: <input type="password" name="password"><br>
  <button type="submit">Daftar</button>
</form>
<p>Sudah punya akun? <a href="/login">Login di sini</a></p>
</body></html>
"""

HTML_DASHBOARD = """
<!DOCTYPE html>
<html><head><title>Dashboard</title>
<style>
body { font-family: Arial; background: #f7f7f7; margin: 40px; }
.container { max-width: 600px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; }
table { width: 100%; border-collapse: collapse; margin-top: 20px; }
th, td { padding: 10px; border: 1px solid #ccc; }
</style>
</head><body>
<div class="container">
<h2>Halo, {{ user }}!</h2>
<form method="post">
  <label>Deskripsi:</label><input name="description" required><br>
  <label>Jumlah:</label><input name="amount" type="number" step="0.01" required><br>
  <label>Kategori:</label>
  <select name="category">
    <option value="Income">Pemasukan</option>
    <option value="Expense">Pengeluaran</option>
  </select><br><br>
  <button type="submit">Tambah</button>
</form>

{% if transactions %}
<table><tr><th>Tanggal</th><th>Deskripsi</th><th>Jumlah</th><th>Kategori</th></tr>
{% for tx in transactions %}
<tr><td>{{ tx['date'] }}</td><td>{{ tx['description'] }}</td><td>{{ tx['amount'] }}</td><td>{{ tx['category'] }}</td></tr>
{% endfor %}
</table>
{% endif %}

<p><strong>Pemasukan:</strong> Rp {{ income }}<br>
<strong>Pengeluaran:</strong> Rp {{ expense }}<br>
<strong>Saldo:</strong> Rp {{ balance }}</p>
<a href="/logout">Logout</a>
</div>
</body></html>
"""

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return 'Username sudah digunakan.'
        users[username] = generate_password_hash(password)
        user_transactions[username] = []
        return redirect('/login')
    return HTML_REGISTER

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect('/dashboard')
        return 'Login gagal.'
    return HTML_LOGIN

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']
    if request.method == 'POST':
        desc = request.form['description']
        amount = float(request.form['amount'])
        category = request.form['category']
        user_transactions[username].append({
            'date': datetime.date.today().strftime('%Y-%m-%d'),
            'description': desc,
            'amount': amount,
            'category': category
        })

    transactions = user_transactions[username]
    income = sum(tx['amount'] for tx in transactions if tx['category'] == 'Income')
    expense = sum(tx['amount'] for tx in transactions if tx['category'] == 'Expense')
    balance = income - expense

    return render_template_string(HTML_DASHBOARD, user=username, transactions=transactions,
                                  income="{:,.2f}".format(income), expense="{:,.2f}".format(expense),
                                  balance="{:,.2f}".format(balance))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
