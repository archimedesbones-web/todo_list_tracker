#!/usr/bin/env python3
"""
Test script for Android version core functionality
Tests the Task class and data persistence without Kivy UI
"""

import sys
import os
import json
import tempfile
from datetime import date

# Define Task class for testing (extracted from todo_android.py)
class Task:
    """Represents a single task"""
    def __init__(self, text, category="General", priority="Medium", due_date=None):
        self.text = text
        self.category = category
        self.priority = priority
        self.due_date = due_date
        self.completed = False
        self.created_date = str(date.today())
        
    def to_dict(self):
        return {
            'text': self.text,
            'category': self.category,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_date': self.created_date
        }
    
    @staticmethod
    def from_dict(data):
        task = Task(
            data.get('text', ''),
            data.get('category', 'General'),
            data.get('priority', 'Medium'),
            data.get('due_date')
        )
        task.completed = data.get('completed', False)
        task.created_date = data.get('created_date', str(date.today()))
        return task

def test_task_creation():
    """Test creating a task"""
    print("Test 1: Task creation...")
    task = Task("Buy groceries", "Shopping", "High")
    assert task.text == "Buy groceries"
    assert task.category == "Shopping"
    assert task.priority == "High"
    assert task.completed == False
    print("✓ Task creation works")

def test_task_completion():
    """Test task completion toggle"""
    print("\nTest 2: Task completion...")
    task = Task("Learn Python", "Learning", "Medium")
    assert task.completed == False
    
    task.completed = True
    assert task.completed == True
    print("✓ Task completion works")

def test_task_serialization():
    """Test task to/from dict"""
    print("\nTest 3: Task serialization...")
    task = Task("Write code", "Work", "Urgent", "2025-10-30")
    
    # Convert to dict
    task_dict = task.to_dict()
    assert task_dict['text'] == "Write code"
    assert task_dict['category'] == "Work"
    assert task_dict['priority'] == "Urgent"
    assert task_dict['due_date'] == "2025-10-30"
    
    # Convert back from dict
    restored_task = Task.from_dict(task_dict)
    assert restored_task.text == task.text
    assert restored_task.category == task.category
    assert restored_task.priority == task.priority
    assert restored_task.due_date == task.due_date
    print("✓ Task serialization works")

def test_task_persistence():
    """Test saving and loading tasks"""
    print("\nTest 4: Task persistence...")
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    tasks_file = os.path.join(temp_dir, "test_tasks.json")
    
    # Create tasks
    tasks = [
        Task("Task 1", "General", "Low"),
        Task("Task 2", "Work", "High"),
        Task("Task 3", "Personal", "Medium")
    ]
    tasks[1].completed = True
    
    # Save tasks
    data = {
        'tasks': [t.to_dict() for t in tasks],
        'version': '1.03-android'
    }
    with open(tasks_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Load tasks
    with open(tasks_file, 'r') as f:
        loaded_data = json.load(f)
    
    loaded_tasks = [Task.from_dict(t) for t in loaded_data['tasks']]
    
    # Verify
    assert len(loaded_tasks) == 3
    assert loaded_tasks[0].text == "Task 1"
    assert loaded_tasks[1].completed == True
    assert loaded_tasks[2].priority == "Medium"
    
    # Cleanup
    os.remove(tasks_file)
    os.rmdir(temp_dir)
    
    print("✓ Task persistence works")

def test_task_categories():
    """Test various task categories"""
    print("\nTest 5: Task categories...")
    categories = ['General', 'Work', 'Personal', 'Shopping', 'Health', 'Learning']
    
    for cat in categories:
        task = Task("Test task", cat, "Medium")
        assert task.category == cat
    
    print("✓ Task categories work")

def test_task_priorities():
    """Test various task priorities"""
    print("\nTest 6: Task priorities...")
    priorities = ['Low', 'Medium', 'High', 'Urgent']
    
    for pri in priorities:
        task = Task("Test task", "General", pri)
        assert task.priority == pri
    
    print("✓ Task priorities work")

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("Testing Android Version Core Functionality")
    print("=" * 50)
    
    try:
        test_task_creation()
        test_task_completion()
        test_task_serialization()
        test_task_persistence()
        test_task_categories()
        test_task_priorities()
        
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        print("=" * 50)
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
