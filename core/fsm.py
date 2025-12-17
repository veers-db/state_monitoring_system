import abc
import time
import multiprocessing
from typing import Optional, Any
from dataclasses import dataclass

@dataclass
class TransitionEvent:
    timestamp: float
    from_state: str
    to_state: str
    metadata: dict

class State(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Unique name of the state."""
        pass

    def on_enter(self, context: dict) -> None:
        """Called when entering the state."""
        pass

    def on_exit(self, context: dict) -> None:
        """Called when exiting the state."""
        pass

    @abc.abstractmethod
    def handle_input(self, input_data: Any) -> Optional['State']:
        """
        Process input and decide if a transition is needed.
        Returns:
            - The new State instance if transition occurs.
            - None if we stay in the current state.
        """
        pass

class InputSource(abc.ABC):
    @abc.abstractmethod
    def get_input(self) -> Any:
        """Blocking or non-blocking method to fetch next input."""
        pass

class StateMachineEngine:
    def __init__(self, start_state: State, input_source: InputSource, event_queue: multiprocessing.Queue):
        self.current_state = start_state
        self.input_source = input_source
        self.event_queue = event_queue
        self.running = True

    def run(self):
        """Main loop of the State Machine Process."""
        context = {}
        self.current_state.on_enter(context)
        
        # Initial state recording
        self._record_transition(None, self.current_state)

        while self.running:
            input_data = self.input_source.get_input()
            if input_data is None:
                # End of input stream or signal to stop
                break
                
            next_state = self.current_state.handle_input(input_data)
            
            if next_state is not None and next_state.name != self.current_state.name:
                self.current_state.on_exit(context)
                self._record_transition(self.current_state, next_state)
                self.current_state = next_state
                self.current_state.on_enter(context)
                
    def _record_transition(self, from_state: Optional[State], to_state: State):
        event = TransitionEvent(
            timestamp=time.time(),
            from_state=from_state.name if from_state else "START",
            to_state=to_state.name,
            metadata={}
        )
        self.event_queue.put(event)

    def stop(self):
        self.running = False
