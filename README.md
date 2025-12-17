# State Monitoring System

A modular backend system for monitoring, detecting, and recording state changes in real-time. This system uses parallel processes to separate state detection from state recording, ensuring robust performance and clean architectural separation.

## Features

- **Parallel Processing**: dedicated processes for State Detection (`Detector`) and State Recording (`Recorder`).
- **Shared State**: Efficient state sharing using `multiprocessing.Manager`.
- **Extensible Design**: Easy to plug in custom State Machines and Input Sources.
- **Event Logging**: Automatic logging of all state transitions with timestamps.

## Project Structure

- `core/`: Contains the core logic (`SystemController`, `StateMachineEngine`, `StateRecorder`).
- `examples/`: Example implementations.
  - `order_fulfillment/`: A simulated order processing system.
  - `traffic_signal/`: A traffic light control system example.
  - `tv_receiver/`: A TV state system example.

## Getting Started

### Prerequisites

- Python 3.13 or higher.

### Running Examples

The examples are located in the `examples/` directory. You can run them directly using Python.

#### Order Fulfillment Example

This example simulates an order lifecycle (New -> Payment -> Transit -> Delivered).

**Run the success scenario:**
```bash
python3 examples/order_fulfillment/run.py
```

**Run a specific scenario:**
You can pass a scenario name as an argument (e.g., `payment_failed`, `cancelled`):
```bash
python3 examples/order_fulfillment/run.py payment_failed
```

The output will show the real-time state transitions, and a log file (e.g., `order_success.jsonl`) will be created in the current directory containing the detailed history.
