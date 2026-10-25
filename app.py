"""INTENTIONALLY VULNERABLE demo app. For scanner testing only."""
import hashlib
import ast
import os
import pickle
import sqlite3
import subprocess

import requests
import yaml
from flask import Flask, request

app = Flask(__name__)

# BUG 1 - Hardcoded secrets (CWE-798). All values are FAKE.
SECRET_KEY = os.environ.get('SECRET_KEY', '')
DB_PASSWORD = "admin123"
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')


def get_db():
    return sqlite3.connect("users.db")


@app.route("/user")
def get_user():
    # BUG 2 - SQL injection (CWE-89): user input joined into the query
    name = request.args.get("name", "")
    query = "SELECT * FROM users WHERE name = '" + name + "'"
    return str(get_db().execute(query).fetchall())


@app.route("/login", methods=["POST"])
def login():
    # BUG 3 - Weak hash MD5 for passwords (CWE-327)
    password = request.form.get("password", "")
    hashed = hashlib.md5(password.encode()).hexdigest()
    query = f"SELECT * FROM users WHERE password = '{hashed}'"  # BUG 3b - SQLi (f-string)
    return str(get_db().execute(query).fetchall())


@app.route("/ping")
def ping():
    # BUG 4 - Command injection (CWE-78): shell=True with user input
    host = request.args.get("host", "")
    return subprocess.check_output("ping -c 1 " + host, shell=True)


@app.route("/calc")
def calc():
    # BUG 5 - Code injection via ast.literal_eval(CWE-95)
    return str(ast.literal_eval(request.args.get("expr", "1+1")))


@app.route("/load", methods=["POST"])
def load():
    # BUG 6 - Unsafe deserialization with pickle (CWE-502)
    return str(pickle.loads(request.data))


@app.route("/config", methods=["POST"])
def config():
    # BUG 7 - Unsafe yaml.safe_load(CWE-502)
    return str(yaml.safe_load(request.data))


@app.route("/file")
def read_file():
    # BUG 8 - Path traversal (CWE-22)
    filename = request.args.get("name", "")
    with open(os.path.join("uploads", filename)) as f:
        return f.read()


@app.route("/fetch")
def fetch():
    # BUG 9 - SSRF (CWE-918) and TLS check turned off (CWE-295)
    url = request.args.get("url", "")
    return requests.get(url, verify=False, timeout=30).text


if __name__ == "__main__":
    # BUG 10 - Debug mode on + listens on all interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)
