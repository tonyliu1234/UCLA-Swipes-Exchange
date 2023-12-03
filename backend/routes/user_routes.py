from components.user import User, UserCollection
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user

user_route = Blueprint("user", __name__)
user_collection = UserCollection()


@user_route.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name: str = data.get("name")
    email: str = data.get("email")
    phone: str = data.get("phone")
    password: str = data.get("password")

    if user_collection.get_by_email(email) is not None:
        return {"message": "Email already in use"}, 409

    hashed_password = User.hash_password(password)
    user = User(name, phone, email, hashed_password)
    try:
        user_collection.create(user.to_bson)
        return {"message": f"User {email} registered successfully"}, 201
    except Exception as e:
        return {"message": f"Registration failed: {e}"}, 500


@user_route.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email: str = data.get("email")
    password: str = data.get("password")

    if not email or not password:
        return {"message": "Email and password are required"}, 400

    user = user_collection.get_by_email(email)
    if user is None:
        return {"message": "User does not exist"}, 401

    if user.password == User.hash_password(password):
        login_user(user)
        return {"message": "Login successful"}, 200
    else:
        return {"message": "Invalid credentials"}, 401


@user_route.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return {"message": "Logged out successfully"}, 200


@user_route.route("/whoami")
@login_required
def whoami():
    user = user_collection.get_by_email(current_user.email)

    user_data = {"phone": user.phone, "name": user.name, "email": user.email}

    return user_data, 200


@user_route.route("/update_profile", methods=["POST"])
@login_required
def profile_change():
    def email_already_in_use(email):
        return (
            email != current_user.email
            and user_collection.get_by_email(email) is not None
        )

    user = User.from_bson(user_collection.get(current_user.id))
    data = request.get_json()

    for attr in ["name", "phone"]:
        if attr_value := data.get(attr):
            setattr(user, attr, attr_value)

    if "email" in data and email_already_in_use(data["email"]):
        return {"message": "Email already in use"}, 409

    if email := data.get("email"):
        user.email = email

    if password := data.get("password"):
        user.password = User.hash_password(password)

    user_collection.update(user.id, user.to_bson)
    return {'message': 'User profile updated successfully'}, 200


@user_route.route("/delete_user", methods=["DELETE"])
@login_required
def delete_user():
    delete_count = user_collection.delete_by_email(current_user.email)
    if delete_count == 0:
        return {"message": "Delete user failed: User not found"}, 500
    logout_user()
    return {"message": "Delete user successfully"}, 200


@user_route.route("/notifications", methods=["GET"])
@login_required
def get_notifications():
    user = user_collection.get_by_email(current_user.email)
    if user is None:
        return {"message": "User not found"}, 404
    notifications = []
    for notification in user.notifications:
        side_str = "BUY" if notification.client_side == 0 else "SELL"
        client = user_collection.get_by_id(notification.client_id)
        if client is None:
            continue
        notification_data = {
            "side": side_str,
            "client": client.name,
            "client_phone": client.phone,
            "client_email": client.email,
        }
        notifications.append(notification_data)

    return jsonify(notifications), 200
