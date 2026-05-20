# API Failure Correlation Agent 🚨

An automated Site Reliability Engineering (SRE) tool that parses multi-system logs, correlates transactions, and uses AI to instantly determine the root cause of API failures.

## 🌟 What This Does
When a transaction fails across a complex microservice architecture, finding the root cause takes time. This agent:
1. **Reads** logs from IBM API Gateway, IBM MQ, and App Connect.
2. **Merges** them using a shared Correlation ID.
3. **Identifies** the exact point of failure (e.g., HTTP 500 or Error events).
4. **Analyzes** the timeline using an AI model (Llama 3 via Groq).
5. **Alerts** the team immediately with an automated email containing the root cause and recommended fix.

---

## 📁 Project Structure

```text
api_failure_correlation_agent/
│
├── agent/                      # Core logic scripts
│   ├── correlation_engine.py   # Builds transaction timelines
│   ├── data_loader.py          # Loads combined CSV data
│   ├── email_notifier.py       # Sends SMTP email alerts
│   ├── failure_extractor.py    # Isolates failed transactions
│   ├── llm_analyzer.py         # Talks to the Groq AI model
│   ├── log_merger.py           # Parses raw logs into CSV
│   └── reporter.py             # Generates the text report
│
├── data/                       # Your raw log files go here
│   ├── apic.log
│   ├── appconnect.log
│   └── mq.log
│
├── output/                     # Generated reports are saved here
│
├── .env                        # Hidden passwords and API keys
├── config.py                   # Dynamic variables and settings
├── main.py                     # The main Python execution script
├── requirements.txt            # Python dependencies
│
├── run_agent.bat               # Windows double-click launcher
└── run_agent.sh                # Mac/Linux/Git Bash launcher


## ⚙️ Setup & Installation

```text
### 1️⃣ Clone or Download the Project

Download the repository or clone it using Git:

```bash
git clone <your-repo-url>

Make sure all project files remain inside the main project folder.

2️⃣ Create a Virtual Environment

Open your terminal inside the project folder and run:

python -m venv venv
3️⃣ Activate the Virtual Environment
🪟 Windows
venv\Scripts\activate
🍎 Mac / 🐧 Linux
source venv/bin/activate
4️⃣ Install Dependencies

Install all required Python packages:

pip install -r requirements.txt

This installs:

Pandas
OpenAI / Groq SDK
python-dotenv
and other required libraries
5️⃣ Create the .env File

Create a file named exactly:

.env

Add your sensitive credentials inside it:

GROQ_API_KEY=your_groq_api_key_here
SMTP_PASSWORD=your_email_app_password_here

⚠️ Never share or upload your .env file publicly.

🛠️ Configuration

Open:

config.py

Customize the following settings according to your environment.

🔹 STATUS_KEYWORDS

Add keywords your logs use for HTTP or status codes.

Example:

STATUS_KEYWORDS = ["Status", "StatusCode", "HttpCode"]
🔹 CORRELATION_KEYWORDS

Add keywords used for transaction or correlation tracking IDs.

Example:

CORRELATION_KEYWORDS = ["X-Correlation-ID", "CorrelId"]
🔹 Email Settings

Update the sender and receiver email addresses:

SENDER_EMAIL = "your_email@gmail.com"
RECEIVER_EMAIL = "team_email@gmail.com"
🚀 Running the Agent
✅ Recommended Method (Automatic)
🪟 Windows

Simply double-click:

run_agent.bat
🍎 Mac / 🐧 Linux / Git Bash

Run:

./run_agent.sh

These scripts automatically:

Activate the virtual environment
Run the project
Handle execution setup for you
🧑‍💻 Manual Method

If you prefer running the project manually:

python main.py
📈 Outputs

After execution, the agent automatically:

✅ Generates Clean CSV Files

Merged and processed logs are saved inside:

data/
✅ Creates Detailed Reports

Comprehensive transaction analysis reports are saved inside:

output/
✅ Sends Instant Email Alerts

For every failed transaction detected, the system:

Identifies the root cause
Generates AI-powered analysis
Sends an automated alert email immediately