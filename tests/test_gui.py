"""
Test script to verify the GUI application can be initialized.
This test runs without displaying the GUI for CI environments.
"""

import sys
import os
import tkinter as tk

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from gui.tkinter_interface import BelbinTestGUI


def test_gui_initialization():
    """Test that the GUI can be initialized without errors."""
    try:
        # Create root window (but don't show it)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Create the application
        app = BelbinTestGUI(root)
        
        # Test that basic components are created
        assert hasattr(app, 'belbin_test')
        assert hasattr(app, 'db_manager')
        assert hasattr(app, 'username')
        assert hasattr(app, 'current_question')
        assert hasattr(app, 'answers')
        
        # Test initial state
        assert app.username == ""
        assert app.current_question == 0
        assert app.answers == {}
        assert app.test_completed == False
        
        # Destroy the window
        root.destroy()
        
        print("✓ GUI initialization test passed")
        return True
        
    except Exception as e:
        print(f"✗ GUI initialization test failed: {e}")
        return False


def test_question_data():
    """Test that question data is properly loaded."""
    try:
        root = tk.Tk()
        root.withdraw()
        
        app = BelbinTestGUI(root)
        
        # Test that questions are available
        questions = app.belbin_test.QUESTIONS
        assert len(questions) > 0
        
        # Test question structure
        for question in questions:
            assert 'question' in question
            assert 'options' in question
            assert len(question['options']) > 0
        
        root.destroy()
        
        print("✓ Question data test passed")
        return True
        
    except Exception as e:
        print(f"✗ Question data test failed: {e}")
        return False


def test_database_integration():
    """Test that database integration works."""
    try:
        root = tk.Tk()
        root.withdraw()
        
        app = BelbinTestGUI(root)
        
        # Test saving sample results
        sample_scores = {
            'PL': 10, 'RI': 8, 'CO': 6, 'SH': 4, 'ME': 2,
            'TW': 1, 'IMP': 1, 'CF': 1, 'SP': 0
        }
        
        result_id = app.db_manager.save_results("test_user_gui", sample_scores)
        assert result_id > 0
        
        # Test retrieving results
        results = app.db_manager.get_user_results("test_user_gui")
        assert len(results) == 1
        assert results[0]['username'] == "test_user_gui"
        
        root.destroy()
        
        print("✓ Database integration test passed")
        return True
        
    except Exception as e:
        print(f"✗ Database integration test failed: {e}")
        return False


if __name__ == "__main__":
    print("Running GUI tests...")
    
    all_passed = True
    all_passed &= test_gui_initialization()
    all_passed &= test_question_data()
    all_passed &= test_database_integration()
    
    if all_passed:
        print("\n✓ All GUI tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some GUI tests failed!")
        sys.exit(1)