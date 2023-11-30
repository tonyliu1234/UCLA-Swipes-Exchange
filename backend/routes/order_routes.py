from __future__ import annotations

from enum import Enum
from heapq import heappop, heappush
from typing import Optional

from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from .user import UserCollection, User
from .order import Side, Order, OrderMatchingEngine

order_route = Blueprint('order', __name__)
order_matching_engine = OrderMatchingEngine()
user_collection = UserCollection()

@order_route.route('/get_order', methods=['GET'])
@login_required
def get_order():
    email: str = current_user.email
    user_orders = user_collection.get_by_email(email)['orders']
    user_orders = [Order.from_bson(order) for order in user_orders]
    order_id = request.get_json().get('id')

    filtered_order = next((order for order in user_orders if str(order.id) == order_id), None)

    if not filtered_order:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify(filtered_order.to_bson), 200


@order_route.route('/list_order', methods=['GET'])
@login_required
def list_order():
    email: str = current_user.email
    user_orders = user_collection.get_by_email(email)['orders']
    return jsonify(user_orders), 200

@order_route.route('/create_order', methods=['POST'])
@login_required
def create_order():
    data = request.get_json()
    price: str = data.get('price')
    email: str = current_user.email
    side: Side = Side(data.get('side'))

    user = User.from_bson(user_collection.get_by_email(email))
    order = user.create_order(price, side)
    print(user.orders)
    user_collection.update_by_email(email, user.to_bson)

    # TODO: Use Message Queue (Extremely Low Priority)
    process_new_order(order)
    return jsonify(order.to_bson), 200

def process_new_order(order: Order):
    order_matching_engine.push(order)
    # matched_orders = order_matching_engine.match()
    # TODO: append Notification to user's database


