from Views.View import View
from flask import views, session, render_template, redirect, url_for, request, Response
from Class.Expense import Expense


class DownloadData(View):
    methods = ["POST", "GET"]

    def dispatch_request(self):
        user_id = session.get("user_id", None)
        if user_id is None:
            return redirect(url_for("login"))

        if request.method != "POST":
            return render_template("seeall.html")

        expenses = Expense.getExpenses(user_id, None)
        csv = Expense.generateCsv(expenses, ";")

        headers = {
            "Content-disposition": "attachment; filename=data.csv"
        }

        return Response(csv, mimetype="text/csv", headers=headers)
