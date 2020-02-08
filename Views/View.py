from flask import views, session, request, redirect, url_for

class View(views.View):
    def check_login(self):
        user_id = session.get("user_id", None)
        if user_id is None:
            return redirect(url_for("login"))
        return user_id