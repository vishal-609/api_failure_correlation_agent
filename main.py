import time      # Helps us measure how long the script takes to run and pause the script when needed
from agent.log_merger import parse_logs # Imports our function that combines the raw log files
from agent.data_loader import load_data # Imports our function that loads the combined CSV data
from agent.failure_extractor import extract_failures # Imports our function that finds the bad transactions
from agent.correlation_engine import analyze_transactions # Imports our function that builds the transaction timelines
from agent.llm_analyzer import analyze_transaction # Imports our function that sends the timeline to the AI
from agent.reporter import generate_report, save_report # Imports our functions that format and save the text report
from config import CSV_FILE_PATH, OUTPUT_FILE_PATH, TRANSACTION_DELAY_SECONDS # Imports our file paths and wait time
from agent.email_notifier import send_alert_email # Imports our function that sends the email warning

def main():
    # Start a stopwatch so we can see exactly how long the whole process takes
    start_time = time.time()

    # Step 1: Read the raw text logs and combine them into one clean CSV file
    parse_logs()
    
    # Step 2: Load that clean CSV file into our Python memory (as a pandas DataFrame)
    df = load_data(CSV_FILE_PATH)
    
    # Step 3: Scan the data and isolate only the transactions that had an error or a bad status code
    failures_df = extract_failures(df)
    print(f"FAILURE EXTRACTION COMPLETED: {len(failures_df)} failure events found.")
    
    # Step 4: Group those failures into complete timelines (Dependency Chains)
    results = analyze_transactions(failures_df) 
    
    # Create an empty list to hold the AI's final root cause reports
    analyses = []

    # Step 5: Loop through every single failed transaction one by one
    # enumerate(..., start=1) just gives us a counter (i) starting at 1 so we can track our progress
    for i, item in enumerate(results, start=1):
        correlation_id = item['correlationId']
        
        # Print a status update to the terminal (flush=True forces it to print immediately without waiting)
        print(f"{i}. Transaction {correlation_id} working...", end=" ", flush=True)
        
        # Send this specific transaction's timeline to Groq/Llama3 and get the root cause back
        analysis = analyze_transaction(item)
        analyses.append(analysis) # Save the AI's answer to our list

        # Generate a mini text report that ONLY contains the data for this one specific failure
        single_report = generate_report([item], [analysis])

        # Email that mini report to the team immediately so they don't have to wait for the whole script to finish
        send_alert_email(single_report, correlation_id)

        # Update our running master report on the hard drive, just in case the computer crashes halfway through
        current_report = generate_report(results[:i], analyses)
        save_report(current_report, OUTPUT_FILE_PATH)

        # To avoid hitting API rate limits (sending too many requests too fast), pause the script here
        # (We skip the pause on the very last item because we are already done)
        if i < len(results):
            time.sleep(TRANSACTION_DELAY_SECONDS)
    
    # Step 6: Now that the loop is finished, generate one massive final report containing every transaction
    report = generate_report(results, analyses)
    save_report(report, OUTPUT_FILE_PATH)
    
    # Stop the stopwatch and calculate the total time
    end_time = time.time()
    total_time = end_time - start_time

    # Print the final success messages and the total execution time
    print(f"\nAnalysis complete. Results saved to {OUTPUT_FILE_PATH}")
    print(f"Total processing time: {total_time:.2f} seconds")

# This line ensures the script only runs if you execute this file directly
if __name__ == "__main__":
    main()