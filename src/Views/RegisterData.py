from Views.View import View
from flask import session, render_template, redirect, url_for, flash, request
from Class.Expense import Expense

class RegisterData(View):
    methods = ["POST", "GET"]

    def dispatch_request(self):
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
