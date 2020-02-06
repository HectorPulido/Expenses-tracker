import firebase_admin
from flask import jsonify
from flask import Flask, session, redirect, url_for, request, render_template
from firebase_admin import credentials, firestore
from Class.Expense import Expense
from Class.User import User
from const import *

app = Flask(__name__)
app.secret_key = SECRET_FLASK_KEY


@app.route('/')
def index():
    user_id = session.get('user_id', None)
    if user_id is None:
        return redirect(url_for('login'))
    expenses = Expense.getExpenses(user_id)
    return render_template('expenses.html', expenses=expenses)


@app.route('/register_data', methods=['POST', 'GET'])
def register_data():
    user_id = session.get('user_id', None)
    if user_id is None:
        return redirect(url_for('login'))
    if request.method != 'POST':
        return redirect(url_for('index'))

    type_of_register = request.form.get("type_of_register", None)
    value = request.form.get("value", None)
    description = request.form.get("description", None)

    if type_of_register is None:
        return redirect(url_for('index'))
    if value is None:
        return redirect(url_for('index'))
    if description is None:
        return redirect(url_for('index'))

    Expense()

    return redirect(url_for('index'))


@app.route('/seeall')
def seeall():
    user_id = session.get('user_id', None)
    if user_id is None:
        return redirect(url_for('login'))
    return redirect(url_for('index'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        password = request.form.get("password", None)
        username = request.form.get("username", None)

        if password is None:
            return render_template('login.html', error="Password missing")

        if username is None:
            return render_template('login.html', error="Username missing")

        val, id = User.validate_user(username, password)
        if val:
            session["user_id"] = id
            return redirect(url_for('index'))

        return render_template('login.html', error="Username or Password invalid")

    return render_template('login.html')


if __name__ == "__main__":
    cred = credentials.Certificate(CERTIFICATE)
    firebase_admin.initialize_app(cred)
    app.run(debug=True, host="0.0.0.0", port=5000)
