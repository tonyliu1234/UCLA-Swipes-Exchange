from typing import cast
from components.user import User
from flask import Blueprint, request
from flask_login import current_user, login_required, login_user, logout_user

from monad import option

user_route = Blueprint("user", __name__)


@user_route.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name: str = data.get("name")
    email: str = data.get("email")
    phone: str = data.get("phone")
    password: str = data.get("password")

    if User.from_email(email) is not None:
        return {"message": "Email already in use"}, 409

    hashed_password = User.hash_password(password)
    user = User(name, phone, email, hashed_password)
    try:
        user.create()
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

    user = User.from_email(email)
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
    user = cast(User, current_user)
    return {
        "email": user.email,
        "name": user.name,
        "phone": user.phone,
    }, 200


@user_route.route("/update_profile", methods=["POST"])
@login_required
def profile_change():
    user = cast(User, current_user)
    data = request.get_json()

    if name := data.get("name"):
        user.name = name

    if phone := data.get("phone"):
        user.phone = phone

    if email := data.get("email"):
        if email != user.email and option.some(User.from_email(email)):
            return {"message": "Email already in use"}, 409
        user.email = email

    if password := data.get("password"):
        user.password = User.hash_password(password)

    user.persist()
    return {"message": "User profile updated successfully"}, 200


@user_route.route("/delete_user", methods=["DELETE"])
@login_required
def delete_user():
    user = cast(User, current_user)
    delete_count = user.delete()
    if delete_count == 0:
        return {"message": "Delete user failed: User not found"}, 500
    logout_user()
    return {"message": "Delete user successfully"}, 200


@user_route.route("/notifications", methods=["GET"])
@login_required
def get_notifications():
    user = cast(User, current_user)

    notifications = []
    for notification in user.notifications:
        client = option.unwrap(User.from_id(notification.client_id))
        notifications.append(
            {
                "side": str(notification.client_side),
                "client": client.name,
                "client_phone": client.phone,
                "client_email": client.email,
            }
        )

    return notifications, 200
