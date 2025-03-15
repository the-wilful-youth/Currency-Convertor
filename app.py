from flask import Flask, request, jsonify, render_template
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://v6.exchangerate-api.com/v6/"

@app.route("/")  # This serves the webpage
def home():
    return render_template("index.html")

@app.route("/currencies", methods=["GET"])
def get_currencies():
    response = requests.get(f"{BASE_URL}{API_KEY}/codes")
    data = response.json()
    if response.status_code != 200:
        return jsonify({"error": "Failed to load currencies"}), 500
    return jsonify({"currencies": {code: name for code, name in data["supported_codes"]}})

@app.route("/convert", methods=["GET"])
def convert_currency():
    from_currency = request.args.get("from")
    to_currency = request.args.get("to")
    amount = request.args.get("amount", type=float, default=1)

    if not from_currency or not to_currency:
        return jsonify({"error": "Please provide valid currencies"}), 400

    url = f"{BASE_URL}{API_KEY}/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or "conversion_rates" not in data:
        return jsonify({"error": "Failed to fetch exchange rates"}), 500

    rate = data["conversion_rates"].get(to_currency)
    if rate is None:
        return jsonify({"error": "Invalid conversion rate"}), 400

    converted_amount = round(amount * rate, 2)
    return jsonify({"converted_amount": converted_amount, "exchange_rate": rate})

if __name__ == "__main__":
    app.run(debug=True)
