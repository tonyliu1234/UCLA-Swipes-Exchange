from __future__ import annotations

import hashlib
from itertools import chain
from typing import Optional

from bson import ObjectId
from database.connection import DBConnection
from flask_login import UserMixin
from monad import option
from pymongo.collection import Collection

from components.notification import Notification
from components.order import Order


class User(UserMixin):
    """
    Represents a user in the system.

    Attributes:
        name (str): The name of the user.
        phone (str): The phone number of the user.
        email (str): The email address of the user.
        password (str): The hashed password of the user.
        orders (list[Order]): List of orders associated with the user.
        notifications (list[Notification]): List of notifications associated with the user.
        id (ObjectId): The unique identifier of the user in the database.
    """

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
        """
        Initialize a new user instance.

        Args:
            name (str): The name of the user.
            phone (str): The phone number of the user.
            email (str): The email address of the user.
            password (str): The hashed password of the user.
            orders (Optional[list[Order]]): Optional; List of orders associated with the user.
            notifications (Optional[list[Notification]]): Optional; List of notifications associated with the user.
            id (Optional[ObjectId]): Optional; The unique identifier of the user.
        """
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.orders = option.unwrap_or(orders, [])
        self.notifications = option.unwrap_or(notifications, [])
        self.id = option.unwrap_or(id, ObjectId())

    @staticmethod
    def from_id(id: ObjectId):
        """
        Retrieves a user from the database by their unique identifier.

        Args:
            id (ObjectId): The unique identifier of the user in the database.

        Returns:
            User: An instance of the User class if found, otherwise None.
        """
        return UserCollection().get(id)

    @staticmethod
    def from_email(email: str):
        """
        Retrieves a user from the database by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            User: An instance of the User class if found, otherwise None.
        """

        return UserCollection().get_by_email(email)

    @classmethod
    def from_bson(cls, bson: dict):
        """
        Creates a User instance from a BSON object.

        Args:
            bson (dict): A dictionary representing a user's data, typically retrieved from the database.

        Returns:
            User: An instance of the User class constructed from the BSON data.
        """
        return cls(
            bson["name"],
            bson["phone"],
            bson["email"],
            bson["password"],
            list(map(Order.from_bson, bson["orders"])),
            list(map(Notification.from_bson, bson["notifications"])),
            bson["_id"],
        )

    @property
    def to_bson(self):
        """
        Converts the User instance to a BSON format for database storage.

        Returns:
            dict: A dictionary representing the User instance, suitable for MongoDB storage.
        """
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "password": self.password,
            "orders": [order.to_bson for order in self.orders],
            "notifications": [
                notification.to_bson for notification in self.notifications
            ],
        }

    @property
    def to_dict(self) -> dict:
        """
        Converts the User instance to a dictionary, excluding the database ID.

        Returns:
            dict: A dictionary representation of the User instance, excluding the '_id' field.
        """
        bson = self.to_bson
        del bson["_id"]
        return bson

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using SHA-256.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        password_bytes = password.encode("utf-8")
        hash_object = hashlib.sha256(password_bytes)
        return hash_object.hexdigest()

    def create(self) -> None:
        """
        Stores the User instance in the database.
        """
        UserCollection().create(self)

    def persist(self) -> None:
        """
        Updates the existing User record in the database with the current instance's values.
        """

        UserCollection().update(self.id, self)

    def delete(self) -> None:
        """
        Deletes the User record from the database.
        """
        UserCollection().delete(self.id)

    def create_order(self, order: Order) -> None:
        """
        Adds an order to the user's list of orders and updates the database record.

        Args:
            order (Order): The order to add to the user's list of orders.
        """
        self.orders.append(order)
        self.persist()

    def get_order(self, order_id: ObjectId) -> Optional[Order]:
        """
        Retrieves an order by its ID from the user's list of orders.

        Args:
            order_id (ObjectId): The unique identifier of the order.

        Returns:
            Optional[Order]: The order if found, otherwise None.
        """
        return list(filter(lambda order: order.id == order_id, self.orders))[0]

    def create_notification(self, notification: Notification) -> None:
        """
        Adds a notification to the user's list of notifications and updates the database record.

        Args:
            notification (Notification): The notification to add to the user's list of notifications.
        """
        self.notifications.append(notification)
        self.persist()


class UserCollection:
    """
    Represents a collection of User documents in the database.

    This class provides methods to interact with the users' collection in the database, 
    including creating, retrieving, updating, and deleting user documents.
    """

    connection: DBConnection
    collection: Collection

    def __init__(self):
        """
        Initialize a new UserCollection instance.
        """
        self.connection = DBConnection()
        self.collection = self.connection.get_collection("users")
        self.collection.create_index("email", unique=True)

    def create(self, user: User) -> ObjectId:
        """
        Create a new user document in the database.

        Args:
            user (User): The user instance to be stored in the database.

        Returns:
            ObjectId: The ID of the created document in the database.
        """
        return self.collection.insert_one(user.to_bson).inserted_id

    def get(self, document_id: ObjectId) -> Optional[User]:
        """
        Retrieves a user from the database by their document ID.

        Args:
            document_id (ObjectId): The unique identifier of the user document in the database.

        Returns:
            Optional[User]: The user if found, otherwise None.
        """

        return option.and_then(
            self.collection.find_one({"_id": document_id}), User.from_bson
        )

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieves a user from the database by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            Optional[User]: The user if found, otherwise None.
        """
        return option.and_then(
            self.collection.find_one({"email": email}), User.from_bson
        )

    def get_all(self) -> list[User]:
        """
        Retrieves all users from the database.

        Returns:
            list[User]: A list of User instances.
        """
        return list(map(User.from_bson, self.collection.find({})))

    def get_all_order(self) -> list[Order]:
        """
        Retrieves all orders from all users.

        Returns:
            list[Order]: A list of Order instances from all users.
        """
        return [
            order
            for order in chain.from_iterable(
                map(lambda user: user.orders, UserCollection().get_all())
            )
        ]

    def update(self, document_id: ObjectId, user: User) -> int:
        """
        Updates a user document in the database.

        Args:
            document_id (ObjectId): The unique identifier of the user document to update.
            user (User): The user instance with updated information.

        Returns:
            int: The number of documents modified.
        """
        return self.collection.update_one(
            {"_id": document_id}, {"$set": user.to_bson}
        ).modified_count

    def delete(self, document_id: ObjectId) -> int:
        """
        Deletes a user document from the database.

        Args:
            document_id (ObjectId): The unique identifier of the user document to delete.

        Returns:
            int: The number of documents deleted.
        """

        return self.collection.delete_one({"_id": document_id}).deleted_count
