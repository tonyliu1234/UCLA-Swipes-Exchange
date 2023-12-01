from __future__ import annotations

from datetime import datetime

from typing import Optional

from bson import ObjectId

from monad import option

from .side import Side

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

    def __lt__(self, other: Order) -> bool:
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
        return cls(bson['price'], bson['owner_id'], Side(bson['side']), bson['posted'], bson['is_matched'], bson['_id'])

    @property
    def to_bson(self) -> dict:
        return {
            "price": self.price,
            "owner_id": str(self.owner_id),
            "side": self.side.value,
            "posted": self.posted,
            "is_matched": self.is_matched,
            "_id": str(self.id),
        }
