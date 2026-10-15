## Hotel Room Booking Example

This example simulates a hotel room booking lifecycle supporting standard stays, check-ins and cancellations.

(Available &rarr; Reserve &rarr; Check in &rarr; Check out).


## Running the Interactive System

You can run the interactive front-desk manager directly from your terminal:

```bash
python3 examples/hotel_room_booking/run.py

```

---

## User flow

1. **Real-Time Menu:** At every step, the system displays the current room status and prompts you with a clean menu:
* `1. Reserve (RESERVE)`
* `2. Check-in (CHECK_IN)`
* `3. Check-out (CHECK_OUT)`
* `4. Cancel (CANCEL)`


2. **State-Aware Validation:** If you attempt an illegal action (e.g., trying to check out directly without checking in), the system instantly rejects the action with a clear warning and prompts you again.

3. **Audit Logging:** Every state transition is recorded in real-time, creating a session log file (e.g., `hotel_booking_interactive.jsonl`) in your working directory.
