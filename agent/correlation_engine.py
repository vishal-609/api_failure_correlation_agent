import pandas as pd
import re
from config import DEPENDENCY_CHAIN

def analyze_transactions(df):
    results = []
    
    # Sort all data chronologically so events appear in the exact order they happened
    df = df.sort_values(by="timestamp")
    
    # Group the data by transaction ID so we can analyze one complete transaction at a time
    grouped = df.groupby("correlationId", sort=False)
    
    for i, (cid, group) in enumerate(grouped):

        # Testing limit: Stop processing after 10 transactions (remove this block to process all logs)
        if i == 10:
            break
            
        events = []    # Stores every log entry for the current transaction
        failures = []  # Stores only the failed log entries for the current transaction
        
        # Loop through each log entry within this specific transaction
        for _, row in group.iterrows():
            
            # Package the important details into a neat dictionary
            event_data = {
                "timestamp": row["timestamp"],
                "system": row["system"],
                "eventType": row["eventType"],
                "details": row.get("details_or_flowName", "")
            }
            
            # Add this entry to our complete timeline of events
            events.append(event_data)
            
            is_failure = False  # Assume the event is successful until proven otherwise
            
            # CONDITION 1: The log explicitly states it is an error
            if row["eventType"] == "ERROR":
                is_failure = True
            
            # CONDITION 2: Check for HTTP status codes (like 404 or 500)
            if pd.notna(row.get("details_or_flowName")):
                # Search for 'Status=' or 'StatusCode=' followed by a number
                match = re.search(r'Status(?:Code)?=(\d+)', str(row["details_or_flowName"]))
                
                # If a code is found, flag it if it is outside the 200-299 success range
                if match and not (200 <= int(match.group(1)) <= 299):
                    is_failure = True
                    
            # If either condition marked this as a failure, save it to our failures list
            if is_failure:
                failures.append(event_data)
                
        # If this transaction had at least one failure, save its entire history for the final report
        if failures:
            results.append({
                "correlationId": cid,
                "events": events,
                "failures": failures,
                "dependency_chain": DEPENDENCY_CHAIN
            })
            
    # Return the final list of all failed transactions and their timelines
    return results