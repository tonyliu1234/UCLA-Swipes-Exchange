from __future__ import annotations

import os
from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from monad import option


class DBConnection:
    __instance: Optional[DBConnection] = None
    client: MongoClient
    database: Database

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(DBConnection, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        host = os.getenv("MONGO_HOST")
        port = option.and_then(os.getenv("MONGO_PORT"), int)
        database_name = option.unwrap_or(
            os.getenv("MONGO_DATABASE_NAME"), "ucla_swipes_exchange"
        )
        self.client = MongoClient(host, port)
        self.database = self.client[database_name]

    def get_collection(self, collection_name: str) -> Collection:
        return self.database[collection_name]
