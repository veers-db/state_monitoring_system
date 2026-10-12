from typing import Any, Optional
from ...core.fsm import State

# --- Base ---
class HotelState(State):
    pass

# --- States ---
class Available(HotelState):
    @property
    def name(self) -> str:
        return "AVAILABLE"
    
    def handle_input(self, input_data: Any) -> Optional['State']:
        if input_data == "RESERVE":
            return Reserved()
        elif input_data == "CHECK_IN":
            return CheckedIn()
        return None

class Reserved(HotelState):
    @property
    def name(self) -> str:
        return "RESERVED"
    
    def handle_input(self, input_data: Any) -> Optional['State']:
        if input_data == "CHECK_IN":
            return CheckedIn()
        elif input_data == "CANCEL":
            return Cancelled()
        return None

class CheckedIn(HotelState):
    @property
    def name(self) -> str:
        return "CHECKED_IN"
    
    def handle_input(self, input_data: Any) -> Optional['State']:
        if input_data == "COMPLETE":
            return Completed()
        return None

class Completed(HotelState):
    @property
    def name(self) -> str:
        return "COMPLETED"
    
    def handle_input(self, input_data: Any) -> Optional['State']:
        return None # Terminal state

class Cancelled(HotelState):
    @property
    def name(self) -> str:
        return "CANCELLED"
    
    def handle_input(self, input_data: Any) -> Optional['State']:
        return None # Terminal state