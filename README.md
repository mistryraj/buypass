# Mouse Activity Simulator

A Python script for bug testing that simulates mouse activity by moving the mouse pointer in a specific direction and performing left/right clicks continuously.

## Features

- Moves mouse in configurable direction (right, left, up, down, or circular)
- Performs left and right mouse clicks at specified intervals
- Runs infinitely until stopped with Ctrl+C
- Configurable movement speed and click frequency

## Installation

1. Install Python 3.6 or higher
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python mouse_activity.py
```

Press **Ctrl+C** to stop the script.

## Configuration

Edit the configuration variables in `mouse_activity.py`:

- `DIRECTION`: Movement direction ('right', 'left', 'up', 'down', 'circular')
- `MOVE_DISTANCE`: Pixels to move per step (default: 5)
- `CLICK_INTERVAL`: Seconds between clicks (default: 2.0)
- `MOVE_INTERVAL`: Seconds between mouse movements (default: 0.1)

## Example

```python
DIRECTION = 'right'      # Move mouse to the right
MOVE_DISTANCE = 5        # Move 5 pixels per step
CLICK_INTERVAL = 2.0     # Click every 2 seconds
MOVE_INTERVAL = 0.1      # Move every 0.1 seconds
```

## Notes

- The script will move the mouse continuously and perform clicks at the specified interval
- Make sure to position your mouse in a safe area before starting
- Use Ctrl+C to stop the script safely

