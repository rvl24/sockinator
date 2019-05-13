import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    return render_template("apology.html")


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def check():
    """Return true if username available, else false, in JSON format"""
    status = db.execute("SELECT * FROM users WHERE username = :name", name=request.args.get("username"))

    if len(status) > 0:
        return jsonify(False)

    else:
        return jsonify(True)
