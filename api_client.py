import logging as log
import pprint

from types_1 import *
from pybit.unified_trading import HTTP

class ApiClient:

    def __init__(self, api_key: str, api_secret: str, testnet: bool = False, demo: bool = True):
        """
        Initializes the API client for trading.
        
        :param api_key: API key.
        :param api_secret: API secret.
        :param testnet: Whether to use the testnet.
        :param demo: Whether to use the demo.
        """
        self.session = HTTP(testnet=testnet, demo=demo, api_key=api_key, api_secret=api_secret)
        log.info("Initialized ApiClient with testnet=%s", testnet)



    def place_order(self, 
                category: Category,
                symbol: str, 
                side: Side, 
                order_type: OrderType, 
                qty: str, 
                price: str = None, 
                time_in_force: TimeInForce = TimeInForce.IOC, 
                order_link_id: str = None, 
                is_leverage: int = 0, 
                order_filter: OrderFilter = OrderFilter.ORDER,
                market_unit: str = None, 
                trigger_price: str = None,
                trigger_direction: TriggerDirection = None, 
                trigger_by: TriggerBy = None,
                take_profit: str = None, 
                stop_loss: str = None,
                tp_trigger_by: TriggerBy = None, 
                sl_trigger_by: TriggerBy = None,
                reduce_only: bool = None, 
                close_on_trigger: bool = None,
                tp_sl_mode: TP_SL_Mode = None,
                tp_limit_price: str = None, 
                sl_limit_price: str = None,
                tp_order_type: TP_SL_OrderType = None, 
                sl_order_type: TP_SL_OrderType = None):
        """
        Places an order using the pybit API.

        :param category: Product category (spot, linear, inverse, option).
        :param symbol: Trading symbol.
        :param side: Order side (Buy/Sell).
        :param order_type: Order type (Market/Limit).
        :param qty: Order quantity.
        :param price: Price (required for limit orders).
        :param time_in_force: Time in force for the order (GTC, IOC, FOK, PostOnly).
        :param order_link_id: Custom order ID (optional).
        :param is_leverage: Leverage for spot trading (default 0).
        :param order_filter: Order filter (default 'Order', TP/SL order, or Stop order).
        :param market_unit: Unit for qty in spot market orders (baseCoin/quoteCoin).
        :param trigger_price: Conditional order trigger price.
        :param trigger_direction: Trigger direction (rises_to or falls_to).
        :param trigger_by: Type of price to trigger the conditional order (LastPrice, IndexPrice, MarkPrice).
        :param take_profit: Take profit price.
        :param stop_loss: Stop loss price.
        :param tp_trigger_by: Price type to trigger take profit (LastPrice, IndexPrice, MarkPrice).
        :param sl_trigger_by: Price type to trigger stop loss (LastPrice, IndexPrice, MarkPrice).
        :param reduce_only: Reduce-only order flag.
        :param close_on_trigger: Close-on-trigger order flag.
        :param tp_sl_mode: TP/SL mode (Full/Partial).
        :param tp_limit_price: Limit price for take profit.
        :param sl_limit_price: Limit price for stop loss.
        :param tp_order_type: Order type when take profit is triggered (Market, Limit).
        :param sl_order_type: Order type when stop loss is triggered (Market, Limit).
        :return: Response from the API.
        """
        log.info("Placing %s order for %s: %s %s, qty=%s, price=%s", 
                    order_type.value, symbol, side.value, category.value, qty, price)

        order_data = {
            "category": category.value,
            "symbol": symbol,
            "side": side.value,
            "orderType": order_type.value,
            "qty": qty,
            "timeInForce": time_in_force.value,
            "isLeverage": is_leverage,
            "orderFilter": order_filter.value
        }

        if price is not None:
            order_data["price"] = price
        if order_link_id:
            order_data["orderLinkId"] = order_link_id
        if market_unit:
            order_data["marketUnit"] = market_unit
        if trigger_price:
            order_data["triggerPrice"] = trigger_price
        if trigger_direction:
            order_data["triggerDirection"] = trigger_direction.value
        if trigger_by:
            order_data["triggerBy"] = trigger_by.value
        if take_profit:
            order_data["takeProfit"] = take_profit
        if stop_loss:
            order_data["stopLoss"] = stop_loss
        if tp_trigger_by:
            order_data["tpTriggerBy"] = tp_trigger_by.value
        if sl_trigger_by:
            order_data["slTriggerBy"] = sl_trigger_by.value
        if reduce_only is not None:
            order_data["reduceOnly"] = reduce_only
        if close_on_trigger is not None:
            order_data["closeOnTrigger"] = close_on_trigger
        if tp_sl_mode:
            order_data["tpslMode"] = tp_sl_mode.value
        if tp_limit_price:
            order_data["tpLimitPrice"] = tp_limit_price
        if sl_limit_price:
            order_data["slLimitPrice"] = sl_limit_price
        if tp_order_type:
            order_data["tpOrderType"] = tp_order_type.value
        if sl_order_type:
            order_data["slOrderType"] = sl_order_type.value

        try:
            response = self.session.place_order(**order_data)
            log.info("Order placed successfully: %s", pprint.pformat(response))
            return response
        except Exception as e:
            log.error("Failed to place order: %s", pprint.pformat(e))
            raise


    def get_wallet_balance(self, account_type: AccountType, coin: str = None):
        """
        Get wallet balance for the specified account type and coin.
        
        :param account_type: The type of account (CONTRACT, SPOT).
        :param coin: Coin name, optional (e.g., BTC, USDC). Must be uppercase.
                     Multiple coins can be passed, separated by a comma.
                     If not provided, it will return non-zero asset information.
        :return: Response from the API with wallet balance information.
        """
        log.info("Fetching wallet balance for account type %s and coin %s", account_type.value, coin)

        params = {
            "accountType": account_type.value
        }
        if coin:
            params["coin"] = coin

        try:
            response = self.session.get_wallet_balance(**params)
            log.info("Wallet balance retrieved successfully: %s", pprint.pformat(response))
            return response
        except Exception as e:
            log.error("Failed to fetch wallet balance: %s", pprint.pformat(e))
            raise

    def get_tickers(self, category: Category, symbol: str = None, base_coin: str = None, exp_date: str = None):
        """
        Get the latest price snapshot, best bid/ask price, and trading volume in the last 24 hours.

        :param category: Product type (spot, linear, inverse, option).
        :param symbol: Symbol name (optional), like BTCUSDT, uppercase only.
        :param base_coin: Base coin (optional), uppercase only. Applies to options only.
        :param exp_date: Expiry date (optional). Applies to options only, e.g., 25DEC22.
        :return: Response from the API with ticker information.
        """
        log.info("Fetching tickers for category=%s, symbol=%s, base_coin=%s, exp_date=%s", 
                 category, symbol, base_coin, exp_date)

        params = {
            "category": category.value
        }

        if symbol:
            params["symbol"] = symbol
        if base_coin:
            params["baseCoin"] = base_coin
        if exp_date:
            params["expDate"] = exp_date

        try:
            response = self.session.get_tickers(**params)
            log.info("Tickers retrieved successfully: %s", pprint.pformat(response))
            return response
        except Exception as e:
            log.error("Failed to fetch tickers: %s", pprint.pformat(e))
            raise

    def get_order_by_id(self, category: Category, order_id: str):
        """
        Query real-time information about a specific order using its order ID.
        
        :param category: Product category (spot, linear, inverse, option).
        :param order_id: The unique ID of the order you want to query.
        :return: Response from the API with the order details.
        """
        log.info("Fetching order details for order_id=%s in category=%s", order_id, category)
        
        params = {
            "category": category.value,
            "orderId": order_id
        }
        
        try:
            response = self.session.get_open_orders(**params)
            log.info("Order details retrieved successfully: %s", pprint.pformat(response))
            return response
        except Exception as e:
            log.error("Failed to retrieve order details: %s", pprint.pformat(e))
            raise

    def set_trading_stop(self, 
                         category: Category,
                         symbol: str, 
                         take_profit: str = None,
                         stop_loss: str = None,
                         trailing_stop: str = None,
                         tp_trigger_by: TriggerBy = None,
                         sl_trigger_by: TriggerBy = None,
                         active_price: str = None,
                         tpsl_mode: TP_SL_Mode = TP_SL_Mode.FULL,
                         tp_size: str = None,
                         sl_size: str = None,
                         tp_limit_price: str = None,
                         sl_limit_price: str = None,
                         tp_order_type: TP_SL_OrderType = TP_SL_OrderType.MARKET,
                         sl_order_type: TP_SL_OrderType = TP_SL_OrderType.MARKET,
                         position_idx: int = 0):
        """
        Sets take profit, stop loss, or trailing stop for an open position.

        :param category: Product category (linear, inverse).
        :param symbol: Trading symbol (e.g., BTCUSDT).
        :param take_profit: Take profit price.
        :param stop_loss: Stop loss price.
        :param trailing_stop: Trailing stop by price distance.
        :param tp_trigger_by: Take profit trigger price type (LastPrice, IndexPrice, MarkPrice).
        :param sl_trigger_by: Stop loss trigger price type (LastPrice, IndexPrice, MarkPrice).
        :param active_price: Trailing stop trigger price.
        :param tpsl_mode: Take profit / stop loss mode (Full or Partial).
        :param tp_size: Take profit size (for Partial mode).
        :param sl_size: Stop loss size (for Partial mode).
        :param tp_limit_price: The limit order price for take profit.
        :param sl_limit_price: The limit order price for stop loss.
        :param tp_order_type: Order type for take profit (Market or Limit).
        :param sl_order_type: Order type for stop loss (Market or Limit).
        :param position_idx: Used to identify positions (0 for one-way mode, 1 for hedge Buy, 2 for hedge Sell).
        :return: Response from the API.
        """
        log.info("Setting trading stop for %s: TP=%s, SL=%s, TS=%s", symbol, take_profit, stop_loss, trailing_stop)

        order_data = {
            "category": category.value,
            "symbol": symbol,
            "tpslMode": tpsl_mode.value,
            "positionIdx": position_idx
        }

        if take_profit is not None:
            order_data["takeProfit"] = take_profit
        if stop_loss is not None:
            order_data["stopLoss"] = stop_loss
        if trailing_stop is not None:
            order_data["trailingStop"] = trailing_stop
        if tp_trigger_by:
            order_data["tpTriggerBy"] = tp_trigger_by.value
        if sl_trigger_by:
            order_data["slTriggerBy"] = sl_trigger_by.value
        if active_price:
            order_data["activePrice"] = active_price
        if tp_size:
            order_data["tpSize"] = tp_size
        if sl_size:
            order_data["slSize"] = sl_size
        if tp_limit_price:
            order_data["tpLimitPrice"] = tp_limit_price
        if sl_limit_price:
            order_data["slLimitPrice"] = sl_limit_price
        if tp_order_type:
            order_data["tpOrderType"] = tp_order_type.value
        if sl_order_type:
            order_data["slOrderType"] = sl_order_type.value

        try:
            response = self.session.set_trading_stop(**order_data)
            log.info("Trading stop set successfully: %s", pprint.pformat(response))
            return response
        except Exception as e:
            log.error("Failed to set trading stop: %s", pprint.pformat(e))
            raise

    def get_instruments_info(self, 
                             category: Category, 
                             symbol: str = None, 
                             status: str = None, 
                             base_coin: str = None, 
                             limit: int = None, 
                             cursor: str = None):
        """
        Get instrument information for trading pairs (Spot, Linear, Inverse, Option).

        :param category: Product type (spot, linear, inverse, option).
        :param symbol: Symbol name (optional), like BTCUSDT.
        :param status: Symbol status filter (optional).
        :param base_coin: Base coin (optional, applies to linear, inverse, option only).
        :param limit: Limit for data size per page. Range [1, 1000].
        :param cursor: Pagination cursor (optional).
        :return: Response from the API with instrument information.
        """
        log.info("Fetching instrument info for category=%s, symbol=%s, status=%s, base_coin=%s", 
                 category, symbol, status, base_coin)
        
        params = {
            "category": category.value
        }
        
        if limit:
            params["limit"] = limit
        if symbol:
            params["symbol"] = symbol
        if status:
            params["status"] = status
        if base_coin:
            params["baseCoin"] = base_coin
        if cursor:
            params["cursor"] = cursor

        try:
            response = self.session.get_instruments_info(**params)
            log.info("Instrument info retrieved successfully: %s", pprint.pformat(response))
            return response
        except Exception as e:
            log.error("Failed to fetch instrument info: %s", pprint.pformat(e))
            raise