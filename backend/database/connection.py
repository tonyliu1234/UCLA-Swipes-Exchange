from __future__ import annotations

import os
from typing import Generic, Mapping, Optional, TypeVar

from bson import ObjectId
from monad import option
from pymongo import MongoClient,errors
from pymongo.collection import Collection
from pymongo.database import Database

class DBConnection:
    __instance: Optional[DBConnection] = None
    client: MongoClient
    database: Database

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(DBConnection, cls).__new__(
                cls, *args, **kwargs
            )
        return cls.__instance

    def __init__(self):
        """Create a MongoDB connection."""

        host = os.getenv("MONGO_HOST")
        port = option.and_then(os.getenv("MONGO_PORT"), int)
        database_name = option.unwrap_or(os.getenv("MONGO_DATABASE_NAME"), "ucla_swipes_exchange")
        self.client = MongoClient(host, port)
        self.database = self.client[database_name]

    def get_collection(self, collection_name: str) -> Collection:
        """Get a collection from the connected database."""
        return self.database[collection_name]


T = TypeVar('T', bound=Mapping)


class DBCollection(Generic[T]):
    connection: DBConnection
    collection: Collection[T]

    def __init__(self, collection_name: str):
        self.connection = DBConnection()
        self.collection = self.connection.get_collection(collection_name)

    def create(self, data: T) -> ObjectId:
        return self.collection.insert_one(data).inserted_id

    def get(self, document_id: ObjectId) -> Optional[T]:
        return self.collection.find_one({'_id': document_id})

    def update(self, document_id: ObjectId, data: T) -> int:
        return self.collection.update_one(
            {'_id': document_id},
            {'$set': data}
        ).modified_count

    def delete(self, document_id: ObjectId) -> int:
        return self.collection.delete_one({'_id': document_id}).deleted_count


class UserCollection(DBCollection):
    def __init__(self):
        super().__init__('users')
        # Ensure `email` is unique within the collection
        self.collection.create_index('email', unique=True)

    def get_by_email(self, email: str) -> Optional['User']:
        return User.from_bson(self.collection.find_one({'email': email}))

    def get_by_id(self, id: ObjectId) -> Optional['User']:
        return User.from_bson(self.collection.find_one({'_id': id}))

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
