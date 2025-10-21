# Todo List Tracker

A simple and customizable todo list application built with Python and Tkinter.

## Features

- Add, edit, and remove tasks
- Mark tasks as complete/incomplete
- Multiple color themes
- Automatic theme and task saving
- Import/Export tasks as JSON

## Installation

1. Make sure you have Python 3.x installed
2. No additional packages required (uses built-in tkinter)

## Usage

Run the program:
```bash
python todo_list_tracker.py
```

## File Structure

```
todo_list_tracker/
│
├── todo_list_tracker.py    # Main application file
│
├── data/                   # Data directory
│   └── tasks.json         # Saved tasks and theme preferences
│
├── README.md              # Documentation
└── requirements.txt       # Project dependencies
```

## Data Storage

- Tasks and theme preferences are automatically saved to `data/tasks.json`
- The data directory is created automatically if it doesn't exist
- You can manually save/load tasks to/from different locations using the Save/Load buttons

## Themes

Available themes:
- Light
- Dark
- Monokai
- Solarized Light
- Solarized Dark
- Nord
- GitHub Light
- GitHub Dark

Theme preferences are automatically saved when you close the application.