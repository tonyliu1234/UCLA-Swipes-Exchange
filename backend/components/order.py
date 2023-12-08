from __future__ import annotations

from datetime import datetime
from typing import Optional

from bson import ObjectId
from monad import option

from components.side import Side


class Order:
    """
    Represents a trade order in a financial trading system.

    This class encapsulates the details of a trade order, including price, owner, side (bid or ask), 
    timestamp, match status, and a unique identifier.

    Attributes:
        price (int): The price of the order.
        owner_id (ObjectId): The unique identifier of the owner of the order.
        side (Side): The side of the order (either bid or ask).
        posted (datetime): The timestamp when the order was posted.
        is_matched (bool): A flag indicating whether the order has been matched.
        id (ObjectId): The unique identifier of the order.
    """
    price: int
    owner_id: ObjectId
    side: Side
    posted: datetime
    is_matched: bool
    id: ObjectId

    def __init__(
        self,
        price: int,
        owner_id: ObjectId,
        side: Side,
        posted: Optional[datetime] = None,
        is_matched: bool = False,
        id: Optional[ObjectId] = None,
    ):
        """
        Initializes a new instance of Order.

        Args:
            price (int): The price of the order.
            owner_id (ObjectId): The unique identifier of the owner of the order.
            side (Side): The side of the order (either bid or ask).
            posted (Optional[datetime]): The timestamp when the order was posted. Defaults to the current datetime if not provided.
            is_matched (bool): A flag indicating whether the order has been matched. Defaults to False.
            id (Optional[ObjectId]): The unique identifier of the order. A new ObjectId is generated if not provided.
        """
        self.price = price
        self.owner_id = owner_id
        self.side = side
        self.posted = option.unwrap_or(posted, datetime.now())
        self.is_matched = is_matched
        self.id = option.unwrap_or(id, ObjectId())

    def __lt__(self, other: Order) -> bool:
        """
        Defines the less than (<) comparison behavior for Order objects.

        For bid orders, an order is considered 'less' if its price is lower. For ask orders, it's 'less' if its price is higher.

        Args:
            other (Order): The other Order object to compare to.

        Returns:
            bool: True if this order is considered 'less' than the other, False otherwise.

        Raises:
            TypeError: If the orders are not of the same side or the comparison is otherwise invalid.
        """
        if self.side != other.side:
            raise TypeError()

        match self.side:
            case Side.BID:
                return self.price < other.price
            case Side.ASK:
                return self.price > other.price
            case _:
                raise TypeError()

    @classmethod
    def from_bson(cls, bson: dict):
        """
        Creates an Order instance from a BSON object.

        This method is typically used to convert data retrieved from the database back into an Order instance.

        Args:
            bson (dict): A dictionary representing an order's data, typically retrieved from the database.

        Returns:
            Order: An instance of the Order class constructed from the BSON data.
        """
        return cls(
            bson["price"],
            ObjectId(bson["owner_id"]),
            Side(bson["side"]),
            bson["posted"],
            bson["is_matched"],
            bson["_id"],
        )

    @property
    def to_bson(self) -> dict:
        """
        Converts the Order instance to a BSON format for database storage.

        Returns:
            dict: A dictionary representing the Order instance, suitable for MongoDB storage.
        """
        return {
            "price": self.price,
            "owner_id": self.owner_id,
            "side": self.side.value,
            "posted": self.posted,
            "is_matched": self.is_matched,
            "_id": self.id,
        }

    @property
    def to_dict(self) -> dict:
        """
        Converts the Order instance to a dictionary, excluding certain fields like the database ID and owner ID.

        This is often used for JSON serialization, where some fields are not required.

        Returns:
            dict: A dictionary representation of the Order instance, excluding the '_id' and 'owner_id' fields.
        """

        bson = self.to_bson
        del bson["_id"]
        del bson["owner_id"]
        return bson
