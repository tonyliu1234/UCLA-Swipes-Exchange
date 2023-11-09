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
          side: Side,
          posted = None,
          is_matched: bool = False,
          _id = None,
      ):
        self.id = ObjectId() if not _id else 
        self.price = price
        self.owner_id = owner_id
        self.side = side
        self.is_matched = is_matched if not is_matched else is_matched
        self.posted = datetime.now() if not posted else posted
        
    @classmethod
    def parse_from(cls, order_binary_object):
      _id = order_binary_object['_id']
      price = order_binary_object['price']
      owner_id = order_binary_object['owner_id']
      is_matched = order_binary_object['is_matched']
      posted = order_binary_object['posted']
      side = Side.BUY if order_binary_object['side'] == "BUY" else Side.SELL
      return cls(price, owner_id, side, posted, is_matched, _id)

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
