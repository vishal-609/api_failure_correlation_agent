import pandas as pd
import re
from config import DEPENDENCY_CHAIN, COLUMN_TIMESTAMP, COLUMN_CORRELATION_ID, COLUMN_SYSTEM, COLUMN_EVENT_TYPE, COLUMN_DETAILS

def analyze_transactions(df):
    results = []
    
    df = df.sort_values(by=COLUMN_TIMESTAMP)
    grouped = df.groupby(COLUMN_CORRELATION_ID, sort=False)
    
    for i, (cid, group) in enumerate(grouped):

        # To run for entire log files => (remove i==10 & break)
        if i == 10:
            break
            
        events = []  # will hold every single log entry related to this transaction.
        failures = [] # will hold failure log entry related to this transaction.
        
        for _, row in group.iterrows():
            event_data = {
                "timestamp": row[COLUMN_TIMESTAMP],
                "system": row[COLUMN_SYSTEM],
                "eventType": row[COLUMN_EVENT_TYPE],
                "details": row.get(COLUMN_DETAILS, "")
            }
            events.append(event_data)
            
            is_failure = False
            
            if row[COLUMN_EVENT_TYPE] == "ERROR":
                is_failure = True
            
            if pd.notna(row.get(COLUMN_DETAILS)):
                match = re.search(r'Status(?:Code)?=(\d+)', str(row[COLUMN_DETAILS]))
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