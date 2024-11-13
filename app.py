import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
from libs.db import Database
from auth.authentication import UserAuth  # Import the UserAuth class from auth/authentication.py

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

db = Database()
users_collection = db.get_users_collection()

user_auth = UserAuth(users_collection)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if user_auth.register_user(username, email, password):
            flash("Registration successful. Please log in.")
            return redirect(url_for("login"))
        else:
            flash("User already exists.")
    return render_template("register.html")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if user_auth.login_user(email, password):
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password.")
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", username=session["user"])
    else:
        flash("You need to log in first.")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully.")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
