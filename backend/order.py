from enum import Enum
from datetime import datetime

class Side(Enum):
  BUY = "BUY"
  SELL = "SELL"

class Order:
    def __init__(
          self,
          id: int, 
          price: int, 
          owner_id: int, 
          side: Side
      ):
        self.id = id
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
        