from flask import request, session, render_template, redirect, url_for
from app.config import firebase_config
from app import app
from pyrebase import initialize_app

# @app.route('/')
# @app.route('/index')
# def index():
#     return "Hello, World!"

# Initialize firebase
firebase = initialize_app(firebase_config)
auth = firebase.auth()

# Home route
@app.route("/")
def home():
    if "user" in session:
        return f"Welcome, {session['user']}"
    return redirect(url_for("login"))

# Signup route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session["user"] = email
            return redirect(url_for("home"))
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template("signup.html")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session["user"] = email
            return redirect(url_for("home"))
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template("login.html")

# Logout route
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))