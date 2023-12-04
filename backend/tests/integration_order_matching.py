import requests

class UserClient:
    def __init__(self, base_url, email, password, phone, name):
        self.session = requests.Session()
        self.base_url = base_url
        self.email = email
        self.password = password
        self.phone = phone
        self.name = name

    def register(self):
        url = f"{self.base_url}/user/register"
        data = {"email": self.email, "password": self.password, "phone": self.phone, "name": self.name}
        return self.session.post(url, json=data)

    def login(self):
        url = f"{self.base_url}/user/login"
        data = {"email": self.email, "password": self.password}
        return self.session.post(url, json=data)

    def create_order(self, price, side):
        url = f"{self.base_url}/order/create_order"
        data = {"price": price, "side": side}
        return self.session.post(url, json=data)

    def notification(self):
        url = f"{self.base_url}/user/notifications"
        return self.session.get(url)

    def delete_user(self):
        url = f"{self.base_url}/user/delete_user"
        return self.session.delete(url)


base_url = "http://127.0.0.1:5000"

# Create User Clients
seller = UserClient(base_url, "john.sell@example.com", "yourpassword", "1234567890", "John Doe")
buyer = UserClient(base_url, "john.buy@example.com", "yourpassword", "9876543210", "John NMSL")

try:
    # Register and Login Users
    print("Registering and logging in users...")
    assert seller.register().status_code == 201
    assert buyer.register().status_code == 201
    assert seller.login().status_code == 200
    assert buyer.login().status_code == 200

    # Creating orders
    print("Creating orders...")
    assert seller.create_order(114514, "ASK").status_code == 200
    assert buyer.create_order(1919810, "BID").status_code == 200

    # Getting notifications
    print("Getting notifications...")
    seller_notification = seller.notification()
    buyer_notification = buyer.notification()
    assert seller_notification.status_code == 200
    assert buyer_notification.status_code == 200
    assert len(seller_notification.json()) == len(buyer_notification.json()) == 1

except AssertionError as e:
    print(f"An error occurred: {e}")
    raise e
finally:
    # Delete users
    print("Deleting test users...")
    assert seller.delete_user().status_code == 200
    assert buyer.delete_user().status_code == 200
    print("Test users deleted.")
