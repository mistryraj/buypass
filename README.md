# Mouse Activity Simulator

A Python script with GUI for bug testing that simulates mouse activity by moving the mouse pointer in a specific direction within a selected window and performing left/right clicks continuously.

## Features

- **GUI Interface**: Easy-to-use graphical interface for configuration
- **Window Selection**: Select a specific window to constrain mouse movement within
- **Direction Control**: Move mouse in configurable direction (right, left, up, down, or circular)
- **Automatic Clicks**: Performs left and right mouse clicks at specified intervals
- **Boundary Detection**: Automatically reverses direction when hitting window boundaries
- **Real-time Status**: Shows current status and activity in the GUI
- **Infinite Operation**: Runs continuously until stopped via GUI button

## Installation

1. Install Python 3.6 or higher
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script to launch the GUI:
```bash
python mouse_activity.py
```

### Using the GUI:

1. **Select Target Window**: 
   - Choose a window from the dropdown list
   - Click "Refresh" to update the window list
   - Select "No window selected" to move freely across the screen

2. **Configure Settings**:
   - **Direction**: Choose movement direction (right, left, up, down, circular)
   - **Move Distance**: Pixels to move per step (default: 5)
   - **Click Interval**: Seconds between clicks (default: 2.0)
   - **Move Interval**: Seconds between mouse movements (default: 0.1)

3. **Start/Stop**:
   - Click "Start" to begin mouse activity
   - Click "Stop" to halt the simulation
   - Status updates are shown in real-time

## Configuration Options

### Direction Options:
- **right**: Moves mouse to the right
- **left**: Moves mouse to the left
- **up**: Moves mouse upward
- **down**: Moves mouse downward
- **circular**: Moves mouse in a circular pattern

### Settings:
- **Move Distance**: Number of pixels to move per step (recommended: 1-10)
- **Click Interval**: Time in seconds between click sequences (recommended: 1.0-5.0)
- **Move Interval**: Time in seconds between movements (recommended: 0.05-0.5)

## Window Constraint

When a window is selected:
- Mouse movement is constrained to the selected window's boundaries
- The mouse automatically reverses direction when hitting window edges
- Window boundaries are updated periodically to handle window movement
- A 10-pixel padding is maintained from window edges

## Notes

- The target window must be visible and not minimized for proper operation
- If the selected window is closed, the script will continue but may behave unexpectedly
- Use the "Refresh" button to update the window list after opening/closing applications
- The script runs in a separate thread, so the GUI remains responsive
- Make sure the target window is in focus or visible for best results

## Troubleshooting

- **Window not appearing in list**: Click "Refresh" to update the window list
- **Mouse not moving**: Ensure the target window is visible and not minimized
- **Import errors**: Make sure all dependencies are installed: `pip install -r requirements.txt`
