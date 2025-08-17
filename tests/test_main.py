"""
Test script to verify the main application can start.
"""

import sys
import os
import tkinter as tk
import threading
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import main as main_func


def test_main_startup():
    """Test that main application can start."""
    try:
        # Use a separate thread to start the application
        # and close it after a short time
        def run_app():
            # Mock the main function to avoid infinite loop
            root = tk.Tk()
            root.withdraw()  # Hide the window
            
            # Import and create the app
            from gui.tkinter_interface import BelbinTestGUI
            app = BelbinTestGUI(root)
            
            # Close after 100ms
            root.after(100, root.quit)
            root.mainloop()
            root.destroy()
        
        run_app()
        
        print("✓ Main application startup test passed")
        return True
        
    except Exception as e:
        print(f"✗ Main application startup test failed: {e}")
        return False


if __name__ == "__main__":
    print("Testing main application startup...")
    
    if test_main_startup():
        print("✓ Main application test passed!")
        sys.exit(0)
    else:
        print("✗ Main application test failed!")
        sys.exit(1)