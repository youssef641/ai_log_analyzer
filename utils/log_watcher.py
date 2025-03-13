import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils.log_reader import read_log_file
from models.ollama_model import summarize_logs_with_ollama
from config import LLM_PROVIDER

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, log_file):
        self.log_file = log_file
        self.last_size = 0  # Track file size
        self.errors = []  # Store error logs

    def on_modified(self, event):
        if event.src_path == self.log_file:
            self.process_new_logs()

    def process_new_logs(self):
        logs = read_log_file(self.log_file)
        new_size = len(logs)

        # Check for new logs
        if new_size > self.last_size:
            print("\n🔄 New log entries detected! Updating summary...")
            new_logs = logs[self.last_size:]  # Get only new lines
            self.last_size = new_size  # Update last size

            # Extract errors from new logs
            error_logs = [log for log in new_logs if "ERROR" in log]

            if error_logs:
                self.errors.extend(error_logs)  # Store errors
                self.save_errors_to_json()

            # Generate summary
            if LLM_PROVIDER == "ollama":
                summary = summarize_logs_with_ollama(new_logs)
            else:
                from models.openai_model import summarize_logs_with_openai
                summary = summarize_logs_with_openai(new_logs)

            print("\n🔹 Updated Log Summary:\n", summary)

    def save_errors_to_json(self):
        """Save extracted error logs to a JSON file."""
        with open("errors.json", "w") as json_file:
            json.dump(self.errors, json_file, indent=4)

        print("✅ Errors saved to errors.json")

def start_log_monitor(log_file):
    event_handler = LogFileHandler(log_file)
    observer = Observer()
    observer.schedule(event_handler, path=log_file, recursive=False)
    observer.start()

    print(f"👀 Watching {log_file} for changes... (Press Ctrl+C to stop)")

    try:
        while True:
            time.sleep(2)  # Keep script running
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Log monitoring stopped.")
    observer.join()
