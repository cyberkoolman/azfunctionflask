from flask import Flask
import requests

# Always use relative import for custom module
from .package.module import MODULE_VALUE

app = Flask(__name__)

@app.route("/")
def index():
    return (
        "Try /joke for a randome joke"
    )

@app.route("/joke", methods=['GET'])
def joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    data = response.json()
    joke = data["setup"] + " . . . . . " + data["punchline"]

    return f"{joke}"

@app.route("/module")
def module():
    return f"loaded from FlaskApp.package.module = {MODULE_VALUE}"

if __name__ == "__main__":
    app.run()