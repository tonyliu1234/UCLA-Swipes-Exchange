from flask import Flask, render_template, request, jsonify
from dbconnection import DBConnection, DBOperations
# from flask_login import LoginManager, login_required  # noqa: F401
from user import User
import hashlib

db_connection = DBConnection()
db_connection.connect()

user_operations = DBOperations(db_connection, 'users')
order_operations = DBOperations(db_connection, 'orders')

# usage:
# user_id = user_operations.create(UserObj.binary_value)

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    if user_operations.get(email):
        return jsonify({'status': 'error', 'message': 'Email already in use'}), 409
    
    def hash_password(password):
      password_bytes = password.encode('utf-8')
      hash_object = hashlib.sha256(password_bytes)
      return hash_object.hexdigest()

    hashed_password = hash_password(password)
    user = User(name, email, phone, hashed_password)
    try:
      user_id = user_operations.create(user.binary_value)
      return jsonify({'status': 'success', 'message': 'User {0} registered successfully'.format(user_id)}), 201
    except:
      return jsonify({'status': 'error', 'message': 'Registration failed'}), 500

@app.route('/login', methods=['POST'])
def login():
    pass

@app.route('/orders', methods=['GET'])
def get_orders():
  pass

@app.route('/orders', methods=['POST'])
def create_order():
  pass

if __name__ == '__main__':
  app.run(debug=True)
