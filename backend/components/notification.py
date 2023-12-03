from typing import Optional

from bson import ObjectId

from monad import option

from .side import Side


class Notification:
    client_id: ObjectId
    client_side: Side
    id: ObjectId

    def __init__(
        self, client_id: ObjectId, client_side: "Side", id: Optional[ObjectId] = None
    ):
        self.client_id = client_id
        self.client_side = client_side
        self.id = option.unwrap_or(id, ObjectId())

    @property
    def to_bson(self) -> dict:
        return {
            "_id": self.id,
            "client_id": self.client_id,
            "client_side": self.client_side,
        }

    @classmethod
    def from_bson(cls, bson: dict):
        return cls(bson["client_id"], bson["client_side"], bson["_id"])

    def __repr__(self):
        return str(self.to_bson)
