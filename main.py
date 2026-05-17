import time
from agent.log_merger import parse_logs 
from agent.data_loader import load_data
from agent.failure_extractor import extract_failures
from agent.correlation_engine import analyze_transactions
from agent.llm_analyzer import analyze_transaction
from agent.reporter import generate_report, save_report
# IMPORT THE NEW VARIABLE HERE:
from config import CSV_FILE_PATH, OUTPUT_FILE_PATH, TRANSACTION_DELAY_SECONDS
from agent.email_notifier import send_alert_email

def main():
    start_time = time.time()

    parse_logs()
    
    df = load_data(CSV_FILE_PATH)
    
    failures_df = extract_failures(df)
    print(f"FAILURE EXTRACTION COMPLETED: {len(failures_df)} failure events found.")
    
    results = analyze_transactions(failures_df) 
    analyses = []

    for i, item in enumerate(results, start=1):
        correlation_id = item['correlationId']
        print(f"{i}. Transaction {correlation_id} working...", end=" ", flush=True)
        
        analysis = analyze_transaction(item)
        analyses.append(analysis)

        # 1. Generate a mini-report for JUST THIS ONE transaction
        single_report = generate_report([item], [analysis])

        # 2. Send the email for this specific transaction immediately
        send_alert_email(single_report, correlation_id)

        # 3. Save a backup to the hard drive for EVERY transaction
        current_report = generate_report(results[:i], analyses)
        save_report(current_report, OUTPUT_FILE_PATH)

        # 4. Sleep for 15 seconds BEFORE the next loop (skip on the final item)
        if i < len(results):
            time.sleep(TRANSACTION_DELAY_SECONDS)
    
    # Generate the massive final report with ALL transactions
    report = generate_report(results, analyses)
    save_report(report, OUTPUT_FILE_PATH)
    
    end_time = time.time()
    total_time = end_time - start_time

    print(f"\nAnalysis complete. Results saved to {OUTPUT_FILE_PATH}")
    print(f"Total processing time: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()