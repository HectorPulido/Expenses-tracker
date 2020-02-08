from Views.View import View
from flask import views, session, render_template, redirect, url_for
from Class.Expense import Expense
from werkzeug.wrappers.response import Response

class Logout(View):
    methods = ['GET']

    def dispatch_request(self):
        session["user_id"] = None
        return redirect(url_for("login"))
