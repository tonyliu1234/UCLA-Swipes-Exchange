from heapq import heappop, heappush

from monad import option

from .notification import Notification
from .order import Order
from .side import Side
from .user import UserCollection


class OrderMatchingEngine:
    bid_queue: list[Order]
    ask_queue: list[Order]
    user_collection: UserCollection

    def __init__(self, user_collection=None) -> None:
        self.bid_queue = []
        self.ask_queue = []
        if user_collection is None:
            self.user_collection = UserCollection()
        else:
            self.user_collection = user_collection

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
    def _find_match(self) -> list[Order]:
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
        matched_orders = self._find_match()
        # found a match
        if len(matched_orders) == 2:
            bid, ask = matched_orders
            buyer = option.unwrap(self.user_collection.get(bid.owner_id))
            seller = option.unwrap(self.user_collection.get(ask.owner_id))

            # update user's order
            def mark_order_as_matched(user, order):
                new_orders = []
                for user_order in user.orders:
                    if user_order.id == order.id:
                        user_order.is_matched = True
                    new_orders.append(user_order)
                user.orders = new_orders

            mark_order_as_matched(buyer, bid)
            mark_order_as_matched(seller, ask)

            # create Notification
            buyer.notifications.append(Notification(seller.id, Side.ASK))
            seller.notifications.append(Notification(buyer.id, Side.BID))
            # update user
            self.user_collection.update(buyer.id, buyer.to_bson)
            self.user_collection.update(seller.id, seller.to_bson)
