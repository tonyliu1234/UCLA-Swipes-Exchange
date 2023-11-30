from __future__ import annotations

from datetime import datetime
from enum import Enum
from heapq import heappop, heappush
from typing import Optional

from bson import ObjectId
from flask import Blueprint

from monad import option
from user import UserCollection
from notification import Notification


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


class OrderMatchingEngine:
    bid_queue: list[Order]
    ask_queue: list[Order]
    user_collection: UserCollection

    def __init__(self) -> None:
        self.bid_queue = []
        self.ask_queue = []
        self.user_collection = UserCollection()

    def push(self, order: Order) -> None:
        match order.side:
            case Side.BID:
                heappush(self.bid_queue, order)
            case Side.ASK:
                heappush(self.ask_queue, order)
            case _:
                raise TypeError()

    # Matches the best bid order with the best ask order
    # whenever the highest bid price exceeds the lowest ask price
    def __find_match(self) -> list[Order]:
        matched_orders = []
        while self.bid_queue and self.ask_queue:
            top_bid = self.bid_queue[0]
            top_ask = self.ask_queue[0]
            if top_bid.price < top_ask.price:
                break

            matched_orders.append(top_bid)
            matched_orders.append(top_ask)

            top_bid.is_matched = True
            top_ask.is_matched = True

            heappop(self.bid_queue)
            heappop(self.ask_queue)

        return matched_orders

    # implement the match method that generate a match and create Notification
    # to the users
    def match(self) -> None:
        matched_orders = self.__find_match()
        if matched_orders == 2: # found a match
            bid, ask = matched_orders
            buyer = option.unwrap(self.user_collection.get(bid.owner_id))
            seller = option.unwrap(self.user_collection.get(ask.owner_id))
            # create Notification
            buyer.notifications.append(Notification(seller.id, Side.ASK))
            seller.notifications.append(Notification(buyer.id, Side.BID))
            # update user
            self.user_collection.update(buyer.id, buyer.to_bson)
            self.user_collection.update(seller.id, seller.to_bson)
