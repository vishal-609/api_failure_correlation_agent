# API Failure Correlation Agent 🚨

An automated Site Reliability Engineering (SRE) tool that parses multi-system logs, correlates transactions, and uses AI to determine the root cause of API failures.

## 🌟 What This Does

This agent helps SRE teams quickly identify and resolve API failures across complex microservice environments.

- **Reads** logs from IBM API Gateway, IBM MQ, and App Connect.
- **Merges** logs using a shared correlation ID.
- **Detects** failure points such as HTTP 5xx or error events.
- **Analyzes** the timeline with an AI model (Groq Llama 3).
- **Alerts** the team with a summary email containing the root cause and recommended fix.

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
├── data/                       # Raw log files and generated CSVs
│   ├── apic.log
│   ├── appconnect.log
│   └── mq.log
│
├── output/                     # Generated reports are saved here
│
├── .env                        # Hidden passwords and API keys
├── config.py                   # Dynamic variables and settings
├── main.py                     # Main Python execution script
├── requirements.txt            # Python dependencies
├── run_agent.bat               # Windows launcher
└── run_agent.sh                # Mac/Linux/Git Bash launcher
```

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd api_failure_correlation_agent
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
```

### 3️⃣ Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux / Git Bash:

```bash
source venv/bin/activate
```

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

This installs dependencies such as:

- pandas
- Groq SDK
- python-dotenv
- other required libraries

### 5️⃣ Create the `.env` file

Create a file named `.env` in the project root and add your credentials:

```env
GROQ_API_KEY=your_groq_api_key_here
SMTP_PASSWORD=your_email_app_password_here
```

> Never commit `.env` or share it publicly.

### 6️⃣ Configure the project

Open `config.py` and update the settings for your environment.

Example values:

```python
STATUS_KEYWORDS = ["Status", "StatusCode", "HttpCode"]
CORRELATION_KEYWORDS = ["X-Correlation-ID", "CorrelId"]
SENDER_EMAIL = "your_email@gmail.com"
RECEIVER_EMAIL = "team_email@gmail.com"
```

---

## 🚀 Running the Agent

### Recommended: automatic launch

Windows:

```bash
run_agent.bat
```

macOS / Linux / Git Bash:

```bash
./run_agent.sh
```

These launcher scripts typically:

- activate the virtual environment
- run the project
- handle execution setup

### Manual method

```bash
python main.py
```

---

## 📈 Outputs

When the agent runs successfully, it will:

- generate merged CSV files in `data/`
- create detailed analysis reports in `output/`
- send instant email alerts for detected failed transactions

## ✅ Summary

This repository is built to simplify failure correlation across:

- IBM API Gateway logs
- IBM MQ logs
- App Connect logs

It uses correlation IDs, timeline analysis, and AI to pinpoint root causes quickly and notify your team automatically.
