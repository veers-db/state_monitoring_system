import time
import random
from typing import Any, List
from ...core.fsm import InputSource

class OrderEventSimulator(InputSource):
    def __init__(self, scenario: str = "success"):
        self.scenario = scenario
        self.steps = []
        self._index = 0
        
        if scenario == "success":
            self.steps = ["PROCESS_PAYMENT", "PAYMENT_APPROVED", "SHIP", "DELIVER"]
        elif scenario == "failure":
            self.steps = ["PROCESS_PAYMENT", "PAYMENT_FAILED", "CANCEL"]
        elif scenario == "retry":
            self.steps = ["PROCESS_PAYMENT", "PAYMENT_FAILED", "RETRY", "PAYMENT_APPROVED", "SHIP", "DELIVER"]
            
    def get_input(self) -> Any:
        time.sleep(0.8)
        if self._index >= len(self.steps):
            return None
            
        event = self.steps[self._index]
        self._index += 1
        return event
