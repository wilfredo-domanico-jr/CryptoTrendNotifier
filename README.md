# CryptoTrendNotifier 🚀

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**CryptoTrendNotifier** is a Python application that tracks real-time Cryptocurrency prices, sends instant alerts for significant price changes, and predicts future price trends using machine learning. It’s built with APIs, webhooks, and data-driven forecasting techniques, making it ideal for crypto enthusiasts, traders, and developers exploring financial data applications.

---

## Screenshot

<p align="center">
  <img src="static/images/screenshot.png" alt="MiniURL Screenshot" width="700">
</p>

---

## Features

- Real-time Cryptocurrency price tracking using public APIs.
- Instant notifications for significant price movements.
- Predictive modeling for future price trends using machine learning.
- Integration with webhooks to send alerts to external services.
- Modular Python code for easy customization and extension.

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/wilfredo-domanico-jr/CryptoTrendNotifier.git
cd CryptoTrendNotifier
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Usage

1. Configure your API keys or webhook URLs in `config.example.py` (or your own `config.py`).
2. Run the application:

```bash
python main.py
```

3. Monitor real-time Cryptocurrency prices and receive alerts on your configured service.

---

## Technologies & Libraries

- Python 3.13+
- `requests` – HTTP API requests
- `pandas` – data manipulation
- `scikit-learn` – machine learning predictions
- Webhooks – notifications to external services
- Flask for web app interface

---

## License

This project is licensed under the [MIT License](LICENSE).

---
