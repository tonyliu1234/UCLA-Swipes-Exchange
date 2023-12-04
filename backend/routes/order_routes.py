from __future__ import annotations

from typing import cast
from components.order import Order, Side
from components.order_matching_engine import OrderMatchingEngine
from components.user import User, UserCollection
from flask import Blueprint, request
from flask_login import current_user, login_required
from itertools import chain
from monad import option

order_route = Blueprint("order", __name__)
order_matching_engine = OrderMatchingEngine()


@order_route.route("/get_order", methods=["GET"])
@login_required
def get_order():
    user = cast(User, current_user)
    order_id = request.get_json().get("id")

    return option.map_or(
        user.get_order(order_id),
        lambda order: (order.to_bson, 200),
        ({"error": "order not found"}, 404),
    )


@order_route.route("/list_order", methods=["GET"])
@login_required
def list_order():
    user = cast(User, current_user)
    return [order.to_bson for order in user.orders], 200


@order_route.route("/list_all_order", methods=["GET"])
@login_required
def list_all_order():
    return [order.to_bson for order in UserCollection().get_all_order()], 200


@order_route.route("/create_order", methods=["POST"])
@login_required
def create_order():
    user = cast(User, current_user)
    data = request.get_json()
    price: str = data.get("price")
    side: Side = Side(data.get("side"))

    order = Order(int(price), user.id, side)
    user.create_order(order)
    user.persist()

    order_matching_engine.push(order)
    order_matching_engine.match()
    return order.to_bson, 200
