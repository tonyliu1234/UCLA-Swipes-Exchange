from heapq import heappop, heappush

from monad import option

from components.notification import Notification
from components.order import Order
from components.side import Side
from components.user import User, UserCollection


class OrderMatchingEngine:
    """
    A class that implements an order matching engine for a trading system.

    This engine matches bid and ask orders based on their prices. It uses two priority queues (heaps) to manage and match these orders efficiently.

    Attributes:
        bid_queue (list[Order]): A min-heap of bid (buy) orders, sorted by price.
        ask_queue (list[Order]): A min-heap of ask (sell) orders, sorted by price.
    """
    bid_queue: list[Order]
    ask_queue: list[Order]

    def __init__(self) -> None:
        """
        Initializes the OrderMatchingEngine with empty bid and ask queues.

        It retrieves all unmatched orders from the UserCollection and attempts to match them upon initialization.
        """
        self.bid_queue = []
        self.ask_queue = []

        for order in UserCollection().get_all_order():
            if order.is_matched:
                continue
            self.push(order)
            self.match()

    def push(self, order: Order) -> None:
        """
        Adds an order to the appropriate queue based on its side (bid or ask).

        Args:
            order (Order): The order to be added to the queue.

        Raises:
            TypeError: If the order's side is neither bid nor ask.
        """
        match order.side:
            case Side.BID:
                heappush(self.bid_queue, order)
            case Side.ASK:
                heappush(self.ask_queue, order)
            case _:
                raise TypeError()

    def match(self) -> None:
        """
        Attempts to match orders from the bid and ask queues.

        The matching process is based on the order prices. A bid and an ask order are matched if the bid price is 
        equal to or higher than the ask price. Matched orders are removed from the queues, and notifications are 
        sent to the respective users.
        """
        while self.bid_queue and self.ask_queue:
            top_bid = self.bid_queue[0]
            top_ask = self.ask_queue[0]
            if top_bid.price < top_ask.price:
                break

            heappop(self.bid_queue)
            heappop(self.ask_queue)

            bid_user = option.unwrap(User.from_id(top_bid.owner_id))
            option.unwrap(bid_user.get_order(top_bid.id)).is_matched = True
            bid_user.create_notification(Notification(top_ask.owner_id, Side.ASK))
            bid_user.persist()

            ask_user = option.unwrap(User.from_id(top_ask.owner_id))
            option.unwrap(ask_user.get_order(top_ask.id)).is_matched = True
            ask_user.create_notification(Notification(top_bid.owner_id, Side.BID))
            ask_user.persist()
