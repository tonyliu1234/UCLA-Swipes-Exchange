#!/bin/bash

# Navigate to the directory containing app.py
cd ../

# Start the Python application in the background
python app.py &
APP_PID=$!

# Wait for the server to start
sleep 5

# Navigate to the test script directory and run the tests
cd -  # Goes back to the previous directory
python integration_order_create_manual_test.py

# Terminate the Python application
kill $APP_PID