from datetime import datetime
from enum import Enum
from typing import Optional

from bson import ObjectId
from flask import Blueprint
from monad import option


class Side(Enum):
    BID = "BID"
    ASK = "ASK"


class Order:
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
        self.price = price
        self.owner_id = owner_id
        self.side = side
        self.posted = option.unwrap_or(posted, datetime.now())
        self.is_matched = is_matched
        self.id = option.unwrap_or(id, ObjectId())

    @classmethod
    def from_bson(cls, bson: dict):
        return cls(bson['price'], bson['owner_id'], Side(bson['side']), bson['posted'], bson['is_matched'], bson['_id'])

    def to_bson(self) -> dict:
        return {
            "price": self.price,
            "owner_id": self.owner_id,
            "side": self.side.value,
            "posted": self.posted,
            "is_matched": self.is_matched,
            "_id": self.id,
        }


order_route = Blueprint('order', __name__)


@order_route.route('/', methods=['GET'])
def get_order():
    pass


@order_route.route('/', methods=['LIST'])
def list_order():
    pass


@order_route.route('/', methods=['POST'])
def create_order():
    pass
