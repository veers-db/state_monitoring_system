import time
import sys
import os
from multiprocessing import Queue

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from state_monitoring_system.core.controller import SystemController
from state_monitoring_system.examples.hotel_room_booking.states import Available
from state_monitoring_system.examples.hotel_room_booking.input import HotelFrontDeskSimulator

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
            
            # skipping initializing to directly show available
            if cs == "INITIALIZING":
                time.sleep(0.1)
                continue
            
            #shows status when changed
            if cs != last_state:
                print(f"\n[Room Status Update] Current State: **{cs}**")
                last_state = cs

            if cs in ["CHECKED_OUT", "CANCELLED"]:
                print("\nTerminal state reached. Closing session.")
                break

            #menu for user to select
            print("\n--- Hotel Front Desk Menu input any number---")
            print("1. Reserve")
            print("2. Check-in")
            print("3. Check-out")
            print("4. Cancel")
            
            choice = input("Select action (1-4): ").strip()
            
            event_map = {
                "1": "RESERVE",
                "2": "CHECK_IN",
                "3": "CHECK_OUT",
                "4": "CANCEL"
            }
            
            event = event_map.get(choice)
            if not event:
                print("[Warning] Invalid menu selection. Please choose between 1 and 4.")
                continue

            valid = True
            warning_msg = ""

            if cs == "AVAILABLE":
                if event == "CHECK_OUT":
                    warning_msg = "[Action Denied] You cannot check out an available room. Please reserve or check-in first."
                    valid = False
                elif event == "CANCEL":
                    warning_msg = "[Action Denied] You cannot cancel because there is no active reservation."
                    valid = False

            elif cs == "RESERVED":
                if event == "RESERVE":
                    warning_msg = "[Action Denied] The room is already reserved."
                    valid = False
                elif event == "CHECK_OUT":
                    warning_msg = "[Action Denied] You cannot check out directly after reserving. You must check-in first!"
                    valid = False

            elif cs == "CHECKED_IN":
                if event == "RESERVE":
                    warning_msg = "[Action Denied] Cannot reserve a room that is already occupied."
                    valid = False
                elif event == "CHECK_IN":
                    warning_msg = "[Action Denied] The guest is already checked in."
                    valid = False
                elif event == "CANCEL":
                    warning_msg = "[Action Denied] Cannot cancel a reservation that is already checked in."
                    valid = False

            if not valid:
                print(f"\n{warning_msg}")
                continue

            input_queue.put(event)
            time.sleep(0.3)

    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()

if __name__ == "__main__":
    main()