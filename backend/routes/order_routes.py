from __future__ import annotations

from typing import cast
from components.order import Order, Side
from components.order_matching_engine import OrderMatchingEngine
from components.user import User, UserCollection
from flask import Blueprint, request
from flask_login import current_user, login_required
from monad import option

order_route = Blueprint("order", __name__)
order_matching_engine = OrderMatchingEngine()


@order_route.route("/get_order", methods=["GET"])
@login_required
def get_order():
    """
    Retrieves a specific order for the currently logged-in user.

    This route handles a GET request and expects an 'id' field in the JSON payload to specify the order's ID. 
    If the order exists and belongs to the current user, it returns the order details.

    Returns:
        A tuple containing the order details in JSON format and an HTTP status code. 
        Returns a 404 error if the order is not found.
    """
    user = cast(User, current_user)
    order_id = request.get_json().get("id")

    return option.map_or(
        user.get_order(order_id),
        lambda order: (order.to_dict, 200),
        ({"error": "order not found"}, 404),
    )


@order_route.route("/list_order", methods=["GET"])
@login_required
def list_order():
    """
    Lists all orders for the currently logged-in user.

    This route handles a GET request and returns a list of all orders associated with the current user.

    Returns:
        A tuple containing a list of the user's orders in JSON format and an HTTP status code.
    """
    user = cast(User, current_user)
    return [order.to_dict for order in user.orders], 200


@order_route.route("/list_all_order", methods=["GET"])
@login_required
def list_all_order():
    """
    Lists all orders in the system.

    This route handles a GET request and returns a list of all orders from all users. 
    It is typically used for administrative purposes or data analysis.

    Returns:
        A tuple containing a list of all orders in JSON format and an HTTP status code.
    """
    return [order.to_dict for order in UserCollection().get_all_order()], 200


@order_route.route("/create_order", methods=["POST"])
@login_required
def create_order():
    """
    Creates a new order for the currently logged-in user.

    This route handles a POST request with JSON payload containing the order's price and side (BID or ASK). 
    The order is added to the user's list of orders and then passed to the order matching engine.

    Returns:
        A tuple containing the created order's details in JSON format and an HTTP status code.
    """
    user = cast(User, current_user)
    data = request.get_json()
    price: str = data.get("price")
    side: Side = Side(data.get("side"))

    order = Order(int(price), user.id, side)
    user.create_order(order)

    order_matching_engine.push(order)
    order_matching_engine.match()
    return order.to_dict, 200
