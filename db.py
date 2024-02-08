"""
A single file key-value store with a HTTP interface.
"""
from collections import defaultdict

from flask import Flask, request

INDEX = defaultdict(int)
STORE = "store.data"

def generateIndex():
    """ Generates in-memory hash index. """
    with open(STORE) as f:
        offset = 0
        while (line := f.readline()):
            key, _ = line.strip().split(",")
            INDEX[key] = offset
            offset = f.tell()

    return "", 200

def setupApp():
    # Boot-up the hash index into memory. Before you say it, I know this is a
    # sucky implementation. But hey, it works and it makes the store somewhat
    # durable between restarts so I call it a win.
    generateIndex()
    return Flask(__name__)

# "The" db.
db = setupApp()

@db.route("/")
def home():
    return "<h1> Welcome to foo.db </h1>"

@db.get("/db/<key>")
def get(key):
    print(INDEX)
    offset = INDEX.get(key, None)
    if offset is None:
        return "Missing Key", 404

    with open(STORE) as f:
        f.seek(offset)
        key, value = f.readline().strip().split(",")
        return value

@db.post("/db/<key>")
def put(key):
    body = str(request.data, encoding="utf8")

    # Simple log structured storage.
    with open(STORE, "a") as f:
        offset = f.tell()
        print(f"{key},{body}", file=f)
        INDEX[key] = offset # INDEX stores the segment offset.

    return "", 200

if __name__ == "__main__":
    db.run(debug=True)
