import logging as log

from api_client import ApiClient
from bybit_manager import BybitManager
from types_1 import *

API_KEY = ""
API_SECRET = ""

def main():
    log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    api_client = ApiClient(api_key=API_KEY, api_secret=API_SECRET)
    bybit_manager = BybitManager(api_client=api_client)
    bybit_manager.place_market_order_spot_to_usdt(coin="BTC", side=Side.BUY, percent_of_balance=10, tp_percentage=10, sl_percentage=10)

if __name__ == "__main__":
    main()
