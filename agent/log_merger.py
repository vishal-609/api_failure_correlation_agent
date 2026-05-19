import re
import csv
import os

def parse_logs():
    all_events = []

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    apic_path = os.path.join(data_dir, 'apic.log')
    mq_path = os.path.join(data_dir, 'mq.log')
    appconnect_path = os.path.join(data_dir, 'appconnect.log')
    output_path = os.path.join(data_dir, 'merged_logs.csv')

    apic_regex = re.compile(r'^(\S+)\s+\w+\s+\[apic-gateway\]\s+(?:\[X-Correlation-ID:\s+([^\]]+)\]|\[([^\]]+)\])\s+(.*)$')
    mq_regex = re.compile(r'^(\S+)\s+\w+\s+\[ibm-mq\]\s+\[CorrelId:\s+([^\]]+)\]\s+(.*)$')
    appc_regex = re.compile(r'^(\S+)\s+\w+\s+\[app-connect\]\s+(?:\[CorrelationId:\s+([^\]]+)\]|\[([^\]]+)\])\s+(.*)$')

    if os.path.exists(apic_path):
        with open(apic_path, "r") as f:
            for line in f:
                match = apic_regex.match(line.strip())
                if match:
                    ts = match.group(1)
                    cid = match.group(2) if match.group(2) else match.group(3)
                    msg = match.group(4)
                    
                    event_type = ""
                    details = ""
                    
                    if "Incoming" in msg:
                        event_type = "REQUEST"
                        details = msg.split("Incoming ")[1] 
                    elif "Error" in msg:
                        event_type = "ERROR"
                        details = msg.split("Error ")[1] 
                    elif "Response" in msg:
                        event_type = "RESPONSE"
                        details = msg.split("Response ")[1]

                    all_events.append([ts, cid, "API", event_type, details])
    else:
        print(f"[!] Warning: APIC log not found at {apic_path}. Skipping.")

    if os.path.exists(mq_path):
        with open(mq_path, "r") as f:
            for line in f:
                match = mq_regex.match(line.strip())
                if match:
                    ts = match.group(1)
                    cid = match.group(2)
                    msg = match.group(3)

                    event_type = ""
                    details = ""
                    
                    if "PUT" in msg:
                        event_type = "MESSAGE_PUT"
                        details = msg.replace("PUT ", "")
                    elif "GET" in msg:
                        event_type = "MESSAGE_GET"
                        details = msg.replace("GET ", "")
                    elif "Error" in msg or "ERROR" in msg or "failed" in msg:
                        event_type = "ERROR"
                        details = msg

                    all_events.append([ts, cid, "MQ", event_type, details])
    else:
        print(f"[!] Warning: MQ log not found at {mq_path}. Skipping.")

    if os.path.exists(appconnect_path):
        with open(appconnect_path, "r") as f:
            for line in f:
                match = appc_regex.match(line.strip())
                if match:
                    ts = match.group(1)
                    cid = match.group(2) if match.group(2) else match.group(3)
                    msg = match.group(4)

                    event_type = ""
                    details = ""

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

                    all_events.append([ts, cid, "APP_CONNECT", event_type, details])
    else:
        print(f"[!] Warning: AppConnect log not found at {appconnect_path}. Skipping.")

    all_events.sort(key=lambda x: x[0])

    if not all_events:
        print("[!] No log events parsed. Writing empty CSV with headers to prevent downstream errors.")

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "correlationId", "system", "eventType", "details_or_flowName"])
        writer.writerows(all_events)

if __name__ == "__main__":
    parse_logs()