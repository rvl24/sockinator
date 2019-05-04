import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)


@app.route('/')
def homepage():
    return """
    <h1>Hello, World!</h1>
    """


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
