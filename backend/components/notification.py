from typing import Optional

from bson import ObjectId
from monad import option

from components.side import Side


class Notification:
    """
    Represents a notification related to a client.

    Attributes:
        client_id (ObjectId): The unique identifier of the client associated with the notification.
        client_side (Side): An enum representing the side of the client.
        id (ObjectId): The unique identifier of the notification.
    """

    client_id: ObjectId
    client_side: Side
    id: ObjectId

    def __init__(
        self, client_id: ObjectId, client_side: Side, id: Optional[ObjectId] = None
    ):
        """
        Initializes a new instance of Notification.

        Args:
            client_id (ObjectId): The unique identifier of the client.
            client_side (Side): The side of the client (e.g., buyer or seller).
            id (Optional[ObjectId]): The unique identifier of the notification. If not provided, a new ObjectId will be generated.
        """
        self.client_id = client_id
        self.client_side = client_side
        self.id = option.unwrap_or(id, ObjectId())

    @property
    def to_bson(self) -> dict:
        """
        Converts the notification instance to a BSON format for database storage.

        Returns:
            dict: A dictionary representing the Notification instance, suitable for MongoDB storage.
        """
        return {
            "_id": self.id,
            "client_id": self.client_id,
            "client_side": self.client_side.value,
        }

    @classmethod
    def from_bson(cls, bson: dict):
        """
        Creates a Notification instance from a BSON object.

        This method is typically used to convert data retrieved from the database back into a Notification instance.

        Args:
            bson (dict): A dictionary representing a notification's data, typically retrieved from the database.

        Returns:
            Notification: An instance of the Notification class constructed from the BSON data.
        """
        return cls(
            ObjectId(bson["client_id"]),
            Side(bson["client_side"]),
            ObjectId(bson["_id"]),
        )

    @property
    def to_dict(self) -> dict:
        """
        Converts the Notification instance to a dictionary, excluding the database ID.

        This is often used for JSON serialization, where the database ID is not required.

        Returns:
            dict: A dictionary representation of the Notification instance, excluding the '_id' field.
        """
        bson = self.to_bson
        del bson["_id"]
        return bson
