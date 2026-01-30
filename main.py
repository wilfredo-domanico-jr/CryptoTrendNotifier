import requests
import json
import time
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
from config import BTC_API_URL, WEBHOOK_URL, PREDICTION_DAYS

# Function to get current Bitcoin price
def get_btc_price():
    response = requests.get(BTC_API_URL)
    data = response.json()
    price = float(data['bpi']['USD']['rate'].replace(',', ''))
    return price

# Function to send a webhook notification
def send_notification(message):
    if WEBHOOK_URL == "YOUR_WEBHOOK_URL_HERE":
        print(f"[Notification] {message}")
        return
    payload = {"content": message}
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Failed to send notification: {e}")

# Function to predict future Bitcoin price using linear regression
def predict_price(price_history, days=PREDICTION_DAYS):
    df = pd.DataFrame(price_history, columns=["day", "price"])
    X = df["day"].values.reshape(-1, 1)
    y = df["price"].values
    model = LinearRegression()
    model.fit(X, y)
    future_day = [[df["day"].max() + days]]
    predicted_price = model.predict(future_day)[0]
    return round(predicted_price, 2)

# Main loop
def main():
    price_history = []
    day_counter = 1

    while True:
        try:
            price = get_btc_price()
            print(f"[{datetime.now()}] Current BTC Price: ${price}")
            price_history.append((day_counter, price))

            # Keep only the last 30 entries for prediction
            if len(price_history) > 30:
                price_history.pop(0)

            # Predict future price
            predicted = predict_price(price_history)
            print(f"Predicted BTC Price in {PREDICTION_DAYS} days: ${predicted}")

            # Send notification if price moves significantly (+/-5% as example)
            if len(price_history) > 1:
                previous_price = price_history[-2][1]
                change_percent = ((price - previous_price) / previous_price) * 100
                if abs(change_percent) >= 5:
                    send_notification(f"Bitcoin price changed {change_percent:.2f}%: Current ${price}, Predicted ${predicted}")

            day_counter += 1
            time.sleep(60)  # Fetch price every 60 seconds
        except KeyboardInterrupt:
            print("Stopping CryptoTrendNotifier...")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
