#!/bin/bash
echo "Starting API Failure Correlation Agent..."

# Navigate to the folder where the script is located
cd "$(dirname "$0")"

# Activate the virtual environment
# (Checks for both Linux/Mac 'bin' folder and Windows Git Bash 'Scripts' folder)
if [ -d "venv/bin" ]; then
    source venv/bin/activate
elif [ -d "venv/Scripts" ]; then
    source venv/Scripts/activate
else
    echo "Virtual environment not found! Please check your venv folder."
    exit 1
fi

# Run the agent (Use python3 for Mac/Linux environments)
python agent_runner.py

# Deactivate the environment when done
deactivate
echo "Process complete."