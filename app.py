from flask import Flask, render_template, request, redirect, url_for, g,flash

import sqlite3

app = Flask(__name__)
app.secret_key = 'secret'

# create database and table
conn = sqlite3.connect('expenses.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS expenses
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              party_name TEXT,
              name TEXT,
              amount FLOAT)''')
conn.commit()
conn.close()

# define routes
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'mypassword':
            return redirect(url_for('home'))
        else:
            flash('Invalid password. Please try again.', 'error')
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    password = request.form['password']
    if password == 'mypassword':
        return redirect(url_for('home'))
    else:
        flash('Invalid password. Please try again.', 'error')
        return redirect(url_for('login'))


@app.route('/home')
def home():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT party_name, name, SUM(amount) FROM expenses GROUP BY party_name, name')
    data = c.fetchall()
    conn.close()
    return render_template('home.html', data=data)

@app.before_request
def before_request():
    g.db = sqlite3.connect('expenses.db')

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/add_expense')
def add_expense():
    return render_template('add_expense.html')

@app.route('/submit_expense', methods=['POST'])
def submit_expense():
    party_name = request.form['party_name']
    name = request.form['name']
    amount = float(request.form['amount'])
    c = g.db.cursor()
    c.execute('INSERT INTO expenses (party_name, name, amount) VALUES (?, ?, ?)', (party_name, name, amount))
    g.db.commit()
    return redirect(url_for('home'))

@app.route('/delete_expense', methods=['POST'])
def delete_expense():
    party_name = request.form['party_name']
    name = request.form['name']
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE party_name = ? AND name = ?', (party_name, name))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

