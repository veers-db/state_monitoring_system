from typing import Any, Optional
from ...core.fsm import State

class TrafficLightState(State):
    """Base state for traffic lights to share common logic if needed."""
    def handle_input(self, input_data: Any) -> Optional['State']:
        # Simple string matching for this example
        if input_data == "RED" and self.name != "RED":
            return RedLight()
        if input_data == "YELLOW" and self.name != "YELLOW":
            return YellowLight()
        if input_data == "GREEN" and self.name != "GREEN":
            return GreenLight()
        return None

class RedLight(TrafficLightState):
    @property
    def name(self) -> str:
        return "RED"
    
    def on_enter(self, context: dict) -> None:
        print(">>> Traffic Light Changed to RED")

class YellowLight(TrafficLightState):
    @property
    def name(self) -> str:
        return "YELLOW"
        
    def on_enter(self, context: dict) -> None:
        print(">>> Traffic Light Changed to YELLOW")

class GreenLight(TrafficLightState):
    @property
    def name(self) -> str:
        return "GREEN"
        
    def on_enter(self, context: dict) -> None:
        print(">>> Traffic Light Changed to GREEN")
