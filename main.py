#!/usr/bin/env python3
"""
Main entry point for the Belbin Test application.

This application implements a complete Belbin Team Roles test with:
- Tkinter GUI for user interaction
- SQLite database for storing results
- Matplotlib visualization of results
"""

import tkinter as tk
import sys
import os

# Add current directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.tkinter_interface import BelbinTestGUI


def main():
    """Main function to start the Belbin Test application."""
    try:
        # Create main window
        root = tk.Tk()
        
        # Create and start the application
        app = BelbinTestGUI(root)
        
        # Start the main loop
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()