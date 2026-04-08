import logging
import json
from datetime import datetime

class ETLAuditTrail:
    def __init__(self):
        self.logs = []
        self.start_time = datetime.now()
        self.metrics = {"input_rows": 0, "output_rows": 0, "nulls_handled": 0}

    def log_step(self, step_name: str, status: str, details: dict):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step_name,
            "status": status,
            "details": details
        }
        self.logs.append(log_entry)
        print(f"[AUDIT] {json.dumps(log_entry)}") # Structured log to stdout

    def generate_report(self):
        duration = (datetime.now() - self.start_time).total_seconds()
        return {
            "duration_seconds": duration,
            "metrics": self.metrics,
            "audit_trail": self.logs
        }
