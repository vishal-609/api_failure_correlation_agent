#!/bin/bash
echo "Starting API Failure Correlation Agent..."

# 1. Go directly to your project folder (using forward slashes for Bash)
cd "C:/Users/vishal.rakesh.kumar/OneDrive - Accenture/Desktop/code/api_failure_correlation_agent"

# 2. Activate the virtual environment
if [ -d "venv/bin" ]; then
    source venv/bin/activate
elif [ -d "venv/Scripts" ]; then
    source venv/Scripts/activate
else
    echo "Virtual environment not found! Please check your venv folder."
    exit 1
fi

# 3. Run the python script
python agent_runner.py

# 4. Deactivate the environment when done
deactivate
echo "Process complete."