from typing import Any, Optional
from ...core.fsm import State

class TVState(State):
    """Base class for TV States."""
    pass

class TVOff(TVState):
    @property
    def name(self) -> str:
        return "TV_OFF"
    
    def on_enter(self, context: dict) -> None:
        print(">>> TV is now OFF.")

    def handle_input(self, input_data: Any) -> Optional['State']:
        if input_data == "POWER":
            return TVOn()
        return None

class TVOn(TVState):
    @property
    def name(self) -> str:
        return "TV_ON"
        
    def on_enter(self, context: dict) -> None:
        print(">>> TV is now ON.")

    def handle_input(self, input_data: Any) -> Optional['State']:
        if input_data == "POWER":
            return TVOff()
        return None
