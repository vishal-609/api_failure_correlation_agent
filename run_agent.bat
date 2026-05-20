@echo off
echo Starting API Failure Correlation Agent...

:: This line ensures the script runs in the correct folder no matter where you click it from
cd /d "%~dp0"

:: Activate your virtual environment
call venv\Scripts\activate.bat

:: Run your main python script (Change to main.py if that is your primary entry point)
python agent_runner.py

:: Keeps the terminal window open after it finishes so you can read the output
echo.
echo Process complete. Press any key to exit.
pause >nul