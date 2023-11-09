from flask import Flask, render_template, request, jsonify
from dbconnection import DBConnection, DBOperations
from flask_login import LoginManager, login_required, logout_user, login_user
from user import User, UserDBOperation


db_connection = DBConnection()
db_connection.connect()

user_operations = UserDBOperation(db_connection)
order_operations = DBOperations(db_connection, 'orders')

# usage:
# user_id = user_operations.create(UserObj.binary_value)

app = Flask(__name__)
app.secret_key = '114514,1919810,000024'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Implement a method to load a user given a user_idss
    # You would probably query your database here and return the user instance if found
    return user_operations.get(user_id)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    if user_operations.get(email):
        return jsonify({'status': 'error', 'message': 'Email already in use'}), 409

    hashed_password = User.hash_password(password)
    user = User(name=name, email=email, phone=phone, password=hashed_password)
    try:
      user_operations.create(user.binary_value)
      return jsonify({'status': 'success', 'message': 'User {0} registered successfully'.format(email)}), 201
    except Exception as e:
      return jsonify({'status': 'error', 'message': 'Registration failed: {0}'.format(e)}), 500

@app.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  email = data.get('email')
  password = data.get('password')

  if not email or not password:
      return jsonify({'status': 'error', 'message': 'Email and password are required'}), 400

  user = user_operations.get_user_by_email(email)

  if user is None:
      return jsonify({'status': 'error', 'message': 'User does not exist'}), 401
  user = User.parse_from(user)
  if user.password == User.hash_password(password):
      login_user(user)
      return jsonify({'status': 'success', 'message': 'Login successful'}), 200
  else:
      return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'success', 'message': 'Logged out successfully'}), 200

@app.route('/orders', methods=['GET'])
def get_orders():
  pass

@app.route('/orders', methods=['POST'])
def create_order():
  pass

if __name__ == '__main__':
  app.run(debug=True)
