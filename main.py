from flask import Flask
import requests
import json

# Edit These Flags To Customize the software
PORT=1991
KEY="6ohcvqhs11a7"

print("Initializing Web Server")
app = Flask(__name__)


@app.route("/")
def main():
    return "<p>Flask is Running<P>"

if __name__ == "__main__":
    app.run(port=PORT)