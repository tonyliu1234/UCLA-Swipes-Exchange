from .order import Order

class User:
  def __init__(
      self,
      id: int, 
      name: str, 
      phone: str, 
      email: str
    ):
    self.id = id
    self.name = name
    self.phone = phone
    self.email = email
    self.notifications = []

  def create_order(self, price, side):
    pass