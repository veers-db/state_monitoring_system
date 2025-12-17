import time
import random
from typing import Any
from ...core.fsm import InputSource

class TrafficCamSimulator(InputSource):
    def __init__(self, cycle_interval: float = 1.0):
        self.cycle_interval = cycle_interval
        # Force a cycle for demonstration: Red -> Green -> Yellow -> Red
        self._sequence = ["GREEN", "YELLOW", "RED", "GREEN", "YELLOW", "RED"]
        self._index = 0

    def get_input(self) -> Any:
        time.sleep(self.cycle_interval)
        if self._index >= len(self._sequence):
            return None # Stop
            
        signal = self._sequence[self._index]
        self._index += 1
        return signal
