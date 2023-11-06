from enum import Enum
from bson import ObjectId
from datetime import datetime

class Side(Enum):
  BUY = "BUY"
  SELL = "SELL"

class Order:
    def __init__(
          self,
          price: int, 
          owner_id: int, 
          side: Side
      ):
        self.id = ObjectId()
        self.price = price
        self.owner_id = owner_id
        self.is_matched = False
        self.posted = datetime.now()
        self.side = side

    def update_order(self, price):
        self.price = price
        # ... code to handle updating order ...

    def cancel(self):
      pass

    @property
    def binary_value(self):
      return {
        "_id": self.id,
        "price": self.price,
        "owner_id": self.owner_id,
        "is_matched": self.is_matched,
        "posted": self.posted,
        "side": self.side.value  # Serialize the enum to its value
      }
