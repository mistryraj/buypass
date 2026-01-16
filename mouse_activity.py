"""
Mouse Activity Simulator for Bug Testing with GUI
Moves mouse in a specific direction within a selected window and performs left/right clicks continuously
"""

import time
import sys
import threading
import math
from pynput.mouse import Controller, Button
import tkinter as tk
from tkinter import ttk, messagebox
try:
    import pygetwindow as gw
    WINDOW_DETECTION_AVAILABLE = True
except ImportError:
    WINDOW_DETECTION_AVAILABLE = False
    print("Warning: pygetwindow not installed. Window detection disabled.")


class MouseActivitySimulator:
    def __init__(self, direction='right', move_distance=5, click_interval=2.0, move_interval=0.1, target_window=None):
        """
        Initialize the mouse activity simulator
        
        Args:
            direction: Direction to move mouse ('right', 'left', 'up', 'down', 'circular')
            move_distance: Pixels to move per step
            click_interval: Seconds between clicks
            move_interval: Seconds between mouse movements
            target_window: Window object to constrain mouse to (None for no constraint)
        """
        self.mouse = Controller()
        self.direction = direction.lower()
        self.move_distance = move_distance
        self.click_interval = click_interval
        self.move_interval = move_interval
        self.running = False
        self.start_position = None
        self.target_window = target_window
        self.window_bounds = None
        self.current_pos_in_window = None
        
        if target_window:
            self._update_window_bounds()
        
    def _update_window_bounds(self):
        """Update the window boundaries"""
        if self.target_window:
            try:
                # Get window position and size
                left = self.target_window.left
                top = self.target_window.top
                width = self.target_window.width
                height = self.target_window.height
                
                # Set bounds with some padding to stay within window
                padding = 10
                self.window_bounds = {
                    'left': left + padding,
                    'right': left + width - padding,
                    'top': top + padding,
                    'bottom': top + height - padding,
                    'width': width - (padding * 2),
                    'height': height - (padding * 2)
                }
                
                # Initialize position to center of window if not set
                if self.current_pos_in_window is None:
                    self.current_pos_in_window = {
                        'x': self.window_bounds['left'] + self.window_bounds['width'] // 2,
                        'y': self.window_bounds['top'] + self.window_bounds['height'] // 2
                    }
            except Exception as e:
                print(f"Error updating window bounds: {e}")
                self.window_bounds = None
    
    def _clamp_to_bounds(self, x, y):
        """Clamp coordinates to window bounds"""
        if not self.window_bounds:
            return x, y
        
        x = max(self.window_bounds['left'], min(x, self.window_bounds['right']))
        y = max(self.window_bounds['top'], min(y, self.window_bounds['bottom']))
        return x, y
    
    def _reverse_direction_if_at_boundary(self, dx, dy):
        """Reverse direction if at window boundary"""
        if not self.window_bounds or not self.current_pos_in_window:
            return dx, dy
        
        x = self.current_pos_in_window['x']
        y = self.current_pos_in_window['y']
        
        # Check boundaries and reverse if needed
        if x + dx > self.window_bounds['right'] or x + dx < self.window_bounds['left']:
            dx = -dx
        if y + dy > self.window_bounds['bottom'] or y + dy < self.window_bounds['top']:
            dy = -dy
        
        return dx, dy
        
    def get_direction_vector(self):
        """Get the movement vector based on direction"""
        vectors = {
            'right': (self.move_distance, 0),
            'left': (-self.move_distance, 0),
            'up': (0, -self.move_distance),
            'down': (0, self.move_distance),
            'circular': self._get_circular_vector()
        }
        base_dx, base_dy = vectors.get(self.direction, (self.move_distance, 0))
        
        # Adjust for window boundaries
        if self.window_bounds:
            base_dx, base_dy = self._reverse_direction_if_at_boundary(base_dx, base_dy)
        
        return base_dx, base_dy
    
    def _get_circular_vector(self):
        """Calculate circular movement vector"""
        if not hasattr(self, '_angle'):
            self._angle = 0
        radius = min(50, self.window_bounds['width'] // 4 if self.window_bounds else 50)
        x = int(radius * math.cos(math.radians(self._angle)))
        y = int(radius * math.sin(math.radians(self._angle)))
        self._angle = (self._angle + 10) % 360
        return (x, y)
    
    def move_mouse(self):
        """Move mouse in the specified direction, constrained to window if specified"""
        try:
            if self.window_bounds and self.current_pos_in_window:
                # Use relative position within window
                dx, dy = self.get_direction_vector()
                
                new_x = self.current_pos_in_window['x'] + dx
                new_y = self.current_pos_in_window['y'] + dy
                
                # Clamp to bounds
                new_x, new_y = self._clamp_to_bounds(new_x, new_y)
                
                # Update position
                self.current_pos_in_window['x'] = new_x
                self.current_pos_in_window['y'] = new_y
                
                # Move mouse to absolute position
                self.mouse.position = (new_x, new_y)
            else:
                # No window constraint - move freely
                current_pos = self.mouse.position
                dx, dy = self.get_direction_vector()
                
                new_x = current_pos[0] + dx
                new_y = current_pos[1] + dy
                
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
    
    def run(self, status_callback=None):
        """Main loop - runs until stopped"""
        self.running = True
        self.start_position = self.mouse.position
        last_click_time = 0
        
        # Initialize position in window if needed
        if self.window_bounds and self.current_pos_in_window is None:
            self.current_pos_in_window = {
                'x': self.window_bounds['left'] + self.window_bounds['width'] // 2,
                'y': self.window_bounds['top'] + self.window_bounds['height'] // 2
            }
            self.mouse.position = (self.current_pos_in_window['x'], self.current_pos_in_window['y'])
        
        try:
            while self.running:
                current_time = time.time()
                
                # Update window bounds periodically (in case window moves)
                if self.target_window and current_time % 1.0 < self.move_interval:
                    self._update_window_bounds()
                
                # Move mouse continuously
                self.move_mouse()
                
                # Perform clicks at specified interval
                if current_time - last_click_time >= self.click_interval:
                    self.perform_clicks()
                    last_click_time = current_time
                
                if status_callback:
                    status_callback(f"Running... Clicks: {int((current_time - last_click_time) * 10) / 10:.1f}s")
                
                time.sleep(self.move_interval)
                
        except Exception as e:
            if status_callback:
                status_callback(f"Error: {e}")
            print(f"Error: {e}")
            self.running = False
    
    def stop(self):
        """Stop the simulator"""
        self.running = False


class MouseActivityGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Activity Simulator")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        self.simulator = None
        self.simulator_thread = None
        self.target_window = None
        
        self.create_widgets()
        self.refresh_windows()
        
    def create_widgets(self):
        """Create GUI widgets"""
        # Title
        title_label = tk.Label(self.root, text="Mouse Activity Simulator", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Window Selection Frame
        window_frame = ttk.LabelFrame(self.root, text="Target Window", padding=10)
        window_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        self.window_var = tk.StringVar()
        self.window_combo = ttk.Combobox(window_frame, textvariable=self.window_var, 
                                        width=50, state="readonly")
        self.window_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        refresh_btn = tk.Button(window_frame, text="Refresh", command=self.refresh_windows)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="Settings", padding=10)
        settings_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        # Direction
        tk.Label(settings_frame, text="Direction:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.direction_var = tk.StringVar(value="right")
        direction_combo = ttk.Combobox(settings_frame, textvariable=self.direction_var,
                                       values=["right", "left", "up", "down", "circular"],
                                       state="readonly", width=15)
        direction_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Move Distance
        tk.Label(settings_frame, text="Move Distance (px):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.move_distance_var = tk.StringVar(value="5")
        move_distance_entry = tk.Entry(settings_frame, textvariable=self.move_distance_var, width=15)
        move_distance_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Click Interval
        tk.Label(settings_frame, text="Click Interval (sec):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.click_interval_var = tk.StringVar(value="2.0")
        click_interval_entry = tk.Entry(settings_frame, textvariable=self.click_interval_var, width=15)
        click_interval_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Move Interval
        tk.Label(settings_frame, text="Move Interval (sec):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.move_interval_var = tk.StringVar(value="0.1")
        move_interval_entry = tk.Entry(settings_frame, textvariable=self.move_interval_var, width=15)
        move_interval_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Control Buttons Frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.start_btn = tk.Button(control_frame, text="Start", command=self.start_simulator,
                                   bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                                   width=15, height=2)
        self.start_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        self.stop_btn = tk.Button(control_frame, text="Stop", command=self.stop_simulator,
                                  bg="#f44336", fg="white", font=("Arial", 12, "bold"),
                                  width=15, height=2, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        # Status Frame
        status_frame = ttk.LabelFrame(self.root, text="Status", padding=10)
        status_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        
        self.status_label = tk.Label(status_frame, text="Ready. Select a window and click Start.",
                                     font=("Arial", 10), wraplength=450, justify=tk.LEFT)
        self.status_label.pack(fill=tk.BOTH, expand=True)
        
        # Info Label
        info_label = tk.Label(self.root, 
                             text="Note: Mouse will move within the selected window only.\n"
                                  "Make sure the target window is visible and not minimized.",
                             font=("Arial", 8), fg="gray", justify=tk.CENTER)
        info_label.pack(pady=5)
        
    def refresh_windows(self):
        """Refresh the list of available windows"""
        if not WINDOW_DETECTION_AVAILABLE:
            self.window_combo['values'] = ["Window detection not available"]
            self.status_label.config(text="Warning: pygetwindow not installed. Install it to use window detection.")
            return
        
        try:
            windows = gw.getAllWindows()
            window_titles = [f"{w.title} ({w.width}x{w.height})" for w in windows if w.title.strip()]
            window_titles.insert(0, "No window selected (move freely)")
            self.window_combo['values'] = window_titles
            if not self.window_var.get():
                self.window_var.set(window_titles[0])
            self.status_label.config(text=f"Found {len(windows)} windows. Select one to constrain mouse movement.")
        except Exception as e:
            self.status_label.config(text=f"Error refreshing windows: {e}")
    
    def get_selected_window(self):
        """Get the selected window object"""
        if not WINDOW_DETECTION_AVAILABLE:
            return None
        
        selected = self.window_var.get()
        if not selected or selected == "No window selected (move freely)":
            return None
        
        try:
            # Extract window title (before the size info)
            title = selected.split(" (")[0]
            windows = gw.getWindowsWithTitle(title)
            if windows:
                return windows[0]
        except Exception as e:
            print(f"Error getting window: {e}")
        return None
    
    def start_simulator(self):
        """Start the mouse activity simulator"""
        try:
            # Get settings
            direction = self.direction_var.get()
            move_distance = int(self.move_distance_var.get())
            click_interval = float(self.click_interval_var.get())
            move_interval = float(self.move_interval_var.get())
            
            # Get target window
            self.target_window = self.get_selected_window()
            
            # Create simulator
            self.simulator = MouseActivitySimulator(
                direction=direction,
                move_distance=move_distance,
                click_interval=click_interval,
                move_interval=move_interval,
                target_window=self.target_window
            )
            
            # Update UI
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            window_name = self.target_window.title if self.target_window else "No window (free movement)"
            self.status_label.config(text=f"Starting... Target: {window_name}")
            
            # Start simulator in separate thread
            self.simulator_thread = threading.Thread(target=self.run_simulator, daemon=True)
            self.simulator_thread.start()
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please check your input values:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start simulator:\n{e}")
    
    def run_simulator(self):
        """Run simulator in thread"""
        def update_status(text):
            self.status_label.config(text=text)
        
        self.simulator.run(status_callback=update_status)
        
        # Update UI when stopped
        self.root.after(0, self.on_simulator_stopped)
    
    def on_simulator_stopped(self):
        """Called when simulator stops"""
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Stopped. Ready to start again.")
    
    def stop_simulator(self):
        """Stop the mouse activity simulator"""
        if self.simulator:
            self.simulator.stop()
            self.status_label.config(text="Stopping...")


def main():
    """Main function - launch GUI"""
    root = tk.Tk()
    app = MouseActivityGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
