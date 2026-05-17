import pandas as pd
import re
import os
from config import COLUMN_EVENT_TYPE, COLUMN_CORRELATION_ID, COLUMN_DETAILS

def extract_failures(df):
    if df is None or df.empty or COLUMN_EVENT_TYPE not in df.columns:
        return pd.DataFrame()

    df = df.copy()
    failed_ids = set()
    
    for _, row in df.iterrows():
        if row[COLUMN_EVENT_TYPE] == "ERROR":
            failed_ids.add(row[COLUMN_CORRELATION_ID])
            continue
            
        if pd.notna(row.get(COLUMN_DETAILS)):
            match = re.search(r'Status(?:Code)?=(\d+)', str(row[COLUMN_DETAILS]))
            if match and not (200 <= int(match.group(1)) <= 299):
                failed_ids.add(row[COLUMN_CORRELATION_ID])

    failed_df = df[df[COLUMN_CORRELATION_ID].isin(list(failed_ids))]

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    output_path = os.path.join(data_dir, 'failed_logs.csv')
    failed_df.to_csv(output_path, index=False)

    return failed_df