import firebase_admin
from flask import jsonify
from flask import Flask, session, redirect, url_for, request, render_template, flash
from firebase_admin import credentials, firestore
from Class.Expense import Expense
from Class.User import User
from const import *

app = Flask(__name__)
app.secret_key = SECRET_FLASK_KEY


@app.route("/")
def index():
    user_id = session.get("user_id", None)
    if user_id is None:
        return redirect(url_for("login"))
    expenses = Expense.getExpenses(user_id)
    return render_template("expenses.html", expenses=expenses)

@app.route("/seeall")
def seeall():
    user_id = session.get("user_id", None)
    if user_id is None:
        return redirect(url_for("login"))
    expenses = Expense.getExpenses(user_id, None)
    return render_template("expenses.html", expenses=expenses)

@app.route("/register_data", methods=["POST", "GET"])
def register_data():
    user_id = session.get("user_id", None)
    if user_id is None:
        return redirect(url_for("login"))
    if request.method != "POST":
        return redirect(url_for("index"))

    type_data = request.form.get("type_data", None)
    value = request.form.get("value", None)
    description = request.form.get("description", None)

    if type_data is None:
        flash("type data is necessary to continue")
        return redirect(url_for("index"))
    if value is None:
        flash("value is necessary to continue")
        return redirect(url_for("index"))
    if description is None:
        flash("descriptionis necessary to continue")
        return redirect(url_for("index"))

    exp = Expense(description, value, type_data, user_id)
    exp.saveExpense()

    return redirect(url_for("index"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        password = request.form.get("password", None)
        username = request.form.get("username", None)

        if password is None:
            flash("Password missing")
            return render_template("login.html")

        if username is None:
            flash("Username missing")
            return render_template("login.html")

        val, id = User.validate_user(username, password)
        if val:
            session["user_id"] = id
            return redirect(url_for("index"))

        flash("Username or Password invalid")
        return render_template("login.html")

    return render_template("login.html")


if __name__ == "__main__":
    cred = credentials.Certificate(CERTIFICATE)
    firebase_admin.initialize_app(cred)
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
