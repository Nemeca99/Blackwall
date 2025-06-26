"""
Lungs

Interface/buffer for external connections, logs, and diagnostics.
Handles input/output for logs, metrics, and system health.

Expected Interface:
- inhale(): capture external input
- exhale(): output system metrics/logs
- receive_signal(source, payload): handle incoming messages (optional)
- Optionally register for 'state_update' or 'input_received' events from body
"""
import os
import re
import json

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'log')
LOG_FILE = os.path.join(LOG_DIR, 'BLACKWALL_LOGS.md')
FRAGMENT_HISTORY_FILE = os.path.join(LOG_DIR, 'fragment_weights_history.jsonl')

class Lungs:
    def __init__(self):
        """Initialize lungs state and metrics."""
        self.metrics = {}
        self.log_path = LOG_FILE
        self.fragment_history_path = FRAGMENT_HISTORY_FILE

    def inhale(self):
        """Capture environmental or external input (stub)."""
        # TODO: Implement input logic (e.g., from API, dashboard, etc.)
        return None

    def exhale(self):
        """Output system metrics or logs (stub)."""
        # TODO: Implement output logic (e.g., to dashboard, webhook, etc.)
        pass

    def read_log(self, n=100):
        """Read the last n lines from the main log file."""
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return lines[-n:]
        return []

    def parse_fragment_history(self, n=100):
        """Parse the last n entries from the fragment weights history log."""
        if os.path.exists(self.fragment_history_path):
            with open(self.fragment_history_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[-n:]
            return [json.loads(line) for line in lines if line.strip()]
        return []

    def summarize_logs(self):
        """Summarize key events or metrics from logs (stub)."""
        # TODO: Implement log parsing and summary logic
        return {}

    def collect_metrics(self):
        """Collect and return system health metrics (stub)."""
        # TODO: Implement metrics collection (CPU, memory, etc.)
        return self.metrics

    def receive_signal(self, source, payload):
        """Handle incoming messages (from Body or other modules)."""
        message_type = payload.get("type", "")
        data = payload.get("data", {})
        print(f"[Lungs] Received signal from {source}: {message_type}")
        if message_type == "log":
            log_entry = data.get("entry", "")
            if log_entry:
                with open(self.log_path, 'a', encoding='utf-8') as f:
                    f.write(log_entry + "\n")
                print(f"[Lungs] Logged entry: {log_entry}")
        # Add more message types as needed
        return True

    def register_with_body(self, body):
        """Register this module with the Body system."""
        if body:
            result = body.register_module("lungs", self)
            print("[Lungs] Registered with body system")
            return result
        return False
