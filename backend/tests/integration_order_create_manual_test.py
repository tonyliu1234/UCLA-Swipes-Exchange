import requests

# Base URL of the server
base_url = 'http://127.0.0.1:5000'

# Start a session to persist cookies
session = requests.Session()

def login(email, password):
    """Log in to the server and store the session cookie."""
    url = f'{base_url}/user/login'
    data = {'email': email, 'password': password}
    response = session.post(url, json=data)
    return response.json()

def whoami():
    """Who am I"""
    url = f'{base_url}/user/whoami'
    response = session.get(url)
    return response.json()

def create_order(price, side):
    """Create a new order."""
    url = f'{base_url}/order/create_order'
    data = {'price': price, 'side': side}
    response = session.post(url, json=data)
    return response.json()

def list_orders():
    """List all orders."""
    url = f'{base_url}/order/list_order'
    response = session.get(url)
    return response.json()

def get_order(id):
    """get all orders."""
    url = f'{base_url}/order/get_order'
    data = {'id': id}
    response = session.get(url, json=data)
    return response.json()

def list_all_orders():
    """List all orders."""
    url = f'{base_url}/order/list_all_order'
    response = session.get(url)
    return response.json()

# Test the API
print("Logging in...")
login_response = login('john@example.com', 'yourpassword')
print("Login response:", login_response)

print("Who am I...")
whoami_response = whoami()
print("Whoami response:", whoami_response)

print("\nCreating an order...")
create_order_response = create_order(100, 'BID')
print("Create order response:", create_order_response)

print("\nListing orders...")
list_orders_response = list_orders()
print("List orders response:", list_orders_response)

print("\Getting orders...")
order_id = list_orders_response[0]['_id']
get_orders_response = get_order(order_id)
print("get orders response:", get_orders_response)

print("\Getting ALL orders...")
all_order_response = list_all_orders()
print("get ALL orders response:", all_order_response)
