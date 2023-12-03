REM Navigate to the directory containing app.py
cd ..

REM Start the Python application in the background
start /b python app.py

REM Wait for a few seconds to allow the server to start
timeout /t 5 /nobreak > nul

REM Navigate to the test script directory and run the tests
cd tests
python integration_order_create_manual_test.py

REM Terminate the Python application
taskkill /IM python.exe /F
