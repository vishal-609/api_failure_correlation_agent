# Input and Output file paths
CSV_FILE_PATH = "output/merged_logs.csv"
OUTPUT_FILE_PATH = "output/correlation_report.txt"

# Delays
TRANSACTION_DELAY_SECONDS = 2 # Delay for each transaction id 
POLL_INTERVAL_SECONDS = 15 # repeatition of agent_runner for entire transaction so it keeps running

# Email Alert Configuration
SMTP_SERVER = "smtp.gmail.com" 
SMTP_PORT = 587
SENDER_EMAIL = "vishalsender.2002@gmail.com"
RECEIVER_EMAIL = "vishalreceiver.2002@gmail.com"

# Dependency chain 
DEPENDENCY_CHAIN = "API -> APP_CONNECT -> MQ"

# Status Code keywords to look for in logs (case-insensitive)
STATUS_KEYWORDS = ["Status", "StatusCode", "code", "HttpCode"]

# Correlation ID keywords to look for in logs (case-insensitive)
CORRELATION_KEYWORDS = ["X-Correlation-ID", "CorrelId", "CorrelationId"]

