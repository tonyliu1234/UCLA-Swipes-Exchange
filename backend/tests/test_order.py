from bson import ObjectId
from unittest.mock import Mock
from components.user import User
from components.order import Order
from components.side import Side

from components.order_matching_engine import OrderMatchingEngine


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


def test_find_matched_orders():
    order_matching_engine = OrderMatchingEngine()
    bid_order = Order(105, ObjectId(), Side.BID)
    ask_order = Order(100, ObjectId(), Side.ASK)
    order_matching_engine.push(bid_order)
    order_matching_engine.push(ask_order)
    matched_orders = order_matching_engine._find_match()
    assert len(matched_orders) == 2


def test_no_match_orders():
    order_matching_engine = OrderMatchingEngine()
    bid_order = Order(95, ObjectId(), Side.BID)
    ask_order = Order(100, ObjectId(), Side.ASK)
    order_matching_engine.push(bid_order)
    order_matching_engine.push(ask_order)
    matched_orders = order_matching_engine._find_match()
    assert matched_orders == []
def test_match_orders():
    user_collection_mock = Mock()
    buyer = User(
        "buyer",
        "123456789",
        "test@test.com",
        "password",
        id='i am buyer'
    )
    seller = User(
        "seller",
        "987654321",
        "test2@test.com",
        "password",
        id='i am seller'
    )

    def mock_get(id):
        if id == "123456789":
            return buyer
        elif id == "987654321":
            return seller
        else:
            return None
        
    user_collection_mock.get = mock_get

    order_matching_engine = OrderMatchingEngine(user_collection_mock)
    bid_order = Order(105, "123456789", Side.BID)
    ask_order = Order(100, "987654321", Side.ASK)
    order_matching_engine.push(bid_order)
    order_matching_engine.push(ask_order)
    order_matching_engine.match()

    user_collection_mock.update.assert_called()

    assert buyer.notifications[0].client_id == seller.id
    assert seller.notifications[0].client_id == buyer.id
