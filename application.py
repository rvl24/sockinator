import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
app = Flask(__name__)

db = SQL("https://data.heroku.com/datastores/5a1cc4d0-c58e-4bd7-b61f-0baa18e96e51")


@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello, World!</h1>
    """


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
