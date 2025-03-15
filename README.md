# 🌍 Real-Time Currency Converter

A sleek, modern, and responsive **real-time currency converter** built using **Flask, JavaScript, and TailwindCSS**. It fetches the latest exchange rates from an external API and provides a seamless user experience with smooth animations and a minimalist UI.

## ✨ Features

✅ **Live Currency Conversion** – Get real-time exchange rates with API integration.  
✅ **Cache Optimization** – Rates are cached for **10 minutes** to improve performance.  
✅ **Minimalistic & Responsive UI** – Designed with **TailwindCSS** for a smooth experience.  
✅ **Swap Functionality** – Easily switch between currencies with a single click.  
✅ **Auto Rate Updates** – Automatically fetches fresh exchange rates every **10 minutes**.  
✅ **Error Handling** – Displays user-friendly messages for invalid inputs or API failures.

---

## 🚀 Tech Stack

🔹 **Backend:** Flask (Python)  
🔹 **Frontend:** HTML, JavaScript, TailwindCSS  
🔹 **API:** ExchangeRate-API  
🔹 **Environment Variables:** dotenv for secure API key storage

---

## 📦 Installation

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/yourusername/currency-converter.git
cd currency-converter
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)

```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables

Create a `.env` file in the project root and add your **ExchangeRate-API key**:

```sh
API_KEY=your_api_key_here
```

### 5️⃣ Run the Application

```sh
python app.py
```

The app will run on **`http://127.0.0.1:5000`**.

---

## 🖥️ API Endpoints

### 🔹 Get Available Currencies

```http
GET /currencies
```

**Response:**

```json
{
  "currencies": {
    "USD": "United States Dollar",
    "EUR": "Euro",
    "INR": "Indian Rupee"
  }
}
```

### 🔹 Convert Currency

```http
GET /convert?from=USD&to=INR&amount=100
```

**Response:**

```json
{
  "converted_amount": 8300.5,
  "exchange_rate": 83.005,
  "from_currency": "USD",
  "to_currency": "INR"
}
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

---
