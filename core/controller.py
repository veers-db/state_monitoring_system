import multiprocessing
import time
import os
from typing import Type, Any, Dict
from state_monitoring_system.core.fsm import State, InputSource, StateMachineEngine
from state_monitoring_system.core.recorder import StateRecorder

def detector_target(start_node, source, q):
    engine = StateMachineEngine(start_node, source, q)
    engine.run()

def recorder_target(q, shared, log_path):
    recorder = StateRecorder(q, shared, log_path)
    recorder.run()

class SystemController:
    def __init__(self, start_state: State, input_source: InputSource, log_file: str = "state_log.jsonl"):
        self.start_state = start_state
        self.input_source = input_source
        self.log_file = log_file
        
        self.manager = multiprocessing.Manager()
        self.shared_state = self.manager.dict()
        self.event_queue = multiprocessing.Queue()
        
        self.detector_process = None
        self.recorder_process = None

    def start(self):
        """Starts the Detector and Recorder processes."""
        if self.is_running():
            print("System is already running.")
            return

        # Initialize shared state
        self.shared_state.update({
            'current_state': "INITIALIZING",
            'last_updated': time.time(),
            'history_count': 0
        })

        # Define targets are now at module level

        # Start Processes
        self.recorder_process = multiprocessing.Process(
            target=recorder_target, 
            args=(self.event_queue, self.shared_state, self.log_file)
        )
        self.recorder_process.start()
        
        self.detector_process = multiprocessing.Process(
            target=detector_target, 
            args=(self.start_state, self.input_source, self.event_queue)
        )
        self.detector_process.start()
        
        print(f"System started. PID Recorder: {self.recorder_process.pid}, PID Detector: {self.detector_process.pid}")

    def stop(self):
        """Stops the processes safely."""
        if not self.is_running():
            return

        # Stop Detector simply by Terminating (or we could have a value in shared mem to signal stop)
        # For this example, we assume terminating the Process is acceptable or InputSource stops yielding.
        if self.detector_process.is_alive():
            self.detector_process.terminate()
            self.detector_process.join()

        # Send STOP to recorder to let it finish writing
        self.event_queue.put("STOP")
        if self.recorder_process.is_alive():
            self.recorder_process.join()

        self.detector_process = None
        self.recorder_process = None
        print("System stopped.")

    def get_current_state(self) -> Dict[str, Any]:
        """Returns the real-time state from shared memory."""
        return dict(self.shared_state)

    def is_running(self) -> bool:
        return (self.detector_process is not None and self.detector_process.is_alive()) or \
               (self.recorder_process is not None and self.recorder_process.is_alive())
