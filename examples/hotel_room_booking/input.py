from typing import Any, Optional
from multiprocessing import Queue
from ...core.fsm import InputSource

class HotelFrontDeskSimulator(InputSource):
    def __init__(self, input_queue: Optional[Queue] = None):
        self.input_queue = input_queue if input_queue is not None else Queue()

    def get_input(self) -> Any:
        return self.input_queue.get()