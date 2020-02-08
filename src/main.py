import firebase_admin
from flask import jsonify
from flask import Flask, session, redirect, url_for, request, render_template, flash
from firebase_admin import credentials, firestore
from Views.Index import Index
from Views.RegisterData import RegisterData
from Views.SeeAll import SeeAll
from Views.Login import Login
from Views.Logout import Logout
from Views.DownloadData import DownloadData
from const import CERTIFICATE, SECRET_FLASK_KEY, PORT, DEBUG

app = Flask(__name__)
app.secret_key = SECRET_FLASK_KEY

app.add_url_rule('/', view_func=Index.as_view('index'))
app.add_url_rule('/register_data', view_func=RegisterData.as_view('register'))
app.add_url_rule('/see_all', view_func=SeeAll.as_view('seeall'))
app.add_url_rule('/login', view_func=Login.as_view('login'))
app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
app.add_url_rule('/download_data', view_func=DownloadData.as_view('download_data'))

if __name__ == "__main__":
    cred = credentials.Certificate(CERTIFICATE)
    firebase_admin.initialize_app(cred)
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
