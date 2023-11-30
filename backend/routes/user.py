import hashlib
from typing import Optional

from bson import ObjectId
from database.connection import DBCollection
from flask import Blueprint, request
from flask_login import (UserMixin, current_user, login_required, login_user,
                         logout_user)
from monad import option
from pymongo import errors
from pymongo.cursor import Cursor

from routes.notification import Notification
from routes.order import Order, Side


class User(UserMixin):
    name: str
    phone: str
    email: str
    password: str
    orders: list[Order]
    notifications: list[Notification]
    id: ObjectId

    def __init__(
        self,
        name: str,
        phone: str,
        email: str,
        password: str,
        orders: list[Order] = [],
        notifications: list[Notification] = [],
        id: Optional[ObjectId] = None,
    ):
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.orders = orders
        self.notifications = notifications
        self.id = option.unwrap_or(id, ObjectId())

    @classmethod
    def from_bson(cls, bson: dict):
        # TODO: Convert each `Order` and `Notification` to their corresponding object
        return cls(bson['name'], bson['phone'], bson['email'], bson['password'], [Order.from_bson(order) for order in bson['orders']], bson['notifications'], bson['_id'])

    @property
    def to_bson(self):
        return {
            "_id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "password": self.password,
            # TODO: Implement `Notificationto_bson()`
            "notifications": [],
            "orders": [order.to_bson for order in self.orders]
        }

    @staticmethod
    def hash_password(password: str) -> str:
        password_bytes = password.encode('utf-8')
        hash_object = hashlib.sha256(password_bytes)
        return hash_object.hexdigest()

    def create_order(self, price: int, side: Side) -> Order:
        order = Order(price, self.id, side)
        self.orders.append(order)
        return order


class UserCollection(DBCollection):
    def __init__(self):
        super().__init__('users')
        # Ensure `email` is unique within the collection
        self.collection.create_index('email', unique=True)

    def get_by_email(self, email: str) -> Optional[dict]:
        return self.collection.find_one({'email': email})
    
    def get_all_user(self) -> Optional[Cursor[dict]]:
        return self.collection.find({})

    def update_by_email(self, email: str, data: dict) -> int:
        # Ensure that the data doesn't try to change the email to one that already exists
        if 'email' in data:
            existing_user = self.get_by_email(data['email'])
            if existing_user and existing_user['email'] != email:
                raise errors.DuplicateKeyError(
                    "Cannot update user: the new email is already in use by another user."
                )

        return self.collection.update_one(
            {'email': email},
            {'$set': data}
        ).modified_count

    def delete_by_email(self, email: str) -> int:
        return self.collection.delete_one({'email': email}).deleted_count
