import time
from agent.log_merger import parse_logs 
from agent.data_loader import load_data
from agent.failure_extractor import extract_failures
from agent.correlation_engine import analyze_transactions
from agent.llm_analyzer import analyze_transaction
from agent.reporter import generate_report, save_report
from config import CSV_FILE_PATH, OUTPUT_FILE_PATH
from agent.email_notifier import send_alert_email

def main():
    start_time = time.time()

    parse_logs()
    
    df = load_data(CSV_FILE_PATH)
    
    failures_df = extract_failures(df)
    print(f"FAILURE EXTRACTION COMPLETED: {len(failures_df)} failure events found.")

    print("\n--- ERROR COUNT BY SYSTEM ---")
    print(failures_df[failures_df['eventType'] == 'ERROR']['system'].value_counts())
    print("-----------------------------\n")
    
    results = analyze_transactions(failures_df) 
    analyses = []

    for i, item in enumerate(results, start=1):
        print(f"{i}. Transaction {item['correlationId']} working...", end=" ", flush=True)
        analysis = analyze_transaction(item)
        analyses.append(analysis)

        # Save every 5 transactions to balance speed and safety
        if i % 5 == 0 or i == len(results):
            current_report = generate_report(results[:i], analyses)
            save_report(current_report, OUTPUT_FILE_PATH)
            
        print("completed")

    report = generate_report(results, analyses)
    save_report(report, OUTPUT_FILE_PATH)
    
    send_alert_email(report)

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\nAnalysis complete. Results saved to {OUTPUT_FILE_PATH}")
    print(f"Total processing time: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()