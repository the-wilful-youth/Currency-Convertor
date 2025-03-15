import os
from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API Key securely from .env
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://v6.exchangerate-api.com/v6/"

@app.route("/")
def home():
    return render_template("index.html")

# API to fetch available currencies
@app.route("/currencies", methods=["GET"])
def get_currencies():
    url = f"{BASE_URL}{API_KEY}/codes"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return jsonify({"error": "Failed to load currencies"}), 500

    currencies = {code: name for code, name in data["supported_codes"]}
    return jsonify({"currencies": currencies})

# API to convert currency
@app.route("/convert", methods=["GET"])
def convert_currency():
    from_currency = request.args.get("from")
    to_currency = request.args.get("to")
    amount = float(request.args.get("amount", 1))

    url = f"{BASE_URL}{API_KEY}/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or to_currency not in data["conversion_rates"]:
        return jsonify({"error": "Invalid currency"}), 400

    rate = data["conversion_rates"][to_currency]
    converted_amount = round(amount * rate, 2)

    return jsonify({"converted_amount": converted_amount})

if __name__ == "__main__":
    app.run(debug=True)
