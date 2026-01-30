from flask import Flask, render_template
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
from config import CRYPTOCURRENCIES, API_URL, WEBHOOK_URL, PREDICTION_DAYS

app = Flask(__name__)

# Store price history for predictions
price_history = {coin: [] for coin in CRYPTOCURRENCIES}

# Function to fetch cryptocurrency prices
def get_crypto_prices():
    coin_ids = ','.join(CRYPTOCURRENCIES.values())
    response = requests.get(API_URL, params={'ids': coin_ids, 'vs_currencies': 'usd'})
    data = response.json()
    
    # Map API data back to tickers
    prices = {ticker: data[coin_id]['usd'] for ticker, coin_id in CRYPTOCURRENCIES.items()}
    return prices

# Function to predict future price using linear regression
def predict_price(history):
    if len(history) < 2:
        return None
    df = pd.DataFrame(history, columns=["day", "price"])
    X = df["day"].values.reshape(-1, 1)
    y = df["price"].values
    model = LinearRegression()
    model.fit(X, y)
    future_day = [[df["day"].max() + PREDICTION_DAYS]]
    return round(model.predict(future_day)[0], 2)

# Function to send webhook notifications
def send_notification(message):
    if WEBHOOK_URL == "YOUR_WEBHOOK_URL_HERE":
        print(f"[Notification] {message}")
        return
    payload = {"content": message}
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Webhook error: {e}")

# Route to display dashboard
@app.route("/")
def dashboard():
    global price_history
    prices = get_crypto_prices()
    predictions = {}

    for coin, price in prices.items():
        # Add price to history
        day = len(price_history[coin]) + 1
        price_history[coin].append((day, price))
        if len(price_history[coin]) > 30:
            price_history[coin].pop(0)

        # Predict price
        predicted = predict_price(price_history[coin])
        predictions[coin] = predicted

        # Send notification if change >5%
        if len(price_history[coin]) > 1:
            prev_price = price_history[coin][-2][1]
            change = ((price - prev_price) / prev_price) * 100
            if abs(change) >= 5:
                send_notification(f"{coin} price changed {change:.2f}%: Current ${price}, Predicted ${predicted}")

    return render_template("index.html", prices=prices, predictions=predictions, timestamp=datetime.now())

if __name__ == "__main__":
    app.run(debug=True)
