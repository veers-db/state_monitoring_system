import time
import sys
import os
from multiprocessing import Queue

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from state_monitoring_system.core.controller import SystemController
from state_monitoring_system.examples.hotel_room_booking.states import Available
from state_monitoring_system.examples.hotel_room_booking.input import HotelFrontDeskSimulator

event_map = {
    "1": ("RESERVE", "RESERVED"),
    "2": ("CHECK_IN", "CHECKED_IN"),
    "3": ("CHECK_OUT", "CHECKED_OUT"),
    "4": ("CANCEL", "CANCELLED")
}

invalid_transitions = {
    "AVAILABLE": {
        "CHECK_OUT": "[Action Denied] You cannot check out an available room. Please reserve or check-in first.",
        "CANCEL": "[Action Denied] You cannot cancel because there is no active reservation."
    },
    "RESERVED": {
        "RESERVE": "[Action Denied] The room is already reserved.",
        "CHECK_OUT": "[Action Denied] You cannot check out directly after reserving. You must check-in first!"
    },
    "CHECKED_IN": {
        "RESERVE": "[Action Denied] Cannot reserve a room that is already occupied.",
        "CHECK_IN": "[Action Denied] The guest is already checked in.",
        "CANCEL": "[Action Denied] Cannot cancel a reservation that is already checked in."
    }
}

def main():
    print("Starting Hotel Room Booking System...")

    start_state = Available()
    input_queue = Queue()
    input_source = HotelFrontDeskSimulator(input_queue=input_queue)
    
    controller = SystemController(start_state, input_source, log_file="hotel_booking_interactive.jsonl")
    controller.start()
    
    try:
        last_state = None
        while controller.is_running():
            status = controller.get_current_state()
            cs = status.get('current_state')
            
            # Skipping initializing to directly show available
            if cs == "INITIALIZING":
                time.sleep(0.1)
                continue
            
            # Show status when changed
            if cs != last_state:
                print(f"\n[Room Status Update] Current State: **{cs}**")
                last_state = cs

            if cs in ["CHECKED_OUT", "CANCELLED"]:
                print("\nTerminal state reached. Closing session.")
                break

            print("\n--- Hotel Front Desk Menu ---")
            print("1. Reserve\n2. Check-in\n3. Check-out\n4. Cancel")
            
            choice = input("Select action (1-4): ").strip()
            action_info = event_map.get(choice)
            
            if not action_info:
                print("[Warning] Invalid menu selection. Please choose between 1 and 4.")
                continue

            event, expected_state = action_info

            warning_msg = invalid_transitions.get(cs, {}).get(event)
            if warning_msg:
                print(f"\n{warning_msg}")
                continue

            input_queue.put(event)
            
            timeout = 5.0
            start_wait = time.time()
            state_updated = False
            
            print(f"Processing action '{event}'... Waiting for state update.")
            while time.time() - start_wait < timeout:
                if controller.get_current_state().get('current_state') == expected_state:
                    state_updated = True
                    break
                time.sleep(0.1)
                
            if not state_updated:
                print(f"[Warning] Timeout ({timeout}s) reached while waiting for state to update to '{expected_state}'.")

    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()

if __name__ == "__main__":
    main()