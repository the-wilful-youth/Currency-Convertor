import os
import time
from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Secure API Key
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://v6.exchangerate-api.com/v6/"

# Global storage for currency data
CURRENCIES = {}
EXCHANGE_RATES_CACHE = {}
CACHE_TIMESTAMP = 0
CACHE_EXPIRY = 600  # Cache expiration time in seconds (10 minutes)

def load_currencies():
    """Fetch available currencies and store them globally."""
    global CURRENCIES
    url = f"{BASE_URL}{API_KEY}/codes"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "supported_codes" in data:
        CURRENCIES = {code: name for code, name in data["supported_codes"]}
    else:
        CURRENCIES = {}

# Load currencies when the server starts
load_currencies()

@app.route("/")
def home():
    """Render the main HTML page."""
    return render_template("index.html")

@app.route("/currencies", methods=["GET"])
def get_currencies():
    """Return available currencies."""
    if not CURRENCIES:
        return jsonify({"error": "Failed to load currencies"}), 500
    return jsonify({"currencies": CURRENCIES})

@app.route("/convert", methods=["GET"])
def convert_currency():
    """Convert currency using cached exchange rates."""
    global EXCHANGE_RATES_CACHE, CACHE_TIMESTAMP

    from_currency = request.args.get("from")
    to_currency = request.args.get("to")
    amount = request.args.get("amount", type=float, default=1)

    # Validate inputs
    if not from_currency or not to_currency or from_currency not in CURRENCIES or to_currency not in CURRENCIES:
        return jsonify({"error": "Invalid or unsupported currency"}), 400

    current_time = time.time()
    
    # Check if cached data is still valid
    if from_currency in EXCHANGE_RATES_CACHE and (current_time - CACHE_TIMESTAMP) < CACHE_EXPIRY:
        exchange_rate = EXCHANGE_RATES_CACHE[from_currency].get(to_currency)
    else:
        # Fetch latest exchange rates and update cache
        url = f"{BASE_URL}{API_KEY}/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or "conversion_rates" not in data:
            return jsonify({"error": "Failed to fetch exchange rates"}), 500

        EXCHANGE_RATES_CACHE[from_currency] = data["conversion_rates"]
        CACHE_TIMESTAMP = current_time
        exchange_rate = data["conversion_rates"].get(to_currency)

    if not exchange_rate:
        return jsonify({"error": "Conversion rate not found"}), 400

    converted_amount = round(amount * exchange_rate, 2)

    return jsonify({
        "converted_amount": converted_amount,
        "exchange_rate": exchange_rate,
        "from_currency": from_currency,
        "to_currency": to_currency
    })

if __name__ == "__main__":
    app.run(debug=True)
