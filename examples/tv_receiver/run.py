import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from state_monitoring_system.core.controller import SystemController
from state_monitoring_system.examples.tv_receiver.states import TVOff
from state_monitoring_system.examples.tv_receiver.input import RemoteControlSimulator

def main():
    start_state = TVOff()
    # Press power button 4 times: Off -> On -> Off -> On -> Off
    input_source = RemoteControlSimulator(interval=0.5, presses=4)
    
    controller = SystemController(start_state, input_source, log_file="tv.jsonl")
    
    print("Starting TV Receiver Monitoring...")
    controller.start()
    
    try:
        while controller.is_running():
            status = controller.get_current_state()
            print(f"[TV Status] {status.get('current_state')}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        controller.stop()

if __name__ == "__main__":
    main()
