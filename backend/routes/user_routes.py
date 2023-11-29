import hashlib
from typing import Optional

from flask import Blueprint, request
from flask_login import (current_user, login_required, login_user,
                         logout_user)
from monad import option
from pymongo import errors

from .user import User, UserCollection


user_route = Blueprint('user', __name__)
user_collection = UserCollection()


@user_route.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name: str = data.get('name')
    email: str = data.get('email')
    phone: str = data.get('phone')
    password: str = data.get('password')

    if user_collection.get_by_email(email) is not None:
        return {'message': 'Email already in use'}, 409

    hashed_password = User.hash_password(password)
    user = User(name, phone, email, hashed_password)
    try:
        user_collection.create(user.to_bson)
        return {'message': f'User {email} registered successfully'}, 201
    except Exception as e:
        return {'message': f'Registration failed: {e}'}, 500


@user_route.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email: str = data.get('email')
    password: str = data.get('password')

    if not email or not password:
        return {'message': 'Email and password are required'}, 400

    user_bson = user_collection.get_by_email(email)
    if user_bson is None:
        return {'message': 'User does not exist'}, 401

    user = User.from_bson(user_bson)
    if user.password == User.hash_password(password):
        login_user(user)
        return {'message': 'Login successful'}, 200
    else:
        return {'message': 'Invalid credentials'}, 401


@user_route.route('/logout')
@login_required
def logout():
    logout_user()
    return {'message': 'Logged out successfully'}, 200


@user_route.route('/whoami')
@login_required
def whoami():
    return {'message': f"{current_user.email}"}, 200