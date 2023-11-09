from dbconnection import DBOperations
from order import Order, Side
from bson import ObjectId
from pymongo import errors
from flask_login import UserMixin
import hashlib

class User(UserMixin):
  def __init__(
      self,
      name: str, 
      phone: str, 
      email: str,
      password: str,
      _id = None,
      notifications = [],
      orders = [],
    ):
    self.id = _id or ObjectId()
    self.name = name
    self.phone = phone
    self.email = email
    self.password = password
    self.notifications = notifications
    self.orders = orders

  @classmethod
  def parse_from(cls, user_binary_object):
    id = user_binary_object['_id']
    name = user_binary_object['name']
    phone = user_binary_object['phone']
    email = user_binary_object['email']
    notifications = user_binary_object['notifications']
    orders = user_binary_object['orders']
    password = user_binary_object['password']
    return cls(name=name, phone=phone, email=email, _id=id, password=password, notifications=notifications, orders=orders)
  
  @classmethod
  def hash_password(cls, password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()

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
        "password": self.password,
        "notifications": [notification.binary_value for notification in self.notifications],  
        "orders": [order.binary_value for order in self.orders]
    }

class UserDBOperation(DBOperations):
  def __init__(self, db_connection):
    super().__init__(db_connection, 'users')
    # Ensure email is unique within the collection
    self.db_connection.get_collection(self.collection_name).create_index('email', unique=True)

  def get_user_by_email(self, email):
      return self.get(email, key="email")

  def update_user_by_email(self, user_email, update_data):
      # Ensure that the update_data doesn't try to change the email to one that already exists
      if 'email' in update_data:
        existing_user = self.find_user_by_email(update_data['email'])
        if existing_user and existing_user['email'] != user_email:
          raise errors.DuplicateKeyError("Cannot update user: the new email is already in use by another user.")

      result = self.update(user_email, update_data, key='email')
      return result
  
  def delete_user_by_email(self, email):
      return self.delete(email, key='email')