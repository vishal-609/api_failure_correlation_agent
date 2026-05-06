import pandas as pd
import re

def extract_failures(df):
    df = df.copy()
    
    failed_ids = set()
    
    # Go through the rows to find any failures
    for _, row in df.iterrows():
        # 1. Check if the eventType is explicitly an ERROR
        if row["eventType"] == "ERROR":
            failed_ids.add(row["correlationId"])
            continue
            
        # 2. Check if there is a bad status code in the details column
        if pd.notna(row["details_or_flowName"]):
            match = re.search(r'Status(?:Code)?=(\d+)', str(row["details_or_flowName"]))
            if match and not (200 <= int(match.group(1)) <= 299):
                failed_ids.add(row["correlationId"])

    # Return all rows (the whole transaction history) for the failed IDs
    return df[df["correlationId"].isin(list(failed_ids))]