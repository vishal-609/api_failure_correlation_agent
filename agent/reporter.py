import os

def generate_report(results, analyses):
    # Set up the top header of our final text report
    report_lines = [
        "===== TRANSACTION FAILURE REPORT =====\n",
        f"Total Transactions Analyzed: {len(results)}\n",
        "=" * 50 + "\n"
    ]

    # zip() lets us loop through the raw data (results) and the AI's thoughts (analyses) at the same time
    for item, analysis in zip(results, analyses):
        
        # Start a new section for this specific transaction
        report_lines.append(f"--- Transaction ({item['correlationId']}) ---")
        
        # Extract a list of all systems involved. Using set() automatically removes duplicates (like MQ, MQ, API -> MQ, API)
        systems = list(set(e['system'] for e in item["events"]))
        report_lines.append(f"Systems Involved: {systems}")

        # If there are any recorded failures for this transaction, list them out line by line
        if item["failures"]:
            report_lines.append("Failures:")
            for f in item["failures"]:
                report_lines.append(f"{f.get('timestamp', 'Unknown')} - {f.get('system', '')} - {f.get('eventType', '')} - {f.get('details', '')}")
        else:
            report_lines.append("Failures: None")

        # Paste the AI's detailed root-cause analysis below the raw data
        report_lines.append("\nAI Analysis:")
        report_lines.append(analysis)
        report_lines.append("-" * 50 + "\n")

    # Combine all our separate lines into one massive block of text separated by "newline" characters
    return "\n".join(report_lines)

def save_report(report, file_path="output/final_report.txt"):
    # Safety Check: Create the 'output' folder if it doesn't already exist on the user's computer
    os.makedirs(os.path.dirname(file_path) or "output", exist_ok=True)
    
    # Open the file in "w" (write) mode, which will create the file or overwrite it if it already exists
    with open(file_path, "w") as f:
        f.write(report) # Write our massive block of text into the file
        
    # Print a success message to the terminal so the user knows it finished
    print("Report saved to", file_path)