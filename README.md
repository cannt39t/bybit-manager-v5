# Bybit Trading Manager

This project is a simple Python-based trading bot for the **Bybit** exchange. The bot leverages the Bybit API to place market orders on the spot market. It is designed to make automated trades based on a percentage of your account balance, including optional take-profit (TP) and stop-loss (SL) features.

## 📋 Requirements

- Python 3.8 or higher
- `requests` library for HTTP requests
- Bybit API credentials (API_KEY and API_SECRET)

## 📦 Installation

1. Clone the repository or download the project files:
    ```bash
    git clone https://github.com/your_repo/bybit-trading-bot.git
    cd bybit-trading-bot
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

- Set your API keys in `main.py`:
    ```python
    API_KEY = "your_api_key"
    API_SECRET = "your_api_secret"
    ```

- Customize the order parameters:
    - `coin`: Specify the coin ticker, e.g., `"BTC"`.
    - `side`: Specify the order side — `Side.BUY` or `Side.SELL`.
    - `percent_of_balance`: The percentage of your balance to use for the trade.
    - `tp_percentage`: The take-profit percentage (optional).
    - `sl_percentage`: The stop-loss percentage (optional).

Example usage:
```python
bybit_manager.place_market_order_spot_to_usdt(coin="BTC", side=Side.BUY, percent_of_balance=10, tp_percentage=10, sl_percentage=10)
```

## 🚀 Running the Bot

To start the bot, use the following command:
```bash
python main.py
```

## 📄 Project Structure

```bash
.
├── main.py             # Main script to run the bot
├── api_client.py       # Module for interacting with Bybit API
├── bybit_manager.py    # Module for order management
├── types_1.py          # Module for data types and enums
├── requirements.txt    # Dependencies file
└── README.md           # Project documentation
```

### Modules Overview

- **api_client.py**: Handles API requests to Bybit.
- **bybit_manager.py**: Contains the logic for placing orders on the exchange.
- **types_1.py**: Defines enums and data types, such as `Side.BUY` and `Side.SELL`.

## 🛠️ API Setup

To use the bot, you need to generate API keys from [Bybit](https://www.bybit.com):
- Go to "API Management" in your Bybit account.
- Create a new API key with the necessary permissions (recommended: "Trade" only).

## ⚠️ Warnings

- **Use at your own risk!** Cryptocurrency trading involves significant risk.
- Test the bot with a demo account before using it in a live environment.
- Ensure your API keys are kept safe and not exposed publicly.
