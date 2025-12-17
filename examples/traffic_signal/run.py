import time
import sys
import os

# Ensure we can import core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from state_monitoring_system.core.controller import SystemController
from state_monitoring_system.examples.traffic_signal.states import RedLight
from state_monitoring_system.examples.traffic_signal.input import TrafficCamSimulator

def main():
    # Setup
    start_state = RedLight()
    input_source = TrafficCamSimulator(cycle_interval=1.0)
    
    controller = SystemController(start_state, input_source, log_file="traffic.jsonl")
    
    print("Starting Traffic Signal Monitoring System...")
    controller.start()
    
    # User Application Loop (Monitor the system)
    try:
        while controller.is_running():
            status = controller.get_current_state()
            print(f"[Dashboard] Current System State: {status.get('current_state')} (Updates: {status.get('history_count', 0)})")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopping...")
        controller.stop()
        
    print("Done.")

if __name__ == "__main__":
    main()
