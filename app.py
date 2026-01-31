from flask import Flask, render_template
from datetime import datetime
from crypto_utils import get_top_coins, get_crypto_data, predict_price, send_notification

app = Flask(__name__)

# Fetch top coins and initialize price history
CRYPTOCURRENCIES = get_top_coins(limit=5)
price_history = {coin: [] for coin in CRYPTOCURRENCIES}
market_cap_history = []


@app.route("/")
def dashboard():
    global price_history, market_cap_history

    # Fetch current prices
    prices, market_caps, total_market_cap = get_crypto_data(CRYPTOCURRENCIES)

    # Track total market cap history and calculate change
    market_cap_history.append(total_market_cap)
    if len(market_cap_history) > 2:
        market_cap_history.pop(0)

    if len(market_cap_history) > 1:
        prev_total = market_cap_history[-2]
        total_market_cap_change = ((total_market_cap - prev_total) / prev_total) * 100
    else:
        total_market_cap_change = 0

    # Price predictions & notifications
    predictions = {}
    for coin, price in prices.items():
        if coin not in price_history:
            price_history[coin] = []

        day = len(price_history[coin]) + 1
        price_history[coin].append((day, price))
        if len(price_history[coin]) > 30:
            price_history[coin].pop(0)

        predicted = predict_price(price_history[coin])
        predictions[coin] = predicted

        if len(price_history[coin]) > 1:
            prev_price = price_history[coin][-2][1]
            change = ((price - prev_price) / prev_price) * 100
            if abs(change) >= 5:
                send_notification(f"{coin} price changed {change:.2f}%: Current ${price}, Predicted ${predicted}")

    return render_template(
        "index.html",
        prices=prices,
        predictions=predictions,
        market_caps=market_caps,
        total_market_cap=total_market_cap,
        total_market_cap_change=total_market_cap_change,
        timestamp=datetime.now()
    )


if __name__ == "__main__":
    app.run(debug=True)
