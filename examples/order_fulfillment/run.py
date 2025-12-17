import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from state_monitoring_system.core.controller import SystemController
from state_monitoring_system.examples.order_fulfillment.states import NewOrder
from state_monitoring_system.examples.order_fulfillment.input import OrderEventSimulator

def main():
    scenario = "success"
    if len(sys.argv) > 1:
        scenario = sys.argv[1]
        
    print(f"Running scenario: {scenario}")
    
    start_state = NewOrder()
    input_source = OrderEventSimulator(scenario=scenario)
    
    controller = SystemController(start_state, input_source, log_file=f"order_{scenario}.jsonl")
    
    controller.start()
    
    try:
        while controller.is_running():
            status = controller.get_current_state()
            print(f"[Order Status] {status.get('current_state')}")
            time.sleep(0.5)
            
            # Simple check to stop monitoring if terminal state mostly reached (hack for demo)
            cs = status.get('current_state')
            if cs in ["DELIVERED", "CANCELLED"]:
                print("Terminal state reached.")
                break
                
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()

if __name__ == "__main__":
    main()
