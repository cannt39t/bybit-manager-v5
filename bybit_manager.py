import logging
import math
from api_client import ApiClient
from types_1 import *

log = logging.getLogger(__name__)

class BybitManager:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        log.info("BybitManager initialized with API client.")

    def place_market_order_spot_to_usdt(
        self, coin: str, side: Side, percent_of_balance: float, 
        tp_percentage: float = None, sl_percentage: float = None
    ):
        """
        Place a spot market order and set take profit and/or stop loss if specified.
        """
        symbol = f"{coin}USDT"
        order_id = self._execute_market_order(symbol, side, percent_of_balance)
        avg_price = self._get_avg_price(Category.SPOT, order_id)
        qty = self._get_formatted_balance(coin, symbol)

        if sl_percentage:
            self._set_stop_loss(avg_price, qty, symbol, sl_percentage)
        if tp_percentage:
            self._set_take_profit(avg_price, qty, symbol, tp_percentage)

    def _execute_market_order(self, symbol: str, side: Side, percent_of_balance: float) -> str:
        """
        Executes a market order and returns the order ID.
        """
        qty = self._calculate_order_qty(symbol, percent_of_balance)
        log.info(f"Executing market order for {symbol} - Side: {side}, Quantity: {qty}, Percent of Balance: {percent_of_balance}%")
        response = self.api_client.place_order(
            category=Category.SPOT, symbol=symbol, side=side, order_type=OrderType.MARKET, 
            qty=qty, market_unit="quoteCoin"
        )
        return response['result']['orderId']

    def _set_take_profit(self, avg_price: float, qty: float, symbol: str, tp_percentage: float):
        """
        Sets a take profit order at a specified percentage above the average price.
        """
        tp_price = self._calculate_target_price(symbol, avg_price, tp_percentage, is_take_profit=True)
        self._place_limit_order(symbol, qty, tp_price, Side.SELL)

    def _set_stop_loss(self, avg_price: float, qty: float, symbol: str, sl_percentage: float):
        """
        Sets a stop-loss order at a specified percentage below the average price.
        """
        sl_price = self._calculate_target_price(symbol, avg_price, sl_percentage, is_take_profit=False)
        self._place_stop_loss(symbol, qty, sl_price)

    def _calculate_target_price(self, symbol: str, avg_price: float, percentage: float, is_take_profit: bool) -> float:
        """
        Calculates target price based on percentage for take-profit or stop-loss.
        """
        multiplier = 1 + (percentage / 100) if is_take_profit else 1 - (percentage / 100)
        target_price = avg_price * multiplier
        return round(target_price, self._get_price_precision(Category.SPOT, symbol))

    def _place_limit_order(self, symbol: str, qty: float, price: float, side: Side, 
                           time_in_force: TimeInForce = TimeInForce.GTC):
        """
        Places a limit order with the given parameters.
        """
        log.info(f"Placing limit order for {symbol} - Side: {side}, Quantity: {qty}, Price: {price}")
        response = self.api_client.place_order(
            category=Category.SPOT, symbol=symbol, side=side, order_type=OrderType.LIMIT, 
            qty=qty, price=price, time_in_force=time_in_force
        )
        log.info(f"Limit order placed successfully: Order ID {response['result']['orderId']}")
        return response['result']['orderId']

    def _place_stop_loss(self, symbol: str, qty: float, trigger_price: float):
        """
        Places a stop-loss order.
        """
        log.info(f"Setting stop-loss for {symbol} - Quantity: {qty}, Trigger Price: {trigger_price}")
        response = self.api_client.place_order(
            category=Category.SPOT, symbol=symbol, side=Side.SELL, order_type=OrderType.MARKET, 
            qty=qty, trigger_price=trigger_price, order_filter=OrderFilter.STOP_ORDER
        )
        log.info(f"Stop-loss order placed successfully: {response}")
        return response

    def _get_formatted_balance(self, coin: str, symbol: str) -> float:
        """
        Retrieves and formats the balance for the given coin and symbol.
        """
        balance = self.get_balance(coin)
        precision = self._get_qty_precision(Category.SPOT, symbol)
        return self._round_to_precision(float(balance), precision)

    def get_balance(self, coin: str) -> float:
        """
        Retrieves the balance for a specified coin.
        """
        log.info(f"Fetching balance for {coin}")
        balance = self.api_client.get_wallet_balance(account_type=AccountType.UNIFIED, coin=coin)
        available_balance = float(balance['result']['list'][0]['coin'][0]['availableToWithdraw'])
        log.info(f"Available balance for {coin}: {available_balance}")
        return available_balance

    def _calculate_order_qty(self, symbol: str, percent_of_balance: float) -> float:
        """
        Calculates quantity based on a percentage of the USDT balance.
        """
        usdt_balance = self.get_balance("USDT")
        qty_in_usdt = usdt_balance * (percent_of_balance / 100)
        log.info(f"Calculated quantity for {symbol}: {qty_in_usdt}")
        return round(qty_in_usdt, 0)

    def _get_avg_price(self, category: Category, order_id: str) -> float:
        """
        Retrieves the average price for a completed order.
        """
        order_data = self.api_client.get_order_by_id(category=category, order_id=order_id)
        return float(order_data['result']['list'][0]['avgPrice'])

    def _get_qty_precision(self, category: Category, symbol: str) -> int:
        """
        Retrieves the precision for quantity values based on the lot size filter.
        """
        lot_size_filter = self.api_client.get_instruments_info(category=category, symbol=symbol)
        precision_str = lot_size_filter['result']['list'][0]['lotSizeFilter']['basePrecision']
        return self._count_decimal_places(precision_str)

    def _get_price_precision(self, category: Category, symbol: str) -> int:
        """
        Retrieves the precision for price values based on the tick size filter.
        """
        tick_size_filter = self.api_client.get_instruments_info(category=category, symbol=symbol)
        precision_str = tick_size_filter['result']['list'][0]['priceFilter']['tickSize']
        return self._count_decimal_places(precision_str)

    @staticmethod
    def _count_decimal_places(value: str) -> int:
        """
        Counts the decimal places in a given string representation of a number.
        """
        if '.' in value:
            return len(value.split('.')[1])
        return 0

    @staticmethod
    def _round_to_precision(value: float, precision: int) -> float:
        """
        Rounds a value down to a specified decimal precision.
        """
        factor = 10 ** precision
        return math.floor(value * factor) / factor

    

    # TODO: probably should be changed, don't need now
    def set_tp_full(self, symbol: str, category: Category, order_id: str, take_profit_percentage: float):
        avg_price = self._get_avg_price_of_order(category=category, order_id=order_id)
        take_profit_price = avg_price * (1 + take_profit_percentage / 100)

        log.info(f"Setting FULL take profit for {symbol}: TP Price={take_profit_price:.4f}, Type={TP_SL_Mode.FULL.value}")
        response = self.api_client.set_trading_stop(
            category=Category.LINEAR,
            symbol=symbol,
            take_profit=str(take_profit_price),
            tpsl_mode=TP_SL_Mode.FULL
        )

        return response
    
    # TODO: implement
    def set_tp_partial(self, symbol: str, order_id: str, tp_qty: str = None, take_profit_percentage: float = None, tp_order_type: OrderType = OrderType.LIMIT):
        return 