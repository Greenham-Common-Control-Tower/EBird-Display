from flask import Flask
import requests
import json

# Edit These Flags To Customize the software
PORT=1991
KEY="6ohcvqhs11a7"
LOCATION=""

#Begining of Function Definitions
def fetchData():
    headers = {'X-eBirdApiToken': KEY}
    response = requests.get(f"https://api.ebird.org/v2/data/obs/{LOCATION}/recent", headers=headers)
    data = response.text
    return data

## Begining of Active Code
print("Initializing Web Server")
app = Flask(__name__)


@app.route("/")
def main():
    return "<p>Flask is Running<P>"

if __name__ == "__main__":
    app.run(port=PORT)