import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)


@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello, World!</h1>
    """


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
