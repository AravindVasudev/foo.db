"""
A single file key-value store with a HTTP interface.
"""
from collections import defaultdict

from flask import Flask, request

# "The" db.
db = Flask(__name__)
store = defaultdict(str)

@db.route("/")
def home():
    return "<h1> Welcome to foo.db </h1>"

@db.get("/db/<key>")
def get(key):
    return store[key]

@db.post("/db/<key>")
def put(key):
    # Raw request body is stored.
    store[key] = request.data
    return "", 200
