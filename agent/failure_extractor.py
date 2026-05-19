import pandas as pd
import re
import os
from config import STATUS_KEYWORDS

def extract_failures(df):
    if df is None or df.empty or "eventType" not in df.columns:
        return pd.DataFrame()

    df = df.copy()
    failed_ids = set()

    pattern = rf'(?:{"|".join(STATUS_KEYWORDS)})=(\d+)'
    
    for _, row in df.iterrows():
        if row["eventType"] == "ERROR":
            failed_ids.add(row["correlationId"])
            continue
            
        if pd.notna(row.get("details_or_flowName")):
            match = re.search(pattern, str(row["details_or_flowName"]), re.IGNORECASE)
            if match and not (200 <= int(match.group(1)) <= 299):
                failed_ids.add(row["correlationId"])

    failed_df = df[df["correlationId"].isin(list(failed_ids))]

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    output_path = os.path.join(data_dir, 'failed_logs.csv')
    failed_df.to_csv(output_path, index=False)

    return failed_df