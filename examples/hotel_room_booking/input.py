import time
from typing import Any
from ...core.fsm import InputSource

class HotelFrontDeskSimulator(InputSource):
    def __init__(self, scenario: str = "standard", interval: float = 0.5):
        self.scenario = scenario
        self.interval = interval
        self.steps = []
        self._index = 0
        
        if scenario == "standard":
            self.steps = ["RESERVE", "CHECK_IN", "COMPLETE"]
        elif scenario == "cancelled":
            self.steps = ["RESERVE", "CANCEL"]
        elif scenario == "check_in":
            self.steps = ["CHECK_IN", "COMPLETE"]
        else:
            self.steps = ["RESERVE", "CHECK_IN", "COMPLETE"]
            
    def get_input(self) -> Any:
        time.sleep(self.interval)
        if self._index >= len(self.steps):
            return None
            
        event = self.steps[self._index]
        self._index += 1
        return event