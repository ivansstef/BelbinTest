# BelbinTest

Belbin Team Roles Test - a comprehensive application for assessing team role preferences using the Belbin methodology.

## Features

- **Interactive GUI**: Easy-to-use Tkinter interface for taking the test
- **Comprehensive Test**: Implements the official Belbin team roles assessment
- **Data Persistence**: SQLite database to store test results
- **Visualization**: Matplotlib pie charts to visualize results
- **Multi-user Support**: Support for multiple users taking the test

## Team Roles

The test identifies preferences for 9 team roles:

1. **Plant (Creative)** - Creative, imaginative, free-thinking
2. **Resource Investigator** - Outgoing, enthusiastic, explores opportunities
3. **Coordinator** - Mature, confident, clarifies goals and delegates
4. **Shaper** - Challenging, dynamic, thrives on pressure
5. **Monitor Evaluator** - Sober, strategic, sees all options
6. **Teamworker** - Co-operative, mild, perceptive, diplomatic
7. **Implementer** - Disciplined, reliable, turns ideas into actions
8. **Completer Finisher** - Painstaking, conscientious, searches out errors
9. **Specialist** - Single-minded, self-starting, dedicated

## Installation

### Prerequisites

- Python 3.6 or higher
- tkinter (usually included with Python)
- matplotlib

### Install Dependencies

On Ubuntu/Debian:
```bash
sudo apt install python3-tk python3-matplotlib
```

On other systems:
```bash
pip install matplotlib
```

## Usage

### Running the Application

```bash
python main.py
```

### Taking the Test

1. Enter your name on the welcome screen
2. Answer the test questions by distributing 10 points among the given options
3. Navigate through questions using the Previous/Next buttons
4. View your results with detailed scores and visualization

### Test Instructions

For each question:
- Read the scenario carefully
- Distribute exactly 10 points among the response options
- Give more points to responses that best describe you
- Use the navigation buttons to move between questions

## Project Structure

```
BelbinTest/
├── main.py                    # Main application entry point
├── gui/
│   ├── __init__.py
│   └── tkinter_interface.py   # GUI implementation
├── utils/
│   ├── __init__.py
│   └── data_processing.py     # Test logic and database operations
├── data/
│   └── results.db            # SQLite database (created automatically)
├── tests/
│   ├── __init__.py
│   ├── test_belbin.py        # Unit tests for core functionality
│   ├── test_gui.py           # GUI tests
│   └── test_main.py          # Main application tests
└── README.md
```

## Testing

Run the unit tests:

```bash
# Run all tests
python -m unittest discover tests/ -v

# Run specific test modules
python -m unittest tests.test_belbin -v
python -m unittest tests.test_gui -v
```

For GUI testing in headless environments:
```bash
DISPLAY=:99 xvfb-run -a python -m unittest tests.test_gui -v
```

## Database Schema

The application uses SQLite to store test results:

```sql
CREATE TABLE test_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    pl_score INTEGER DEFAULT 0,     -- Plant
    ri_score INTEGER DEFAULT 0,     -- Resource Investigator
    co_score INTEGER DEFAULT 0,     -- Coordinator
    sh_score INTEGER DEFAULT 0,     -- Shaper
    me_score INTEGER DEFAULT 0,     -- Monitor Evaluator
    tw_score INTEGER DEFAULT 0,     -- Teamworker
    imp_score INTEGER DEFAULT 0,    -- Implementer
    cf_score INTEGER DEFAULT 0,     -- Completer Finisher
    sp_score INTEGER DEFAULT 0      -- Specialist
);
```

## Development

### Architecture

- **main.py**: Application entry point
- **gui/tkinter_interface.py**: Complete GUI implementation with welcome screen, test questions, and results visualization
- **utils/data_processing.py**: Core test logic, scoring algorithms, and database operations

### Key Classes

- `BelbinTest`: Handles test questions, scoring logic, and role calculations
- `DatabaseManager`: Manages SQLite database operations
- `BelbinTestGUI`: Main GUI application class

## License

This project is for educational purposes.