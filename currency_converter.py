import requests
import tkinter as tk
from tkinter import ttk, messagebox

# API Key (Replace with your actual API key)
API_KEY = "1c3baa16d853be0c965ae0aa"
BASE_URL = "https://v6.exchangerate-api.com/v6/"

# Function to fetch exchange rates
def get_exchange_rate(from_currency, to_currency):
    try:
        url = f"{BASE_URL}{API_KEY}/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            messagebox.showerror("Error", "Failed to fetch exchange rates")
            return None
        
        return data["conversion_rates"].get(to_currency, None)
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching exchange rate: {e}")
        return None

# Function to perform currency conversion
def convert_currency():
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_box.get()
        to_currency = to_currency_box.get()
        
        rate = get_exchange_rate(from_currency, to_currency)
        if rate is None:
            messagebox.showerror("Error", "Invalid currency selection")
            return
        
        converted_amount = round(amount * rate, 2)
        result_label.config(text=f"Converted Amount: {converted_amount} {to_currency}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")

# GUI Setup
root = tk.Tk()
root.title("Currency Converter")
root.geometry("350x300")
root.resizable(False, False)

# Title Label
title_label = tk.Label(root, text="Currency Converter", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Amount Entry
amount_entry = tk.Entry(root, font=("Arial", 14))
amount_entry.pack(pady=5)
amount_entry.insert(0, "1")  # Default value

# Currency Dropdowns
currencies = ["USD", "EUR", "INR", "GBP", "AUD", "JPY", "CAD", "CNY"]
from_currency_box = ttk.Combobox(root, values=currencies, font=("Arial", 12))
from_currency_box.pack(pady=5)
from_currency_box.set("USD")

to_currency_box = ttk.Combobox(root, values=currencies, font=("Arial", 12))
to_currency_box.pack(pady=5)
to_currency_box.set("INR")

# Convert Button
convert_button = tk.Button(root, text="Convert", font=("Arial", 12), command=convert_currency)
convert_button.pack(pady=10)

# Result Label
result_label = tk.Label(root, text="Converted Amount: ", font=("Arial", 14, "bold"))
result_label.pack(pady=10)

# Run the GUI
root.mainloop()
