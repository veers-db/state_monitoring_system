## Hotel Room Booking Example

This example simulates a hotel room booking lifecycle supporting standard stays, check-ins and cancellations.

(Available -> Reserve -> Check in -> Completed).


**Run the standard scenario:**
```bash
python3 examples/hotel_room_booking/run.py
```

**Run a specific scenario:**

You can pass a scenario name as an argument (e.g., `cancelled`, `check_in`):
```bash
python3 examples/hotel_room_booking/run.py cancelled
```

The output will show the real-time state transitions, and a log file (e.g., `hotel_booking_standard.jsonl`) will be created in the current directory containing the detailed history.