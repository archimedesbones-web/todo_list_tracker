"""
Todo List Tracker - Android Version
A simplified mobile version using Kivy framework
"""

__version__ = "1.03-android"

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.metrics import dp
import json
import os
from datetime import date, datetime


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


class TaskWidget(BoxLayout):
    """Widget to display a single task"""
    def __init__(self, task, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = dp(5)
        self.spacing = dp(5)
        self.task = task
        self.app_instance = app_instance
        
        # Task info layout
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
        
        # Task text
        task_label = Label(
            text=task.text,
            font_size='16sp',
            halign='left',
            valign='middle',
            text_size=(None, None)
        )
        task_label.bind(size=task_label.setter('text_size'))
        
        # Task details
        details = f"{task.category} | {task.priority}"
        if task.due_date:
            details += f" | Due: {task.due_date}"
        details_label = Label(
            text=details,
            font_size='12sp',
            color=(0.7, 0.7, 0.7, 1),
            halign='left',
            valign='middle',
            text_size=(None, None)
        )
        details_label.bind(size=details_label.setter('text_size'))
        
        info_layout.add_widget(task_label)
        info_layout.add_widget(details_label)
        
        # Buttons layout
        btn_layout = BoxLayout(orientation='vertical', size_hint_x=0.3, spacing=dp(2))
        
        # Complete button
        complete_btn = Button(
            text='✓ Done' if not task.completed else '↻ Undo',
            size_hint_y=0.5,
            background_color=(0.2, 0.8, 0.2, 1) if not task.completed else (0.8, 0.8, 0.2, 1)
        )
        complete_btn.bind(on_press=self.toggle_complete)
        
        # Delete button
        delete_btn = Button(
            text='✕ Delete',
            size_hint_y=0.5,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        delete_btn.bind(on_press=self.delete_task)
        
        btn_layout.add_widget(complete_btn)
        btn_layout.add_widget(delete_btn)
        
        self.add_widget(info_layout)
        self.add_widget(btn_layout)
        
        # Apply strikethrough style if completed
        if task.completed:
            task_label.color = (0.5, 0.5, 0.5, 1)
    
    def toggle_complete(self, instance):
        self.task.completed = not self.task.completed
        self.app_instance.save_tasks()
        self.app_instance.refresh_tasks()
    
    def delete_task(self, instance):
        self.app_instance.tasks.remove(self.task)
        self.app_instance.save_tasks()
        self.app_instance.refresh_tasks()


class TodoAndroidApp(App):
    """Main Kivy application"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tasks = []
        self.data_dir = self.get_data_dir()
        self.tasks_file = os.path.join(self.data_dir, 'tasks_android.json')
        self.load_tasks()
        
    def get_data_dir(self):
        """Get platform-specific data directory"""
        if hasattr(self, 'user_data_dir'):
            data_dir = self.user_data_dir
        else:
            data_dir = os.path.join(os.path.expanduser('~'), '.todo_android')
        
        os.makedirs(data_dir, exist_ok=True)
        return data_dir
    
    def build(self):
        """Build the UI"""
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Header
        header = Label(
            text='📋 Todo List Tracker',
            font_size='24sp',
            size_hint_y=None,
            height=dp(50),
            bold=True
        )
        main_layout.add_widget(header)
        
        # Add task section
        add_task_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(180),
            spacing=dp(5)
        )
        
        # Task input
        self.task_input = TextInput(
            hint_text='Enter task description...',
            size_hint_y=None,
            height=dp(40),
            multiline=False
        )
        
        # Category and priority selectors
        selectors_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(5)
        )
        
        self.category_spinner = Spinner(
            text='Category',
            values=('General', 'Work', 'Personal', 'Shopping', 'Health', 'Learning'),
            size_hint_x=0.5
        )
        
        self.priority_spinner = Spinner(
            text='Priority',
            values=('Low', 'Medium', 'High', 'Urgent'),
            size_hint_x=0.5
        )
        
        selectors_layout.add_widget(self.category_spinner)
        selectors_layout.add_widget(self.priority_spinner)
        
        # Add button
        add_btn = Button(
            text='➕ Add Task',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.6, 1, 1)
        )
        add_btn.bind(on_press=self.add_task)
        
        add_task_layout.add_widget(self.task_input)
        add_task_layout.add_widget(selectors_layout)
        add_task_layout.add_widget(add_btn)
        
        main_layout.add_widget(add_task_layout)
        
        # Filter section
        filter_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(5)
        )
        
        all_btn = Button(text='All', on_press=lambda x: self.filter_tasks('all'))
        active_btn = Button(text='Active', on_press=lambda x: self.filter_tasks('active'))
        completed_btn = Button(text='Completed', on_press=lambda x: self.filter_tasks('completed'))
        
        filter_layout.add_widget(all_btn)
        filter_layout.add_widget(active_btn)
        filter_layout.add_widget(completed_btn)
        
        main_layout.add_widget(filter_layout)
        
        # Tasks list
        self.tasks_layout = GridLayout(
            cols=1,
            spacing=dp(5),
            size_hint_y=None
        )
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))
        
        scroll_view = ScrollView()
        scroll_view.add_widget(self.tasks_layout)
        
        main_layout.add_widget(scroll_view)
        
        # Stats footer
        self.stats_label = Label(
            text='',
            size_hint_y=None,
            height=dp(30),
            font_size='14sp'
        )
        main_layout.add_widget(self.stats_label)
        
        # Initial task refresh
        self.current_filter = 'all'
        self.refresh_tasks()
        
        return main_layout
    
    def add_task(self, instance):
        """Add a new task"""
        task_text = self.task_input.text.strip()
        
        if not task_text:
            self.show_popup('Error', 'Please enter a task description')
            return
        
        category = self.category_spinner.text if self.category_spinner.text != 'Category' else 'General'
        priority = self.priority_spinner.text if self.priority_spinner.text != 'Priority' else 'Medium'
        
        task = Task(task_text, category, priority)
        self.tasks.append(task)
        self.save_tasks()
        
        # Clear inputs
        self.task_input.text = ''
        self.category_spinner.text = 'Category'
        self.priority_spinner.text = 'Priority'
        
        self.refresh_tasks()
    
    def filter_tasks(self, filter_type):
        """Filter tasks by type"""
        self.current_filter = filter_type
        self.refresh_tasks()
    
    def refresh_tasks(self):
        """Refresh the tasks display"""
        self.tasks_layout.clear_widgets()
        
        # Filter tasks
        if self.current_filter == 'active':
            display_tasks = [t for t in self.tasks if not t.completed]
        elif self.current_filter == 'completed':
            display_tasks = [t for t in self.tasks if t.completed]
        else:
            display_tasks = self.tasks
        
        # Display tasks
        for task in display_tasks:
            task_widget = TaskWidget(task, self)
            self.tasks_layout.add_widget(task_widget)
        
        # Update stats
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t.completed])
        active = total - completed
        self.stats_label.text = f'Total: {total} | Active: {active} | Completed: {completed}'
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            data = {
                'tasks': [task.to_dict() for task in self.tasks],
                'version': __version__
            }
            with open(self.tasks_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(t) for t in data.get('tasks', [])]
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []
    
    def show_popup(self, title, message):
        """Show a popup message"""
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()


def main():
    """Main entry point"""
    TodoAndroidApp().run()


if __name__ == '__main__':
    main()
