from __future__ import annotations

import hashlib
from typing import Optional

from bson import ObjectId
from database.connection import DBConnection
from flask_login import UserMixin
from monad import option
from pymongo import errors
from pymongo.collection import Collection

from components.notification import Notification
from components.order import Order


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
        orders: Optional[list[Order]] = None,
        notifications: Optional[list[Notification]] = None,
        id: Optional[ObjectId] = None,
    ):
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.orders = option.unwrap_or(orders, [])
        self.notifications = option.unwrap_or(notifications, [])
        self.id = option.unwrap_or(id, ObjectId())

    @classmethod
    def from_id(cls, id: ObjectId):
        return UserCollection().get(id)

    @classmethod
    def from_bson(cls, bson: dict):
        return cls(
            bson["name"],
            bson["phone"],
            bson["email"],
            bson["password"],
            list(map(Notification.from_bson, bson["orders"])),
            list(map(Notification.from_bson, bson["notifications"])),
            bson["_id"],
        )

    @property
    def to_bson(self):
        return {
            "_id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "password": self.password,
            "orders": [order.to_bson for order in self.orders],
            "notifications": [
                notification.to_bson for notification in self.notifications
            ],
        }

    @staticmethod
    def hash_password(password: str) -> str:
        password_bytes = password.encode("utf-8")
        hash_object = hashlib.sha256(password_bytes)
        return hash_object.hexdigest()

    def persist(self) -> None:
        UserCollection().update(self.id, self.to_bson)

    def create_order(self, order: Order) -> None:
        self.orders.append(order)
        self.persist()

    def get_order(self, order_id: ObjectId) -> Optional[Order]:
        return filter(lambda order: order.id == order_id, self.orders)[0]

    def create_notification(self, notification: Notification) -> None:
        self.notifications.append(notification)
        self.persist()

class UserCollection:
    connection: DBConnection
    collection: Collection

    def __init__(self):
        self.connection = DBConnection()
        self.collection = self.connection.get_collection("users")
        self.collection.create_index("email", unique=True)

    def create(self, data: User) -> ObjectId:
        return self.collection.insert_one(data.to_bson).inserted_id

    def get(self, document_id: ObjectId) -> Optional[User]:
        return option.and_then(
            self.collection.find_one({"_id": document_id}), User.from_bson
        )

    def get_by_email(self, email: str) -> Optional[User]:
        return option.and_then(
            self.collection.find_one({"email": email}), User.from_bson
        )

    def get_all(self) -> list[User]:
        return map(User.from_bson, self.collection.find({}))

    def update(self, document_id: ObjectId, user: User) -> int:
        return self.collection.update_one(
            {"_id": document_id}, {"$set": user.to_bson}
        ).modified_count

    def update_by_email(self, email: str, data: dict) -> int:
        # Ensure that the data doesn't try to change the email to one that already exists
        if "email" in data:
            existing_user = self.get_by_email(data["email"])
            if existing_user and existing_user.email != email:
                raise errors.DuplicateKeyError(
                    "Cannot update user: the new email is already in use by another user."
                )

        return self.collection.update_one(
            {"email": email}, {"$set": data}
        ).modified_count

    def delete(self, document_id: ObjectId) -> int:
        return self.collection.delete_one({"_id": document_id}).deleted_count

    def delete_by_email(self, email: str) -> int:
        return self.collection.delete_one({"email": email}).deleted_count
