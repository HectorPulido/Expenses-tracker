from Views.View import View
from flask import views, session, render_template, redirect, url_for, request, flash
from Class.Expense import Expense
from Class.User import User

class Login(View):
    methods = ["GET", "POST"]
    def dispatch_request(self):
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
