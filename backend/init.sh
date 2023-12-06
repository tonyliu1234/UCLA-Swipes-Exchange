#!/bin/bash
service mongodb start

# Wait for a few seconds to ensure MongoDB starts
sleep 5

# Command to create database and collection
mongo UCLA-exchange --eval "db.createCollection('users');"

# Start your Flask application
gunicorn backend.app:app
