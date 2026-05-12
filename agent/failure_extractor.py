import pandas as pd
import re
import os

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

    # Extract the failed transactions into a new DataFrame
    failed_df = df[df["correlationId"].isin(list(failed_ids))]

    # --- NEW CODE TO SAVE THE FILE ---
    # Find the data directory (assuming this script is in your 'agent' folder)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    
    # Define the output path for the new file
    output_path = os.path.join(data_dir, 'failed_logs.csv')
    
    # Save the isolated failures to a physical CSV file
    failed_df.to_csv(output_path, index=False)
    # ---------------------------------

    # Return the DataFrame so main.py can still send it to the LLM
    return failed_df