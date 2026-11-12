"""
Deliberately vulnerable Flask app for a GitHub code scanning (CodeQL) demo.
DO NOT deploy this anywhere. Each route contains a classic bug CodeQL will flag.
"""
import os
import sqlite3
import subprocess

from flask import Flask, request

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect("demo.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)")
    return conn


# 1) SQL injection — user input concatenated into a query
@app.route("/user")
def get_user():
    name = request.args.get("name", "")
    query = "SELECT * FROM users WHERE name = '" + name + "'"
    rows = get_db().execute(query).fetchall()
    return {"rows": rows}


# 2) Command injection — user input passed to a shell
@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    output = subprocess.check_output("ping -c 1 " + host, shell=True)
    return output


# 3) Path traversal — user controls which file is read
@app.route("/read")
def read_file():
    filename = request.args.get("file", "readme.txt")
    with open(os.path.join("files", filename)) as f:
        return f.read()


# 4) Reflected XSS — user input echoed into HTML
@app.route("/hello")
def hello():
    name = request.args.get("name", "world")
    return "<h1>Hello " + name + "</h1>"


if __name__ == "__main__":
    # 5) Flask debug mode enabled
    app.run(debug=True)
