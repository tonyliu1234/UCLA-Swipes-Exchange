from bson import ObjectId

from routes.order import Order, OrderMatchingEngine, Side


def test_push_bid_order():
    order_matching_engine = OrderMatchingEngine()
    order = Order(100, ObjectId(), Side.BID)
    order_matching_engine.push(order)
    assert order_matching_engine.bid_queue[0] == order


def test_push_ask_order():
    order_matching_engine = OrderMatchingEngine()
    order = Order(100, ObjectId(), Side.ASK)
    order_matching_engine.push(order)
    assert order_matching_engine.ask_queue[0] == order


def test_match_orders():
    order_matching_engine = OrderMatchingEngine()
    bid_order = Order(105, ObjectId(), Side.BID)
    ask_order = Order(100, ObjectId(), Side.ASK)
    order_matching_engine.push(bid_order)
    order_matching_engine.push(ask_order)
    matched_orders = order_matching_engine.match()
    assert len(matched_orders) == 2


def test_no_match_orders():
    order_matching_engine = OrderMatchingEngine()
    bid_order = Order(95, ObjectId(), Side.BID)
    ask_order = Order(100, ObjectId(), Side.ASK)
    order_matching_engine.push(bid_order)
    order_matching_engine.push(ask_order)
    matched_orders = order_matching_engine.match()
    assert matched_orders == []
