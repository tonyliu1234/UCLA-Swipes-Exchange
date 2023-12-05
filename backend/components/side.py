from enum import Enum


class Side(Enum):
    """
    Enumeration for representing the side of an order in a trading system.

    This enum classifies orders into two categories: BID and ASK.
    BID represents a buy order, and ASK represents a sell order.

    Members:
        BID (str): Represents a buy order.
        ASK (str): Represents a sell order.
    """
    BID = "BID"
    ASK = "ASK"
