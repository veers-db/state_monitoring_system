import unittest
import multiprocessing
import tempfile
import time
import os
import json
from ..core.recorder import StateRecorder
from ..core.fsm import TransitionEvent

class TestRecorder(unittest.TestCase):
    def test_recorder_logging(self):
        event_queue = multiprocessing.Queue()
        manager = multiprocessing.Manager()
        shared_state = manager.dict()
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_file:
            log_path = tmp_file.name
            
        recorder = StateRecorder(event_queue, shared_state, log_path)
        
        # Start recorder in a separate process or thread? 
        # Since run() is a loop, we can just run it in a thread or process.
        # But for unit testing, we might just queue items and STOP, then run synchronously.
        
        event1 = TransitionEvent(time.time(), "A", "B", {})
        event_queue.put(event1)
        event_queue.put("STOP")
        
        recorder.run()
        
        # Check Shared State
        self.assertEqual(shared_state['current_state'], "B")
        self.assertEqual(shared_state['history_count'], 1)
        
        # Check File
        with open(log_path, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            data = json.loads(lines[0])
            self.assertEqual(data['to_state'], "B")
            
        os.unlink(log_path)

if __name__ == '__main__':
    unittest.main()
