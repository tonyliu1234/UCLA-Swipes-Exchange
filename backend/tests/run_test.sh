#!/bin/bash

# Navigate to the directory containing app.py
cd ../

# Start the Python application in the background
python app.py &
APP_PID=$!

# Wait for the server to start
sleep 5

# Navigate to the test script directory
cd -  # Goes back to the previous directory

# Run the second test script, test2.py
python integration_order_matching.py
# Capture the exit status of the second test script
TEST2_STATUS=$?

# Run the first test script
python integration_order_create_manual_test.py
# Capture the exit status of the first test script
TEST1_STATUS=$?

# Terminate the Python application
kill $APP_PID

# Check if both tests passed
if [ $TEST1_STATUS -eq 0 ] && [ $TEST2_STATUS -eq 0 ]; then
    exit 0  # Exit with success if both tests passed
else
    exit 1  # Exit with failure if any test failed
fi
