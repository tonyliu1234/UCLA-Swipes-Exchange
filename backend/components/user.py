import hashlib
from typing import Optional

from bson import ObjectId
from flask_login import UserMixin
from monad import option
from pymongo import errors
from pymongo.cursor import Cursor

from components.notification import Notification
from components.order import Order
from components.side import Side
from database.connection import DBCollection


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
        orders: list[Order] = None,
        notifications: list[Notification] = None,
        id: Optional[ObjectId] = None,
    ):
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.orders = [] if orders is None else orders
        self.notifications = [] if notifications is None else notifications
        self.id = option.unwrap_or(id, ObjectId())

    @classmethod
    def from_bson(cls, bson: dict):
        return cls(
            bson['name'],
            bson['phone'], 
            bson['email'], 
            bson['password'], 
            [Order.from_bson(order) for order in bson['orders']], 
            [Notification.from_bson(notification) for notification in bson['notifications']], 
            bson['_id']
        )

    @property
    def to_bson(self):
        return {
            "_id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "password": self.password,
            "notifications": [notification.to_bson for notification in self.notifications],
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
    
    def fetch_notifications(self, user_collection: 'UserCollection') -> list[Notification]:
        new_data = user_collection.get_by_id(self.id)
        if new_data:
            self.notifications = new_data.notifications
            return self.notifications
        else:
            return self.notifications

class UserCollection(DBCollection):
    def __init__(self):
        super().__init__('users')
        # Ensure `email` is unique within the collection
        self.collection.create_index('email', unique=True)
    
    def get_all_user(self) -> Optional[Cursor[dict]]:
        return self.collection.find({})

    def get_by_email(self, email: str) -> Optional[User]:
        return User.from_bson(self.collection.find_one({'email': email}))

    def get_by_id(self, id: ObjectId) -> Optional[User]:
        return User.from_bson(self.collection.find_one({'_id': id}))

    def update_by_email(self, email: str, data: dict) -> int:
        # Ensure that the data doesn't try to change the email to one that already exists
        if 'email' in data:
            existing_user = self.get_by_email(data['email'])
            if existing_user and existing_user.email != email:
                raise errors.DuplicateKeyError(
                    "Cannot update user: the new email is already in use by another user."
                )

        return self.collection.update_one(
            {'email': email},
            {'$set': data}
        ).modified_count

    def delete_by_email(self, email: str) -> int:
        return self.collection.delete_one({'email': email}).deleted_count