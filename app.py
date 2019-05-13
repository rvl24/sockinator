import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, check


# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use Heroku PostgreSQL database
db = SQL("postgres://djguwhovfgmtjf:3b8fb50c286e296f59a503a6893348914c572b77073848d9835a94120818dd13@ec2-50-19-127-115.compute-1.amazonaws.com:5432/d4h7gvb1ahdvmu")

@app.route("/check", methods=["GET"])
def check_username():
    check()

@app.route("/")
def index():
    """Show main page"""
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Username required", category='message')
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Password required", category='message')
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], request.form.get("password")):
            flash("Invalid username and/or password", category='message')
            return render_template("login.html")
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            flash("Username and password required", category='message')
            return render_template("/register")

        # Check if username available
        status = db.execute("SELECT * FROM users WHERE username = :name", name=request.args.get("username"))
        if len(status) > 0:
            flash("Username taken", category='message')
            return render_template("/register")

        # check whether confirmation is the same as the original
        if request.form.get("password")!= request.form.get("confirmation"):
            flash("Passwords do not match", category='message')
            return render_template("/register")

        # hash the password (method, salt length poached from werkzeug example)
        password_hash = generate_password_hash(request.form.get("password"),
                                               method='pbkdf2:sha256', salt_length=8)

        # store username, password hash in database
        db.execute("INSERT INTO users (username, password_hash) VALUES (:u, :p)",
                   u=request.form.get("username"), p=password_hash)

        # notify the user that they've been properly registered
        flash("Registered!")
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/my_patterns", methods=["GET"])
def show_patterns():
    """Display saved patterns"""
    if session.get("user_id") is None:
        return render_template("my_patterns.html")
    else:
        return render_template("my_patterns_loggedin.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
