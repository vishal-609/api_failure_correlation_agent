import re
import csv
import os
from config import CORRELATION_KEYWORDS

def parse_logs():
    # This empty list will eventually hold all the log entries from every system
    all_events = []

    # Figure out where this script is located and point to the 'data' folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    
    # Create the 'data' folder if it doesn't exist yet
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Define the exact file paths for our 3 input logs and our 1 final output CSV
    apic_path = os.path.join(data_dir, 'apic.log')
    mq_path = os.path.join(data_dir, 'mq.log')
    appconnect_path = os.path.join(data_dir, 'appconnect.log')
    output_path = os.path.join(data_dir, 'merged_logs.csv')

    # Create a dynamic search pattern that catches any correlation ID format you defined in config.py
    id_pattern = rf'(?:\[(?:{"|".join(CORRELATION_KEYWORDS)}):\s+([^\]]+)\]|\[([^\]]+)\])'

    # Inject that ID pattern into the specific search rules for each system's log structure
    apic_regex = re.compile(rf'^(\S+)\s+\w+\s+\[apic-gateway\]\s+{id_pattern}\s+(.*)$', re.IGNORECASE)
    mq_regex = re.compile(rf'^(\S+)\s+\w+\s+\[ibm-mq\]\s+{id_pattern}\s+(.*)$', re.IGNORECASE)
    appc_regex = re.compile(rf'^(\S+)\s+\w+\s+\[app-connect\]\s+{id_pattern}\s+(.*)$', re.IGNORECASE)

    # --- PROCESS API LOGS ---
    if os.path.exists(apic_path):
        with open(apic_path, "r") as f:
            for line in f:
                # Test if the line matches our API log pattern
                match = apic_regex.match(line.strip())
                if match:
                    # Extract the pieces of information based on their position (group) in the pattern
                    ts = match.group(1)
                    cid = match.group(2) if match.group(2) else match.group(3)
                    msg = match.group(4)
                    
                    event_type = ""
                    details = ""
                    
                    # Figure out what is happening based on keywords in the message
                    if "Incoming" in msg:
                        event_type = "REQUEST"
                        details = msg.split("Incoming ")[1] 
                    elif "Error" in msg:
                        event_type = "ERROR"
                        details = msg.split("Error ")[1] 
                    elif "Response" in msg:
                        event_type = "RESPONSE"
                        details = msg.split("Response ")[1]

                    # Save this cleaned-up row to our master list
                    all_events.append([ts, cid, "API", event_type, details])
    else:
        print(f"[!] Warning: APIC log not found at {apic_path}. Skipping.")

    # --- PROCESS MQ LOGS ---
    if os.path.exists(mq_path):
        with open(mq_path, "r") as f:
            for line in f:
                # Test if the line matches our MQ log pattern
                match = mq_regex.match(line.strip())
                if match:
                    # Extract the pieces of information
                    ts = match.group(1)
                    cid = match.group(2) if match.group(2) else match.group(3)
                    msg = match.group(4) 

                    event_type = ""
                    details = ""
                    
                    # Categorize the MQ event
                    if "PUT" in msg:
                        event_type = "MESSAGE_PUT"
                        details = msg.replace("PUT ", "")
                    elif "GET" in msg:
                        event_type = "MESSAGE_GET"
                        details = msg.replace("GET ", "")
                    elif "Error" in msg or "ERROR" in msg or "failed" in msg:
                        event_type = "ERROR"
                        details = msg

                    # Save to master list
                    all_events.append([ts, cid, "MQ", event_type, details])
    else:
        print(f"[!] Warning: MQ log not found at {mq_path}. Skipping.")

    # --- PROCESS APP CONNECT LOGS ---
    if os.path.exists(appconnect_path):
        with open(appconnect_path, "r") as f:
            for line in f:
                # Test if the line matches our App Connect log pattern
                match = appc_regex.match(line.strip())
                if match:
                    # Extract the pieces of information
                    ts = match.group(1)
                    cid = match.group(2) if match.group(2) else match.group(3)
                    msg = match.group(4)

                    event_type = ""
                    details = ""

                    # Categorize the App Connect event
                    if "Flow started" in msg:
                        event_type = "FLOW_START"
                        details = msg.split("API=")[1] if "API=" in msg else msg
                    elif "Flow error" in msg:
                        event_type = "ERROR"
                        details = msg.split("Flow error propagated ")[1]
                    elif "Flow completed" in msg:
                        event_type = "FLOW_END"
                        details = msg.split("Flow completed ")[1]
                    elif "Transform" in msg:
                        event_type = "TRANSFORM"

                    # Save to master list
                    all_events.append([ts, cid, "APP_CONNECT", event_type, details])
    else:
        print(f"[!] Warning: AppConnect log not found at {appconnect_path}. Skipping.")

    # Sort the master list chronologically by the timestamp (which is at index 0)
    all_events.sort(key=lambda x: x[0])

    # Safety check: Prevent errors later if the logs were totally empty
    if not all_events:
        print("[!] No log events parsed. Writing empty CSV with headers to prevent downstream errors.")

    # Create the final CSV file and write all our sorted data into it
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        # Write the top header row
        writer.writerow(["timestamp", "correlationId", "system", "eventType", "details_or_flowName"])
        # Write all the actual data rows
        writer.writerows(all_events)

if __name__ == "__main__":
    parse_logs()