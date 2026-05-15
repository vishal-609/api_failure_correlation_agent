import time
import datetime
from config import POLL_INTERVAL_SECONDS
import main  # Imports your main.py file

def start_daemon():
    print(f"[*] Starting Correlation Agent Daemon...")
    print(f"[*] Polling interval set to {POLL_INTERVAL_SECONDS} seconds.\n")
    
    while True:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"--- [ {current_time} ] Starting new analysis cycle ---")
        
        try:
            main.main()
        except Exception as e:
            print(f"[!] An error occurred during this cycle: {str(e)}")
            
        print(f"--- Cycle complete. Sleeping for {POLL_INTERVAL_SECONDS} seconds ---\n")
        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    start_daemon()