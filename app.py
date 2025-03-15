from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Replace with your actual API key
API_KEY = "1c3baa16d853be0c965ae0aa"
BASE_URL = "https://v6.exchangerate-api.com/v6/"

# Route to serve the webpage
@app.route("/")
def home():
    return render_template("index.html")

# API route to get exchange rates
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
