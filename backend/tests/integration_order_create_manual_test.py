"""
Pre-Run Instructions:
---------------------

1. Start the Backend Server:
   - Navigate to the backend server directory.
   - Run the command: `python app.py`.
     This starts the backend server needed for the application.

2. Start MongoDB:
   - Run the command: `mongod`.
     This initiates the MongoDB server.

3. Database Setup:
   - Ensure that a MongoDB database named 'ucla_swipes_exchange' is created.
   - Within the 'ucla_swipes_exchange' database, there should be a collection named 'user'.
     This collection is required for the application's user management.

Note: These steps are essential to ensure that the application runs correctly. Make sure the backend server and MongoDB are running before executing the application.
"""

import requests

# Base URL of the server
base_url = 'http://127.0.0.1:5000'

# Start a session to persist cookies
session = requests.Session()

def register(email, password, phone, name):
    """Log in to the server and store the session cookie."""
    url = f'{base_url}/user/register'
    data = {
        'email': email,
        'password': password,
        'phone': phone,
        'name': name
    }
    response = session.post(url, json=data)
    return response

def update_profile(email, password, phone, name):
    """Log in to the server and store the session cookie."""
    url = f'{base_url}/user/update_profile'
    data = {
        'email': email,
        'password': password,
        'phone': phone,
        'name': name
    }
    response = session.post(url, json=data)
    return response

def login(email, password):
    """Log in to the server and store the session cookie."""
    url = f'{base_url}/user/login'
    data = {'email': email, 'password': password}
    response = session.post(url, json=data)
    return response

def whoami():
    """Who am I"""
    url = f'{base_url}/user/whoami'
    response = session.get(url)
    return response

def create_order(price, side):
    """Create a new order."""
    url = f'{base_url}/order/create_order'
    data = {'price': price, 'side': side}
    response = session.post(url, json=data)
    return response

def list_orders():
    """List all orders."""
    url = f'{base_url}/order/list_order'
    response = session.get(url)
    return response

def get_order(id):
    """get all orders."""
    url = f'{base_url}/order/get_order'
    data = {'id': id}
    response = session.get(url, json=data)
    return response

def list_all_orders():
    """List all orders."""
    url = f'{base_url}/order/list_all_order'
    response = session.get(url)
    return response

def delete_user():
    """Delete User"""
    url = f'{base_url}/user/delete_user'
    response = session.delete(url)
    return response

# Test the API
print("Register...")
register_response = register(email='john@example.com', password='yourpassword', phone='1234567890', name='John Doe')
assert register_response.status_code == 201, f"Registration failed with status code {register_response.status_code}"
print("Register response:", register_response.json())

print("Logging in...")
login_response = login('john@example.com', 'yourpassword')
assert login_response.status_code == 200, f"Login failed with status code {login_response.status_code}"
print("Login response:", login_response.json())

print("Who am I...")
whoami_response = whoami()
assert whoami_response.status_code == 200, f"Whoami failed with status code {whoami_response.status_code}"
print("Whoami response:", whoami_response.json())

print("\nCreating an order...")
create_order_response = create_order(100, 'BID')
assert create_order_response.status_code == 200, f"Create order failed with status code {create_order_response.status_code}"
print("Create order response:", create_order_response.json())

print("\nListing orders...")
list_orders_response = list_orders()
assert list_orders_response.status_code == 200, f"List orders failed with status code {list_orders_response.status_code}"
print("List orders response:", list_orders_response.json())

print("\Getting orders...")
order_id = list_orders_response.json()[0]['_id']
get_orders_response = get_order(order_id)
assert get_orders_response.status_code == 200, f"Get order failed with status code {get_orders_response.status_code}"
print("get orders response:", get_orders_response.json())

print("\Getting ALL orders...")
all_order_response = list_all_orders()
assert all_order_response.status_code == 200, f"List all orders failed with status code {all_order_response.status_code}"
print("get ALL orders response:", all_order_response.json())

print("Updating User Name...")
update_response = update_profile(email='john@example.com', password='yourpassword', phone='1234567890', name='John NMSL')
assert update_response.status_code == 200, f"Update Profile failed with status code {update_response.status_code}"
print("get ALL orders response:", update_response.json())

print("Who am I...")
whoami_response = whoami()
assert whoami_response.status_code == 200, f"Whoami failed with status code {whoami_response.status_code}"
assert whoami_response.json()['name'] == 'John NMSL'
print("Whoami response:", whoami_response.json())

print("Finished Testing: deleting test user...")
delete_user_response = delete_user()
assert delete_user_response.status_code == 200, f"Delete user failed with status code {delete_user_response.status_code}"
print("delete response:", delete_user_response.json())
