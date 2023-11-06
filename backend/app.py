from flask import Flask
from .dbconnection import DBConnection, DBOperations

db_connection = DBConnection()
db_connection.connect()

user_operations = DBOperations(db_connection, 'users')
order_operations = DBOperations(db_connection, 'orders')

# usage:
# user_id = user_operations.create(UserObj.binary_value)

app = Flask(__name__)


@app.route('/register', methods=['POST'])
def register():
  pass

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
