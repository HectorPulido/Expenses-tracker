from Views.View import View
from flask import views, session, render_template, redirect, url_for
from Class.Expense import Expense


class SeeAll(View):
    methods = ["POST", "GET"]

    def dispatch_request(self):
        user_id = session.get("user_id", None)
        if user_id is None:
            return redirect(url_for("login"))
        expenses = Expense.getExpenses(user_id, None)
        average = Expense.averageOfExpenses(expenses)
        sumOfExpenses = Expense.sumOfExpenses(expenses)
        return render_template("seeall.html", expenses=expenses, average=average, sumOfExpenses=sumOfExpenses)
