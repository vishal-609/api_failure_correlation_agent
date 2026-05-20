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


⚙️ Setup & Installation

1. Clone or Download the Project :

Make sure all your files are in the main project folder.

2. Set Up a Virtual Environment:

Open your terminal and run:

Bash
python -m venv venv

3. Install Dependencies:

Activate your environment and install the required packages (Pandas, OpenAI, python-dotenv):

Windows: venv\Scripts\activate

Mac/Linux: source venv/bin/activate

Bash
pip install -r requirements.txt

4. Create the .env File:

Create a file named exactly .env in your main folder. Add your sensitive keys here (do not share this file!):

Code snippet
GROQ_API_KEY=your_groq_api_key_here
SMTP_PASSWORD=your_email_app_password_here

🛠️ Configuration:

Open config.py to customize the agent for your specific logs:

STATUS_KEYWORDS: Add words your logs use for status codes (e.g., ["Status", "StatusCode", "HttpCode"]).

CORRELATION_KEYWORDS: Add words your logs use for tracking IDs (e.g., ["X-Correlation-ID", "CorrelId"]).

Email Settings: Update the SENDER_EMAIL and RECEIVER_EMAIL to match your team's routing.

🚀 How to Run the Agent:

The Easiest Way (Recommended):

Windows: Simply double-click the run_agent.bat file.

Mac/Linux/Git Bash: Run ./run_agent.sh in your terminal.
(These scripts will automatically activate your environment and run the code for you!)

The Manual Way:
If you prefer running it manually via the terminal:

Bash
python main.py

📈 Outputs:

Once the agent finishes running, it will:

Save a clean CSV of merged logs in the data/ folder.

Save a comprehensive text report in the output/ folder.

Send an immediate email alert for every failed transaction it finds.