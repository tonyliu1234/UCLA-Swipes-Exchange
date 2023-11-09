from .order import Order, Side
from bson import ObjectId

class User:
  def __init__(
      self,
      name: str, 
      phone: str, 
      email: str,
      _id = None,
      notifications = [],
      orders = [],
    ):
    self.id = ObjectId() if not _id else _id
    self.name = name
    self.phone = phone
    self.email = email
    self.notifications = notifications
    self.orders = orders

  @classmethod
  def parse_from(cls, user_binary_object):
    _id = user_binary_object['_id']
    name = user_binary_object['name']
    phone = user_binary_object['phone']
    email = user_binary_object['email']
    notifications = user_binary_object['notifications']
    orders = user_binary_object['orders']
    return cls(name, phone, email, _id, notifications, orders)

  def create_order(self, price, side: Side):
    order = Order(price, self.id, side)
    self.orders.append(order)
    return order
  
  def fetch_notifications(self):
    # for notifications in all notifications
    #   if notification.belong_to_user(self.id):
    #     add to current user's notifications
    pass
  
  @property
  def binary_value(self):
    # Serialize the user instance to a dictionary
    return {
        "_id": self.id,
        "name": self.name,
        "phone": self.phone,
        "email": self.email,
        "notifications": [notification.binary_value for notification in self.notifications],  
        "orders": [order.binary_value for order in self.orders]
    }