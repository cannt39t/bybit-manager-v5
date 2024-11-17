from enum import Enum

class Category(Enum):
    SPOT = "spot"
    LINEAR = "linear"
    INVERSE = "inverse"
    OPTION = "option"

class OrderType(Enum):
    MARKET = "Market"
    LIMIT = "Limit"

class Side(Enum):
    BUY = "Buy"
    SELL = "Sell"

class TimeInForce(Enum):
    GTC = "GTC"
    IOC = "IOC"
    FOK = "FOK"
    POST_ONLY = "PostOnly"

class AccountType(Enum):
    SPOT = "SPOT"
    CONTRACT = "CONTRACT"
    UNIFIED = "UNIFIED"

class TriggerDirection(Enum):
    RISES_TO = 1
    FALLS_TO = 2

class TriggerBy(Enum):
    LAST_PRICE = "LastPrice"
    INDEX_PRICE = "IndexPrice"
    MARK_PRICE = "MarkPrice"

class OrderFilter(Enum):
    ORDER = "Order"
    TP_SL_ORDER = "tpslOrder"
    STOP_ORDER = "StopOrder"

class TP_SL_Mode(Enum):
    FULL = "Full"
    PARTIAL = "Partial"

class TP_SL_OrderType(Enum):
    MARKET = "Market"
    LIMIT = "Limit"