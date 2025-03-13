from utils.log_reader import read_log_file
from utils.log_watcher import start_log_monitor
from config import LLM_PROVIDER
from models.ollama_model import summarize_logs_with_ollama

import os

if __name__ == "__main__":
    # Ask user for log file path
    while True:
        log_path = input("Enter the path to the log file: ").strip()
        
        # Convert relative path to absolute path
        log_path = os.path.abspath(log_path)

        if os.path.exists(log_path) and os.path.isfile(log_path):
            break
        else:
            print(f"❌ Invalid file path: {log_path}. Please enter a valid log file path.")

    # Load initial logs
    log_data = read_log_file(log_path)

    # Generate initial log summary
    if LLM_PROVIDER == "ollama":
        summary = summarize_logs_with_ollama(log_data)
    else:
        raise ValueError("Invalid LLM provider! Choose 'ollama' or 'openai'.")

    print("\n🔹 Initial Log Summary:\n", summary)

    # Start real-time log monitoring
    print(f"\n👀 Watching {log_path} for real-time updates...\n")
    start_log_monitor(log_path)
