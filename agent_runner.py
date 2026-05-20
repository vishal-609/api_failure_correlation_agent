import time      # Helps us pause or "sleep" the script
import datetime  # Helps us get the current clock time
from config import POLL_INTERVAL_SECONDS # Imports our custom wait time
import main      # Imports your main.py file so we can run it

def start_daemon():
    # A "daemon" is simply a program that runs continuously in the background
    print(f"[*] Starting Correlation Agent Daemon...")
    print(f"[*] Polling interval set to {POLL_INTERVAL_SECONDS} seconds.\n")
    
    # An infinite loop: this keeps running forever until you manually close the terminal
    while True:
        # Grab the exact current date and time so we know when the check started
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"--- [ {current_time} ] Starting new analysis cycle ---")
        
        # 'try' tells Python to attempt this code, but not to crash the whole program if it fails
        try:
            main.main() # Triggers your entire log analysis process
        except Exception as e:
            # If an error happens (like a missing file), print the error and move on safely
            print(f"[!] An error occurred during this cycle: {str(e)}")
            
        print(f"--- Cycle complete. Sleeping for {POLL_INTERVAL_SECONDS} seconds ---\n")
        
        # Pauses the script for the specified amount of time before looping back to the top
        time.sleep(POLL_INTERVAL_SECONDS)

# This line ensures the loop only starts if you run this file directly
if __name__ == "__main__":
    start_daemon()