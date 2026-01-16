"""
Mouse Activity Simulator for Bug Testing
Moves mouse in a specific direction and performs left/right clicks continuously
Press Ctrl+C to stop the script
"""

import time
import sys
from pynput.mouse import Controller, Button
from pynput import mouse
import threading

class MouseActivitySimulator:
    def __init__(self, direction='right', move_distance=5, click_interval=2.0, move_interval=0.1):
        """
        Initialize the mouse activity simulator
        
        Args:
            direction: Direction to move mouse ('right', 'left', 'up', 'down', 'circular')
            move_distance: Pixels to move per step
            click_interval: Seconds between clicks
            move_interval: Seconds between mouse movements
        """
        self.mouse = Controller()
        self.direction = direction.lower()
        self.move_distance = move_distance
        self.click_interval = click_interval
        self.move_interval = move_interval
        self.running = False
        self.start_position = None
        
    def get_direction_vector(self):
        """Get the movement vector based on direction"""
        vectors = {
            'right': (self.move_distance, 0),
            'left': (-self.move_distance, 0),
            'up': (0, -self.move_distance),
            'down': (0, self.move_distance),
            'circular': self._get_circular_vector()
        }
        return vectors.get(self.direction, (self.move_distance, 0))
    
    def _get_circular_vector(self):
        """Calculate circular movement vector"""
        if not hasattr(self, '_angle'):
            self._angle = 0
        import math
        radius = 50
        x = int(radius * math.cos(math.radians(self._angle)))
        y = int(radius * math.sin(math.radians(self._angle)))
        self._angle = (self._angle + 10) % 360
        return (x, y)
    
    def move_mouse(self):
        """Move mouse in the specified direction"""
        try:
            current_pos = self.mouse.position
            dx, dy = self.get_direction_vector()
            
            # Calculate new position
            new_x = current_pos[0] + dx
            new_y = current_pos[1] + dy
            
            # Move mouse
            self.mouse.position = (new_x, new_y)
        except Exception as e:
            print(f"Error moving mouse: {e}")
    
    def perform_clicks(self):
        """Perform left and right mouse clicks"""
        try:
            # Left click
            self.mouse.click(Button.left)
            time.sleep(0.1)
            # Right click
            self.mouse.click(Button.right)
        except Exception as e:
            print(f"Error performing clicks: {e}")
    
    def run(self):
        """Main loop - runs until interrupted"""
        print(f"Starting mouse activity simulator...")
        print(f"Direction: {self.direction}")
        print(f"Move distance: {self.move_distance} pixels")
        print(f"Click interval: {self.click_interval} seconds")
        print(f"Move interval: {self.move_interval} seconds")
        print(f"Press Ctrl+C to stop\n")
        
        self.running = True
        self.start_position = self.mouse.position
        last_click_time = 0
        
        try:
            while self.running:
                current_time = time.time()
                
                # Move mouse continuously
                self.move_mouse()
                
                # Perform clicks at specified interval
                if current_time - last_click_time >= self.click_interval:
                    self.perform_clicks()
                    last_click_time = current_time
                
                time.sleep(self.move_interval)
                
        except KeyboardInterrupt:
            print("\n\nStopping mouse activity simulator...")
            self.running = False
            print("Script stopped successfully.")
        except Exception as e:
            print(f"\nError: {e}")
            self.running = False

def main():
    """Main function with configurable parameters"""
    # Configuration - adjust these values as needed
    DIRECTION = 'right'      # Options: 'right', 'left', 'up', 'down', 'circular'
    MOVE_DISTANCE = 5        # Pixels to move per step
    CLICK_INTERVAL = 2.0     # Seconds between clicks (2 seconds default)
    MOVE_INTERVAL = 0.1      # Seconds between mouse movements (0.1 seconds = 10 moves/sec)
    
    # Create and run simulator
    simulator = MouseActivitySimulator(
        direction=DIRECTION,
        move_distance=MOVE_DISTANCE,
        click_interval=CLICK_INTERVAL,
        move_interval=MOVE_INTERVAL
    )
    
    simulator.run()

if __name__ == "__main__":
    main()

