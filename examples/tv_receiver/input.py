import time
import random
from typing import Any
from ...core.fsm import InputSource

class RemoteControlSimulator(InputSource):
    def __init__(self, interval: float = 1.0, presses: int = 5):
        self.interval = interval
        self.presses = presses
        self.count = 0

    def get_input(self) -> Any:
        time.sleep(self.interval)
        if self.count >= self.presses:
            return None
        
        # Simulate pushing the power button
        self.count += 1
        return "POWER"
