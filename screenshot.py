#!/usr/bin/env python3
"""
Screenshot script to capture the GUI interface for documentation.
"""

import sys
import os
import tkinter as tk
from PIL import Image
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.tkinter_interface import BelbinTestGUI


def capture_welcome_screen():
    """Capture the welcome screen."""
    root = tk.Tk()
    app = BelbinTestGUI(root)
    
    # Wait a moment for rendering
    root.update()
    time.sleep(0.1)
    
    # Capture screenshot
    root.after(500, lambda: capture_and_save(root, "welcome_screen"))
    root.mainloop()


def capture_and_save(root, filename):
    """Capture and save screenshot."""
    try:
        # Get window geometry
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        width = root.winfo_width()
        height = root.winfo_height()
        
        # Use PIL to capture (if available)
        try:
            import PIL.ImageGrab as ImageGrab
            img = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            img.save(f"{filename}.png")
            print(f"Screenshot saved as {filename}.png")
        except ImportError:
            print("PIL not available for screenshots")
        
    except Exception as e:
        print(f"Could not capture screenshot: {e}")
    
    root.quit()


if __name__ == "__main__":
    print("Attempting to capture GUI screenshots...")
    try:
        capture_welcome_screen()
    except Exception as e:
        print(f"Screenshot capture failed: {e}")
        print("This is normal in headless environments.")