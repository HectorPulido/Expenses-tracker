from Views.View import View
from flask import views, session, render_template, redirect, url_for
from Class.Expense import Expense
from werkzeug.wrappers.response import Response


class Index(View):
    methods = ['GET']

    def dispatch_request(self):
        user_id = session.get("user_id", None)
        if user_id is None:
            return redirect(url_for("login"))
        expenses = Expense.getExpenses(user_id)
        return render_template("expenses.html", expenses=expenses)
