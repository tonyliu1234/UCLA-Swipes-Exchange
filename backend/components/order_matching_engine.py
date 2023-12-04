from heapq import heappop, heappush

from monad import option

from components.notification import Notification
from components.order import Order
from components.side import Side
from components.user import User, UserCollection


class OrderMatchingEngine:
    bid_queue: list[Order]
    ask_queue: list[Order]

    def __init__(self) -> None:
        self.bid_queue = []
        self.ask_queue = []

        for order in UserCollection().get_all_order():
            if order.is_matched:
                continue
            self.push(order)
            self.match()

    def push(self, order: Order) -> None:
        match order.side:
            case Side.BID:
                heappush(self.bid_queue, order)
            case Side.ASK:
                heappush(self.ask_queue, order)
            case _:
                raise TypeError()

    def match(self) -> None:
        while self.bid_queue and self.ask_queue:
            top_bid = self.bid_queue[0]
            top_ask = self.ask_queue[0]
            if top_bid.price < top_ask.price:
                break

            heappop(self.bid_queue)
            heappop(self.ask_queue)

            bid_user = option.unwrap(User.from_id(top_bid.owner_id))
            ask_user = option.unwrap(User.from_id(top_ask.owner_id))
            print("fuck", top_bid.id, top_ask.id)
            option.unwrap(bid_user.get_order(top_bid.id)).is_matched = True
            bid_user.create_notification(Notification(ask_user.id, Side.ASK))
            bid_user.persist()

            option.unwrap(ask_user.get_order(top_ask.id)).is_matched = True
            ask_user.create_notification(Notification(bid_user.id, Side.BID))
            ask_user.persist()
