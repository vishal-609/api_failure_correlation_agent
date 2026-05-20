@echo off
echo Starting API Failure Correlation Agent...

:: 2. Go to the project folder
cd /d "C:\Users\vishal.rakesh.kumar\OneDrive - Accenture\Desktop\code\api_failure_correlation_agent"

:: 3. Activate the virtual environment
call venv\Scripts\activate.bat

:: 4. Run the python script
python agent_runner.py

echo.
echo Process complete. Press any key to exit.
pause >nul