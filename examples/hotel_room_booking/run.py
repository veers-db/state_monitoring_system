import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from state_monitoring_system.core.controller import SystemController
from state_monitoring_system.examples.hotel_room_booking.states import Available
from state_monitoring_system.examples.hotel_room_booking.input import HotelFrontDeskSimulator

def main():
    scenario = "standard"
    if len(sys.argv) > 1:
        scenario = sys.argv[1]
        
    print(f"Running scenario: {scenario}")

    start_state = Available()
    input_source = HotelFrontDeskSimulator(scenario=scenario, interval=0.5)
    
    controller = SystemController(start_state, input_source, log_file=f"hotel_booking_{scenario}.jsonl")
    
    print("Starting Hotel Booking System Monitoring...")
    controller.start()
    
    try:
        while controller.is_running():
            status = controller.get_current_state()
            print(f"[Room Status] {status.get('current_state')}")
            time.sleep(0.5)

            cs = status.get('current_state')
            if cs in ["COMPLETED", "CANCELLED"]:
                print("Terminal state reached.")
                break

    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()

if __name__ == "__main__":
    main()
