import unittest
import multiprocessing
import queue
from ..core.fsm import State, InputSource, StateMachineEngine, TransitionEvent

class MockState(State):
    def __init__(self, name: str):
        self._name = name
        self.entered = False
        self.exited = False

    @property
    def name(self) -> str:
        return self._name

    def on_enter(self, context: dict) -> None:
        self.entered = True

    def on_exit(self, context: dict) -> None:
        self.exited = True

    def handle_input(self, input_data):
        if input_data == "NEXT":
            return MockState("STATE_2")
        return None

class MockInput(InputSource):
    def __init__(self, inputs):
        self.inputs = inputs
        self.index = 0

    def get_input(self):
        if self.index >= len(self.inputs):
            return None
        data = self.inputs[self.index]
        self.index += 1
        return data

class TestFSM(unittest.TestCase):
    def test_state_transitions(self):
        start_state = MockState("STATE_1")
        input_source = MockInput(["STAY", "NEXT", "STAY"])
        event_queue = multiprocessing.Queue()
        
        engine = StateMachineEngine(start_state, input_source, event_queue)
        engine.run()
        
        # Check Events
        # 1. Init transition (None -> STATE_1)
        # 2. Transition (STATE_1 -> STATE_2)
        
        events = []
        while not event_queue.empty():
            events.append(event_queue.get())
            
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0].to_state, "STATE_1")
        self.assertEqual(events[1].from_state, "STATE_1")
        self.assertEqual(events[1].to_state, "STATE_2")
        
        self.assertTrue(start_state.entered)
        self.assertTrue(start_state.exited)

if __name__ == '__main__':
    unittest.main()
