import pandas as pd
import re
import os
from config import STATUS_KEYWORDS

def extract_failures(df):
    
    if df is None or df.empty or "eventType" not in df.columns:
        return pd.DataFrame()

    # Make a copy of the data so we don't accidentally change the original table
    df = df.copy()
    
    # Use a 'set' to store the IDs of failed transactions (a set automatically prevents duplicates)
    failed_ids = set()

    # Create a dynamic search pattern using the keywords from config.py (e.g., looks for Status=, StatusCode=, etc.)
    pattern = rf'(?:{"|".join(STATUS_KEYWORDS)})=(\d+)'
    
    # Loop through every single row in the data table one by one
    for _, row in df.iterrows():
        
        # CONDITION 1: If the event type explicitly says "ERROR", save this transaction's ID
        if row["eventType"] == "ERROR":
            failed_ids.add(row["correlationId"])
            continue # Move on to check the next row immediately
            
        # CONDITION 2: Check if there is text in the 'details_or_flowName' column
        if pd.notna(row.get("details_or_flowName")):
            # Search the text for our status code pattern (ignoring capital/lowercase letters)
            match = re.search(pattern, str(row["details_or_flowName"]), re.IGNORECASE)
            
            # If we found a status code, check if it is NOT a success code (Success codes are between 200 and 299)
            if match and not (200 <= int(match.group(1)) <= 299):
                failed_ids.add(row["correlationId"]) # If it's a bad code (like 500), save the ID

    # Create a new table that ONLY contains rows where the 'correlationId' matches one of our failed IDs
    failed_df = df[df["correlationId"].isin(list(failed_ids))]

    # Figure out exactly where this file is located on the computer to create a save folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    
    # Create the 'data' folder if it doesn't already exist
    os.makedirs(data_dir, exist_ok=True)
    
    # Save our new table of failed transactions as a CSV file so we can look at it later
    output_path = os.path.join(data_dir, 'failed_logs.csv')
    failed_df.to_csv(output_path, index=False)

    # Return the filtered table back to whatever script called this function
    return failed_df