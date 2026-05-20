# API Failure Correlation Agent

A professional Site Reliability Engineering (SRE) utility for correlating API failures across IBM API Gateway, IBM MQ, and App Connect.

This project ingests logs from multiple systems, unifies them using correlation IDs, detects failure patterns, and generates actionable insight using AI-driven analysis.

## What it does

- Collects and parses log data from IBM API Gateway, IBM MQ, and App Connect.
- Aligns events across systems using correlation IDs.
- Identifies failure indicators such as HTTP 5xx responses and error events.
- Builds a chronological transaction timeline for each correlated flow.
- Uses an AI model to summarize root cause and remediation recommendations.
- Sends alert notifications to operations teams.

## Project layout

```text
api_failure_correlation_agent/
├── agent/
│   ├── correlation_engine.py   # transaction timeline builder
│   ├── data_loader.py          # merged CSV loader
│   ├── email_notifier.py       # SMTP alert sender
│   ├── failure_extractor.py    # failed transaction detector
│   ├── llm_analyzer.py         # AI analysis integration
│   ├── log_merger.py           # raw log parser and merger
│   └── reporter.py             # report generator
├── data/                       # raw logs and merged outputs
│   ├── apic.log
│   ├── appconnect.log
│   └── mq.log
├── output/                     # generated reports
├── .env                        # secrets and credentials
├── config.py                   # environment-specific settings
├── main.py                     # execution entry point
├── requirements.txt            # Python requirements
├── run_agent.bat               # Windows launcher
└── run_agent.sh                # macOS/Linux launcher
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/vishal-609/api_failure_correlation_agent.git
cd api_failure_correlation_agent
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux / Git Bash:

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create the `.env` file in the project root and add credentials:

```env
GROQ_API_KEY=your_groq_api_key_here
SMTP_PASSWORD=your_email_app_password_here
```

> Keep `.env` out of version control.

6. Update `config.py` for your environment.

Example:

```python
STATUS_KEYWORDS = ["Status", "StatusCode", "code", "HttpCode"]
CORRELATION_KEYWORDS = ["X-Correlation-ID", "CorrelId", "CorrelationId"]
SENDER_EMAIL = "your_email@gmail.com"
RECEIVER_EMAIL = "team_email@gmail.com"
```

## Running the agent

Recommended:

Windows:

```bash
run_agent.bat
```

macOS / Linux / Git Bash:

```bash
./run_agent.sh
```

Manual:

```bash
python main.py
```

## Output

When the process completes successfully, it will:

- produce merged CSV files in `data/`
- write analysis reports in `output/`
- send email alerts for detected failed transactions

## Summary

This repository provides a structured approach for failure correlation across IBM API Gateway, IBM MQ, and App Connect log streams. It combines log parsing, correlation tracking, transaction timeline assembly, and AI-assisted analysis to help operations teams identify root cause and reduce mean time to resolution.
