import multiprocessing
import json
import time
from typing import Dict, Any

class StateRecorder:
    def __init__(self, event_queue: multiprocessing.Queue, shared_state: Dict[str, Any], log_file: str):
        self.event_queue = event_queue
        self.shared_state = shared_state
        self.log_file = log_file
        self.running = True

    def run(self):
        """Main loop of the Recorder Process."""
        try:
            with open(self.log_file, 'a') as f:
                while self.running:
                    event = self.event_queue.get()
                    
                    if event == "STOP":
                        self.running = False
                        break
                    
                    # Update shared state for real-time access
                    self.shared_state['current_state'] = event.to_state
                    self.shared_state['last_updated'] = event.timestamp
                    self.shared_state['history_count'] = self.shared_state.get('history_count', 0) + 1
                    
                    # Persist to disk
                    record = {
                        "timestamp": event.timestamp,
                        "from_state": event.from_state,
                        "to_state": event.to_state,
                        "metadata": event.metadata
                    }
                    f.write(json.dumps(record) + "\n")
                    f.flush()
        except Exception as e:
            # In a real app, use a proper logger
            print(f"Recorder Error: {e}")
