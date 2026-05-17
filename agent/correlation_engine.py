import pandas as pd
import re

DEPENDENCY_CHAIN = "API -> APP_CONNECT -> MQ"

def analyze_transactions(df):
    results = []
    
    df = df.sort_values(by="timestamp")
    grouped = df.groupby("correlationId", sort=False)
    
    for i, (cid, group) in enumerate(grouped):

        # To run for entire log files => (remove i==20 & break)
        if i == 20:
            break
            
        events = []  # will hold every single log entry related to this transaction.
        failures = [] # will hold failure log entry related to this transaction.
        
        for _, row in group.iterrows():
            event_data = {
                "timestamp": row["timestamp"],
                "system": row["system"],
                "eventType": row["eventType"],
                "details": row.get("details_or_flowName", "")
            }
            events.append(event_data)
            
            is_failure = False
            
            if row["eventType"] == "ERROR":
                is_failure = True
            
            if pd.notna(row.get("details_or_flowName")):
                match = re.search(r'Status(?:Code)?=(\d+)', str(row["details_or_flowName"]))
                if match and not (200 <= int(match.group(1)) <= 299):
                    is_failure = True
                    
            if is_failure:
                failures.append(event_data)
                
        if failures:
            results.append({
                "correlationId": cid,
                "events": events,
                "failures": failures,
                "dependency_chain": DEPENDENCY_CHAIN
            })
            
    return results