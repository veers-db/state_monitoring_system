from typing import Any, Optional
from ...core.fsm import State

# --- Base ---
class OrderState(State):
    pass

# --- States ---
class NewOrder(OrderState):
    @property
    def name(self) -> str:
        return "NEW_ORDER"
    
    def handle_input(self, input_data: Any) -> Optional['State']:
        if input_data == "PROCESS_PAYMENT":
            return PaymentProcessing()
        return None

class PaymentProcessing(OrderState):
    @property
    def name(self) -> str:
        return "PAYMENT_PROCESSING"
    
    def handle_input(self, input_data: Any) -> Optional['State']:
        # Branching logic
        if input_data == "PAYMENT_APPROVED":
            return PaymentApproved()
        elif input_data == "PAYMENT_FAILED":
            return PaymentFailed()
        return None

class PaymentApproved(OrderState):
    @property
    def name(self) -> str:
        return "PAYMENT_APPROVED"

    def handle_input(self, input_data: Any) -> Optional['State']:
        if input_data == "SHIP":
            return InTransit()
        return None

class PaymentFailed(OrderState):
    @property
    def name(self) -> str:
        return "PAYMENT_FAILED"

    def handle_input(self, input_data: Any) -> Optional['State']:
        if input_data == "CANCEL":
            return Cancelled()
        elif input_data == "RETRY":
            return PaymentProcessing()
        return None

class InTransit(OrderState):
    @property
    def name(self) -> str:
        return "IN_TRANSIT"
    
    def handle_input(self, input_data: Any) -> Optional['State']:
        if input_data == "DELIVER":
            return Delivered()
        return None

class Delivered(OrderState):
    @property
    def name(self) -> str:
        return "DELIVERED"
    
    def handle_input(self, input_data: Any) -> Optional['State']:
        return None # Terminal state

class Cancelled(OrderState):
    @property
    def name(self) -> str:
        return "CANCELLED"
    
    def handle_input(self, input_data: Any) -> Optional['State']:
        return None # Terminal state
