from typing import cast
from components.user import User
from flask import Blueprint, request
from flask_login import current_user, login_required, login_user, logout_user

from monad import option

user_route = Blueprint("user", __name__)


@user_route.route("/register", methods=["POST"])
def register():
    """
    Registers a new user.

    This endpoint processes a POST request with JSON payload containing the user's name, email, phone, and password. 
    It checks if the email is already in use and if not, creates a new user with the provided details.

    Returns:
        A tuple containing a JSON message indicating the outcome (success or failure) and an HTTP status code.
    """

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
    """
    Authenticates a user.

    This endpoint processes a POST request with JSON payload containing the user's email and password.
    It checks if the user exists and if the password matches, then logs the user in.

    Returns:
        A tuple containing a JSON message indicating the outcome (success, invalid credentials, or requirement of credentials) and an HTTP status code.
    """

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
    """
    Logs out the current user.

    This endpoint handles the logging out of a logged-in user. It requires that the user is already authenticated.

    Returns:
        A tuple containing a JSON message indicating successful logout and an HTTP status code.
    """

    logout_user()
    return {"message": "Logged out successfully"}, 200


@user_route.route("/whoami")
@login_required
def whoami():
    """
    Returns the current user's information.

    This endpoint provides information about the currently authenticated user, such as email, name, and phone.

    Returns:
        A tuple containing the user's details in JSON format and an HTTP status code.
    """

    user = cast(User, current_user)
    return {
        "email": user.email,
        "name": user.name,
        "phone": user.phone,
    }, 200


@user_route.route("/update_profile", methods=["POST"])
@login_required
def profile_change():
    """
    Updates the profile of the current user.

    This endpoint allows the logged-in user to update their profile information (name, phone, email, and password).
    It checks for unique email and applies changes to the user's profile.

    Returns:
        A tuple containing a JSON message indicating the outcome of the update and an HTTP status code.
    """

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
    """
    Deletes the current user's account.

    This endpoint handles the deletion of the account of the currently authenticated user. It ensures that the user exists before attempting deletion.

    Returns:
        A tuple containing a JSON message indicating the outcome of the deletion and an HTTP status code.
    """

    user = cast(User, current_user)
    delete_count = user.delete()
    if delete_count == 0:
        return {"message": "Delete user failed: User not found"}, 500
    logout_user()
    return {"message": "Delete user successfully"}, 200


@user_route.route("/notifications", methods=["GET"])
@login_required
def get_notifications():
    """
    Retrieves notifications for the current user.

    This endpoint fetches and returns all notifications associated with the currently authenticated user.

    Returns:
        A tuple containing a list of notifications in JSON format and an HTTP status code.
    """

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
