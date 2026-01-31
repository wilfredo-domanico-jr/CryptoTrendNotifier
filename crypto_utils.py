import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
from config import API_URL, WEBHOOK_URL, PREDICTION_DAYS

# Fetch top coins by market cap
def get_top_coins(limit=5):
    url = f"{API_URL}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": "false"
    }
    response = requests.get(url, params=params)
    coins = response.json()
    return {coin['symbol'].upper(): coin['id'] for coin in coins}


# Fetch current prices and market caps
def get_crypto_data(cryptocurrencies):
    coin_ids = ','.join(cryptocurrencies.values())
    url = f"{API_URL}/simple/price"
    response = requests.get(
        url,
        params={
            'ids': coin_ids,
            'vs_currencies': 'usd',
            'include_market_cap': 'true'
        }
    )
    data = response.json()
    prices = {ticker: data[coin_id]['usd'] for ticker, coin_id in cryptocurrencies.items()}
    market_caps = {ticker: data[coin_id]['usd_market_cap'] for ticker, coin_id in cryptocurrencies.items()}
    total_market_cap = sum(market_caps.values())
    return prices, market_caps, total_market_cap


# Predict price using linear regression
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


# Send webhook notifications
def send_notification(message):
    if WEBHOOK_URL == "YOUR_WEBHOOK_URL_HERE":
        print(f"[Notification] {message}")
        return
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print(f"Webhook error: {e}")



def get_btc_dominance():
    url = f"{API_URL}/global"
    response = requests.get(url)
    data = response.json()
    dominance = data['data']['market_cap_percentage']['btc']  # BTC dominance %
    return dominance
