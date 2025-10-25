"""
Todo List Tracker v1.03
A comprehensive task management application with AI assistance, multiple views, and advanced features.
"""

__version__ = "1.03"
__author__ = "Task Manager Pro"
__date__ = "2025-10-25"

import os
import sys
import json
from datetime import date, timedelta
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox, ttk

def get_app_dir():
	if getattr(sys, 'frozen', False):
		# Running as PyInstaller exe
		return os.path.dirname(sys.executable)
	else:
		# Running as script
		return os.path.dirname(os.path.abspath(__file__))

APP_DIR = get_app_dir()
DATA_DIR = os.path.join(APP_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Default paths
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")
DEFAULT_THEME = "Light"

class TodoApp:
	def __init__(self, root):
		self.root = root
		root.title(f"To-Do List Tracker v{__version__}")
        
		# Set up window close handler
		root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
		# Define color themes
		self.themes = {
			"Light": {
				"bg": "#ffffff",
				"fg": "#000000",
				"button_bg": "#f0f0f0",
				"button_fg": "#000000",
				"listbox_bg": "#ffffff",
				"listbox_fg": "#000000",
				"entry_bg": "#ffffff",
				"entry_fg": "#000000"
			},
			"Sky Gradient": {
				"bg": "#e3f2fd",
				"bg_gradient": "#90caf9",
				"fg": "#0d47a1",
				"button_bg": "#bbdefb",
				"button_fg": "#0d47a1",
				"listbox_bg": "#e3f2fd",
				"listbox_fg": "#0d47a1",
				"entry_bg": "#ffffff",
				"entry_fg": "#0d47a1"
			},
			"Dark": {
				"bg": "#2d2d2d",
				"fg": "#ffffff",
				"button_bg": "#404040",
				"button_fg": "#ffffff",
				"listbox_bg": "#363636",
				"listbox_fg": "#ffffff",
				"entry_bg": "#363636",
				"entry_fg": "#ffffff"
			},
			"Monokai": {
				"bg": "#272822",
				"fg": "#f8f8f2",
				"button_bg": "#75715e",
				"button_fg": "#f8f8f2",
				"listbox_bg": "#3e3d32",
				"listbox_fg": "#f8f8f2",
				"entry_bg": "#3e3d32",
				"entry_fg": "#f8f8f2"
			},
			"Solarized Light": {
				"bg": "#fdf6e3",
				"fg": "#657b83",
				"button_bg": "#eee8d5",
				"button_fg": "#657b83",
				"listbox_bg": "#fdf6e3",
				"listbox_fg": "#657b83",
				"entry_bg": "#eee8d5",
				"entry_fg": "#657b83"
			},
			"Solarized Dark": {
				"bg": "#002b36",
				"fg": "#839496",
				"button_bg": "#073642",
				"button_fg": "#93a1a1",
				"listbox_bg": "#073642",
				"listbox_fg": "#93a1a1",
				"entry_bg": "#073642",
				"entry_fg": "#93a1a1"
			},
			"Nord": {
				"bg": "#2e3440",
				"fg": "#d8dee9",
				"button_bg": "#3b4252",
				"button_fg": "#e5e9f0",
				"listbox_bg": "#3b4252",
				"listbox_fg": "#e5e9f0",
				"entry_bg": "#3b4252",
				"entry_fg": "#e5e9f0"
			},
			"GitHub Light": {
				"bg": "#ffffff",
				"fg": "#24292e",
				"button_bg": "#fafbfc",
				"button_fg": "#24292e",
				"listbox_bg": "#ffffff",
				"listbox_fg": "#24292e",
				"entry_bg": "#fafbfc",
				"entry_fg": "#24292e"
			},
			"GitHub Dark": {
				"bg": "#0d1117",
				"fg": "#c9d1d9",
				"button_bg": "#21262d",
				"button_fg": "#c9d1d9",
				"listbox_bg": "#21262d",
				"listbox_fg": "#c9d1d9",
				"entry_bg": "#21262d",
				"entry_fg": "#c9d1d9"
			}
		}
        
		self.current_theme = self.themes["Light"]
		
		# Load custom themes from file
		self._load_themes_from_file()
		
		# Initialize XP system
		self.xp = 0
		self.level = 1
		self.tasks_completed = 0
		self.XP_PER_TASK = 10
		self.unlocked_items = set()
		self.pets = []  # List of active pets {"type": str, "x": int, "y": int, "direction": str}
		self.custom_assets = []  # List of custom PNG assets {"path": str, "x": float, "y": float, "scale": float}
		self.STARTER_PETS = ["pet_cat", "pet_dog"]
		
		# Define unlock thresholds (level -> unlockable items)
		self.UNLOCKS = {
			2: ["hat_wizard", "pet_cat"],
			3: ["shirt_leather_jacket"],
			4: ["pants_camo"],
			5: ["hat_sombrero", "pet_dog"],
			7: ["shirt_tuxedo"],
			8: ["pet_bird"],
			10: ["hat_viking", "pants_rainbow"],
			12: ["shirt_superhero"],
			15: ["pet_dragon", "hat_halo"],
			20: ["shirt_gold", "pants_gold"]
		}

		# Theme selector frame
		theme_frame = tk.Frame(root)
		theme_frame.pack(padx=8, pady=(6,0), fill="x")
		
		self.theme_label = tk.Label(theme_frame, text="Theme:")
		self.theme_label.pack(side="left")
		self.theme_var = tk.StringVar(value="Light")
		self.theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, 
								  values=list(self.themes.keys()), state="readonly", width=15)
		self.theme_combo.pack(side="left", padx=(6,0))
		self.theme_combo.bind('<<ComboboxSelected>>', lambda e: self.change_theme())
		
		# Scenes notebook
		self.notebook = ttk.Notebook(root)
		self.notebook.pack(padx=8, pady=(6,8), fill="both", expand=True)
		self.tasks_tab = tk.Frame(self.notebook)
		self.stats_tab = tk.Frame(self.notebook)
		self.calendar_tab = tk.Frame(self.notebook)
		self.theme_editor_tab = tk.Frame(self.notebook)
		# New Daily tab
		self.daily_tab = tk.Frame(self.notebook)
		# New AI Tasks tab
		self.ai_tasks_tab = tk.Frame(self.notebook)
		# New Settings tab
		self.settings_tab = tk.Frame(self.notebook)
		# New Avatar Room tab
		self.avatar_room_tab = tk.Frame(self.notebook)
		self.notebook.add(self.tasks_tab, text="Tasks")
		self.notebook.add(self.daily_tab, text="Daily")
		self.notebook.add(self.ai_tasks_tab, text="AI Tasks")
		self.notebook.add(self.stats_tab, text="Stats")
		self.notebook.add(self.calendar_tab, text="Calendar")
		self.notebook.add(self.theme_editor_tab, text="Themes")
		self.notebook.add(self.settings_tab, text="Settings")
		self.notebook.add(self.avatar_room_tab, text="Avatar Room")
		
		# Enable tab dragging
		self._drag_data = {"tab": None, "x": 0}
		self.notebook.bind("<ButtonPress-1>", self._on_tab_press)
		self.notebook.bind("<B1-Motion>", self._on_tab_drag)
		self.notebook.bind("<ButtonRelease-1>", self._on_tab_release)

		# Top input row (Tasks tab)
		self.top_frame = tk.Frame(self.tasks_tab)
		self.top_frame.pack(padx=8, pady=6, fill="x")
		
		# View selector on the left
		view_label = tk.Label(self.top_frame, text="View:")
		view_label.pack(side="left", padx=(0, 5))
		
		self.view_mode_var = tk.StringVar(value="Tree")
		self.view_combo = ttk.Combobox(self.top_frame, textvariable=self.view_mode_var,
									   values=["Tree", "Kanban", "List", "Compact"], 
									   state="readonly", width=10)
		self.view_combo.pack(side="left", padx=(0, 15))
		self.view_combo.bind('<<ComboboxSelected>>', lambda e: self._change_view_mode())

		self.entry = tk.Entry(self.top_frame, bg="#ffffff", fg="#000000")
		self.entry.pack(side="left", expand=True, fill="x", padx=(0,6))
		self.entry.bind("<Return>", lambda e: self.add_task())
		# Placeholder text
		self.entry_placeholder = "type tasks here!"
		self.entry_has_placeholder = True
		self.entry.insert(0, self.entry_placeholder)
		self.entry.config(fg="#999999")
		self.entry.bind("<FocusIn>", self._on_entry_focus_in)
		self.entry.bind("<FocusOut>", self._on_entry_focus_out)

		self.category_var = tk.StringVar()
		# Use a Combobox as a scrollable wheel for categories; allow typing new ones
		self.category_combo = ttk.Combobox(self.top_frame, textvariable=self.category_var, width=16, state="normal")
		self.category_combo.pack(side="left", padx=(0,6))
		self.category_var.set("General")
		# Scroll through categories with mouse wheel
		self.category_combo.bind("<MouseWheel>", self._category_on_mousewheel)

		self.priority_var = tk.StringVar(value="Medium")
		self.priority_combo = ttk.Combobox(self.top_frame, textvariable=self.priority_var, 
									  values=["High", "Medium", "Low"], state="readonly", width=16)
		self.priority_combo.pack(side="left", padx=(0,6))

		# Deadline for new tasks with visual indicator
		self.add_deadline_var = tk.StringVar(value="")
		
		self.deadline_btn = tk.Button(self.top_frame, textvariable=self.add_deadline_var, width=10, command=self._pick_add_deadline)
		self.deadline_btn.pack(side="left", padx=(0,6))
		
		# Set default text for deadline button
		self.add_deadline_var.set("📅 Deadline")
		
		# Update deadline button when variable changes
		self.add_deadline_var.trace_add('write', lambda *args: self._update_deadline_display())

		add_btn = tk.Button(self.top_frame, text="Add", width=10, command=self.add_task)
		add_btn.pack(side="left")

		# Main view container for tasks (supports multiple view modes)
		self.view_container = tk.Frame(self.tasks_tab)
		self.view_container.pack(padx=8, pady=(0,6), fill="both", expand=True)
		
		# Tree view (default)
		self.tree_view_frame = tk.Frame(self.view_container)
		
		self.tree = ttk.Treeview(self.tree_view_frame, columns=("status", "priority", "deadline"), show="tree headings", selectmode="extended")
		self.tree.heading("#0", text="Tasks", command=self._sort_categories_alphabetically)
		self.tree.heading("status", text="Status")
		self.tree.heading("priority", text="Priority")
		self.tree.heading("deadline", text="Deadline")
		self.tree.column("status", width=70, anchor="center")
		self.tree.column("priority", width=80, anchor="center")
		self.tree.column("deadline", width=100, anchor="center")
		self.tree.pack(side="left", fill="both", expand=True)

		tree_scrollbar = ttk.Scrollbar(self.tree_view_frame, orient="vertical", command=self.tree.yview)
		tree_scrollbar.pack(side="right", fill="y")
		self.tree.configure(yscrollcommand=tree_scrollbar.set)
		
		# Kanban view
		self.kanban_view_frame = tk.Frame(self.view_container)
		self._setup_kanban_view()
		
		# List view
		self.list_view_frame = tk.Frame(self.view_container)
		self._setup_list_view()
		
		# Compact view
		self.compact_view_frame = tk.Frame(self.view_container)
		self._setup_compact_view()
		
		# Show tree view by default
		self.tree_view_frame.pack(fill="both", expand=True)
		self.current_view = "Tree"

		# Buttons row (Tasks tab)
		self.btn_frame = tk.Frame(self.tasks_tab)
		self.btn_frame.pack(padx=8, pady=(0,8), fill="x")

		tk.Button(self.btn_frame, text="Edit", width=10, command=self.edit_task).pack(side="left")
		tk.Button(self.btn_frame, text="Remove", width=10, command=self.remove_task).pack(side="left", padx=6)
		tk.Button(self.btn_frame, text="Toggle Complete", width=16, command=self.toggle_complete).pack(side="left")
		tk.Button(self.btn_frame, text="Clear Completed", width=16, command=self.clear_completed).pack(side="left", padx=6)
		tk.Button(self.btn_frame, text="Load Demo", width=12, command=self._seed_test_tasks).pack(side="right")
		tk.Button(self.btn_frame, text="Save", width=10, command=self.save_tasks).pack(side="right")
		tk.Button(self.btn_frame, text="Load", width=10, command=self.load_tasks).pack(side="right", padx=(0,6))

		# Bindings
		self.tree.bind("<Double-1>", lambda e: self.toggle_complete())
		self.tree.bind("<Delete>", lambda e: self.remove_task())
		self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)
		self.tree.bind("<Button-3>", self._on_tree_right_click)  # Right-click context menu
		# Drag & drop
		self.tree.bind("<ButtonPress-1>", self._on_tree_press)
		self.tree.bind("<B1-Motion>", self._on_tree_motion)
		self.tree.bind("<ButtonRelease-1>", self._on_tree_release)

		# Category tracking and colors
		self.categories = {}  # name -> tree item id
		self.category_colors = {}  # name -> color
		self._last_category = "General"  # remember last used category
		self._priority_sort_reverse = False  # False=High->Low, True=Low->High
		self._category_sort_reverse = False  # False=A->Z, True=Z->A
		# Stats tracking
		self.stats_daily = {}  # date_str -> count
		self.task_meta = {}    # tree item id -> {"last_completed_date": str|None, "deadline": str|None}
		self._color_palette = [
			"#e6194B", "#3cb44b", "#ffe119", "#0082c8", "#f58231",
			"#911eb4", "#46f0f0", "#f032e6", "#d2f53c", "#fabebe",
			"#008080", "#e6beff", "#aa6e28", "#800000", "#aaffc3",
			"#808000", "#ffd8b1", "#000080", "#808080", "#FFFFFF"
		]
		self._drag_item = None
		self._drag_over = None

		# --- Stats tab UI (7-day completion graph) ---
		self.stats_header = tk.Frame(self.stats_tab)
		self.stats_header.pack(padx=8, pady=8, fill="x")
		self.stats_title_label = tk.Label(self.stats_header, text="Task Completion (7 Days)")
		self.stats_title_label.pack(side="left")
		# Stats navigation (center date prev/next/today) and info text
		self.stats_nav_frame = tk.Frame(self.stats_header)
		self.stats_nav_frame.pack(side="left", padx=10)
		self.stats_prev_btn = tk.Button(self.stats_nav_frame, text="◀", width=3, command=self._stats_prev_day,
									   highlightthickness=0, bd=0, relief="flat")
		self.stats_prev_btn.pack(side="left", padx=2)
		self.stats_center_label = tk.Label(self.stats_nav_frame, text="", width=22)
		self.stats_center_label.pack(side="left", padx=6)
		self.stats_next_btn = tk.Button(self.stats_nav_frame, text="▶", width=3, command=self._stats_next_day,
									   highlightthickness=0, bd=0, relief="flat")
		self.stats_next_btn.pack(side="left", padx=2)
		self.stats_today_btn = tk.Button(self.stats_nav_frame, text="Today", width=8, command=self._stats_today,
									   highlightthickness=0, bd=0, relief="flat")
		self.stats_today_btn.pack(side="left", padx=10)

		# Small added hint text (does not replace title)
		self.stats_hint_label = tk.Label(self.stats_header, text="Past 3 / Today / Next 3", font=("Arial", 9))
		self.stats_hint_label.pack(side="left", padx=8)
		
		# Graph type selector
		self.stats_graph_type = tk.StringVar(value="bar")
		self.stats_type_frame = tk.Frame(self.stats_header)
		self.stats_type_frame.pack(side="right")
		self.stats_bar_radio = tk.Radiobutton(self.stats_type_frame, text="Bar", variable=self.stats_graph_type,
										 value="bar", command=self._update_stats_view,
										 highlightthickness=0, bd=0, relief="flat", indicatoron=True, takefocus=0)
		self.stats_bar_radio.pack(side="left", padx=2)
		self.stats_line_radio = tk.Radiobutton(self.stats_type_frame, text="Line", variable=self.stats_graph_type,
										  value="line", command=self._update_stats_view,
										  highlightthickness=0, bd=0, relief="flat", indicatoron=True, takefocus=0)
		self.stats_line_radio.pack(side="left", padx=2)
		
		self.stats_canvas = tk.Canvas(self.stats_tab, height=300, highlightthickness=0)
		self.stats_canvas.pack(padx=8, pady=(0,8), fill="both", expand=True)
		self.stats_canvas.bind("<Configure>", lambda e: self._update_stats_view())

		# Stats center date for scrolling
		self.stats_center_date = date.today()
		
		# --- Calendar tab UI (navigable monthly/weekly view) ---
		self.cal_header = tk.Frame(self.calendar_tab)
		self.cal_header.pack(padx=8, pady=8, fill="x")
		
		# Navigation controls
		self.nav_frame = tk.Frame(self.cal_header)
		self.nav_frame.pack(side="left")
		self.cal_prev_btn = tk.Button(self.nav_frame, text="◀", width=3, command=self._calendar_prev,
									  highlightthickness=0, bd=0, relief="flat")
		self.cal_prev_btn.pack(side="left", padx=2)
		self.cal_date_label = tk.Label(self.nav_frame, text="", width=20, bd=1, relief="solid")
		self.cal_date_label.pack(side="left", padx=10)
		self.cal_next_btn = tk.Button(self.nav_frame, text="▶", width=3, command=self._calendar_next,
									  highlightthickness=0, bd=0, relief="flat")
		self.cal_next_btn.pack(side="left", padx=2)
		self.cal_today_btn = tk.Button(self.nav_frame, text="Today", width=8, command=self._calendar_today,
									   highlightthickness=0, bd=0, relief="flat")
		self.cal_today_btn.pack(side="left", padx=10)
		
		# View toggle
		self.cal_view_var = tk.StringVar(value="monthly")
		self.view_toggle_frame = tk.Frame(self.cal_header)
		self.view_toggle_frame.pack(side="right")
		self.cal_weekly_radio = tk.Radiobutton(self.view_toggle_frame, text="Weekly", variable=self.cal_view_var, 
											   value="weekly", command=self._update_calendar_view,
											   highlightthickness=0, bd=0, relief="flat", indicatoron=True)
		self.cal_weekly_radio.pack(side="left", padx=2)
		self.cal_monthly_radio = tk.Radiobutton(self.view_toggle_frame, text="Monthly", variable=self.cal_view_var, 
												value="monthly", command=self._update_calendar_view,
												highlightthickness=0, bd=0, relief="flat", indicatoron=True)
		self.cal_monthly_radio.pack(side="left", padx=2)
		
		self.calendar_canvas = tk.Canvas(self.calendar_tab, height=300, highlightthickness=0)
		self.calendar_canvas.pack(padx=8, pady=(0,8), fill="both", expand=True)
		self.calendar_canvas.bind("<Configure>", lambda e: self._update_calendar_view())
		
		# Calendar navigation state
		self.cal_current_date = date.today()

		# ===== SETTINGS =====
		self._init_settings()

		# ===== THEME EDITOR TAB =====
		self._setup_theme_editor()

		# ===== AI TASKS TAB =====
		self._setup_ai_tasks_tab()

		# ===== SETTINGS TAB =====
		self._setup_settings_tab()

		# ===== AVATAR ROOM TAB =====
		self._setup_avatar_room_tab()

		# Initial load and theme
		self.load_tasks(startup=True)
		self.apply_theme()
		self._refresh_all_category_colors()  # Ensure consistent 25% opacity on all categories
		self.tree.heading("priority", command=self._sort_all_by_priority)
		self._update_stats_view()
		self._update_calendar_view()
		# Ensure the window cannot be resized so small that controls are hidden
		self._update_min_window_size()

	def _update_min_window_size(self):
		"""Compute and set a reasonable minimum window size so controls don't get clipped."""
		try:
			# Let Tk compute requested sizes first
			self.root.update_idletasks()
			min_w = 0
			# Consider the top input row and the bottom buttons row
			if hasattr(self, 'top_frame') and self.top_frame.winfo_exists():
				min_w = max(min_w, self.top_frame.winfo_reqwidth())
			if hasattr(self, 'btn_frame') and self.btn_frame.winfo_exists():
				min_w = max(min_w, self.btn_frame.winfo_reqwidth())
			# Add some padding for tab margins and scrollbar
			min_w = max(min_w + 32, 720)
			# Height: keep a sensible minimum so trees/canvases remain usable
			min_h = max(self.root.winfo_reqheight(), 460)
			self.root.minsize(min_w, min_h)
		except Exception:
			# Fallback conservative minimums
			self.root.minsize(720, 460)

	def _setup_kanban_view(self):
		"""Set up Kanban board view with To Do, In Progress, Done columns."""
		# Create three columns
		columns_frame = tk.Frame(self.kanban_view_frame)
		columns_frame.pack(fill="both", expand=True, padx=5, pady=5)
		
		self.kanban_columns = {}
		column_names = ["To Do", "In Progress", "Done"]
		column_colors = ["#ffebee", "#fff3e0", "#e8f5e9"]
		
		for i, (col_name, col_color) in enumerate(zip(column_names, column_colors)):
			col_frame = tk.Frame(columns_frame, bg=col_color, relief="ridge", bd=2)
			col_frame.grid(row=0, column=i, sticky="nsew", padx=5)
			columns_frame.columnconfigure(i, weight=1, uniform="cols")
			columns_frame.rowconfigure(0, weight=1)
			
			# Column header
			header = tk.Label(col_frame, text=col_name, font=("", 12, "bold"), 
							 bg=col_color, pady=10)
			header.pack(fill="x")
			
			# Scrollable task area
			canvas = tk.Canvas(col_frame, bg=col_color, highlightthickness=0)
			scrollbar = ttk.Scrollbar(col_frame, orient="vertical", command=canvas.yview)
			task_container = tk.Frame(canvas, bg=col_color)
			
			canvas.configure(yscrollcommand=scrollbar.set)
			scrollbar.pack(side="right", fill="y")
			canvas.pack(side="left", fill="both", expand=True)
			
			canvas_window = canvas.create_window((0, 0), window=task_container, anchor="nw")
			task_container.bind("<Configure>", 
							   lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))
			canvas.bind("<Configure>", 
					   lambda e, c=canvas, w=canvas_window: c.itemconfig(w, width=e.width))
			
			self.kanban_columns[col_name] = {
				"frame": col_frame,
				"container": task_container,
				"canvas": canvas
			}
	
	def _setup_list_view(self):
		"""Set up simple list view without tree hierarchy."""
		# Create listbox with task items
		list_frame = tk.Frame(self.list_view_frame)
		list_frame.pack(fill="both", expand=True, padx=5, pady=5)
		
		self.list_view_listbox = tk.Listbox(list_frame, font=("", 10), selectmode="extended")
		self.list_view_listbox.pack(side="left", fill="both", expand=True)
		
		list_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", 
									   command=self.list_view_listbox.yview)
		list_scrollbar.pack(side="right", fill="y")
		self.list_view_listbox.configure(yscrollcommand=list_scrollbar.set)
		
		# Double-click to toggle complete
		self.list_view_listbox.bind("<Double-1>", lambda e: self._list_view_toggle_complete())
		
		# Store mapping of listbox index to tree item id
		self.list_view_items = []
	
	def _setup_compact_view(self):
		"""Set up compact view showing only incomplete high-priority tasks."""
		compact_frame = tk.Frame(self.compact_view_frame)
		compact_frame.pack(fill="both", expand=True, padx=10, pady=10)
		
		# Title
		title = tk.Label(compact_frame, text="Focus View - High Priority Tasks", 
						font=("", 14, "bold"))
		title.pack(pady=(0, 10))
		
		# Canvas for scrollable task cards
		canvas = tk.Canvas(compact_frame, highlightthickness=0)
		scrollbar = ttk.Scrollbar(compact_frame, orient="vertical", command=canvas.yview)
		self.compact_container = tk.Frame(canvas)
		
		canvas.configure(yscrollcommand=scrollbar.set)
		scrollbar.pack(side="right", fill="y")
		canvas.pack(side="left", fill="both", expand=True)
		
		canvas_window = canvas.create_window((0, 0), window=self.compact_container, anchor="nw")
		self.compact_container.bind("<Configure>", 
								   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
		canvas.bind("<Configure>", 
				   lambda e, w=canvas_window: canvas.itemconfig(w, width=e.width))
		
		self.compact_canvas = canvas
	
	def _change_view_mode(self):
		"""Switch between different view modes."""
		new_view = self.view_mode_var.get()
		
		# Hide current view
		if self.current_view == "Tree":
			self.tree_view_frame.pack_forget()
		elif self.current_view == "Kanban":
			self.kanban_view_frame.pack_forget()
		elif self.current_view == "List":
			self.list_view_frame.pack_forget()
		elif self.current_view == "Compact":
			self.compact_view_frame.pack_forget()
		
		# Show new view
		if new_view == "Tree":
			self.tree_view_frame.pack(fill="both", expand=True)
		elif new_view == "Kanban":
			self.kanban_view_frame.pack(fill="both", expand=True)
			self._refresh_kanban_view()
		elif new_view == "List":
			self.list_view_frame.pack(fill="both", expand=True)
			self._refresh_list_view()
		elif new_view == "Compact":
			self.compact_view_frame.pack(fill="both", expand=True)
			self._refresh_compact_view()
		
		self.current_view = new_view
	
	def _refresh_kanban_view(self):
		"""Refresh Kanban board with current tasks."""
		# Clear existing cards
		for col_data in self.kanban_columns.values():
			for widget in col_data["container"].winfo_children():
				widget.destroy()
		
		# Get all tasks from tree
		for cat_id in self.tree.get_children():
			category_name = self.tree.item(cat_id, "text").split(" (")[0]
			for task_id in self.tree.get_children(cat_id):
				task_text = self.tree.item(task_id, "text")
				status = self.tree.set(task_id, "status")
				priority = self.tree.set(task_id, "priority")
				deadline = self.tree.set(task_id, "deadline")
				
				# Determine column
				if status == "[✓]":
					col_name = "Done"
				elif "progress" in task_text.lower() or "working" in task_text.lower():
					col_name = "In Progress"
				else:
					col_name = "To Do"
				
				# Create task card
				self._create_kanban_card(col_name, task_id, task_text, category_name, 
									   priority, deadline, status)
	
	def _create_kanban_card(self, column, task_id, text, category, priority, deadline, status):
		"""Create a task card in the Kanban board."""
		container = self.kanban_columns[column]["container"]
		
		# Card frame
		card = tk.Frame(container, relief="raised", bd=2, bg="#ffffff", cursor="hand2")
		card.pack(fill="x", padx=5, pady=5)
		
		# Task text
		task_label = tk.Label(card, text=text, font=("", 10), bg="#ffffff", 
							 anchor="w", wraplength=200, justify="left")
		task_label.pack(fill="x", padx=5, pady=(5, 2))
		
		# Metadata row
		meta_frame = tk.Frame(card, bg="#ffffff")
		meta_frame.pack(fill="x", padx=5, pady=(0, 5))
		
		tk.Label(meta_frame, text=f"📁{category}", font=("", 8), bg="#ffffff", 
				fg="#666666").pack(side="left", padx=(0, 5))
		tk.Label(meta_frame, text=priority, font=("", 8), bg="#ffffff", 
				fg="#666666").pack(side="left", padx=(0, 5))
		if deadline:
			tk.Label(meta_frame, text=f"📅{deadline}", font=("", 8), bg="#ffffff", 
					fg="#666666").pack(side="left")
		
		# Click to toggle complete
		card.bind("<Button-1>", lambda e, tid=task_id: self._kanban_toggle_task(tid))
	
	def _kanban_toggle_task(self, task_id):
		"""Toggle task completion from Kanban view."""
		# Select the task in tree
		self.tree.selection_set(task_id)
		self.toggle_complete()
		# Refresh Kanban view
		self._refresh_kanban_view()
	
	def _refresh_list_view(self):
		"""Refresh list view with all tasks."""
		self.list_view_listbox.delete(0, "end")
		self.list_view_items = []
		
		for cat_id in self.tree.get_children():
			category_name = self.tree.item(cat_id, "text").split(" (")[0]
			
			for task_id in self.tree.get_children(cat_id):
				task_text = self.tree.item(task_id, "text")
				status = self.tree.set(task_id, "status")
				priority = self.tree.set(task_id, "priority")
				deadline = self.tree.set(task_id, "deadline")
				
				# Format: [✓] Task Name | Category | Priority | Deadline
				display = f"{status} {task_text} | {category_name} | {priority}"
				if deadline:
					display += f" | {deadline}"
				
				self.list_view_listbox.insert("end", display)
				self.list_view_items.append(task_id)
	
	def _list_view_toggle_complete(self):
		"""Toggle completion for selected item in list view."""
		selection = self.list_view_listbox.curselection()
		if not selection:
			return
		
		idx = selection[0]
		if idx < len(self.list_view_items):
			task_id = self.list_view_items[idx]
			self.tree.selection_set(task_id)
			self.toggle_complete()
			self._refresh_list_view()
	
	def _refresh_compact_view(self):
		"""Refresh compact view showing high-priority incomplete tasks."""
		# Clear existing cards
		for widget in self.compact_container.winfo_children():
			widget.destroy()
		
		high_priority_tasks = []
		
		# Collect high-priority incomplete tasks
		for cat_id in self.tree.get_children():
			category_name = self.tree.item(cat_id, "text").split(" (")[0]
			for task_id in self.tree.get_children(cat_id):
				status = self.tree.set(task_id, "status")
				priority = self.tree.set(task_id, "priority")
				
				if status != "[✓]" and "🔴" in priority:  # High priority and incomplete
					task_text = self.tree.item(task_id, "text")
					deadline = self.tree.set(task_id, "deadline")
					high_priority_tasks.append((task_id, task_text, category_name, deadline))
		
		if not high_priority_tasks:
			tk.Label(self.compact_container, text="No high-priority tasks! 🎉", 
					font=("", 12), fg="#666666").pack(pady=50)
			return
		
		# Create task cards
		for task_id, text, category, deadline in high_priority_tasks:
			self._create_compact_card(task_id, text, category, deadline)
	
	def _create_compact_card(self, task_id, text, category, deadline):
		"""Create a compact task card."""
		card = tk.Frame(self.compact_container, relief="solid", bd=2, bg="#fff5f5")
		card.pack(fill="x", padx=10, pady=8)
		
		# Header with category
		header = tk.Frame(card, bg="#ffebee")
		header.pack(fill="x")
		tk.Label(header, text=f"🔴 {category}", font=("", 9, "bold"), 
				bg="#ffebee", fg="#c62828").pack(side="left", padx=10, pady=5)
		if deadline:
			tk.Label(header, text=f"📅 {deadline}", font=("", 9), 
					bg="#ffebee", fg="#666666").pack(side="right", padx=10, pady=5)
		
		# Task text
		text_label = tk.Label(card, text=text, font=("", 11), bg="#fff5f5", 
							 anchor="w", wraplength=600, justify="left")
		text_label.pack(fill="x", padx=15, pady=10)
		
		# Complete button
		btn_frame = tk.Frame(card, bg="#fff5f5")
		btn_frame.pack(fill="x", padx=10, pady=(0, 10))
		
		complete_btn = tk.Button(btn_frame, text="✓ Mark Complete", 
								command=lambda tid=task_id: self._compact_toggle_task(tid))
		complete_btn.pack(side="right")
	
	def _compact_toggle_task(self, task_id):
		"""Toggle task completion from compact view."""
		self.tree.selection_set(task_id)
		self.toggle_complete()
		self._refresh_compact_view()
	
	def _refresh_current_view(self):
		"""Refresh whichever view is currently active."""
		if not hasattr(self, 'current_view'):
			return
		
		if self.current_view == "Kanban":
			self._refresh_kanban_view()
		elif self.current_view == "List":
			self._refresh_list_view()
		elif self.current_view == "Compact":
			self._refresh_compact_view()
		# Tree view updates automatically

	def _setup_daily_tab(self):
		"""Create the Daily tab with a stopwatch and next-task-by-priority controls."""
		import time as _time
		self._daily_timer_running = False
		self._daily_timer_last = None
		self._daily_elapsed = 0.0
		self._daily_current_task = None  # tree item id
		# Per-task accumulated time (seconds)
		if not hasattr(self, 'task_time_spent'):
			self.task_time_spent = {}
		# Daily mode: stopwatch or pomodoro
		self._daily_mode_var = tk.StringVar(value="stopwatch")
		self._pomodoro_state = "work"  # work or break
		self._pomodoro_remaining = 0
		self._pomodoro_work_min_var = tk.IntVar(value=25)
		self._pomodoro_break_min_var = tk.IntVar(value=5)

		# Header: current task display
		header = tk.Frame(self.daily_tab)
		header.pack(fill="x", padx=8, pady=(8, 4))
		tk.Label(header, text="Current Task:").pack(side="left")
		self.daily_task_label = tk.Label(header, text="None", anchor="w")
		self.daily_task_label.pack(side="left", padx=6)

		# Stopwatch display
		timer_frame = tk.Frame(self.daily_tab)
		timer_frame.pack(fill="x", padx=8, pady=(4, 8))
		self.daily_timer_label = tk.Label(timer_frame, text="00:00:00", font=("Arial", 24, "bold"))
		self.daily_timer_label.pack(side="left")
		self.daily_total_label = tk.Label(timer_frame, text="Total for task: 00:00:00", font=("Arial", 10))
		self.daily_total_label.pack(side="left", padx=12)
		self.daily_phase_label = tk.Label(timer_frame, text="", font=("Arial", 10))
		self.daily_phase_label.pack(side="left", padx=12)

		# Controls
		ctrl = tk.Frame(self.daily_tab)
		ctrl.pack(fill="x", padx=8, pady=(0, 8))
		self.daily_start_btn = ttk.Button(ctrl, text="Start", command=self._daily_start_pause)
		self.daily_start_btn.pack(side="left")
		tk.Button(ctrl, text="Reset", command=self._daily_reset).pack(side="left")
		tk.Button(ctrl, text="Next by Priority", command=self._daily_pick_next_task).pack(side="left", padx=12)
		tk.Button(ctrl, text="Complete (and Next)", command=self._daily_complete_task).pack(side="left", padx=6)

		# Filters
		filt = tk.LabelFrame(self.daily_tab, text="Next Task Filters")
		filt.pack(fill="x", padx=8, pady=(0,8))
		tk.Label(filt, text="Category:").pack(side="left")
		self.daily_cat_var = tk.StringVar(value="All")
		self.daily_cat_combo = ttk.Combobox(filt, textvariable=self.daily_cat_var, width=18, state="readonly")
		self.daily_cat_combo.pack(side="left", padx=(4,12))
		# Priority includes
		self.daily_inc_high = tk.BooleanVar(value=True)
		self.daily_inc_med = tk.BooleanVar(value=True)
		self.daily_inc_low = tk.BooleanVar(value=True)
		tk.Checkbutton(filt, text="High", variable=self.daily_inc_high).pack(side="left", padx=4)
		tk.Checkbutton(filt, text="Medium", variable=self.daily_inc_med).pack(side="left", padx=4)
		tk.Checkbutton(filt, text="Low", variable=self.daily_inc_low).pack(side="left", padx=4)

		# Mode selector
		mode = tk.LabelFrame(self.daily_tab, text="Mode")
		mode.pack(fill="x", padx=8, pady=(0,8))
		tk.Radiobutton(mode, text="Stopwatch", value="stopwatch", variable=self._daily_mode_var, command=self._daily_on_mode_change).pack(side="left")
		tk.Radiobutton(mode, text="Pomodoro", value="pomodoro", variable=self._daily_mode_var, command=self._daily_on_mode_change).pack(side="left", padx=8)
		tk.Label(mode, text="Work (min):").pack(side="left", padx=(12,2))
		self.pomo_work_spin = tk.Spinbox(mode, from_=5, to=120, textvariable=self._pomodoro_work_min_var, width=4)
		self.pomo_work_spin.pack(side="left")
		tk.Label(mode, text="Break (min):").pack(side="left", padx=(12,2))
		self.pomo_break_spin = tk.Spinbox(mode, from_=1, to=60, textvariable=self._pomodoro_break_min_var, width=4)
		self.pomo_break_spin.pack(side="left")

		# Info
		info = tk.Label(self.daily_tab, text="Daily mode picks the highest-priority incomplete task. Time is tracked per task while the timer runs.", anchor="w")
		info.pack(fill="x", padx=8)

		# Completed today list
		done_frame = tk.LabelFrame(self.daily_tab, text="Completed Today")
		done_frame.pack(fill="both", expand=True, padx=8, pady=(0,8))
		self.daily_done_list = tk.Listbox(done_frame, height=6)
		self.daily_done_list.pack(side="left", fill="both", expand=True)
		done_scroll = ttk.Scrollbar(done_frame, orient="vertical", command=self.daily_done_list.yview)
		done_scroll.pack(side="right", fill="y")
		self.daily_done_list.configure(yscrollcommand=done_scroll.set)

		# Internal timer loop
		self._daily_after_id = None

	def _daily_format(self, secs):
		secs = int(secs)
		h = secs // 3600
		m = (secs % 3600) // 60
		s = secs % 60
		return f"{h:02d}:{m:02d}:{s:02d}"

	def _daily_update_labels(self):
		# Update timer label depending on mode
		if self._daily_mode_var.get() == "pomodoro":
			self.daily_phase_label.config(text=f"{self._pomodoro_state.title()}")
			self.daily_timer_label.config(text=self._daily_format(self._pomodoro_remaining))
		else:
			self.daily_phase_label.config(text="")
			self.daily_timer_label.config(text=self._daily_format(self._daily_elapsed))
		# total for current task
		if self._daily_current_task:
			if self._daily_mode_var.get() == "pomodoro":
				current_run = 0  # we do not add countdown to total; we add only when paused
			else:
				current_run = self._daily_elapsed
			total = int(self.task_time_spent.get(self._daily_current_task, 0) + current_run)
			self.daily_total_label.config(text=f"Total for task: {self._daily_format(total)}")
		else:
			self.daily_total_label.config(text="Total for task: 00:00:00")

	def _daily_tick(self):
		import time as _time
		if not self._daily_timer_running:
			return
		now = _time.time()
		if self._daily_timer_last is None:
			self._daily_timer_last = now
			dt = 0
		else:
			dt = now - self._daily_timer_last
			self._daily_timer_last = now
		if self._daily_mode_var.get() == "pomodoro":
			# countdown
			self._pomodoro_remaining = max(0, int(self._pomodoro_remaining - dt))
			if self._pomodoro_remaining <= 0:
				# switch phase
				if self._pomodoro_state == "work":
					self._pomodoro_state = "break"
					self._pomodoro_remaining = max(1, int(self._pomodoro_break_min_var.get()) * 60)
					# Beep to signal phase change
					try:
						import winsound
						winsound.Beep(800, 300)  # 800 Hz for 300ms
					except Exception:
						pass
				else:
					self._pomodoro_state = "work"
					self._pomodoro_remaining = max(1, int(self._pomodoro_work_min_var.get()) * 60)
					# Beep to signal phase change
					try:
						import winsound
						winsound.Beep(600, 300)  # 600 Hz for 300ms
					except Exception:
						pass
		else:
			# stopwatch
			self._daily_elapsed += dt
		self._daily_update_labels()
		# schedule next tick
		self._daily_after_id = self.root.after(1000, self._daily_tick)

	def _daily_update_tab_indicator(self):
		try:
			text = "Daily"
			if self._daily_timer_running:
				text = "Daily • Running"
			self.notebook.tab(self.daily_tab, text=text)
		except Exception:
			pass

	def _daily_start_pause(self):
		if self._daily_timer_running:
			self._daily_pause()
		else:
			self._daily_start()

	def _daily_start(self):
		import time as _time
		if not self._daily_current_task:
			# pick a task if none selected
			self._daily_pick_next_task()
		if not self._daily_current_task:
			return
		self._daily_timer_running = True
		self._daily_timer_last = _time.time()
		# Initialize pomodoro remaining on first start of a session
		if self._daily_mode_var.get() == "pomodoro" and self._pomodoro_remaining <= 0:
			self._pomodoro_state = "work"
			self._pomodoro_remaining = max(1, int(self._pomodoro_work_min_var.get()) * 60)
		if not self._daily_after_id:
			self._daily_after_id = self.root.after(1000, self._daily_tick)
		# Update UI
		try:
			self.daily_start_btn.config(text="Pause")
		except Exception:
			pass
		self._daily_update_tab_indicator()

	def _daily_pause(self):
		# accumulate elapsed into task total
		self._daily_timer_running = False
		if self._daily_after_id:
			try:
				self.root.after_cancel(self._daily_after_id)
			except Exception:
				pass
			self._daily_after_id = None
		if self._daily_current_task:
			prev = self.task_time_spent.get(self._daily_current_task, 0.0)
			self.task_time_spent[self._daily_current_task] = prev + self._daily_elapsed
			# also store into task_meta for persistence in-memory
			if self._daily_current_task not in self.task_meta:
				self.task_meta[self._daily_current_task] = {}
			self.task_meta[self._daily_current_task]['time_spent'] = self.task_time_spent[self._daily_current_task]
		self._daily_elapsed = 0.0
		self._daily_timer_last = None
		self._daily_update_labels()
		# Update UI
		try:
			self.daily_start_btn.config(text="Start")
		except Exception:
			pass
		self._daily_update_tab_indicator()

	def _daily_reset(self):
		self._daily_pause()
		self._daily_elapsed = 0.0
		if self._daily_mode_var.get() == "pomodoro":
			self._pomodoro_remaining = 0
			self._pomodoro_state = "work"
		self._daily_update_labels()

	def _daily_set_current(self, item_id):
		self._daily_pause()
		self._daily_current_task = item_id
		if not item_id:
			self.daily_task_label.config(text="None")
			self._daily_update_labels()
			return
		text = self.tree.item(item_id, 'text')
		vals = self.tree.item(item_id, 'values') or []
		priority = vals[1] if len(vals) > 1 else "Medium"
		self.daily_task_label.config(text=f"{text} [{priority}]")
		self._daily_update_labels()

	def _daily_is_incomplete(self, item_id):
		vals = self.tree.item(item_id, 'values') or []
		status = vals[0] if len(vals) > 0 else "[ ]"
		return status not in ("[x]", "[✓]")

	def _daily_pick_next_task(self):
		# Gather all incomplete tasks and sort by priority High > Medium > Low,
		# honoring filters for category and included priorities
		candidates = []
		# Determine category scope
		cat_filter = getattr(self, 'daily_cat_var', None).get() if hasattr(self, 'daily_cat_var') else "All"
		cat_ids = []
		if cat_filter and cat_filter != "All" and cat_filter in self.categories:
			cat_ids = [self.categories[cat_filter]]
		else:
			cat_ids = list(self.categories.values())
		# Determine included priorities
		inc_high = getattr(self, 'daily_inc_high', None).get() if hasattr(self, 'daily_inc_high') else True
		inc_med = getattr(self, 'daily_inc_med', None).get() if hasattr(self, 'daily_inc_med') else True
		inc_low = getattr(self, 'daily_inc_low', None).get() if hasattr(self, 'daily_inc_low') else True
		include_set = set()
		if inc_high: include_set.add("High")
		if inc_med: include_set.add("Medium")
		if inc_low: include_set.add("Low")
		if not include_set:
			include_set = {"High", "Medium", "Low"}
		for cat_id in cat_ids:
			for child in self.tree.get_children(cat_id):
				if self._daily_is_incomplete(child):
					vals = self.tree.item(child, 'values') or []
					priority = vals[1] if len(vals) > 1 else "Medium"
					if priority not in include_set:
						continue
					order = self._priority_order(priority)
					candidates.append((order, child))
		if not candidates:
			self._daily_set_current(None)
			return
		# lower order should be higher priority if _priority_order returns 0/1/2; ensure sorting
		candidates.sort(key=lambda x: x[0])
		next_item = candidates[0][1]
		self._daily_set_current(next_item)

	def _daily_complete_task(self):
		# mark current complete and pick next
		if not self._daily_current_task:
			self._daily_pick_next_task()
			return
		# accumulate any running time before completion
		self._daily_pause()
		# record completion in the Daily list
		try:
			text = self.tree.item(self._daily_current_task, 'text')
			total = int(self.task_time_spent.get(self._daily_current_task, 0))
			self.daily_done_list.insert('end', f"✓ {text} ({self._daily_format(total)})")
		except Exception:
			pass
		# Temporarily select the item to reuse toggle_complete
		prev_sel = self.tree.selection()
		try:
			self.tree.selection_set((self._daily_current_task,))
			self.toggle_complete()
		finally:
			# restore previous selection
			try:
				self.tree.selection_set(prev_sel)
			except Exception:
				pass
		# pick next
		self._daily_pick_next_task()
		# Auto-start the next task
		if self._daily_current_task:
			self._daily_start()

	def _daily_on_mode_change(self):
		# Reset counters appropriately when switching modes
		self._daily_pause()
		self._daily_elapsed = 0.0
		self._pomodoro_remaining = 0
		self._pomodoro_state = "work"
		self._daily_update_labels()

	def _setup_theme_editor(self):
		"""Set up the theme editor tab UI."""
		# Theme editor title
		title_label = tk.Label(self.theme_editor_tab, text="Custom Theme Editor", font=("", 14, "bold"))
		title_label.pack(pady=(10, 5))
		
		# Current theme name input
		name_frame = tk.Frame(self.theme_editor_tab)
		name_frame.pack(padx=10, pady=5, fill="x")
		tk.Label(name_frame, text="Theme Name:").pack(side="left", padx=(0, 5))
		self.custom_theme_name_var = tk.StringVar(value="Custom")
		self.custom_theme_name_entry = tk.Entry(name_frame, textvariable=self.custom_theme_name_var, width=20)
		self.custom_theme_name_entry.pack(side="left")
		
		# Set up Daily tab UI
		self._setup_daily_tab()

		# Color pickers frame
		colors_frame = tk.Frame(self.theme_editor_tab)
		colors_frame.pack(padx=10, pady=10, fill="both", expand=True)
		
		# Store color entries
		self.theme_color_vars = {}

		# Tip label
		tk.Label(colors_frame, text="Tip: Set 'Gradient End' to enable a gradient. Leave blank or same as base for solid.",
				anchor="w").pack(fill="x", pady=(0, 8))

		def add_color_row(parent, key, label_text):
			row_frame = tk.Frame(parent)
			row_frame.pack(fill="x", pady=2)
			
			lbl = tk.Label(row_frame, text=label_text + ":", width=20, anchor="w")
			lbl.pack(side="left", padx=(0, 5))
			
			var = tk.StringVar(value=self.current_theme.get(key, "#ffffff"))
			self.theme_color_vars[key] = var
			
			entry = tk.Entry(row_frame, textvariable=var, width=10)
			entry.pack(side="left", padx=(0, 5))
			
			preview = tk.Label(row_frame, text="      ", bg=var.get(), relief="raised", bd=2,
						   width=4, cursor="hand2")
			preview.pack(side="left")
			preview.bind("<Button-1>", lambda e, k=key: self._pick_theme_color(k))
			var.trace_add("write", lambda *args, p=preview, v=var: p.config(bg=v.get()))

		# Grouped sections for clearer organization
		sections = [
			("Background", [
				("bg", "Background"),
				("bg_gradient", "Background Gradient End"),
				("fg", "Foreground Text"),
			]),
			("Buttons", [
				("button_bg", "Button Background"),
				("button_bg_gradient", "Button Gradient End"),
				("button_fg", "Button Text"),
			]),
			("List", [
				("listbox_bg", "List Background"),
				("listbox_bg_gradient", "List Gradient End"),
				("listbox_fg", "List Text"),
			]),
			("Entry", [
				("entry_bg", "Entry Background"),
				("entry_bg_gradient", "Entry Gradient End"),
				("entry_fg", "Entry Text"),
			]),
		]

		for title, fields in sections:
			lf = tk.LabelFrame(colors_frame, text=title)
			lf.pack(fill="x", pady=6)
			for key, label_text in fields:
				add_color_row(lf, key, label_text)
		
		# Buttons frame
		btn_frame = tk.Frame(self.theme_editor_tab)
		btn_frame.pack(padx=10, pady=(10, 15), fill="x")
		
		tk.Button(btn_frame, text="Load from Current Theme", width=22, 
				 command=self._load_current_theme_to_editor).pack(side="left", padx=3)
		tk.Button(btn_frame, text="Preview Theme", width=15, 
				 command=self._preview_custom_theme).pack(side="left", padx=3)
		tk.Button(btn_frame, text="Save Theme", width=15, 
				 command=self._save_custom_theme).pack(side="left", padx=3)
		tk.Button(btn_frame, text="Delete Theme", width=15, 
				 command=self._delete_custom_theme).pack(side="left", padx=3)
		tk.Button(btn_frame, text="Import Theme File", width=15, 
				 command=self._import_theme_file).pack(side="left", padx=3)

	def _pick_theme_color(self, key):
		"""Open quick 1-click color picker for theme color."""
		self._open_quick_color_picker(key)

	def _hsv_to_hex(self, h, s, v):
		"""Convert HSV (0-360,0-1,0-1) to #RRGGBB."""
		h = float(h) % 360
		s = max(0.0, min(1.0, float(s)))
		v = max(0.0, min(1.0, float(v)))
		c = v * s
		x = c * (1 - abs((h / 60.0) % 2 - 1))
		m = v - c
		if 0 <= h < 60:
			r, g, b = c, x, 0
		elif 60 <= h < 120:
			r, g, b = x, c, 0
		elif 120 <= h < 180:
			r, g, b = 0, c, x
		elif 180 <= h < 240:
			r, g, b = 0, x, c
		elif 240 <= h < 300:
			r, g, b = x, 0, c
		else:
			r, g, b = c, 0, x
		r = int((r + m) * 255)
		g = int((g + m) * 255)
		b = int((b + m) * 255)
		return f"#{r:02x}{g:02x}{b:02x}"

	def _open_quick_color_picker(self, key):
		"""Show a lightweight, 1-click color picker with a hue/sat field; click sets color immediately."""
		picker = tk.Toplevel(self.root)
		picker.title("Pick Color")
		picker.transient(self.root)
		picker.resizable(False, False)
		# Make sure it appears above the main window
		try:
			picker.attributes("-topmost", True)
		except Exception:
			pass
		picker.lift()
		# Dimensions
		W, H = 360, 180  # hue across width, saturation down height (value fixed at 1)
		cv = tk.Canvas(picker, width=W, height=H, highlightthickness=0, bd=0, cursor="crosshair")
		cv.pack()

		# Draw a reliable hue-saturation mosaic using rectangles (fast and portable)
		BLOCK = 8  # block size in pixels
		cols = max(1, W // BLOCK)
		rws = max(1, H // BLOCK)
		for by in range(rws):
			s = by / (rws - 1) if rws > 1 else 0
			for bx in range(cols):
				h = (bx / (cols - 1)) * 360.0 if cols > 1 else 0
				color_hex = self._hsv_to_hex(h, s, 1.0)
				x0 = bx * BLOCK
				y0 = by * BLOCK
				x1 = min(W, x0 + BLOCK)
				y1 = min(H, y0 + BLOCK)
				cv.create_rectangle(x0, y0, x1, y1, outline=color_hex, fill=color_hex)

		def on_click(event):
			x = max(0, min(W - 1, event.x))
			y = max(0, min(H - 1, event.y))
			h = (x / (W - 1)) * 360.0
			s = y / (H - 1)
			color = self._hsv_to_hex(h, s, 1.0)
			self.theme_color_vars[key].set(color)
			picker.destroy()

		cv.bind("<Button-1>", on_click)
		picker.bind("<Escape>", lambda e: picker.destroy())
		# Position near mouse and show now
		picker.update_idletasks()
		try:
			picker.geometry(f"+{self.root.winfo_pointerx()}+{self.root.winfo_pointery()}")
		except Exception:
			picker.geometry("+200+200")
	
	def _init_settings(self):
		"""Initialize settings with default values."""
		self.settings = {
			"ai_task_prefix": True,  # Add # prefix to AI-generated tasks
			"ai_smart_categories": True,  # Automatically categorize AI tasks
		}
		# Load settings from file if exists
		self._load_settings()
	
	def _load_settings(self):
		"""Load settings from file."""
		settings_file = os.path.join(DATA_DIR, "todo_settings.json")
		if os.path.exists(settings_file):
			try:
				with open(settings_file, 'r', encoding='utf-8') as f:
					loaded = json.load(f)
					self.settings.update(loaded)
			except Exception:
				pass
	
	def _save_settings(self):
		"""Save settings to file."""
		settings_file = os.path.join(DATA_DIR, "todo_settings.json")
		try:
			with open(settings_file, 'w', encoding='utf-8') as f:
				json.dump(self.settings, f, indent=2)
		except Exception:
			pass
	
	def _setup_settings_tab(self):
		"""Set up the Settings tab."""
		# Main container
		main_frame = tk.Frame(self.settings_tab)
		main_frame.pack(fill="both", expand=True, padx=20, pady=20)
		
		# Title
		title_label = tk.Label(main_frame, text="Settings", font=("", 16, "bold"))
		title_label.pack(pady=(0, 20))
		
		# AI Tasks Settings Section
		ai_frame = tk.LabelFrame(main_frame, text="AI Task Settings", font=("", 11, "bold"))
		ai_frame.pack(fill="x", pady=(0, 15))
		
		# AI Task Prefix setting
		prefix_frame = tk.Frame(ai_frame)
		prefix_frame.pack(fill="x", padx=15, pady=10)
		
		self.ai_prefix_var = tk.BooleanVar(value=self.settings.get("ai_task_prefix", True))
		prefix_check = tk.Checkbutton(prefix_frame, text="Add '#' prefix to AI-generated tasks",
									  variable=self.ai_prefix_var, font=("", 10),
									  command=self._on_setting_change)
		prefix_check.pack(anchor="w")
		
		prefix_desc = tk.Label(prefix_frame, text="When enabled, AI-generated tasks will start with '#' (e.g., '# Research topic')",
							   font=("", 9), fg="#666666", wraplength=500, justify="left")
		prefix_desc.pack(anchor="w", padx=20, pady=(5, 0))
		
		# Smart Categories setting
		category_frame = tk.Frame(ai_frame)
		category_frame.pack(fill="x", padx=15, pady=10)
		
		self.ai_smart_cat_var = tk.BooleanVar(value=self.settings.get("ai_smart_categories", True))
		category_check = tk.Checkbutton(category_frame, text="Automatically categorize AI tasks",
										variable=self.ai_smart_cat_var, font=("", 10),
										command=self._on_setting_change)
		category_check.pack(anchor="w")
		
		category_desc = tk.Label(category_frame, 
								text="When enabled, AI tasks are placed in relevant categories (Fitness, Learning, etc.) instead of 'AI Generated'",
								font=("", 9), fg="#666666", wraplength=500, justify="left")
		category_desc.pack(anchor="w", padx=20, pady=(5, 0))
		
		# General Settings Section (placeholder for future settings)
		general_frame = tk.LabelFrame(main_frame, text="General Settings", font=("", 11, "bold"))
		general_frame.pack(fill="x", pady=(0, 15))
		
		general_info = tk.Label(general_frame, text="More settings coming soon...",
							   font=("", 9), fg="#666666")
		general_info.pack(padx=15, pady=15)
		
		# Save button
		save_btn = tk.Button(main_frame, text="Save Settings", width=20, font=("", 10, "bold"),
							command=self._save_settings_and_confirm)
		save_btn.pack(pady=(10, 0))
	
	def _on_setting_change(self):
		"""Handle setting change."""
		self.settings["ai_task_prefix"] = self.ai_prefix_var.get()
		self.settings["ai_smart_categories"] = self.ai_smart_cat_var.get()
	
	def _save_settings_and_confirm(self):
		"""Save settings and show confirmation."""
		self._save_settings()
		messagebox.showinfo("Settings", "Settings saved successfully!")
	
	def _setup_avatar_room_tab(self):
		"""Set up the Avatar Room tab with customizable avatar and virtual environment."""
		# Initialize avatar state with normalized coordinates (0.0 to 1.0)
		self._avatar_state = {
			"x": 0.5,  # Center x position (normalized)
			"y": 0.5,  # Center y position (normalized)
			"direction": "down",  # down, up, left, right
			"hat": "baseball_cap",
			"shirt": "t_shirt_blue",
			"pants": "jeans_blue"
		}
		
		# Load saved avatar settings if they exist
		if hasattr(self, 'settings') and 'avatar' in self.settings:
			self._avatar_state.update(self.settings['avatar'])
		# Load saved XP data
		if hasattr(self, 'settings'):
			self.xp = self.settings.get('xp', 0)
			self.level = self.settings.get('level', 1)
			self.tasks_completed = self.settings.get('tasks_completed', 0)
			self.unlocked_items = set(self.settings.get('unlocked_items', []))
			self.pets = self.settings.get('pets', [])
			self._placed_items = self.settings.get('placed_items', [])
		
		
		# Main container
		main_frame = tk.Frame(self.avatar_room_tab)
		main_frame.pack(fill="both", expand=True, padx=10, pady=10)
		
		# Title
		title_label = tk.Label(main_frame, text="🎮 Avatar Room", font=("", 14, "bold"))
		title_label.pack(pady=(0, 10))
		# XP and Level Display
		xp_frame = tk.Frame(main_frame)
		xp_frame.pack(fill="x", pady=(0, 10))
		
		# Level and Stats
		stats_text = f"Level {self.level} | Tasks Completed: {self.tasks_completed} | XP: {self.xp}"
		self.xp_stats_label = tk.Label(xp_frame, text=stats_text, font=("", 10, "bold"))
		self.xp_stats_label.pack(pady=(0, 5))
		
		# XP Progress Bar
		xp_bar_frame = tk.Frame(xp_frame)
		xp_bar_frame.pack(fill="x", padx=50)
		
		self.xp_bar_canvas = tk.Canvas(xp_bar_frame, height=25, bg="#e0e0e0", highlightthickness=1, highlightbackground="#888")
		self.xp_bar_canvas.pack(fill="x")
		
		self._update_xp_display()
		
		
		# Create two columns: canvas on left, customization on right
		content_frame = tk.Frame(main_frame)
		content_frame.pack(fill="both", expand=True)
		
		# Left side - Canvas for room
		canvas_frame = tk.Frame(content_frame)
		canvas_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
		
		canvas_label = tk.Label(canvas_frame, text="Your Avatar Room (Use Arrow Keys to Move)", font=("", 10))
		canvas_label.pack(pady=(0, 5))
		
		# Canvas for rendering room and avatar (responsive to window size)
		self.avatar_canvas = tk.Canvas(canvas_frame, bg="#f0f0f0", highlightthickness=2)
		self.avatar_canvas.pack(fill="both", expand=True)
		
		# Bind canvas resize event with heavy debouncing to prevent resize flashing
		self._resize_debounce_id = None
		def _on_canvas_resize(event):
			if hasattr(self, '_resize_debounce_id') and self._resize_debounce_id:
				self.avatar_canvas.after_cancel(self._resize_debounce_id)
			# Don't redraw on resize - let the animation loop handle it
			# This prevents flashing during window resize
			self._resize_debounce_id = None
		self.avatar_canvas.bind("<Configure>", _on_canvas_resize)

		# Initialize animation states for avatar/scene
		import time, random
		self._last_user_move_time = time.time()
		self._avatar_auto_move = True
		self._avatar_walk_phase = 0.0  # for bobbing/swing
		# Blink state: ticks to next blink and current blink progress (0-1)
		self._blink_state = {
			"ticks_to_next": random.randint(20, 50),  # 2-5 seconds at 100ms tick
			"progress": 0.0,
			"active": False
		}
		# Random event state
		self._random_event = {
			"type": None,
			"ticks_left": 0
		}
		# Window animation state
		self._scene_window = {
			"sun_t": 0.0,
			"clouds": [
				{"x": -0.2, "y": 0.2, "speed": 0.005},
				{"x": 0.3, "y": 0.35, "speed": 0.003},
				{"x": 0.8, "y": 0.25, "speed": 0.004}
			]
		}
		
		# Right side - Customization controls with scrollbar
		custom_outer_frame = tk.Frame(content_frame, width=250)
		custom_outer_frame.pack(side="right", fill="both", expand=False)
		custom_outer_frame.pack_propagate(False)
		
		# Scrollable canvas for customization
		custom_canvas = tk.Canvas(custom_outer_frame, highlightthickness=0)
		custom_scrollbar = tk.Scrollbar(custom_outer_frame, orient="vertical", command=custom_canvas.yview)
		custom_frame = tk.Frame(custom_canvas)
		
		custom_frame.bind("<Configure>", lambda e: custom_canvas.configure(scrollregion=custom_canvas.bbox("all")))
		custom_canvas.create_window((0, 0), window=custom_frame, anchor="nw")
		custom_canvas.configure(yscrollcommand=custom_scrollbar.set)
		
		custom_canvas.pack(side="left", fill="both", expand=True)
		custom_scrollbar.pack(side="right", fill="y")
		
		# Enable mousewheel scrolling
		def _on_mousewheel(event):
			custom_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
		custom_canvas.bind_all("<MouseWheel>", _on_mousewheel)
		
		# Customization title
		custom_title = tk.Label(custom_frame, text="Customize Avatar", font=("", 12, "bold"))
		custom_title.pack(pady=(0, 10))
		
		# Collapsible categories state
		self._avatar_sections_expanded = {
			"hats": False,
			"shirts": False,
			"pants": False,
			"pets": False,
			"colors": False
		}
		
		# Hat selection (collapsible)
		hat_header = tk.Frame(custom_frame, relief="raised", borderwidth=1)
		hat_header.pack(fill="x", pady=(0, 2))
		
		self.hat_toggle_btn = tk.Button(hat_header, text="▶ Hats", anchor="w", 
										command=lambda: self._toggle_avatar_section("hats"),
										relief="flat", font=("", 10, "bold"))
		self.hat_toggle_btn.pack(fill="x", padx=5, pady=2)
		
		self.hat_content_frame = tk.Frame(custom_frame)
		# Content initially hidden
		
		self.hat_var = tk.StringVar(value=self._avatar_state["hat"])
		hat_options = [
			("Baseball Cap", "baseball_cap", None),
			("Beanie", "beanie", None),
			("Top Hat", "top_hat", None),
			("Crown", "crown", None),
			("Wizard Hat", "hat_wizard", "hat_wizard"),
			("Sombrero", "hat_sombrero", "hat_sombrero"),
			("Viking Helmet", "hat_viking", "hat_viking"),
			("Halo", "hat_halo", "hat_halo"),
			("No Hat", "none", None)
		]
		for text, value, unlock_key in hat_options:
			is_locked = unlock_key is not None and unlock_key not in self.unlocked_items
			label = f"{text} (Locked)" if is_locked else text
			state = tk.DISABLED if is_locked else tk.NORMAL
			rb = tk.Radiobutton(self.hat_content_frame, text=label, variable=self.hat_var, value=value,
						   command=self._update_avatar_clothing, state=state)
			rb.pack(anchor="w", padx=10)
		
		# Shirt selection (collapsible)
		shirt_header = tk.Frame(custom_frame, relief="raised", borderwidth=1)
		shirt_header.pack(fill="x", pady=(0, 2))
		
		self.shirt_toggle_btn = tk.Button(shirt_header, text="▶ Shirts", anchor="w",
										  command=lambda: self._toggle_avatar_section("shirts"),
										  relief="flat", font=("", 10, "bold"))
		self.shirt_toggle_btn.pack(fill="x", padx=5, pady=2)
		
		self.shirt_content_frame = tk.Frame(custom_frame)
		# Content initially hidden
		
		self.shirt_var = tk.StringVar(value=self._avatar_state["shirt"])
		shirt_options = [
			("Blue T-Shirt", "t_shirt_blue", None),
			("Red T-Shirt", "t_shirt_red", None),
			("Green Hoodie", "hoodie_green", None),
			("Yellow Polo", "polo_yellow", None),
			("Purple Sweater", "sweater_purple", None),
			("Leather Jacket", "shirt_leather_jacket", "shirt_leather_jacket"),
			("Tuxedo", "shirt_tuxedo", "shirt_tuxedo"),
			("Superhero", "shirt_superhero", "shirt_superhero"),
			("Gold Shirt", "shirt_gold", "shirt_gold")
		]
		for text, value, unlock_key in shirt_options:
			is_locked = unlock_key is not None and unlock_key not in self.unlocked_items
			label = f"{text} (Locked)" if is_locked else text
			state = tk.DISABLED if is_locked else tk.NORMAL
			rb = tk.Radiobutton(self.shirt_content_frame, text=label, variable=self.shirt_var, value=value,
						   command=self._update_avatar_clothing, state=state)
			rb.pack(anchor="w", padx=10)
		
		# Pants selection (collapsible)
		pants_header = tk.Frame(custom_frame, relief="raised", borderwidth=1)
		pants_header.pack(fill="x", pady=(0, 2))
		
		self.pants_toggle_btn = tk.Button(pants_header, text="▶ Pants", anchor="w",
										  command=lambda: self._toggle_avatar_section("pants"),
										  relief="flat", font=("", 10, "bold"))
		self.pants_toggle_btn.pack(fill="x", padx=5, pady=2)
		
		self.pants_content_frame = tk.Frame(custom_frame)
		# Content initially hidden
		
		self.pants_var = tk.StringVar(value=self._avatar_state["pants"])
		pants_options = [
			("Blue Jeans", "jeans_blue", None),
			("Black Jeans", "jeans_black", None),
			("Khaki Pants", "khaki", None),
			("Gray Joggers", "joggers_gray", None),
			("Red Shorts", "shorts_red", None),
			("Camo Pants", "pants_camo", "pants_camo"),
			("Rainbow Pants", "pants_rainbow", "pants_rainbow"),
			("Gold Pants", "pants_gold", "pants_gold")
		]
		for text, value, unlock_key in pants_options:
			is_locked = unlock_key is not None and unlock_key not in self.unlocked_items
			label = f"{text} (Locked)" if is_locked else text
			state = tk.DISABLED if is_locked else tk.NORMAL
			rb = tk.Radiobutton(self.pants_content_frame, text=label, variable=self.pants_var, value=value,
						   command=self._update_avatar_clothing, state=state)
			rb.pack(anchor="w", padx=10)

		# Pets selection (collapsible)
		pets_header = tk.Frame(custom_frame, relief="raised", borderwidth=1)
		pets_header.pack(fill="x", pady=(0, 2))
		
		self.pets_toggle_btn = tk.Button(pets_header, text="▶ Pets", anchor="w",
										 command=lambda: self._toggle_avatar_section("pets"),
										 relief="flat", font=("", 10, "bold"))
		self.pets_toggle_btn.pack(fill="x", padx=5, pady=2)
		
		self.pets_content_frame = tk.Frame(custom_frame)
		# Content initially hidden

		self.pet_vars = {}
		present_types = set(p.get("type") for p in (self.pets or []))
		pet_options = [
			("Cat", "pet_cat", None),  # Starter
			("Dog", "pet_dog", None),  # Starter
			("Bird", "pet_bird", "pet_bird"),
			("Dragon", "pet_dragon", "pet_dragon")
		]
		for text, pet_key, unlock_key in pet_options:
			is_starter = unlock_key is None and pet_key in self.STARTER_PETS
			is_unlocked = is_starter or (unlock_key in self.unlocked_items if unlock_key else True)
			label = f"{text} (Locked)" if not is_unlocked else text
			state = tk.NORMAL if is_unlocked else tk.DISABLED
			var = tk.BooleanVar(value=(pet_key in present_types))
			self.pet_vars[pet_key] = var
			cb = tk.Checkbutton(self.pets_content_frame, text=label, variable=var, state=state,
						   command=lambda k=pet_key: self._toggle_pet(k))
			cb.pack(anchor="w", padx=10)
		
		# Room customization (collapsible)
		colors_header = tk.Frame(custom_frame, relief="raised", borderwidth=1)
		colors_header.pack(fill="x", pady=(0, 2))
		
		self.colors_toggle_btn = tk.Button(colors_header, text="▶ Room Customization", anchor="w",
										   command=lambda: self._toggle_avatar_section("colors"),
										   relief="flat", font=("", 10, "bold"))
		self.colors_toggle_btn.pack(fill="x", padx=5, pady=2)
		
		self.colors_content_frame = tk.Frame(custom_frame)
		# Content initially hidden
		
		# Load saved room colors or use defaults
		if hasattr(self, 'settings') and 'room_colors' in self.settings:
			self._room_colors = self.settings['room_colors']
		else:
			self._room_colors = {
				"floor": "#e8dcc0",
				"wall": "#a8a8a8"
			}
		
		# Floor color
		floor_label = tk.Label(self.colors_content_frame, text="Floor Color:", font=("", 9))
		floor_label.pack(anchor="w", padx=10, pady=(5, 0))
		
		floor_color_frame = tk.Frame(self.colors_content_frame)
		floor_color_frame.pack(fill="x", padx=10, pady=(0, 5))
		
		floor_presets = [
			("Beige", "#e8dcc0"),
			("Wood", "#8b7355"),
			("Gray", "#c0c0c0"),
			("White", "#f5f5f5"),
			("Dark Wood", "#654321"),
			("Marble", "#e6e6fa")
		]
		
		for i, (name, color) in enumerate(floor_presets):
			btn = tk.Button(floor_color_frame, text=name, bg=color, width=8,
						   command=lambda c=color: self._set_room_color("floor", c))
			btn.grid(row=i//2, column=i%2, padx=2, pady=2, sticky="ew")
		
		# Wall color
		wall_label = tk.Label(self.colors_content_frame, text="Wall Color:", font=("", 9))
		wall_label.pack(anchor="w", padx=10, pady=(10, 0))
		
		wall_color_frame = tk.Frame(self.colors_content_frame)
		wall_color_frame.pack(fill="x", padx=10, pady=(0, 5))
		
		wall_presets = [
			("Gray", "#a8a8a8"),
			("White", "#f0f0f0"),
			("Cream", "#fff8dc"),
			("Blue", "#b0c4de"),
			("Green", "#98b898"),
			("Pink", "#ffc0cb")
		]
		
		for i, (name, color) in enumerate(wall_presets):
			btn = tk.Button(wall_color_frame, text=name, bg=color, width=8,
						   command=lambda c=color: self._set_room_color("wall", c))
			btn.grid(row=i//2, column=i%2, padx=2, pady=2, sticky="ew")
		
		# Window count
		window_label = tk.Label(self.colors_content_frame, text="Number of Windows:", font=("", 9))
		window_label.pack(anchor="w", padx=10, pady=(10, 0))
		
		# Load saved window count or use default
		if hasattr(self, 'settings') and 'window_count' in self.settings:
			self._window_count = self.settings['window_count']
		else:
			self._window_count = 1
		
		window_count_frame = tk.Frame(self.colors_content_frame)
		window_count_frame.pack(fill="x", padx=10, pady=(0, 5))
		
		for count in [1, 2, 3, 4]:
			btn = tk.Button(window_count_frame, text=str(count), width=4,
						   command=lambda c=count: self._set_window_count(c))
			btn.pack(side="left", padx=2, pady=2)
		
		# Asset Designer button
		asset_designer_label = tk.Label(self.colors_content_frame, text="Custom Assets:", font=("", 9))
		asset_designer_label.pack(anchor="w", padx=10, pady=(10, 0))
		
		asset_designer_btn = tk.Button(self.colors_content_frame, text="🎨 Open Asset Designer", 
									   command=self._open_asset_designer_window,
									   font=("", 9, "bold"))
		asset_designer_btn.pack(fill="x", padx=10, pady=(5, 10))
		
		# Furniture Placement button
		furniture_label = tk.Label(self.colors_content_frame, text="Place Items:", font=("", 9))
		furniture_label.pack(anchor="w", padx=10, pady=(10, 0))
		
		furniture_btn = tk.Button(self.colors_content_frame, text="🛋️ Place Furniture & Decorations", 
									   command=self._open_furniture_window,
									   font=("", 9, "bold"))
		furniture_btn.pack(fill="x", padx=10, pady=(5, 10))
		
		# Movement instructions
		instructions = tk.Label(custom_frame, text="\n⌨️ Controls:\n↑ ↓ ← → Arrow Keys\nto move around",
							   justify="center", font=("", 9))
		instructions.pack(pady=10)
		
		# Bind keyboard controls
		self.avatar_canvas.bind("<Up>", lambda e: self._move_avatar("up"))
		self.avatar_canvas.bind("<Down>", lambda e: self._move_avatar("down"))
		self.avatar_canvas.bind("<Left>", lambda e: self._move_avatar("left"))
		self.avatar_canvas.bind("<Right>", lambda e: self._move_avatar("right"))
		self.avatar_canvas.focus_set()
		
		# Initial room and avatar rendering (use request to avoid double draw)
		self._request_redraw()
		# Start scene animation (pets/window/avatar idle)
		self._animate_pets()
	def _update_xp_display(self):
		"""Update the XP progress bar and stats display."""
		if not hasattr(self, 'xp_bar_canvas'):
			return
		
		# Update stats text
		stats_text = f"Level {self.level} | Tasks Completed: {self.tasks_completed} | XP: {self.xp}"
		self.xp_stats_label.configure(text=stats_text)
		
		# Draw XP bar
		canvas = self.xp_bar_canvas
		canvas.delete("all")
		
		width = canvas.winfo_width()
		if width <= 1:  # Canvas not yet rendered
			width = 500
		
		# Calculate XP progress within current level
		xp_for_current_level = (self.level - 1) * 100
		xp_for_next_level = self.level * 100
		xp_in_level = self.xp - xp_for_current_level
		xp_needed_in_level = 100
		progress = xp_in_level / xp_needed_in_level
		
		# Draw background
		canvas.create_rectangle(0, 0, width, 25, fill="#e0e0e0", outline="")
		
		# Draw progress bar
		bar_width = int(width * progress)
		# Gradient effect - darker at start, lighter at end
		canvas.create_rectangle(0, 0, bar_width, 25, fill="#4CAF50", outline="")
		canvas.create_rectangle(0, 0, bar_width, 12, fill="#66BB6A", outline="")
		
		# Draw text showing XP progress
		text = f"{xp_in_level} / {xp_needed_in_level} XP"
		canvas.create_text(width//2, 12, text=text, font=("", 10, "bold"), fill="#000000")
	
	
	def _draw_avatar_room(self):
		"""Draw the virtual room environment and avatar."""
		canvas = self.avatar_canvas
		# Don't clear here - let animation loop handle it to avoid double-clear flashing
		
		# Get current canvas size (don't call update_idletasks - causes flashing)
		width = canvas.winfo_width()
		height = canvas.winfo_height()
		
		# Use minimum dimensions if canvas hasn't been rendered yet
		if width < 10:
			width = 600
		if height < 10:
			height = 400
		
		# Get custom room colors or use defaults
		if not hasattr(self, '_room_colors'):
			self._room_colors = {"floor": "#e8dcc0", "wall": "#a8a8a8"}
		floor_color = self._room_colors.get("floor", "#e8dcc0")
		wall_color = self._room_colors.get("wall", "#a8a8a8")
		
		# Draw floor
		canvas.create_rectangle(0, 0, width, height, fill=floor_color, outline="")
		
		# Draw floor tiles for depth effect (scale to canvas size)
		# Make tiles slightly darker than base floor color
		import colorsys
		def darken_color(hex_color, factor=0.9):
			# Convert hex to RGB
			hex_color = hex_color.lstrip('#')
			r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
			# Convert to HSV, darken, convert back
			h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
			v = v * factor
			r, g, b = colorsys.hsv_to_rgb(h, s, v)
			return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
		
		tile_color = darken_color(floor_color, 0.85)
		tile_size = max(30, min(50, width // 15))
		for y in range(0, height, tile_size):
			canvas.create_line(0, y, width, y, fill=tile_color, width=1)
		for x in range(0, width, tile_size):
			canvas.create_line(x, 0, x, height, fill=tile_color, width=1)

		# Custom assets: draw floor-covering assets before walls
		self._draw_custom_assets(layer="floor")
		
		# Draw walls (scaled)
		wall_depth = int(height * 0.2)  # 20% of height
		side_wall_width = int(width * 0.08)  # 8% of width
		
		# Calculate wall shading colors
		wall_darker = darken_color(wall_color, 0.7)
		wall_outline = darken_color(wall_color, 0.6)
		
		# Back wall
		canvas.create_rectangle(0, 0, width, wall_depth, fill=wall_color, outline=wall_outline, width=2)
		# Side walls (perspective) - extend to bottom and beyond
		# Left wall extends from top-left corner down past the bottom
		canvas.create_polygon(0, 0, side_wall_width, wall_depth, side_wall_width, height + 100, 0, height + 100, 
							 fill=wall_darker, outline=wall_outline, width=2)
		# Right wall extends from top-right corner down past the bottom
		canvas.create_polygon(width, 0, width - side_wall_width, wall_depth, width - side_wall_width, height + 100, width, height + 100,
							 fill=wall_darker, outline=wall_outline, width=2)
		
		# Draw furniture/decorations (scaled proportionally)
		# Plant in corner
		plant_x = int(width * 0.12)
		plant_y = int(height * 0.75)
		plant_size = int(min(width, height) * 0.067)
		canvas.create_oval(plant_x, plant_y, plant_x + plant_size, plant_y + plant_size, 
						  fill="#6b8e23", outline="#556b2f", width=2)
		canvas.create_rectangle(plant_x + plant_size//4, plant_y + plant_size, 
							   plant_x + 3*plant_size//4, plant_y + int(plant_size * 1.5), 
							   fill="#8b4513", outline="#654321", width=1)
		
		# Table
		table_x = int(width * 0.75)
		table_y = int(height * 0.7)
		table_w = int(width * 0.13)
		table_h = int(height * 0.05)
		canvas.create_rectangle(table_x, table_y, table_x + table_w, table_y + table_h, 
							   fill="#8b4513", outline="#654321", width=2)
		# Table legs
		leg_w = int(table_w * 0.125)
		leg_h = int(height * 0.1)
		canvas.create_rectangle(table_x + leg_w, table_y + table_h, 
							   table_x + 2*leg_w, table_y + table_h + leg_h,
							   fill="#654321", outline="#4a2f1a", width=1)
		canvas.create_rectangle(table_x + table_w - 2*leg_w, table_y + table_h,
							   table_x + table_w - leg_w, table_y + table_h + leg_h,
							   fill="#654321", outline="#4a2f1a", width=1)
		
		# Windows on back wall (1-4 windows equally spaced)
		if not hasattr(self, '_window_count'):
			self._window_count = 1
		
		num_windows = self._window_count
		window_h = int(wall_depth * 0.5)
		window_y = int(wall_depth * 0.2)
		
		# Fixed window width (same size for all windows)
		window_w = int(width * 0.15)  # Each window is 15% of width
		
		# Calculate spacing to spread windows equally across the wall
		if num_windows == 1:
			# Single window centered
			start_x = (width - window_w) // 2
			spacing = 0
		else:
			# Multiple windows: calculate spacing to spread them evenly
			# Total space for windows
			total_window_width = num_windows * window_w
			# Remaining space for gaps (including margins)
			remaining_space = width - total_window_width
			# Divide remaining space into (num_windows + 1) gaps
			spacing = remaining_space // (num_windows + 1)
			start_x = spacing
		
		for i in range(num_windows):
			window_x = start_x + i * (window_w + spacing)
			
			# Draw sky background first
			canvas.create_rectangle(window_x, window_y, window_x + window_w, window_y + window_h,
								   fill="#87ceeb", outline="")
			
			# Draw animated sun and clouds (clipped to window)
			if hasattr(self, '_scene_window'):
				# Only draw sun in the middle window (or first window if only 1)
				if i == num_windows // 2:
					sun_t = self._scene_window.get("sun_t", 0.0)
					# Sun moves in an arc across the window
					sun_x = window_x + int(window_w * (0.2 + 0.6 * sun_t))
					sun_y = window_y + int(window_h * (0.3 + 0.2 * abs(sun_t - 0.5)))
					sun_r = int(min(window_w, window_h) * 0.15)
					# Only draw sun if it's within window bounds
					if window_x <= sun_x <= window_x + window_w and window_y <= sun_y <= window_y + window_h:
						canvas.create_oval(sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r, 
										  fill="#ffff00", outline="#ffa500", width=1)
				
				# Draw different clouds for each window
				clouds = self._scene_window.get("clouds", [])
				# Each window gets a different subset of clouds based on its index
				for cloud_idx, cloud in enumerate(clouds):
					# Distribute clouds across windows (cloud 0 -> window 0, cloud 1 -> window 1, etc., wrapping)
					if cloud_idx % num_windows != i:
						continue
					
					cloud_x_norm = cloud["x"]
					# Only draw clouds that are within or near the window (0 to 1 range)
					if -0.3 <= cloud_x_norm <= 1.3:
						cloud_x = window_x + int(window_w * cloud_x_norm)
						cloud_y = window_y + int(window_h * cloud.get("y", 0.25))
						cloud_w = int(window_w * 0.2)
						cloud_h = int(window_h * 0.15)
						
						# Clip cloud components to window bounds
						x1 = max(window_x, cloud_x)
						x2 = min(window_x + window_w, cloud_x + cloud_w)
						y1 = max(window_y, cloud_y - cloud_h//3)
						y2 = min(window_y + window_h, cloud_y + cloud_h)
						
						# Only draw if visible within window
						if x1 < x2 and y1 < y2:
							# Simple cloud shape (3 circles) - only draw portions inside window
							if cloud_x + cloud_w//2 > window_x and cloud_x < window_x + window_w:
								canvas.create_oval(max(window_x, cloud_x), max(window_y, cloud_y), 
												  min(window_x + window_w, cloud_x + cloud_w//2), 
												  min(window_y + window_h, cloud_y + cloud_h), 
												  fill="#ffffff", outline="")
							if cloud_x + 3*cloud_w//4 > window_x and cloud_x + cloud_w//4 < window_x + window_w:
								canvas.create_oval(max(window_x, cloud_x + cloud_w//4), 
												  max(window_y, cloud_y - cloud_h//3), 
												  min(window_x + window_w, cloud_x + 3*cloud_w//4), 
												  min(window_y + window_h, cloud_y + 2*cloud_h//3), 
												  fill="#ffffff", outline="")
							if cloud_x + cloud_w > window_x and cloud_x + cloud_w//2 < window_x + window_w:
								canvas.create_oval(max(window_x, cloud_x + cloud_w//2), 
												  max(window_y, cloud_y), 
												  min(window_x + window_w, cloud_x + cloud_w), 
												  min(window_y + window_h, cloud_y + cloud_h), 
												  fill="#ffffff", outline="")
			
			# Window frame on top
			canvas.create_rectangle(window_x, window_y, window_x + window_w, window_y + window_h,
								   fill="", outline="#4682b4", width=3)
			# Window panes
			canvas.create_line(window_x + window_w//2, window_y, window_x + window_w//2, window_y + window_h,
							  fill="#4682b4", width=2)
			canvas.create_line(window_x, window_y + window_h//2, window_x + window_w, window_y + window_h//2,
							  fill="#4682b4", width=2)

		# Custom assets: posters on wall, then rugs/furniture on floor surface
		self._draw_custom_assets(layer="wall")
		
		# Draw placed built-in items (posters on wall first)
		self._draw_placed_items(layer="poster")
		
		self._draw_custom_assets(layer="surface")
		
		# Draw placed built-in items (rugs and furniture)
		self._draw_placed_items(layer="rug")
		self._draw_placed_items(layer="furniture")

		# Draw avatar and pets above rugs/furniture
		self._draw_avatar()
		self._draw_pets()
	
	def _draw_placed_items(self, layer=None):
		"""Draw placed built-in furniture/rug/poster items."""
		if not hasattr(self, '_placed_items') or not self._placed_items:
			return
		
		canvas = self.avatar_canvas
		width = canvas.winfo_width() if canvas.winfo_width() > 10 else 600
		height = canvas.winfo_height() if canvas.winfo_height() > 10 else 400
		
		for item in self._placed_items:
			category = item.get("category", "furniture")
			
			# Skip if not matching layer filter
			if layer and category != layer:
				continue
			
			# Get item properties
			x_norm = item.get("x", 0.5)
			y_norm = item.get("y", 0.5)
			size_norm = item.get("size", 0.1)
			color = item.get("color", "#888")
			name = item.get("name", "Item")
			
			# Convert to pixel coordinates
			x = int(width * x_norm)
			y = int(height * y_norm)
			size = int(min(width, height) * size_norm)
			
			# Draw based on category and name
			if category == "rug":
				if "Round" in name:
					canvas.create_oval(x - size, y - size, x + size, y + size, 
									 fill=color, outline=self._darken_hex(color, 0.7), width=2)
					# Add pattern
					canvas.create_oval(x - size//2, y - size//2, x + size//2, y + size//2, 
									 fill="", outline=self._darken_hex(color, 0.5), width=1)
				else:
					canvas.create_rectangle(x - size, y - size, x + size, y + size, 
										  fill=color, outline=self._darken_hex(color, 0.7), width=2)
					# Add pattern
					for i in range(-size, size, size//3):
						canvas.create_line(x - size, y + i, x + size, y + i, 
										 fill=self._darken_hex(color, 0.8), width=1)
			
			elif category == "furniture":
				if "Table" in name:
					# Table top
					table_h = size // 3
					canvas.create_rectangle(x - size, y - table_h, x + size, y + table_h, 
										  fill=color, outline=self._darken_hex(color, 0.6), width=2)
					# Table legs
					leg_w = size // 4
					leg_h = size
					canvas.create_rectangle(x - size + leg_w, y + table_h, 
										  x - size + 2*leg_w, y + table_h + leg_h,
										  fill=self._darken_hex(color, 0.7), outline=self._darken_hex(color, 0.5), width=1)
					canvas.create_rectangle(x + size - 2*leg_w, y + table_h,
										  x + size - leg_w, y + table_h + leg_h,
										  fill=self._darken_hex(color, 0.7), outline=self._darken_hex(color, 0.5), width=1)
				
				elif "Bookshelf" in name:
					# Bookshelf frame
					canvas.create_rectangle(x - size, y - size, x + size, y + size, 
										  fill=color, outline=self._darken_hex(color, 0.6), width=2)
					# Shelves
					for i in range(3):
						shelf_y = y - size + (i + 1) * (2 * size // 4)
						canvas.create_line(x - size, shelf_y, x + size, shelf_y, 
										 fill=self._darken_hex(color, 0.5), width=2)
					# Books
					import random
					random.seed(hash(name + str(x_norm) + str(y_norm)))  # Consistent colors
					for shelf in range(2):
						shelf_y = y - size + (shelf + 1) * (2 * size // 4)
						book_x = x - size + size // 4
						for _ in range(4):
							book_color = random.choice(["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff"])
							canvas.create_rectangle(book_x, shelf_y - size//6, 
												  book_x + size//6, shelf_y, 
												  fill=book_color, outline="#000", width=1)
							book_x += size // 5
				
				elif "Chair" in name:
					# Chair seat
					canvas.create_rectangle(x - size, y, x + size, y + size, 
										  fill=color, outline=self._darken_hex(color, 0.6), width=2)
					# Chair back
					canvas.create_rectangle(x - size, y - size, x + size, y, 
										  fill=color, outline=self._darken_hex(color, 0.6), width=2)
				
				elif "Plant" in name:
					# Plant leaves
					canvas.create_oval(x - size, y - size, x + size, y + size//2, 
									 fill="#6b8e23", outline="#556b2f", width=2)
					# Pot
					canvas.create_polygon(x - size//2, y + size//2, 
										x + size//2, y + size//2,
										x + size//3, y + size,
										x - size//3, y + size,
										fill="#8b4513", outline="#654321", width=2)
				
				elif "Sofa" in name:
					# Sofa seat
					canvas.create_rectangle(x - size, y - size//2, x + size, y + size, 
										  fill=color, outline=self._darken_hex(color, 0.6), width=2)
					# Sofa back
					canvas.create_rectangle(x - size, y - size, x + size, y - size//2, 
										  fill=color, outline=self._darken_hex(color, 0.6), width=2)
					# Armrests
					canvas.create_rectangle(x - size, y - size//2, x - size + size//4, y + size, 
										  fill=self._darken_hex(color, 0.8), outline=self._darken_hex(color, 0.6), width=1)
					canvas.create_rectangle(x + size - size//4, y - size//2, x + size, y + size, 
										  fill=self._darken_hex(color, 0.8), outline=self._darken_hex(color, 0.6), width=1)
				
				elif "Desk" in name:
					# Desk top
					desk_h = size // 3
					canvas.create_rectangle(x - size, y - desk_h, x + size, y + desk_h, 
										  fill=color, outline=self._darken_hex(color, 0.6), width=2)
					# Drawers on left
					drawer_w = size // 3
					drawer_h = size // 4
					for i in range(2):
						drawer_y = y + desk_h + i * drawer_h
						canvas.create_rectangle(x - size, drawer_y, x - size + drawer_w, drawer_y + drawer_h,
											  fill=self._darken_hex(color, 0.8), outline=self._darken_hex(color, 0.6), width=1)
						# Drawer handle
						canvas.create_rectangle(x - size + drawer_w//2 - 3, drawer_y + drawer_h//2 - 2,
											  x - size + drawer_w//2 + 3, drawer_y + drawer_h//2 + 2,
											  fill="#888", outline="#000", width=1)
					# Legs on right
					canvas.create_rectangle(x + size - drawer_w, y + desk_h, 
										  x + size - drawer_w + size//6, y + size,
										  fill=self._darken_hex(color, 0.7), outline=self._darken_hex(color, 0.5), width=1)
			
			elif category == "poster":
				# Poster frame
				canvas.create_rectangle(x - size, y - size, x + size, y + size, 
									  fill=color, outline="#000", width=3)
				
				# Poster content
				if "Star" in name:
					import math
					points = []
					for i in range(10):
						angle = math.pi / 2 + i * 2 * math.pi / 10
						r = size * 0.4 if i % 2 == 0 else size * 0.7
						px = x + r * math.cos(angle)
						py = y - r * math.sin(angle)
						points.extend([px, py])
					canvas.create_polygon(points, fill="#fff", outline="#fff")
				
				elif "Heart" in name:
					canvas.create_text(x, y, text="♥", font=("", int(size * 1.8)), fill="#fff")
				
				elif "Moon" in name:
					canvas.create_oval(x - size//2, y - size//2, x + size//2, y + size//2, 
									 fill="#fff", outline="")
					canvas.create_oval(x - size//4, y - size//2, x + size//2 + size//4, y + size//2, 
									 fill=color, outline="")
				
				elif "Sun" in name:
					canvas.create_oval(x - size//2, y - size//2, x + size//2, y + size//2, 
									 fill="#fff", outline="")
					# Sun rays
					for i in range(8):
						angle = i * math.pi / 4
						x1 = x + size * 0.6 * math.cos(angle)
						y1 = y + size * 0.6 * math.sin(angle)
						x2 = x + size * 0.9 * math.cos(angle)
						y2 = y + size * 0.9 * math.sin(angle)
						canvas.create_line(x1, y1, x2, y2, fill="#fff", width=2)
				
				elif "Music" in name:
					canvas.create_text(x, y, text="♪♫", font=("", int(size * 1.5)), fill="#fff")
	
	def _darken_hex(self, hex_color, factor=0.7):
		"""Darken a hex color by a factor."""
		import colorsys
		hex_color = hex_color.lstrip('#')
		r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
		h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
		v = v * factor
		r, g, b = colorsys.hsv_to_rgb(h, s, v)
		return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
	
	def _draw_custom_assets(self, layer=None):
		"""Draw custom PNG/GIF assets on the avatar room canvas.
		layer controls which categories render:
		- "floor": Floor assets stretched across the floor area
		- "surface": Rugs and Furniture (entities walk over them)
		- "wall": Posters on the back wall
		- None: all assets (fallback)
		"""
		if not hasattr(self, 'custom_assets') or not self.custom_assets:
			return
		
		canvas = self.avatar_canvas
		width = canvas.winfo_width() if canvas.winfo_width() > 10 else 600
		height = canvas.winfo_height() if canvas.winfo_height() > 10 else 400
		
		try:
			from PIL import Image, ImageTk
			
			# Keep references to prevent garbage collection
			if not hasattr(self, '_asset_room_images'):
				self._asset_room_images = []
			self._asset_room_images.clear()
			
			# Determine allowed categories based on layer
			if layer == "floor":
				allowed = {"Floor"}
			elif layer == "surface":
				allowed = {"Rug", "Furniture"}
			elif layer == "wall":
				allowed = {"Poster"}
			else:
				allowed = None  # draw all

			wall_depth = int(height * 0.2)
			for asset in self.custom_assets:
				category = asset.get("category", "Rug")
				if allowed is not None and category not in allowed:
					continue
				filepath = asset.get("path")
				if not filepath:
					continue
				
				x = int(asset.get("x", 0.5) * width)
				y = int(asset.get("y", 0.5) * height)
				scale = asset.get("scale", 1.0)
				
				# Load image
				img = Image.open(filepath)
				
				# Handle animated GIFs
				if asset.get("is_animated", False):
					frame_idx = asset.get("current_frame", 0)
					try:
						img.seek(frame_idx)
					except EOFError:
						asset["current_frame"] = 0
						img.seek(0)
				
				# Convert RGBA if needed (for transparency)
				if img.mode != 'RGBA':
					img = img.convert('RGBA')
				
				# Floor assets stretch across the floor area
				if category == "Floor":
					new_width = int(width)
					new_height = max(1, int(height - wall_depth))
					img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
					photo = ImageTk.PhotoImage(img)
					self._asset_room_images.append(photo)
					canvas.create_image(0, wall_depth, image=photo, anchor="nw")
				else:
					# Scale image normally for rugs/furniture/posters
					new_width = int(img.width * scale)
					new_height = int(img.height * scale)
					img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
					photo = ImageTk.PhotoImage(img)
					self._asset_room_images.append(photo)
					canvas.create_image(x, y, image=photo, anchor="center")
		except ImportError:
			pass  # PIL not installed
		except Exception:
			pass  # Error loading asset
	
	def _draw_avatar(self):
		"""Draw the avatar character with current clothing."""
		canvas = self.avatar_canvas
		
		# Get canvas dimensions
		width = canvas.winfo_width() if canvas.winfo_width() > 10 else 600
		height = canvas.winfo_height() if canvas.winfo_height() > 10 else 400
		
		# Convert normalized position to pixel coordinates
		x = int(self._avatar_state["x"] * width)
		y = int(self._avatar_state["y"] * height)
		
		# Get clothing colors
		shirt_colors = {
			"t_shirt_blue": "#4169e1",
			"t_shirt_red": "#dc143c",
			"hoodie_green": "#32cd32",
			"polo_yellow": "#ffd700",
			"sweater_purple": "#9370db",
			# Unlockable shirts
			"shirt_leather_jacket": "#3b2f2f",
			"shirt_tuxedo": "#111111",
			"shirt_superhero": "#ff0000",
			"shirt_gold": "#daa520"
		}
		pants_colors = {
			"jeans_blue": "#1e90ff",
			"jeans_black": "#2f2f2f",
			"khaki": "#c3b091",
			"joggers_gray": "#808080",
			"shorts_red": "#ff6347",
			# Unlockable pants
			"pants_camo": "#556b2f",
			"pants_rainbow": "#ff69b4",  # approximate
			"pants_gold": "#b8860b"
		}
		
		shirt_color = shirt_colors.get(self._avatar_state["shirt"], "#4169e1")
		pants_color = pants_colors.get(self._avatar_state["pants"], "#1e90ff")
		
		# Shadow (using gray instead of transparent black)
		shadow_y_offset = 0
		if hasattr(self, '_random_event') and self._random_event.get("type") == "jump":
			shadow_y_offset = 0  # Shadow stays on ground during jump
		else:
			shadow_y_offset = 0
		canvas.create_oval(x - 25, y + 45 + shadow_y_offset, x + 25, y + 55 + shadow_y_offset, fill="#c0c0c0", outline="")
		
		# Legs (pants) - apply jump offset to entire body
		body_y_offset = 0
		if hasattr(self, '_random_event') and self._random_event.get("type") == "jump":
			body_y_offset = -8
		
		if "shorts" in self._avatar_state["pants"]:
			# Shorts - shorter legs
			canvas.create_rectangle(x - 12, y + 15 + body_y_offset, x - 2, y + 35 + body_y_offset, fill=pants_color, outline="#000000", width=1)
			canvas.create_rectangle(x + 2, y + 15 + body_y_offset, x + 12, y + 35 + body_y_offset, fill=pants_color, outline="#000000", width=1)
			# Lower legs showing
			canvas.create_rectangle(x - 12, y + 35 + body_y_offset, x - 2, y + 50 + body_y_offset, fill="#fdbcb4", outline="#000000", width=1)
			canvas.create_rectangle(x + 2, y + 35 + body_y_offset, x + 12, y + 50 + body_y_offset, fill="#fdbcb4", outline="#000000", width=1)
		else:
			# Full pants
			canvas.create_rectangle(x - 12, y + 15 + body_y_offset, x - 2, y + 50 + body_y_offset, fill=pants_color, outline="#000000", width=1)
			canvas.create_rectangle(x + 2, y + 15 + body_y_offset, x + 12, y + 50 + body_y_offset, fill=pants_color, outline="#000000", width=1)
		
		# Shoes (with jump animation)
		shoe_y_offset = 0
		if hasattr(self, '_random_event') and self._random_event.get("type") == "jump":
			# Lift avatar for jump
			shoe_y_offset = -8
		
		canvas.create_oval(x - 15, y + 48 + shoe_y_offset, x - 5, y + 54 + shoe_y_offset, fill="#000000", outline="#000000")
		canvas.create_oval(x + 5, y + 48 + shoe_y_offset, x + 15, y + 54 + shoe_y_offset, fill="#000000", outline="#000000")
		
		# Body (shirt) - also needs jump offset
		canvas.create_rectangle(x - 18, y - 10 + body_y_offset, x + 18, y + 20 + body_y_offset, fill=shirt_color, outline="#000000", width=2)
		
		# Arms (with wave animation for random events)
		arm_left_y_offset = 0
		arm_right_y_offset = 0
		if hasattr(self, '_random_event') and self._random_event.get("type") == "wave":
			# Raise right arm for wave
			arm_right_y_offset = -10
		
		canvas.create_rectangle(x - 25, y - 5 + arm_left_y_offset + body_y_offset, x - 18, y + 15 + arm_left_y_offset + body_y_offset, 
							   fill=shirt_color, outline="#000000", width=1)
		canvas.create_rectangle(x + 18, y - 5 + arm_right_y_offset + body_y_offset, x + 25, y + 15 + arm_right_y_offset + body_y_offset, 
							   fill=shirt_color, outline="#000000", width=1)
		# Hands
		canvas.create_oval(x - 28, y + 12 + arm_left_y_offset + body_y_offset, x - 20, y + 20 + arm_left_y_offset + body_y_offset, 
						  fill="#fdbcb4", outline="#000000", width=1)
		canvas.create_oval(x + 20, y + 12 + arm_right_y_offset + body_y_offset, x + 28, y + 20 + arm_right_y_offset + body_y_offset, 
						  fill="#fdbcb4", outline="#000000", width=1)
		
		# Neck
		canvas.create_rectangle(x - 6, y - 15 + body_y_offset, x + 6, y - 10 + body_y_offset, fill="#fdbcb4", outline="#000000", width=1)
		
		# Head (with optional bobbing from walk animation)
		head_y_offset = 0
		if hasattr(self, '_avatar_walk_phase'):
			import math
			head_y_offset = int(2 * math.sin(self._avatar_walk_phase))  # Small bob up/down
		
		head_top = y - 40 + head_y_offset + body_y_offset
		head_bottom = y - 15 + head_y_offset + body_y_offset
		canvas.create_oval(x - 15, head_top, x + 15, head_bottom, fill="#fdbcb4", outline="#000000", width=2)
		
		# Face with blinking animation
		eye_y_top = y - 32 + head_y_offset + body_y_offset
		eye_y_bottom = y - 28 + head_y_offset + body_y_offset
		
		# Check if blinking
		blink_active = False
		blink_progress = 0.0
		if hasattr(self, '_blink_state'):
			blink_active = self._blink_state.get("active", False)
			blink_progress = self._blink_state.get("progress", 0.0)
		
		if blink_active and blink_progress < 0.5:
			# Eyes closing (draw horizontal lines instead of ovals)
			canvas.create_line(x - 8, eye_y_top + 2, x - 4, eye_y_top + 2, fill="#000000", width=2)
			canvas.create_line(x + 4, eye_y_top + 2, x + 8, eye_y_top + 2, fill="#000000", width=2)
		else:
			# Eyes open
			canvas.create_oval(x - 8, eye_y_top, x - 4, eye_y_bottom, fill="#000000", outline="")
			canvas.create_oval(x + 4, eye_y_top, x + 8, eye_y_bottom, fill="#000000", outline="")
		
		# Mouth (change based on random events)
		mouth_y_top = y - 28 + head_y_offset + body_y_offset
		mouth_y_bottom = y - 20 + head_y_offset + body_y_offset
		mouth_style = "smile"  # default
		if hasattr(self, '_random_event'):
			event_type = self._random_event.get("type")
			if event_type == "jump":
				mouth_style = "o"  # Surprised expression
		
		if mouth_style == "o":
			canvas.create_oval(x - 4, mouth_y_top, x + 4, mouth_y_top + 8, fill="#000000", outline="")
		else:
			# Smile
			canvas.create_arc(x - 6, mouth_y_top, x + 6, mouth_y_bottom, start=200, extent=140, outline="#000000", width=2, style="arc")
		
		# Hat
		hat = self._avatar_state["hat"]
		hat_y_offset = head_y_offset + body_y_offset
		if hat == "baseball_cap":
			# Cap top
			canvas.create_arc(x - 16, y - 45 + hat_y_offset, x + 16, y - 30 + hat_y_offset, start=0, extent=180, fill="#ff4500", outline="#000000", width=2, style="pieslice")
			# Bill
			canvas.create_polygon(x - 16, y - 37 + hat_y_offset, x - 25, y - 35 + hat_y_offset, x - 25, y - 33 + hat_y_offset, x - 16, y - 35 + hat_y_offset, fill="#ff4500", outline="#000000", width=1)
		elif hat == "beanie":
			canvas.create_arc(x - 16, y - 48 + hat_y_offset, x + 16, y - 28 + hat_y_offset, start=0, extent=180, fill="#4b0082", outline="#000000", width=2, style="pieslice")
			canvas.create_oval(x - 3, y - 48 + hat_y_offset, x + 3, y - 42 + hat_y_offset, fill="#9370db", outline="#000000", width=1)  # Pom-pom
		elif hat == "top_hat":
			canvas.create_rectangle(x - 12, y - 55 + hat_y_offset, x + 12, y - 40 + hat_y_offset, fill="#000000", outline="#000000", width=2)
			canvas.create_rectangle(x - 16, y - 42 + hat_y_offset, x + 16, y - 38 + hat_y_offset, fill="#000000", outline="#000000", width=2)
		elif hat == "crown":
			# Crown base
			canvas.create_rectangle(x - 14, y - 45 + hat_y_offset, x + 14, y - 38 + hat_y_offset, fill="#ffd700", outline="#ff8c00", width=2)
			# Crown points
			canvas.create_polygon(x - 14, y - 45 + hat_y_offset, x - 10, y - 50 + hat_y_offset, x - 6, y - 45 + hat_y_offset, fill="#ffd700", outline="#ff8c00", width=1)
			canvas.create_polygon(x - 4, y - 45 + hat_y_offset, x, y - 52 + hat_y_offset, x + 4, y - 45 + hat_y_offset, fill="#ffd700", outline="#ff8c00", width=1)
			canvas.create_polygon(x + 6, y - 45 + hat_y_offset, x + 10, y - 50 + hat_y_offset, x + 14, y - 45 + hat_y_offset, fill="#ffd700", outline="#ff8c00", width=1)
			# Jewels
			canvas.create_oval(x - 2, y - 42 + hat_y_offset, x + 2, y - 40 + hat_y_offset, fill="#ff0000", outline="")
		elif hat == "hat_wizard":
			# Wizard hat (purple cone with brim)
			canvas.create_polygon(x - 8, y - 45 + hat_y_offset, x, y - 65 + hat_y_offset, x + 8, y - 45 + hat_y_offset, fill="#6a0dad", outline="#000000", width=2)
			canvas.create_oval(x - 14, y - 42 + hat_y_offset, x + 14, y - 38 + hat_y_offset, fill="#4b0082", outline="#000000", width=2)
		elif hat == "hat_sombrero":
			# Sombrero (wide brim, small top)
			canvas.create_oval(x - 20, y - 40 + hat_y_offset, x + 20, y - 36 + hat_y_offset, fill="#d2b48c", outline="#000000", width=2)
			canvas.create_arc(x - 10, y - 50 + hat_y_offset, x + 10, y - 34 + hat_y_offset, start=0, extent=180, fill="#f4a460", outline="#000000", width=2, style="pieslice")
		elif hat == "hat_viking":
			# Viking helmet (gray with horns)
			canvas.create_arc(x - 16, y - 45 + hat_y_offset, x + 16, y - 30 + hat_y_offset, start=0, extent=180, fill="#c0c0c0", outline="#000000", width=2, style="pieslice")
			canvas.create_polygon(x - 16, y - 40 + hat_y_offset, x - 26, y - 55 + hat_y_offset, x - 20, y - 40 + hat_y_offset, fill="#fff8dc", outline="#000000", width=1)
			canvas.create_polygon(x + 16, y - 40 + hat_y_offset, x + 26, y - 55 + hat_y_offset, x + 20, y - 40 + hat_y_offset, fill="#fff8dc", outline="#000000", width=1)
		elif hat == "hat_halo":
			# Halo (golden ring above head)
			canvas.create_oval(x - 12, y - 58 + hat_y_offset, x + 12, y - 54 + hat_y_offset, fill="#ffd700", outline="#ff8c00", width=2)
		# If hat == "none", draw nothing
	
	def _draw_pets(self):
		"""Draw all pets in the room."""
		if not hasattr(self, 'pets'):
			return
		canvas = self.avatar_canvas
		
		# Get canvas dimensions
		width = canvas.winfo_width() if canvas.winfo_width() > 10 else 600
		height = canvas.winfo_height() if canvas.winfo_height() > 10 else 400
		
		for pet in self.pets:
			# Convert normalized position to pixel coordinates
			x = int(pet.get("x", 0.5) * width)
			y = int(pet.get("y", 0.5) * height)
			ptype = pet.get("type", "pet_cat")
			if ptype == "pet_cat":
				# Body
				canvas.create_oval(x - 12, y - 8, x + 12, y + 8, fill="#ffa500", outline="#000000")
				# Head
				canvas.create_oval(x + 8, y - 10, x + 20, y + 2, fill="#ffa500", outline="#000000")
				# Ears
				canvas.create_polygon(x + 10, y - 10, x + 14, y - 16, x + 18, y - 10, fill="#ffdab9", outline="#000000")
				# Tail
				canvas.create_arc(x - 20, y - 10, x - 4, y + 10, start=200, extent=140, style="arc", outline="#000000", width=2)
			elif ptype == "pet_dog":
				canvas.create_oval(x - 14, y - 9, x + 14, y + 9, fill="#8b4513", outline="#000000")
				canvas.create_oval(x + 6, y - 10, x + 20, y + 4, fill="#a0522d", outline="#000000")
				canvas.create_polygon(x + 8, y - 8, x + 12, y - 14, x + 10, y - 6, fill="#8b4513", outline="#000000")
			elif ptype == "pet_bird":
				canvas.create_oval(x - 8, y - 8, x + 8, y + 8, fill="#87ceeb", outline="#000000")
				canvas.create_polygon(x + 6, y, x + 12, y - 2, x + 12, y + 2, fill="#ffa500", outline="#000000")
			elif ptype == "pet_dragon":
				canvas.create_oval(x - 16, y - 10, x + 16, y + 10, fill="#228b22", outline="#000000")
				canvas.create_polygon(x - 8, y - 10, x, y - 20, x + 8, y - 10, fill="#006400", outline="#000000")
				canvas.create_polygon(x - 16, y, x - 24, y - 4, x - 24, y + 4, fill="#006400", outline="#000000")
			else:
				# Default small pet
				canvas.create_oval(x - 6, y - 6, x + 6, y + 6, fill="#cccccc", outline="#000000")

	def _move_avatar(self, direction):
		"""Move avatar in the specified direction."""
		import time
		# Reset idle timer so auto-walk pauses when user moves manually
		self._last_user_move_time = time.time()
		
		# Get canvas dimensions (no update_idletasks to avoid flashing)
		canvas = self.avatar_canvas
		width = canvas.winfo_width() if canvas.winfo_width() > 10 else 600
		height = canvas.winfo_height() if canvas.winfo_height() > 10 else 400
		
		# Convert pixel step to normalized coordinates
		step_x = 10.0 / width  # Normalized step for horizontal movement
		step_y = 10.0 / height  # Normalized step for vertical movement
		
		# Get current normalized position
		x = self._avatar_state["x"]
		y = self._avatar_state["y"]
		
		# Calculate normalized bounds with wall collision
		wall_depth_norm = 0.2  # Top wall takes 20% of height
		side_wall_width_norm = 0.08  # Side walls take 8% of width
		margin_x = 60.0 / width  # Horizontal margin for avatar size
		margin_y = 60.0 / height  # Vertical margin for avatar size
		
		# Left wall collision boundary (side wall + margin)
		left_boundary = side_wall_width_norm + margin_x
		# Right wall collision boundary (1.0 - side wall - margin)
		right_boundary = 1.0 - side_wall_width_norm - margin_x
		# Top boundary (back wall + margin)
		top_boundary = wall_depth_norm + margin_y
		# Bottom boundary
		bottom_boundary = 1.0 - margin_y
		
		# Update position based on direction with wall collision
		if direction == "up":
			y = max(top_boundary, y - step_y)  # Don't go into back wall
		elif direction == "down":
			y = min(bottom_boundary, y + step_y)  # Don't go past floor
		elif direction == "left":
			x = max(left_boundary, x - step_x)  # Don't go into left wall
		elif direction == "right":
			x = min(right_boundary, x + step_x)  # Don't go into right wall
		
		# Update state with normalized coordinates
		self._avatar_state["x"] = x
		self._avatar_state["y"] = y
		self._avatar_state["direction"] = direction
		
		# Request redraw instead of calling directly to avoid flashing
		self._request_redraw()
		
		# Save avatar position
		self._save_avatar_state()
	
	def _update_avatar_clothing(self):
		"""Update avatar clothing based on selection."""
		selected_hat = self.hat_var.get()
		selected_shirt = self.shirt_var.get()
		selected_pants = self.pants_var.get()
		
		# Guard against selecting locked items
		locked = []
		if selected_hat.startswith("hat_") and selected_hat not in self.unlocked_items:
			locked.append("Hat")
			self.hat_var.set(self._avatar_state.get("hat", "none"))
		else:
			self._avatar_state["hat"] = selected_hat
		
		if selected_shirt.startswith("shirt_") and selected_shirt not in self.unlocked_items:
			locked.append("Shirt")
			self.shirt_var.set(self._avatar_state.get("shirt", "t_shirt_blue"))
		else:
			self._avatar_state["shirt"] = selected_shirt
		
		if selected_pants.startswith("pants_") and selected_pants not in self.unlocked_items:
			locked.append("Pants")
			self.pants_var.set(self._avatar_state.get("pants", "jeans_blue"))
		else:
			self._avatar_state["pants"] = selected_pants
		
		if locked:
			messagebox.showinfo("Locked", f"These items are locked: {', '.join(locked)}\nLevel up to unlock them!")
		
		# Request redraw instead of calling directly
		self._request_redraw()
		
		# Save avatar state
		self._save_avatar_state()
	
	def _save_avatar_state(self):
		"""Save avatar state to settings."""
		if not hasattr(self, 'settings'):
			self.settings = {}
		self.settings['avatar'] = self._avatar_state.copy()
		self._save_settings()
	
	def _toggle_avatar_section(self, section):
		"""Toggle collapsible avatar customization sections."""
		is_expanded = self._avatar_sections_expanded.get(section, False)
		
		# Toggle state
		self._avatar_sections_expanded[section] = not is_expanded
		
		# Get the appropriate frame and button
		frames = {
			"hats": (self.hat_content_frame, self.hat_toggle_btn, "Hats"),
			"shirts": (self.shirt_content_frame, self.shirt_toggle_btn, "Shirts"),
			"pants": (self.pants_content_frame, self.pants_toggle_btn, "Pants"),
			"pets": (self.pets_content_frame, self.pets_toggle_btn, "Pets"),
			"colors": (self.colors_content_frame, self.colors_toggle_btn, "Room Customization")
		}
		
		if section in frames:
			content_frame, toggle_btn, label = frames[section]
			
			if self._avatar_sections_expanded[section]:
				# Expand: show content
				content_frame.pack(fill="x", pady=(0, 5))
				toggle_btn.configure(text=f"▼ {label}")
			else:
				# Collapse: hide content
				content_frame.pack_forget()
				toggle_btn.configure(text=f"▶ {label}")
	
	def _award_xp(self, amount):
		"""Award XP and check for level up and unlocks."""
		old_level = self.level
		self.xp += amount
		self.tasks_completed += amount // self.XP_PER_TASK
		
		# Calculate level (100 XP per level)
		self.level = 1 + (self.xp // 100)
		
		# Check for level up
		if self.level > old_level:
			self._on_level_up(old_level, self.level)
		
		# Save XP state
		if not hasattr(self, 'settings'):
			self.settings = {}
		self.settings['xp'] = self.xp
		self.settings['level'] = self.level
		self.settings['tasks_completed'] = self.tasks_completed
		self.settings['unlocked_items'] = list(self.unlocked_items)
		self.settings['pets'] = self.pets
		self._save_settings()
		
		# Update avatar room display if it exists
		if hasattr(self, 'xp_bar_canvas'):
			self._update_xp_display()
	
	def _on_level_up(self, old_level, new_level):
		"""Handle level up - check for unlocks and show notification."""
		unlocked_this_level = []
		
		# Check all levels from old to new for unlocks
		for level in range(old_level + 1, new_level + 1):
			if level in self.UNLOCKS:
				for item in self.UNLOCKS[level]:
					if item not in self.unlocked_items:
						self.unlocked_items.add(item)
						unlocked_this_level.append(item)
						
						# Auto-equip first pet
						if item.startswith("pet_") and len(self.pets) == 0:
							self._add_pet(item)
		
		# Show unlock notification
		if unlocked_this_level:
			unlock_text = "\n".join([f"🎁 {item.replace('_', ' ').title()}" for item in unlocked_this_level])
			messagebox.showinfo(
				f"🎉 Level {new_level} Reached!",
				f"Congratulations!\n\nYou've unlocked:\n{unlock_text}\n\nCheck the Avatar Room!"
			)
	
	def _add_pet(self, pet_type):
		"""Add a new pet to the avatar room with normalized coordinates."""
		# Initialize pet in a random position (normalized 0.0-1.0)
		# Avoid wall areas: side walls are 8% on each side, back wall is top 20%
		import random
		side_wall_width_norm = 0.08
		wall_depth_norm = 0.2
		margin = 0.1  # Extra margin for safety
		
		# Safe area: between side walls and below back wall
		min_x = side_wall_width_norm + margin
		max_x = 1.0 - side_wall_width_norm - margin
		min_y = wall_depth_norm + margin
		max_y = 0.85  # Keep away from very bottom
		
		pet = {
			"type": pet_type,
			"x": random.uniform(min_x, max_x),  # Normalized x position (avoid side walls)
			"y": random.uniform(min_y, max_y),  # Normalized y position (avoid back wall)
			"direction": random.choice(["left", "right"])
		}
		self.pets.append(pet)
		self._save_pets_state()
		
		# Start pet animation if avatar room is active
		if hasattr(self, 'avatar_canvas'):
			self._animate_pets()

	def _save_pets_state(self):
		"""Persist pets to settings."""
		if not hasattr(self, 'settings'):
			self.settings = {}
		self.settings['pets'] = self.pets
		self._save_settings()

	def _toggle_pet(self, pet_key):
		"""Toggle a pet on/off based on UI checkbox."""
		present_types = set(p.get("type") for p in (self.pets or []))
		want = bool(self.pet_vars.get(pet_key).get())
		if want and pet_key not in present_types:
			self._add_pet(pet_key)
			self._request_redraw()
		elif not want and pet_key in present_types:
			self.pets = [p for p in self.pets if p.get("type") != pet_key]
			self._save_pets_state()
			self._request_redraw()
			# Animation continues even without pets (for window/avatar animations)
			# No need to stop the animation loop
	
	def _set_room_color(self, color_type, color):
		"""Set floor or wall color and save settings."""
		if not hasattr(self, '_room_colors'):
			self._room_colors = {"floor": "#e8dcc0", "wall": "#a8a8a8"}
		
		self._room_colors[color_type] = color
		
		# Save to settings
		if not hasattr(self, 'settings'):
			self.settings = {}
		self.settings['room_colors'] = self._room_colors
		self._save_settings()
		
		# Redraw room
		self._request_redraw()
	
	def _set_window_count(self, count):
		"""Set number of windows on back wall and save settings."""
		self._window_count = count
		
		# Save to settings
		if not hasattr(self, 'settings'):
			self.settings = {}
		self.settings['window_count'] = count
		self._save_settings()
		
		# Redraw room
		self._request_redraw()
	
	def _get_builtin_furniture(self):
		"""Return dictionary of built-in furniture items with their render functions."""
		return {
			# Rugs
			"Round Rug": {"category": "rug", "size": 0.15, "color": "#8b4513"},
			"Square Rug": {"category": "rug", "size": 0.15, "color": "#a0522d"},
			"Blue Rug": {"category": "rug", "size": 0.15, "color": "#4169e1"},
			"Red Rug": {"category": "rug", "size": 0.15, "color": "#dc143c"},
			"Green Rug": {"category": "rug", "size": 0.15, "color": "#228b22"},
			
			# Furniture
			"Small Table": {"category": "furniture", "size": 0.10, "color": "#8b4513"},
			"Large Table": {"category": "furniture", "size": 0.15, "color": "#654321"},
			"Bookshelf": {"category": "furniture", "size": 0.12, "color": "#8b7355"},
			"Chair": {"category": "furniture", "size": 0.08, "color": "#a0522d"},
			"Plant": {"category": "furniture", "size": 0.08, "color": "#6b8e23"},
			"Sofa": {"category": "furniture", "size": 0.18, "color": "#8b4789"},
			"Desk": {"category": "furniture", "size": 0.14, "color": "#d2691e"},
			
			# Posters
			"Star Poster": {"category": "poster", "size": 0.08, "color": "#ffd700"},
			"Heart Poster": {"category": "poster", "size": 0.08, "color": "#ff69b4"},
			"Moon Poster": {"category": "poster", "size": 0.08, "color": "#e6e6fa"},
			"Sun Poster": {"category": "poster", "size": 0.08, "color": "#ffff00"},
			"Music Poster": {"category": "poster", "size": 0.08, "color": "#4169e1"},
		}
	
	def _open_furniture_window(self):
		"""Open furniture placement window with drag-and-drop."""
		# Check if window already exists
		if hasattr(self, '_furniture_window') and self._furniture_window.winfo_exists():
			self._furniture_window.lift()
			return
		
		# Initialize placed items if not exists
		if not hasattr(self, '_placed_items'):
			if hasattr(self, 'settings') and 'placed_items' in self.settings:
				self._placed_items = self.settings['placed_items']
			else:
				self._placed_items = []
		
		# Create popup window
		self._furniture_window = tk.Toplevel(self.root)
		self._furniture_window.title("Place Furniture & Decorations")
		self._furniture_window.geometry("350x600")
		self._furniture_window.transient(self.root)
		
		# Main container
		main_frame = tk.Frame(self._furniture_window)
		main_frame.pack(fill="both", expand=True, padx=10, pady=10)
		
		# Instructions
		instructions = tk.Label(main_frame, 
							   text="Drag items from this list to your room!\nRight-click items in room to delete.",
							   font=("", 9), justify="center", wraplength=320)
		instructions.pack(pady=(0, 10))
		
		# Category tabs
		category_frame = tk.Frame(main_frame)
		category_frame.pack(fill="x", pady=(0, 10))
		
		self._furniture_category = tk.StringVar(value="All")
		categories = ["All", "Rug", "Furniture", "Poster"]
		
		for cat in categories:
			btn = tk.Radiobutton(category_frame, text=cat, variable=self._furniture_category,
							   value=cat, command=self._refresh_furniture_list)
			btn.pack(side="left", padx=5)
		
		# Scrollable furniture list with preview
		list_frame = tk.Frame(main_frame)
		list_frame.pack(fill="both", expand=True)
		
		scrollbar = tk.Scrollbar(list_frame)
		scrollbar.pack(side="right", fill="y")
		
		# Canvas for furniture items (to show visual previews)
		self._furniture_canvas = tk.Canvas(list_frame, yscrollcommand=scrollbar.set, 
										  bg="white", highlightthickness=1)
		self._furniture_canvas.pack(side="left", fill="both", expand=True)
		scrollbar.config(command=self._furniture_canvas.yview)
		
		# Clear placed items button
		clear_frame = tk.Frame(main_frame)
		clear_frame.pack(fill="x", pady=(10, 0))
		
		clear_btn = tk.Button(clear_frame, text="🗑️ Clear All Placed Items", 
							 command=self._clear_all_placed_items, fg="red")
		clear_btn.pack(fill="x")
		
		# Populate list
		self._refresh_furniture_list()
		
		# Bind drag events on avatar canvas
		self.avatar_canvas.bind("<Button-3>", self._on_room_right_click)
	
	def _refresh_furniture_list(self):
		"""Refresh the furniture list based on category filter."""
		canvas = self._furniture_canvas
		canvas.delete("all")
		
		furniture_items = self._get_builtin_furniture()
		filter_cat = self._furniture_category.get().lower()
		
		y_pos = 10
		item_height = 60
		
		for item_name, item_data in furniture_items.items():
			item_cat = item_data["category"]
			
			# Apply filter
			if filter_cat != "all" and item_cat != filter_cat:
				continue
			
			# Draw item preview box
			x1, y1 = 10, y_pos
			x2, y2 = 320, y_pos + item_height
			
			# Background
			canvas.create_rectangle(x1, y1, x2, y2, fill="#f0f0f0", outline="#999", width=2)
			
			# Preview of item (small visual representation)
			preview_x = x1 + 30
			preview_y = y1 + item_height // 2
			preview_size = 25
			
			self._draw_furniture_preview(canvas, item_name, item_data, 
										preview_x, preview_y, preview_size)
			
			# Item name
			canvas.create_text(x1 + 70, y1 + item_height // 2, 
							  text=item_name, anchor="w", font=("", 10, "bold"))
			
			# Make item draggable
			item_id = canvas.create_rectangle(x1, y1, x2, y2, fill="", outline="", width=0)
			canvas.tag_bind(item_id, "<Button-1>", 
						   lambda e, name=item_name, data=item_data: self._start_drag_furniture(e, name, data))
			
			y_pos += item_height + 10
		
		# Update scroll region
		canvas.configure(scrollregion=canvas.bbox("all"))
	
	def _draw_furniture_preview(self, canvas, item_name, item_data, x, y, size):
		"""Draw a small preview of the furniture item."""
		category = item_data["category"]
		color = item_data.get("color", "#888")
		
		if category == "rug":
			# Draw rug shapes
			if "Round" in item_name:
				canvas.create_oval(x - size, y - size, x + size, y + size, 
								 fill=color, outline="#000", width=2)
			else:
				canvas.create_rectangle(x - size, y - size, x + size, y + size, 
									  fill=color, outline="#000", width=2)
		
		elif category == "furniture":
			# Draw furniture representations
			if "Table" in item_name:
				# Table top and legs
				canvas.create_rectangle(x - size, y - size//2, x + size, y + size//2, 
									  fill=color, outline="#000", width=2)
				leg_size = size // 4
				canvas.create_rectangle(x - size + leg_size, y + size//2, 
									  x - size + 2*leg_size, y + size, fill=color, outline="#000")
				canvas.create_rectangle(x + size - 2*leg_size, y + size//2, 
									  x + size - leg_size, y + size, fill=color, outline="#000")
			
			elif "Bookshelf" in item_name:
				# Bookshelf with shelves
				canvas.create_rectangle(x - size, y - size, x + size, y + size, 
									  fill=color, outline="#000", width=2)
				canvas.create_line(x - size, y - size//3, x + size, y - size//3, fill="#000", width=1)
				canvas.create_line(x - size, y + size//3, x + size, y + size//3, fill="#000", width=1)
			
			elif "Chair" in item_name:
				# Simple chair
				canvas.create_rectangle(x - size, y, x + size, y + size, 
									  fill=color, outline="#000", width=2)
				canvas.create_rectangle(x - size, y - size, x + size, y, 
									  fill=color, outline="#000", width=2)
			
			elif "Plant" in item_name:
				# Plant in pot
				canvas.create_oval(x - size, y - size, x + size, y + size//2, 
								 fill="#6b8e23", outline="#000", width=2)
				canvas.create_rectangle(x - size//2, y + size//2, x + size//2, y + size, 
									  fill="#8b4513", outline="#000", width=1)
			
			elif "Sofa" in item_name:
				# Sofa shape
				canvas.create_rectangle(x - size, y - size//2, x + size, y + size, 
									  fill=color, outline="#000", width=2)
				canvas.create_rectangle(x - size, y - size, x + size, y - size//2, 
									  fill=color, outline="#000", width=2)
			
			elif "Desk" in item_name:
				# Desk
				canvas.create_rectangle(x - size, y - size//3, x + size, y + size//3, 
									  fill=color, outline="#000", width=2)
				canvas.create_rectangle(x - size//2, y + size//3, x - size//3, y + size, 
									  fill=color, outline="#000")
				canvas.create_rectangle(x + size//3, y + size//3, x + size//2, y + size, 
									  fill=color, outline="#000")
		
		elif category == "poster":
			# Draw poster shapes
			canvas.create_rectangle(x - size, y - size, x + size, y + size, 
								  fill=color, outline="#000", width=2)
			
			if "Star" in item_name:
				# Star shape
				points = []
				import math
				for i in range(10):
					angle = math.pi / 2 + i * 2 * math.pi / 10
					r = size * 0.4 if i % 2 == 0 else size * 0.7
					px = x + r * math.cos(angle)
					py = y - r * math.sin(angle)
					points.extend([px, py])
				canvas.create_polygon(points, fill="#fff", outline="")
			
			elif "Heart" in item_name:
				# Simple heart indicator
				canvas.create_text(x, y, text="♥", font=("", int(size * 1.5)), fill="#fff")
			
			elif "Moon" in item_name:
				# Crescent moon
				canvas.create_oval(x - size//2, y - size//2, x + size//2, y + size//2, 
								 fill="#fff", outline="")
			
			elif "Sun" in item_name:
				# Sun
				canvas.create_oval(x - size//2, y - size//2, x + size//2, y + size//2, 
								 fill="#fff", outline="")
			
			elif "Music" in item_name:
				# Music note
				canvas.create_text(x, y, text="♪", font=("", int(size * 1.5)), fill="#fff")
	
	def _start_drag_furniture(self, event, item_name, item_data):
		"""Start dragging furniture item from list."""
		# Store drag data
		self._drag_furniture = {
			"name": item_name,
			"data": item_data,
			"active": True
		}
		
		# Create dragging cursor indicator
		self._furniture_window.config(cursor="hand2")
		
		# Bind motion to avatar canvas to show where it will be placed
		self.avatar_canvas.bind("<Motion>", self._drag_furniture_motion)
		self.avatar_canvas.bind("<Button-1>", self._drop_furniture)
	
	def _drag_furniture_motion(self, event):
		"""Show preview of furniture being dragged over room."""
		if not hasattr(self, '_drag_furniture') or not self._drag_furniture.get("active"):
			return
		
		# Remove previous ghost preview
		if hasattr(self, '_drag_ghost_id'):
			self.avatar_canvas.delete(self._drag_ghost_id)
		
		# Get position
		canvas = self.avatar_canvas
		width = canvas.winfo_width()
		height = canvas.winfo_height()
		
		x_norm = event.x / width
		y_norm = event.y / height
		
		# Apply wall collision preview
		category = self._drag_furniture["data"]["category"]
		if category in ("rug", "furniture"):
			side_wall_width_norm = 0.08
			wall_depth_norm = 0.2
			margin = 0.05
			min_x = side_wall_width_norm + margin
			max_x = 1.0 - side_wall_width_norm - margin
			min_y = wall_depth_norm + margin
			max_y = 0.95 - margin
			x_norm = max(min_x, min(max_x, x_norm))
			y_norm = max(min_y, min(max_y, y_norm))
		elif category == "poster":
			min_y = 0.05
			max_y = 0.18
			y_norm = max(min_y, min(max_y, y_norm))
		
		# Draw ghost preview (semi-transparent representation)
		x = int(width * x_norm)
		y = int(height * y_norm)
		size = int(min(width, height) * self._drag_furniture["data"]["size"])
		
		# Create ghost outline
		if category in ("rug", "furniture"):
			if "Round" in self._drag_furniture["name"]:
				self._drag_ghost_id = canvas.create_oval(
					x - size, y - size, x + size, y + size,
					fill="", outline="#00ff00", width=3, dash=(5, 5))
			else:
				self._drag_ghost_id = canvas.create_rectangle(
					x - size, y - size, x + size, y + size,
					fill="", outline="#00ff00", width=3, dash=(5, 5))
		else:  # poster
			self._drag_ghost_id = canvas.create_rectangle(
				x - size, y - size, x + size, y + size,
				fill="", outline="#00ff00", width=3, dash=(5, 5))
		
		self.avatar_canvas.config(cursor="crosshair")
	
	def _drop_furniture(self, event):
		"""Drop furniture item into the room."""
		if not hasattr(self, '_drag_furniture') or not self._drag_furniture.get("active"):
			return
		
		# Get normalized position (0-1 range)
		canvas = self.avatar_canvas
		width = canvas.winfo_width()
		height = canvas.winfo_height()
		
		x_norm = event.x / width
		y_norm = event.y / height
		
		# Apply wall collision for rugs and furniture
		category = self._drag_furniture["data"]["category"]
		if category in ("rug", "furniture"):
			side_wall_width_norm = 0.08
			wall_depth_norm = 0.2
			margin = 0.05
			
			min_x = side_wall_width_norm + margin
			max_x = 1.0 - side_wall_width_norm - margin
			min_y = wall_depth_norm + margin
			max_y = 0.95 - margin
			
			x_norm = max(min_x, min(max_x, x_norm))
			y_norm = max(min_y, min(max_y, y_norm))
		elif category == "poster":
			# Posters go on back wall
			min_y = 0.05
			max_y = 0.18
			y_norm = max(min_y, min(max_y, y_norm))
		
		# Add to placed items
		placed_item = {
			"name": self._drag_furniture["name"],
			"category": category,
			"x": x_norm,
			"y": y_norm,
			"size": self._drag_furniture["data"]["size"],
			"color": self._drag_furniture["data"]["color"]
		}
		
		self._placed_items.append(placed_item)
		self._save_placed_items()
		
		# Clear drag state
		self._drag_furniture["active"] = False
		self._furniture_window.config(cursor="")
		self.avatar_canvas.config(cursor="")
		self.avatar_canvas.unbind("<Motion>")
		self.avatar_canvas.unbind("<Button-1>")
		
		# Remove ghost preview
		if hasattr(self, '_drag_ghost_id'):
			self.avatar_canvas.delete(self._drag_ghost_id)
			del self._drag_ghost_id
		
		# Redraw room
		self._request_redraw()
	
	def _on_room_right_click(self, event):
		"""Handle right-click on room to delete placed items."""
		if not hasattr(self, '_placed_items') or not self._placed_items:
			return
		
		# Get click position in normalized coords
		canvas = self.avatar_canvas
		width = canvas.winfo_width()
		height = canvas.winfo_height()
		
		click_x = event.x / width
		click_y = event.y / height
		
		# Find clicked item (check in reverse order so top items are checked first)
		for i in range(len(self._placed_items) - 1, -1, -1):
			item = self._placed_items[i]
			item_x = item["x"]
			item_y = item["y"]
			item_size = item["size"]
			
			# Check if click is within item bounds
			if abs(click_x - item_x) < item_size and abs(click_y - item_y) < item_size:
				# Remove item
				self._placed_items.pop(i)
				self._save_placed_items()
				self._request_redraw()
				break
	
	def _clear_all_placed_items(self):
		"""Clear all placed furniture items."""
		if hasattr(self, '_placed_items'):
			self._placed_items = []
			self._save_placed_items()
			self._request_redraw()
	
	def _save_placed_items(self):
		"""Save placed items to settings."""
		if not hasattr(self, 'settings'):
			self.settings = {}
		self.settings['placed_items'] = self._placed_items
		self._save_settings()
	
	def _open_asset_designer_window(self):
		"""Open Asset Designer in a popup window."""
		# Check if window already exists
		if hasattr(self, '_asset_designer_window') and self._asset_designer_window.winfo_exists():
			self._asset_designer_window.lift()
			return
		
		# Create popup window
		self._asset_designer_window = tk.Toplevel(self.root)
		self._asset_designer_window.title("Asset Designer")
		self._asset_designer_window.geometry("900x600")
		self._asset_designer_window.transient(self.root)
		
		# Main container
		main_frame = tk.Frame(self._asset_designer_window)
		main_frame.pack(fill="both", expand=True, padx=10, pady=10)
		
		# Left side - Asset list and controls
		left_frame = tk.Frame(main_frame, width=280)
		left_frame.pack(side="left", fill="both", expand=False, padx=(0, 10))
		left_frame.pack_propagate(False)
		
		# Title
		title_label = tk.Label(left_frame, text="Custom Assets", font=("", 14, "bold"))
		title_label.pack(pady=(0, 10))
		
		# Category selection
		category_frame = tk.Frame(left_frame)
		category_frame.pack(fill="x", pady=(0, 5))
		tk.Label(category_frame, text="Category:").pack(side="left", padx=(0, 5))
		self.asset_category_var = tk.StringVar(value="All")
		category_dropdown = ttk.Combobox(category_frame, textvariable=self.asset_category_var,
										 values=["All", "Floor", "Rug", "Furniture", "Poster"],
										 state="readonly", width=12)
		category_dropdown.pack(side="left", fill="x", expand=True)
		category_dropdown.bind("<<ComboboxSelected>>", lambda e: self._refresh_asset_list())
		
		# Upload button
		upload_btn = tk.Button(left_frame, text="📁 Upload PNG Asset", 
							   command=self._upload_asset, font=("", 10, "bold"))
		upload_btn.pack(fill="x", pady=(5, 10))
		
		# Asset list frame with scrollbar
		list_frame = tk.Frame(left_frame)
		list_frame.pack(fill="both", expand=True)
		
		scrollbar = tk.Scrollbar(list_frame)
		scrollbar.pack(side="right", fill="y")
		
		self.asset_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=12)
		self.asset_listbox.pack(side="left", fill="both", expand=True)
		scrollbar.config(command=self.asset_listbox.yview)
		self.asset_listbox.bind("<<ListboxSelect>>", self._on_asset_select)
		
		# Asset controls
		controls_frame = tk.Frame(left_frame)
		controls_frame.pack(fill="x", pady=(10, 0))
		
		# Category for selected asset
		tk.Label(controls_frame, text="Asset Category:").pack(anchor="w")
		self.selected_asset_category_var = tk.StringVar(value="Rug")
		cat_dropdown = ttk.Combobox(controls_frame, textvariable=self.selected_asset_category_var,
										values=["Floor", "Rug", "Furniture", "Poster"],
									state="readonly")
		cat_dropdown.pack(fill="x", pady=(0, 5))
		cat_dropdown.bind("<<ComboboxSelected>>", lambda e: self._update_selected_asset())
		
		tk.Label(controls_frame, text="Position X (0-1):").pack(anchor="w")
		self.asset_x_var = tk.DoubleVar(value=0.5)
		self.asset_x_scale = tk.Scale(controls_frame, from_=0.0, to=1.0, resolution=0.01,
									  orient="horizontal", variable=self.asset_x_var,
									  command=self._update_selected_asset)
		self.asset_x_scale.pack(fill="x")
		
		tk.Label(controls_frame, text="Position Y (0-1):").pack(anchor="w")
		self.asset_y_var = tk.DoubleVar(value=0.5)
		self.asset_y_scale = tk.Scale(controls_frame, from_=0.0, to=1.0, resolution=0.01,
									  orient="horizontal", variable=self.asset_y_var,
									  command=self._update_selected_asset)
		self.asset_y_scale.pack(fill="x")
		
		tk.Label(controls_frame, text="Scale:").pack(anchor="w")
		self.asset_scale_var = tk.DoubleVar(value=1.0)
		self.asset_scale_scale = tk.Scale(controls_frame, from_=0.1, to=3.0, resolution=0.1,
										  orient="horizontal", variable=self.asset_scale_var,
										  command=self._update_selected_asset)
		self.asset_scale_scale.pack(fill="x")
		
		# Delete button
		delete_btn = tk.Button(controls_frame, text="🗑️ Delete Selected Asset",
							   command=self._delete_selected_asset, fg="red")
		delete_btn.pack(fill="x", pady=(10, 0))
		
		# Right side - Preview canvas
		right_frame = tk.Frame(main_frame)
		right_frame.pack(side="right", fill="both", expand=True)
		
		preview_label = tk.Label(right_frame, text="Preview", font=("", 12, "bold"))
		preview_label.pack(pady=(0, 5))
		
		self.asset_preview_canvas = tk.Canvas(right_frame, bg="#e8dcc0", width=500, height=400)
		self.asset_preview_canvas.pack(fill="both", expand=True)
		# Redraw preview whenever the canvas is resized
		self.asset_preview_canvas.bind("<Configure>", lambda e: self._preview_assets())
		
		# Load saved assets
		if hasattr(self, 'settings') and 'custom_assets' in self.settings:
			self.custom_assets = self.settings.get('custom_assets', [])
		
		self._refresh_asset_list()
		self._preview_assets()
	
	def _setup_asset_designer_tab(self):
		"""Set up the Asset Designer tab for uploading and placing PNG assets."""
		# Main container
		main_frame = tk.Frame(self.asset_designer_tab)
		main_frame.pack(fill="both", expand=True, padx=10, pady=10)
		
		# Left side - Asset list and controls
		left_frame = tk.Frame(main_frame, width=280)
		left_frame.pack(side="left", fill="both", expand=False, padx=(0, 10))
		left_frame.pack_propagate(False)
		
		# Title
		title_label = tk.Label(left_frame, text="Custom Assets", font=("", 14, "bold"))
		title_label.pack(pady=(0, 10))
		
		# Category selection
		category_frame = tk.Frame(left_frame)
		category_frame.pack(fill="x", pady=(0, 5))
		tk.Label(category_frame, text="Category:").pack(side="left", padx=(0, 5))
		self.asset_category_var = tk.StringVar(value="All")
		category_dropdown = ttk.Combobox(category_frame, textvariable=self.asset_category_var,
										 values=["All", "Floor", "Rug", "Furniture", "Poster"],
										 state="readonly", width=12)
		category_dropdown.pack(side="left", fill="x", expand=True)
		category_dropdown.bind("<<ComboboxSelected>>", lambda e: self._refresh_asset_list())
		
		# Upload button
		upload_btn = tk.Button(left_frame, text="📁 Upload PNG Asset", 
							   command=self._upload_asset, font=("", 10, "bold"))
		upload_btn.pack(fill="x", pady=(5, 10))
		
		# Asset list frame with scrollbar
		list_frame = tk.Frame(left_frame)
		list_frame.pack(fill="both", expand=True)
		
		scrollbar = tk.Scrollbar(list_frame)
		scrollbar.pack(side="right", fill="y")
		
		self.asset_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=12)
		self.asset_listbox.pack(side="left", fill="both", expand=True)
		scrollbar.config(command=self.asset_listbox.yview)
		self.asset_listbox.bind("<<ListboxSelect>>", self._on_asset_select)
		
		# Asset controls
		controls_frame = tk.Frame(left_frame)
		controls_frame.pack(fill="x", pady=(10, 0))
		
		# Category for selected asset
		tk.Label(controls_frame, text="Asset Category:").pack(anchor="w")
		self.selected_asset_category_var = tk.StringVar(value="Rug")
		cat_dropdown = ttk.Combobox(controls_frame, textvariable=self.selected_asset_category_var,
										values=["Floor", "Rug", "Furniture", "Poster"],
									state="readonly")
		cat_dropdown.pack(fill="x", pady=(0, 5))
		cat_dropdown.bind("<<ComboboxSelected>>", lambda e: self._update_selected_asset())
		
		tk.Label(controls_frame, text="Position X (0-1):").pack(anchor="w")
		self.asset_x_var = tk.DoubleVar(value=0.5)
		self.asset_x_scale = tk.Scale(controls_frame, from_=0.0, to=1.0, resolution=0.01,
									  orient="horizontal", variable=self.asset_x_var,
									  command=self._update_selected_asset)
		self.asset_x_scale.pack(fill="x")
		
		tk.Label(controls_frame, text="Position Y (0-1):").pack(anchor="w")
		self.asset_y_var = tk.DoubleVar(value=0.5)
		self.asset_y_scale = tk.Scale(controls_frame, from_=0.0, to=1.0, resolution=0.01,
									  orient="horizontal", variable=self.asset_y_var,
									  command=self._update_selected_asset)
		self.asset_y_scale.pack(fill="x")
		
		tk.Label(controls_frame, text="Scale:").pack(anchor="w")
		self.asset_scale_var = tk.DoubleVar(value=1.0)
		self.asset_scale_scale = tk.Scale(controls_frame, from_=0.1, to=3.0, resolution=0.1,
										  orient="horizontal", variable=self.asset_scale_var,
										  command=self._update_selected_asset)
		self.asset_scale_scale.pack(fill="x")
		
		# Delete button
		delete_btn = tk.Button(controls_frame, text="🗑️ Delete Selected Asset",
							   command=self._delete_selected_asset, fg="red")
		delete_btn.pack(fill="x", pady=(10, 0))
		
		# Right side - Preview canvas
		right_frame = tk.Frame(main_frame)
		right_frame.pack(side="right", fill="both", expand=True)
		
		preview_label = tk.Label(right_frame, text="Preview", font=("", 12, "bold"))
		preview_label.pack(pady=(0, 5))
		
		self.asset_preview_canvas = tk.Canvas(right_frame, bg="#e8dcc0", width=500, height=400)
		self.asset_preview_canvas.pack(fill="both", expand=True)
		# Redraw preview whenever the canvas is resized so the room stretches with the window
		self.asset_preview_canvas.bind("<Configure>", lambda e: self._preview_assets())
		
		# Load saved assets
		if hasattr(self, 'settings') and 'custom_assets' in self.settings:
			self.custom_assets = self.settings.get('custom_assets', [])
		
		self._refresh_asset_list()
		self._preview_assets()
	
	def _upload_asset(self):
		"""Upload a PNG or GIF file and add it to custom assets."""
		from tkinter import filedialog, simpledialog
		import os
		import shutil
		
		filepath = filedialog.askopenfilename(
			title="Select PNG or GIF Asset",
			filetypes=[("Image files", "*.png *.gif"), ("PNG files", "*.png"), ("GIF files", "*.gif"), ("All files", "*.*")]
		)
		
		if not filepath:
			return
		
		# Ask for category
		from tkinter import messagebox
		category_window = tk.Toplevel(self.root)
		category_window.title("Select Category")
		category_window.geometry("300x150")
		category_window.transient(self.root)
		category_window.grab_set()
		
		selected_category = tk.StringVar(value="Rug")
		
		tk.Label(category_window, text="Choose asset category:", font=("", 11, "bold")).pack(pady=(15, 10))
		
		for cat in ["Floor", "Rug", "Furniture", "Poster"]:
			tk.Radiobutton(category_window, text=cat, variable=selected_category, value=cat).pack(anchor="w", padx=30)
		
		def confirm():
			category_window.destroy()
		
		tk.Button(category_window, text="OK", command=confirm, width=10).pack(pady=(10, 0))
		
		self.root.wait_window(category_window)
		
		# Create assets directory if it doesn't exist
		assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_assets")
		os.makedirs(assets_dir, exist_ok=True)
		
		# Copy file to assets directory
		filename = os.path.basename(filepath)
		dest_path = os.path.join(assets_dir, filename)
		
		# Handle duplicate filenames
		base, ext = os.path.splitext(filename)
		counter = 1
		while os.path.exists(dest_path):
			filename = f"{base}_{counter}{ext}"
			dest_path = os.path.join(assets_dir, filename)
			counter += 1
		
		shutil.copy2(filepath, dest_path)
		
		# Check if it's an animated GIF
		is_animated = False
		frame_count = 1
		try:
			from PIL import Image
			img = Image.open(dest_path)
			if hasattr(img, 'n_frames'):
				frame_count = img.n_frames
				is_animated = frame_count > 1
			img.close()
		except:
			pass
		
		# Add to custom assets list with wall-aware positioning
		category = selected_category.get()
		
		# Default position depends on category
		if category in ("Rug", "Furniture"):
			# Place furniture/rugs in safe area (avoid walls)
			default_x = 0.5  # Center horizontally
			default_y = 0.6  # Centered in floor area (below back wall)
		elif category == "Poster":
			# Posters should be on the wall
			default_x = 0.5
			default_y = 0.1  # In the back wall area
		else:  # Floor
			default_x = 0.5
			default_y = 0.5
		
		asset = {
			"path": dest_path,
			"name": filename,
			"x": default_x,
			"y": default_y,
			"scale": 1.0,
			"category": category,
			"is_animated": is_animated,
			"frame_count": frame_count,
			"current_frame": 0
		}
		self.custom_assets.append(asset)
		self._save_assets()
		self._refresh_asset_list()
		self._preview_assets()
		if hasattr(self, 'avatar_canvas'):
			self._request_redraw()  # Refresh avatar room
	
	def _refresh_asset_list(self):
		"""Refresh the asset listbox based on selected category filter."""
		self.asset_listbox.delete(0, tk.END)
		
		# Get filter category
		filter_cat = self.asset_category_var.get() if hasattr(self, 'asset_category_var') else "All"
		
		# Create mapping from listbox index to asset index
		self._asset_index_map = []
		
		for i, asset in enumerate(self.custom_assets):
			category = asset.get("category", "Other")
			name = asset.get("name", "Unknown")
			is_animated = asset.get("is_animated", False)
			
			# Apply filter
			if filter_cat == "All" or category == filter_cat:
				# Add animation indicator
				anim_indicator = " 🎬" if is_animated else ""
				display_name = f"[{category}] {name}{anim_indicator}"
				self.asset_listbox.insert(tk.END, display_name)
				self._asset_index_map.append(i)
	
	def _on_asset_select(self, event):
		"""Handle asset selection."""
		selection = self.asset_listbox.curselection()
		if not selection:
			return
		
		listbox_idx = selection[0]
		if listbox_idx < len(self._asset_index_map):
			actual_idx = self._asset_index_map[listbox_idx]
			asset = self.custom_assets[actual_idx]
			self.asset_x_var.set(asset.get("x", 0.5))
			self.asset_y_var.set(asset.get("y", 0.5))
			self.asset_scale_var.set(asset.get("scale", 1.0))
			if hasattr(self, 'selected_asset_category_var'):
				self.selected_asset_category_var.set(asset.get("category", "Other"))
			self._preview_assets()
	
	def _update_selected_asset(self, *args):
		"""Update selected asset position/scale."""
		selection = self.asset_listbox.curselection()
		if not selection:
			return
		
		listbox_idx = selection[0]
		if listbox_idx < len(self._asset_index_map):
			actual_idx = self._asset_index_map[listbox_idx]
			
			# Get proposed position
			new_x = self.asset_x_var.get()
			new_y = self.asset_y_var.get()
			category = self.selected_asset_category_var.get() if hasattr(self, 'selected_asset_category_var') else self.custom_assets[actual_idx].get("category", "Rug")
			
			# Apply wall collision for furniture and rugs (not floor or posters)
			if category in ("Rug", "Furniture"):
				side_wall_width_norm = 0.08
				wall_depth_norm = 0.2
				margin = 0.05  # Small margin for asset edges
				
				# Constrain to safe area (avoid walls)
				min_x = side_wall_width_norm + margin
				max_x = 1.0 - side_wall_width_norm - margin
				min_y = wall_depth_norm + margin
				max_y = 0.95 - margin
				
				new_x = max(min_x, min(max_x, new_x))
				new_y = max(min_y, min(max_y, new_y))
				
				# Update the UI variables to reflect clamped values
				self.asset_x_var.set(new_x)
				self.asset_y_var.set(new_y)
			
			self.custom_assets[actual_idx]["x"] = new_x
			self.custom_assets[actual_idx]["y"] = new_y
			self.custom_assets[actual_idx]["scale"] = self.asset_scale_var.get()
			if hasattr(self, 'selected_asset_category_var'):
				self.custom_assets[actual_idx]["category"] = category
			self._save_assets()
			self._preview_assets()
			if hasattr(self, 'avatar_canvas'):
				self._request_redraw()  # Refresh avatar room
	
	def _delete_selected_asset(self):
		"""Delete the selected asset."""
		selection = self.asset_listbox.curselection()
		if not selection:
			return
		
		listbox_idx = selection[0]
		if listbox_idx < len(self._asset_index_map):
			actual_idx = self._asset_index_map[listbox_idx]
			import os
			# Delete file
			filepath = self.custom_assets[actual_idx].get("path")
			if filepath and os.path.exists(filepath):
				try:
					os.remove(filepath)
				except:
					pass
			
			# Remove from list
			self.custom_assets.pop(actual_idx)
			self._save_assets()
			self._refresh_asset_list()
			self._preview_assets()
			if hasattr(self, 'avatar_canvas'):
				self._request_redraw()
			self._refresh_asset_list()
			self._preview_assets()
			self._request_redraw()
	
	def _preview_assets(self):
		"""Preview assets on the canvas with full room background."""
		canvas = self.asset_preview_canvas
		canvas.delete("all")
		
		width = canvas.winfo_width() if canvas.winfo_width() > 10 else 500
		height = canvas.winfo_height() if canvas.winfo_height() > 10 else 400
		
		# Get custom room colors or use defaults
		if not hasattr(self, '_room_colors'):
			self._room_colors = {"floor": "#e8dcc0", "wall": "#a8a8a8"}
		floor_color = self._room_colors.get("floor", "#e8dcc0")
		wall_color = self._room_colors.get("wall", "#a8a8a8")
		
		# Helper to darken colors
		import colorsys
		def darken_color(hex_color, factor=0.9):
			hex_color = hex_color.lstrip('#')
			r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
			h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
			v = v * factor
			r, g, b = colorsys.hsv_to_rgb(h, s, v)
			return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
		
		# Draw floor
		canvas.create_rectangle(0, 0, width, height, fill=floor_color, outline="")
		
		# Draw floor tiles for depth effect (scale to canvas size)
		tile_color = darken_color(floor_color, 0.85)
		tile_size = max(30, min(50, width // 15))
		for y in range(0, height, tile_size):
			canvas.create_line(0, y, width, y, fill=tile_color, width=1)
		for x in range(0, width, tile_size):
			canvas.create_line(x, 0, x, height, fill=tile_color, width=1)
		
		# Draw walls (scaled)
		wall_depth = int(height * 0.2)  # 20% of height
		side_wall_width = int(width * 0.08)  # 8% of width
		
		# Calculate wall shading
		wall_darker = darken_color(wall_color, 0.7)
		wall_outline = darken_color(wall_color, 0.6)
		
		# Back wall
		canvas.create_rectangle(0, 0, width, wall_depth, fill=wall_color, outline=wall_outline, width=2)
		# Side walls (perspective) - extend to bottom and beyond
		# Left wall extends from top-left corner down past the bottom
		canvas.create_polygon(0, 0, side_wall_width, wall_depth, side_wall_width, height + 100, 0, height + 100, 
							 fill=wall_darker, outline=wall_outline, width=2)
		# Right wall extends from top-right corner down past the bottom
		canvas.create_polygon(width, 0, width - side_wall_width, wall_depth, width - side_wall_width, height + 100, width, height + 100,
							 fill=wall_darker, outline=wall_outline, width=2)
		
		# Draw furniture/decorations (scaled proportionally)
		# Plant in corner
		plant_x = int(width * 0.12)
		plant_y = int(height * 0.75)
		plant_size = int(min(width, height) * 0.067)
		canvas.create_oval(plant_x, plant_y, plant_x + plant_size, plant_y + plant_size, 
						  fill="#6b8e23", outline="#556b2f", width=2)
		canvas.create_rectangle(plant_x + plant_size//4, plant_y + plant_size, 
							   plant_x + 3*plant_size//4, plant_y + int(plant_size * 1.5), 
							   fill="#8b4513", outline="#654321", width=1)
		
		# Table
		table_x = int(width * 0.75)
		table_y = int(height * 0.7)
		table_w = int(width * 0.13)
		table_h = int(height * 0.05)
		canvas.create_rectangle(table_x, table_y, table_x + table_w, table_y + table_h, 
							   fill="#8b4513", outline="#654321", width=2)
		# Table legs
		leg_w = int(table_w * 0.125)
		leg_h = int(height * 0.1)
		canvas.create_rectangle(table_x + leg_w, table_y + table_h, 
							   table_x + 2*leg_w, table_y + table_h + leg_h,
							   fill="#654321", outline="#4a2f1a", width=1)
		canvas.create_rectangle(table_x + table_w - 2*leg_w, table_y + table_h,
							   table_x + table_w - leg_w, table_y + table_h + leg_h,
							   fill="#654321", outline="#4a2f1a", width=1)
		
		# Windows on back wall (1-4 windows equally spaced)
		if not hasattr(self, '_window_count'):
			self._window_count = 1
		
		num_windows = self._window_count
		window_h = int(wall_depth * 0.5)
		window_y = int(wall_depth * 0.2)
		
		# Fixed window width (same size for all windows)
		window_w = int(width * 0.15)  # Each window is 15% of width
		
		# Calculate spacing to spread windows equally across the wall
		if num_windows == 1:
			# Single window centered
			start_x = (width - window_w) // 2
			spacing = 0
		else:
			# Multiple windows: calculate spacing to spread them evenly
			# Total space for windows
			total_window_width = num_windows * window_w
			# Remaining space for gaps (including margins)
			remaining_space = width - total_window_width
			# Divide remaining space into (num_windows + 1) gaps
			spacing = remaining_space // (num_windows + 1)
			start_x = spacing
		
		for i in range(num_windows):
			window_x = start_x + i * (window_w + spacing)
			
			# Sky background
			canvas.create_rectangle(window_x, window_y, window_x + window_w, window_y + window_h,
								   fill="#87ceeb", outline="")
			# Window frame
			canvas.create_rectangle(window_x, window_y, window_x + window_w, window_y + window_h,
								   fill="", outline="#4682b4", width=3)
			canvas.create_line(window_x + window_w//2, window_y, window_x + window_w//2, window_y + window_h,
							  fill="#4682b4", width=2)
			canvas.create_line(window_x, window_y + window_h//2, window_x + window_w, window_y + window_h//2,
							  fill="#4682b4", width=2)
		
		# Draw assets
		try:
			from PIL import Image, ImageTk
			
			# Keep reference to prevent garbage collection
			if not hasattr(self, '_asset_preview_images'):
				self._asset_preview_images = []
			self._asset_preview_images.clear()
			
			# 1) Floor assets stretched across floor area
			for asset in self.custom_assets:
				if asset.get("category") != "Floor":
					continue
				filepath = asset.get("path")
				if not filepath:
					continue
				img = Image.open(filepath)
				if img.mode != 'RGBA':
					img = img.convert('RGBA')
				new_width = int(width)
				new_height = max(1, int(height - wall_depth))
				img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
				photo = ImageTk.PhotoImage(img)
				self._asset_preview_images.append(photo)
				canvas.create_image(0, wall_depth, image=photo, anchor="nw")

			# 2) Posters on wall and 3) rugs/furniture on surface
			for desired_group in ("Poster", "Rug/Furniture"):
				for asset in self.custom_assets:
					cat = asset.get("category")
					if desired_group == "Poster" and cat != "Poster":
						continue
					if desired_group == "Rug/Furniture" and cat not in ("Rug", "Furniture"):
						continue

					filepath = asset.get("path")
					if not filepath:
						continue
					
					x = int(asset.get("x", 0.5) * width)
					y = int(asset.get("y", 0.5) * height)
					scale = asset.get("scale", 1.0)
					
					# Load image
					img = Image.open(filepath)
					
					# Handle animated GIFs (show first frame in preview)
					if asset.get("is_animated", False):
						try:
							img.seek(0)
						except Exception:
							pass
					
					# Convert RGBA if needed
					if img.mode != 'RGBA':
						img = img.convert('RGBA')
					
					# Scale image
					new_width = int(img.width * scale)
					new_height = int(img.height * scale)
					img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
					photo = ImageTk.PhotoImage(img)
					
					self._asset_preview_images.append(photo)
					canvas.create_image(x, y, image=photo, anchor="center")
		except ImportError:
			canvas.create_text(width//2, height//2, 
							  text="PIL/Pillow required for PNG/GIF support\nInstall: pip install pillow",
							  font=("", 10), fill="red")
		except Exception as e:
			canvas.create_text(width//2, height//2, text=f"Error: {str(e)}", 
							  font=("", 10), fill="red")
	
	def _save_assets(self):
		"""Save custom assets to settings."""
		if not hasattr(self, 'settings'):
			self.settings = {}
		self.settings['custom_assets'] = self.custom_assets
		self._save_settings()
	
	def _animate_pets(self):
		"""Animate the entire scene: pets, window, avatar idle/walk, and random events."""
		if not hasattr(self, 'avatar_canvas'):
			return
		import random, time
		# Determine canvas bounds (no update_idletasks to prevent flashing)
		canvas = self.avatar_canvas
		width = canvas.winfo_width() if canvas.winfo_width() > 10 else 600
		height = canvas.winfo_height() if canvas.winfo_height() > 10 else 400
		
		# Calculate normalized bounds with wall collision
		wall_depth_norm = 0.2
		side_wall_width_norm = 0.08
		margin_x_norm = 60.0 / width
		margin_y_norm = 60.0 / height
		
		# Wall collision boundaries
		left_boundary = side_wall_width_norm + margin_x_norm
		right_boundary = 1.0 - side_wall_width_norm - margin_x_norm
		top_boundary = wall_depth_norm + margin_y_norm
		bottom_boundary = 1.0 - margin_y_norm
		
		# 1) Pets wander with normalized coordinates and wall collision
		for pet in getattr(self, 'pets', []):
			if random.random() < 0.3:  # 30% chance to change direction
				pet["direction"] = random.choice(["left", "right", "up", "down"])
			# Convert pixel step to normalized
			step_x = 2.0 / width
			step_y = 2.0 / height
			if pet["direction"] == "left":
				pet["x"] = max(left_boundary, pet["x"] - step_x)
			elif pet["direction"] == "right":
				pet["x"] = min(right_boundary, pet["x"] + step_x)
			elif pet["direction"] == "up":
				pet["y"] = max(top_boundary, pet["y"] - step_y)
			elif pet["direction"] == "down":
				pet["y"] = min(bottom_boundary, pet["y"] + step_y)
		
		# 2) Window animation (clouds + sun)
		if hasattr(self, '_scene_window'):
			# advance sun parameter
			self._scene_window["sun_t"] = (self._scene_window.get("sun_t", 0.0) + 0.002) % 1.0
			for cloud in self._scene_window.get("clouds", []):
				cloud["x"] += cloud.get("speed", 0.003)
				if cloud["x"] > 1.2:
					cloud["x"] = -0.25
		
		# 2.5) Animate GIF assets
		for asset in getattr(self, 'custom_assets', []):
			if asset.get("is_animated", False):
				frame_count = asset.get("frame_count", 1)
				current = asset.get("current_frame", 0)
				asset["current_frame"] = (current + 1) % frame_count
		
		# 3) Avatar idle auto-walk + blinking + random events
		now = time.time()
		if getattr(self, '_avatar_auto_move', True) and now - getattr(self, '_last_user_move_time', now) > 3:
			# Occasionally pick new direction
			if random.random() < 0.1:
				self._avatar_state["direction"] = random.choice(["left", "right", "up", "down"])
			# Small step in current direction (normalized)
			dx_norm = dy_norm = 0
			dir = self._avatar_state.get("direction", "down")
			if dir == "left": dx_norm = -2.0 / width
			elif dir == "right": dx_norm = 2.0 / width
			elif dir == "up": dy_norm = -2.0 / height
			elif dir == "down": dy_norm = 2.0 / height
			# Apply wall collision boundaries for auto-walk
			x = max(left_boundary, min(right_boundary, self._avatar_state["x"] + dx_norm))
			y = max(top_boundary, min(bottom_boundary, self._avatar_state["y"] + dy_norm))
			self._avatar_state["x"], self._avatar_state["y"] = x, y
			# advance walk phase for bobbing
			self._avatar_walk_phase = (self._avatar_walk_phase + 0.3) % (2*3.14159)
		
		# Blinking
		if hasattr(self, '_blink_state'):
			bs = self._blink_state
			if not bs.get("active"):
				bs["ticks_to_next"] = bs.get("ticks_to_next", 30) - 1
				if bs["ticks_to_next"] <= 0:
					bs["active"] = True
					bs["progress"] = 0.0
			else:
				# progress 0->1 then finish
				bs["progress"] += 0.25
				if bs["progress"] >= 1.0:
					bs["active"] = False
					bs["ticks_to_next"] = random.randint(20, 50)
		
		# Random event (wave or jump)
		if hasattr(self, '_random_event'):
			re = self._random_event
			if re.get("type") is None and random.random() < 0.02:
				re["type"] = random.choice(["wave", "jump"]) 
				re["ticks_left"] = 10
			else:
				if re.get("ticks_left", 0) > 0:
					re["ticks_left"] -= 1
				else:
					re["type"] = None
		
		# Redraw room directly in animation loop (already scheduled at consistent interval)
		try:
			self.avatar_canvas.delete("all")
			self._draw_avatar_room()
		except Exception:
			pass
		
		# Continue animation at 120ms (smoother than 100ms, reduces flashing)
		self._avatar_animation_id = self.avatar_canvas.after(120, self._animate_pets)

	def _request_redraw(self):
		"""Coalesce redraw requests to avoid flicker and duplicate draws."""
		if not hasattr(self, 'avatar_canvas'):
			return
		# Debounce: only schedule if not already pending
		if getattr(self, '_redraw_scheduled', False):
			return
		self._redraw_scheduled = True
		self._redraw_after_id = self.avatar_canvas.after(10, self._perform_redraw)

	def _perform_redraw(self):
		"""Perform a single scene redraw safely."""
		self._redraw_scheduled = False
		if not hasattr(self, 'avatar_canvas'):
			return
		try:
			# Clear existing items so objects don't accumulate or drift
			self.avatar_canvas.delete("all")
			self._draw_avatar_room()
		except Exception:
			pass
	
	def _setup_ai_tasks_tab(self):
		"""Set up the AI Tasks tab with chat interface for task generation."""
		# Initialize AI chat state
		self._ai_chat_history = []  # List of {"role": "user"|"assistant", "content": str}
		self._ai_suggested_tasks = []  # List of suggested task dicts
		
		# Main container
		main_frame = tk.Frame(self.ai_tasks_tab)
		main_frame.pack(fill="both", expand=True, padx=10, pady=10)
		
		# Title
		title_label = tk.Label(main_frame, text="AI Task Assistant", font=("", 14, "bold"))
		title_label.pack(pady=(0, 10))
		
		# Info label
		info_label = tk.Label(main_frame, text="Chat with AI to brainstorm and generate tasks for your goals",
							  wraplength=600, justify="center")
		info_label.pack(pady=(0, 10))
		
		# Chat history display (Text widget with scrollbar)
		chat_frame = tk.Frame(main_frame)
		chat_frame.pack(fill="both", expand=True, pady=(0, 10))
		
		chat_scroll = tk.Scrollbar(chat_frame)
		chat_scroll.pack(side="right", fill="y")
		
		self.ai_chat_display = tk.Text(chat_frame, wrap="word", state="disabled",
									   yscrollcommand=chat_scroll.set, height=15)
		self.ai_chat_display.pack(side="left", fill="both", expand=True)
		chat_scroll.config(command=self.ai_chat_display.yview)
		
		# Configure text tags for styling
		self.ai_chat_display.tag_config("user", foreground="#0066cc", font=("", 10, "bold"))
		self.ai_chat_display.tag_config("assistant", foreground="#008800", font=("", 10, "bold"))
		self.ai_chat_display.tag_config("task_suggestion", foreground="#cc6600", font=("", 9, "bold"))
		
		# Input frame
		input_frame = tk.Frame(main_frame)
		input_frame.pack(fill="x", pady=(0, 10))
		
		self.ai_input_entry = tk.Entry(input_frame)
		self.ai_input_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
		self.ai_input_entry.bind("<Return>", lambda e: self._ai_send_message())
		
		self.ai_send_btn = tk.Button(input_frame, text="Send", width=10, command=self._ai_send_message)
		self.ai_send_btn.pack(side="left")
		
		# Buttons frame
		btn_frame = tk.Frame(main_frame)
		btn_frame.pack(fill="x")
		
		tk.Button(btn_frame, text="Clear Chat", width=12, command=self._ai_clear_chat).pack(side="left", padx=2)
		tk.Button(btn_frame, text="Quick Start", width=12, command=self._ai_quick_start).pack(side="left", padx=2)
		
		# Suggested tasks frame (will be populated dynamically)
		self.ai_suggestions_frame = tk.Frame(main_frame)
		self.ai_suggestions_frame.pack(fill="x", pady=(10, 0))
		
		# Add welcome message
		self._ai_add_message("assistant", 
			"Hi! I'm your AI task assistant. I'm here to have a conversation with you about your goals and help turn them into actionable tasks.\n\n"
			"You can tell me anything - even if you're not sure what you want or say 'I don't know', I'll ask questions to help you figure it out!\n\n"
			"What's on your mind? What would you like to achieve or improve in your life?")
	
	def _ai_add_message(self, role, content):
		"""Add a message to the chat display."""
		self.ai_chat_display.config(state="normal")
		
		if self._ai_chat_history:  # Add separator if not first message
			self.ai_chat_display.insert("end", "\n\n")
		
		label = "You: " if role == "user" else "AI: "
		self.ai_chat_display.insert("end", label, role)
		self.ai_chat_display.insert("end", content)
		
		self.ai_chat_display.config(state="disabled")
		self.ai_chat_display.see("end")
	
	def _ai_send_message(self):
		"""Send user message and get AI response."""
		user_msg = self.ai_input_entry.get().strip()
		if not user_msg:
			return
		
		# Add user message to history and display
		self._ai_chat_history.append({"role": "user", "content": user_msg})
		self._ai_add_message("user", user_msg)
		self.ai_input_entry.delete(0, "end")
		
		# Disable send button while processing
		self.ai_send_btn.config(state="disabled", text="Thinking...")
		self.root.update_idletasks()
		
		# Get AI response
		self.root.after(100, lambda: self._ai_process_response(user_msg))
	
	def _ai_process_response(self, user_msg):
		"""Process AI response (placeholder for actual AI integration)."""
		# For now, use a simple rule-based system
		# In production, this would call OpenAI/Anthropic/local LLM API
		
		response = self._ai_generate_response(user_msg)
		
		# Add assistant response
		self._ai_chat_history.append({"role": "assistant", "content": response})
		self._ai_add_message("assistant", response)
		
		# Extract and display suggested tasks
		self._ai_extract_and_display_tasks(response)
		
		# Re-enable send button
		self.ai_send_btn.config(state="normal", text="Send")
	
	def _ai_generate_response(self, user_msg):
		"""Generate AI response based on user message with conversational follow-ups."""
		lower_msg = user_msg.lower()
		
		# Track conversation context for better responses
		if not hasattr(self, '_ai_context'):
			self._ai_context = {"topic": None, "depth": 0}
		
		# Handle uncertainty responses
		if any(phrase in lower_msg for phrase in ["don't know", "dont know", "not sure", "maybe", "idk", "unsure", "no idea"]):
			# Provide suggestions based on context
			if self._ai_context.get("topic") == "fitness":
				return ("No worries! Let me ask you some questions to help:\n\n"
						"🤔 Think about:\n"
						"• Do you want to lose weight, gain muscle, or improve general health?\n"
						"• Do you prefer working out at home or at a gym?\n"
						"• How much time can you dedicate per day? (15-30-60 minutes?)\n"
						"• Any physical limitations or injuries I should know about?\n\n"
						"Just tell me whatever you can, and I'll suggest specific tasks!")
			
			elif self._ai_context.get("topic") == "learning":
				return ("That's okay! Let's explore together:\n\n"
						"🤔 Consider:\n"
						"• What interests you? (programming, languages, music, art, business?)\n"
						"• Why do you want to learn? (career, hobby, personal growth?)\n"
						"• Do you learn better from videos, books, or hands-on practice?\n"
						"• How much time can you invest per week?\n\n"
						"Share what feels right, and I'll help you create a learning plan!")
			
			elif self._ai_context.get("topic") == "project":
				return ("Let's brainstorm together! \n\n"
						"🤔 Questions to spark ideas:\n"
						"• What problems frustrate you in daily life?\n"
						"• What would make your work or hobbies easier?\n"
						"• Do you want to build something for yourself or others?\n"
						"• What skills do you already have? (coding, design, writing?)\n\n"
						"Tell me anything that comes to mind!")
			
			else:
				return ("That's completely fine! Let's figure it out together. \n\n"
						"🤔 To help you decide:\n"
						"• What areas of your life would you like to improve?\n"
						"  (health, career, relationships, skills, organization?)\n"
						"• What's been on your mind lately?\n"
						"• If you had one extra hour every day, how would you use it?\n\n"
						"Just share your thoughts, no pressure!")
		
		# Handle follow-up questions and conversation flow
		recent_history = " ".join([msg["content"].lower() for msg in self._ai_chat_history[-3:]])
		
		# Fitness context
		if any(word in lower_msg for word in ["fitness", "health", "exercise", "workout", "gym", "weight", "muscle", "cardio", "strength"]) or self._ai_context.get("topic") == "fitness":
			self._ai_context["topic"] = "fitness"
			self._ai_context["depth"] += 1
			
			# First time discussing fitness
			if self._ai_context["depth"] == 1:
				return ("Great! Let's talk about your fitness goals. \n\n"
						"🏋️ To create a personalized plan, tell me:\n"
						"• What's your main fitness goal? (lose weight, build muscle, improve endurance, feel healthier?)\n"
						"• Where do you want to work out? (home, gym, outdoors?)\n"
						"• How often can you commit? (2-3-4-5 days per week?)\n"
						"• What's your current activity level? (beginner, intermediate, active?)\n\n"
						"Don't worry if you're not sure about everything - just tell me what you know!")
			
			# Deeper conversation
			elif "home" in lower_msg:
				return ("Perfect! Home workouts are super convenient. Based on that:\n\n"
						"📋 TASKS:\n"
						"- Clear workout space in home\n"
						"- Get basic equipment (yoga mat, dumbbells, resistance bands)\n"
						"- Download fitness app (Nike Training Club, FitBod, or YouTube)\n"
						"- Schedule 3 workout days this week\n"
						"- Do 20-min beginner workout (full body)\n"
						"- Track progress in fitness journal\n"
						"- Set weekly fitness goals\n\n"
						"Would you like specific beginner workout ideas or meal planning tips too?")
			
			elif "gym" in lower_msg:
				return ("Awesome! Gym access opens up many options:\n\n"
						"📋 TASKS:\n"
						"- Research and join a nearby gym\n"
						"- Book gym orientation session\n"
						"- Get workout clothes and water bottle\n"
						"- Plan gym schedule (e.g., Mon/Wed/Fri)\n"
						"- Learn basic equipment usage (treadmill, weights, machines)\n"
						"- Start with full-body routine (3x per week)\n"
						"- Consider hiring trainer for first few sessions\n\n"
						"Are you interested in strength training, cardio, or both?")
			
			elif any(word in lower_msg for word in ["lose", "weight", "fat", "slim"]):
				return ("Weight loss is a common goal! It's about consistency:\n\n"
						"📋 TASKS:\n"
						"- Calculate daily calorie needs (BMR calculator)\n"
						"- Set realistic weight loss goal (1-2 lbs per week)\n"
						"- Install food tracking app (MyFitnessPal, Lose It)\n"
						"- Plan healthy meals for the week\n"
						"- Do 30-min cardio 4x per week\n"
						"- Drink 8 glasses of water daily\n"
						"- Take weekly progress photos and measurements\n"
						"- Get 7-8 hours of sleep nightly\n\n"
						"Want help with meal planning or specific exercise routines?")
			
			elif any(word in lower_msg for word in ["muscle", "strong", "strength", "bulk", "gain"]):
				return ("Building muscle requires the right training and nutrition:\n\n"
						"📋 TASKS:\n"
						"- Calculate protein needs (0.8-1g per lb body weight)\n"
						"- Create progressive overload workout plan\n"
						"- Start strength training 3-4x per week\n"
						"- Learn proper form for major lifts (squats, deadlifts, bench press)\n"
						"- Eat in slight caloric surplus (200-300 calories)\n"
						"- Track workout progress (weights and reps)\n"
						"- Get adequate rest between workout days\n"
						"- Consider creatine supplementation\n\n"
						"Do you have access to weights, or should I suggest bodyweight alternatives?")
			
			else:
				# General fitness response
				return ("Here's a solid foundation to get started:\n\n"
						"📋 TASKS:\n"
						"- Set specific, measurable fitness goal\n"
						"- Schedule workout times in calendar\n"
						"- Start with 20-30 min sessions, 3x per week\n"
						"- Mix cardio and strength training\n"
						"- Track workouts in a journal or app\n"
						"- Stay hydrated throughout the day\n"
						"- Focus on whole foods and vegetables\n"
						"- Get 7-9 hours of quality sleep\n\n"
						"What's your biggest challenge with fitness? Time, motivation, or knowledge?")
		
		# Learning context
		elif any(word in lower_msg for word in ["learn", "study", "course", "tutorial", "skill"]) or self._ai_context.get("topic") == "learning":
			self._ai_context["topic"] = "learning"
			self._ai_context["depth"] += 1
			
			if self._ai_context["depth"] == 1:
				return ("I love helping people learn new things! \n\n"
						"📚 Tell me more:\n"
						"• What do you want to learn? (programming, language, instrument, art, business?)\n"
						"• What's your motivation? (career change, hobby, personal growth?)\n"
						"• How do you prefer learning? (videos, books, interactive courses, practice?)\n"
						"• How much time can you dedicate daily or weekly?\n\n"
						"Even a rough idea helps me create a tailored learning path!")
			
			elif any(word in lower_msg for word in ["python", "programming", "code", "coding", "web", "app", "software"]):
				return ("Programming is an amazing skill! Here's a practical path:\n\n"
						"📋 TASKS:\n"
						"- Install Python and VS Code\n"
						"- Complete 'Python for Beginners' course (Codecademy or freeCodeCamp)\n"
						"- Practice 30 minutes daily on coding exercises\n"
						"- Build simple calculator project\n"
						"- Learn git and GitHub basics\n"
						"- Join programming community (Reddit r/learnprogramming)\n"
						"- Build personal project (to-do app, weather app)\n"
						"- Document learning journey in blog\n\n"
						"Have you programmed before, or is this your first time?")
			
			elif any(word in lower_msg for word in ["language", "spanish", "french", "japanese", "chinese", "speak"]):
				return ("Language learning is so rewarding! Consistency is key:\n\n"
						"📋 TASKS:\n"
						"- Choose language learning app (Duolingo, Babbel, Busuu)\n"
						"- Set daily 15-minute practice goal\n"
						"- Learn basic phrases and greetings\n"
						"- Watch shows with subtitles in target language\n"
						"- Find language exchange partner (HelloTalk, Tandem)\n"
						"- Make flashcards for vocabulary\n"
						"- Join language learning subreddit or Discord\n"
						"- Set goal: hold 5-minute conversation in 3 months\n\n"
						"Which language interests you? What's your reason for learning?")
			
			else:
				return ("Here's a general learning framework:\n\n"
						"📋 TASKS:\n"
						"- Define learning goal and target skill level\n"
						"- Research best resources (courses, books, videos)\n"
						"- Create study schedule (consistency beats intensity)\n"
						"- Start with fundamentals\n"
						"- Practice actively (don't just consume)\n"
						"- Join community of learners\n"
						"- Track progress weekly\n"
						"- Apply knowledge in real project\n\n"
						"What specific topic are you leaning towards?")
		
		# Project/Building context
		elif any(word in lower_msg for word in ["project", "build", "create", "develop", "make", "start"]) or self._ai_context.get("topic") == "project":
			self._ai_context["topic"] = "project"
			self._ai_context["depth"] += 1
			
			return ("Exciting! Every great project starts with planning:\n\n"
					"📋 TASKS:\n"
					"- Brainstorm project ideas and goals\n"
					"- Research similar projects for inspiration\n"
					"- Define scope and core features\n"
					"- Break project into 3-5 major phases\n"
					"- Set realistic timeline\n"
					"- Gather necessary tools and resources\n"
					"- Create project roadmap\n"
					"- Start with MVP (minimum viable product)\n\n"
					"What kind of project interests you? Software, creative, business, or something else?")
		
		# Writing context
		elif any(word in lower_msg for word in ["write", "book", "blog", "article", "content", "author"]):
			self._ai_context["topic"] = "writing"
			return ("Writing projects thrive on structure:\n\n"
					"📋 TASKS:\n"
					"- Brainstorm topics and themes\n"
					"- Create detailed outline\n"
					"- Set word count goals (500 words/day)\n"
					"- Schedule daily writing time\n"
					"- Write first draft without editing\n"
					"- Let draft rest 2-3 days\n"
					"- Revise and edit for clarity\n"
					"- Get feedback from beta readers\n"
					"- Polish and proofread final version\n\n"
					"What genre or topic are you writing about?")
		
		# Organization context
		elif any(word in lower_msg for word in ["organize", "clean", "declutter", "tidy", "productivity"]):
			self._ai_context["topic"] = "organization"
			return ("Organization creates mental clarity! Let's systematize:\n\n"
					"📋 TASKS:\n"
					"- List all areas needing organization\n"
					"- Start with one room/area\n"
					"- Sort everything (keep/donate/trash)\n"
					"- Deep clean the space\n"
					"- Get storage solutions (bins, shelves)\n"
					"- Label everything clearly\n"
					"- Take before/after photos\n"
					"- Create maintenance routine (15 min/day)\n\n"
					"Which area of your life needs organization most?")
		
		# Positive acknowledgments
		elif any(word in lower_msg for word in ["yes", "yeah", "sure", "okay", "sounds good", "perfect", "great"]):
			return ("Perfect! I'm here to help you along the way. Feel free to:\n\n"
					"• Click any task suggestion to add it to your list\n"
					"• Ask follow-up questions for more specific advice\n"
					"• Tell me about challenges you're facing\n"
					"• Request modifications to any task\n\n"
					"What else would you like to explore or clarify?")
		
		# Generic/First contact
		else:
			return ("I'm here to help you achieve your goals through actionable tasks!\n\n"
					"💡 Popular topics I can help with:\n"
					"• Fitness and health goals\n"
					"• Learning new skills (programming, languages, etc.)\n"
					"• Starting projects or side hustles\n"
					"• Writing and creative work\n"
					"• Organization and productivity\n"
					"• Career development\n\n"
					"What would you like to work on? (Or just tell me what's on your mind!)")
	
	def _ai_extract_and_display_tasks(self, response):
		"""Extract task suggestions from AI response and display as addable items."""
		# Clear previous suggestions
		for widget in self.ai_suggestions_frame.winfo_children():
			widget.destroy()
		
		self._ai_suggested_tasks = []
		
		# Extract lines that start with "- " (task format)
		lines = response.split("\n")
		tasks = []
		for line in lines:
			stripped = line.strip()
			if stripped.startswith("- "):
				task_text = stripped[2:].strip()
				if task_text:
					tasks.append(task_text)
		
		if not tasks:
			return
		
		# Display header
		tk.Label(self.ai_suggestions_frame, text="Suggested Tasks (click to add):",
				font=("", 10, "bold")).pack(anchor="w", pady=(5, 5))
		
		# Create buttons for each suggested task
		for task_text in tasks:
			self._ai_suggested_tasks.append(task_text)
			
			task_btn_frame = tk.Frame(self.ai_suggestions_frame)
			task_btn_frame.pack(fill="x", pady=2)
			
			# Task button
			task_btn = tk.Button(task_btn_frame, text=f"➕ {task_text}", 
								anchor="w", width=60, command=lambda t=task_text: self._ai_add_task_to_list(t))
			task_btn.pack(side="left", fill="x", expand=True)
	
	def _ai_add_task_to_list(self, task_text):
		"""Add suggested task to the main tasks list with intelligent priority and deadline."""
		from datetime import date, timedelta
		
		# Switch to Tasks tab
		self.notebook.select(self.tasks_tab)
		
		# Determine smart category based on task content and conversation context
		if self.settings.get("ai_smart_categories", True):
			category = self._ai_determine_category(task_text)
		else:
			category = "AI Generated"
		
		# Ensure category exists
		self._ensure_category(category)
		
		# Add # prefix if setting is enabled
		if self.settings.get("ai_task_prefix", True):
			task_text = f"# {task_text}"
		
		# Clear placeholder if present
		if self.entry_has_placeholder:
			self.entry.delete(0, "end")
			self.entry.config(fg=self.current_theme.get("entry_fg", "#000000"))
			self.entry_has_placeholder = False
		
		# Determine intelligent priority based on task content
		priority = self._ai_determine_priority(task_text)
		
		# Determine intelligent deadline based on task content and priority
		deadline_days = self._ai_determine_deadline_days(task_text, priority)
		deadline_date = date.today() + timedelta(days=deadline_days)
		deadline_str = deadline_date.strftime("%Y-%m-%d")
		
		# Add task
		self.entry.delete(0, "end")
		self.entry.insert(0, task_text)
		self.category_var.set(category)
		self.priority_var.set(priority)
		self.add_deadline_var.set(deadline_str)
		
		# Add the task
		self.add_task()
		
		# Show confirmation in AI chat with priority and deadline
		priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(priority, "⚪")
		self._ai_add_message("assistant", 
			f"✅ Added task: {task_text}\n   📁 {category} | {priority_emoji} {priority} | 📅 {deadline_str}")
	
	def _ai_determine_category(self, task_text):
		"""Determine appropriate category based on task content and conversation context."""
		lower_text = task_text.lower()
		
		# Get conversation context
		context_topic = getattr(self, '_ai_context', {}).get("topic")
		
		# Fitness/Health category
		if context_topic == "fitness" or any(word in lower_text for word in [
			"workout", "exercise", "gym", "fitness", "health", "run", "walk", "cardio",
			"strength", "yoga", "stretch", "weight", "muscle", "train", "sport",
			"nutrition", "diet", "meal", "calorie", "water", "sleep"
		]):
			return "Fitness"
		
		# Learning/Education category
		if context_topic == "learning" or any(word in lower_text for word in [
			"learn", "study", "course", "tutorial", "practice", "lesson", "skill",
			"read", "book", "video", "class", "training", "education", "research",
			"programming", "code", "python", "language", "instrument"
		]):
			return "Learning"
		
		# Work/Career category
		if any(word in lower_text for word in [
			"project", "meeting", "presentation", "report", "deadline", "client",
			"email", "call", "interview", "resume", "career", "job", "work",
			"business", "professional", "office", "team", "manager"
		]):
			return "Work"
		
		# Writing/Creative category
		if context_topic == "writing" or any(word in lower_text for word in [
			"write", "blog", "article", "post", "draft", "edit", "publish",
			"content", "story", "book", "chapter", "essay", "creative"
		]):
			return "Writing"
		
		# Home/Organization category
		if any(word in lower_text for word in [
			"organize", "clean", "declutter", "tidy", "home", "room", "kitchen",
			"laundry", "groceries", "shopping", "errand", "maintenance", "repair"
		]):
			return "Home"
		
		# Personal Development category
		if any(word in lower_text for word in [
			"goal", "habit", "routine", "meditate", "journal", "reflect",
			"mindfulness", "growth", "develop", "improve", "better"
		]):
			return "Personal"
		
		# Finance category
		if any(word in lower_text for word in [
			"budget", "money", "finance", "payment", "bill", "tax", "savings",
			"invest", "expense", "bank", "insurance"
		]):
			return "Finance"
		
		# Default: use context topic or AI Generated
		if context_topic:
			return context_topic.capitalize()
		
		return "AI Generated"
	
	def _ai_determine_priority(self, task_text):
		"""Determine task priority based on content analysis."""
		lower_text = task_text.lower()
		
		# High priority indicators
		high_keywords = [
			"urgent", "important", "critical", "asap", "immediately", "emergency",
			"deadline", "must", "required", "essential", "vital", "crucial",
			"schedule", "book", "appointment", "meeting", "interview",
			"health check", "doctor", "medical", "safety"
		]
		
		# Low priority indicators
		low_keywords = [
			"optional", "consider", "maybe", "eventually", "someday",
			"explore", "research", "learn about", "read about", "watch",
			"review", "browse", "organize", "tidy", "label", "sort"
		]
		
		# Check for high priority
		if any(keyword in lower_text for keyword in high_keywords):
			return "High"
		
		# Check for low priority
		if any(keyword in lower_text for keyword in low_keywords):
			return "Low"
		
		# Context-based priority
		context_topic = getattr(self, '_ai_context', {}).get("topic")
		
		# First few steps in a plan are usually higher priority
		if any(word in lower_text for word in ["start", "begin", "first", "initial", "setup", "install", "create account"]):
			return "High"
		
		# Health/fitness immediate tasks
		if context_topic == "fitness" and any(word in lower_text for word in ["today", "schedule", "plan"]):
			return "High"
		
		# Default to Medium
		return "Medium"
	
	def _ai_determine_deadline_days(self, task_text, priority):
		"""Determine reasonable deadline offset in days based on task content and priority."""
		from datetime import date
		
		lower_text = task_text.lower()
		
		# Immediate/today tasks (0-1 days)
		if any(word in lower_text for word in ["today", "now", "immediately", "asap", "urgent"]):
			return 0
		
		# This week tasks (1-7 days based on priority)
		if any(word in lower_text for word in ["this week", "soon", "schedule", "book"]):
			return 3 if priority == "High" else 7
		
		# Research/planning tasks (longer timeframe)
		if any(word in lower_text for word in ["research", "explore", "learn", "study", "read"]):
			return 14 if priority == "High" else 30
		
		# Installation/setup tasks (quick turnaround)
		if any(word in lower_text for word in ["install", "download", "setup", "get", "buy", "purchase"]):
			return 2 if priority == "High" else 7
		
		# Daily/routine tasks (short deadline)
		if any(word in lower_text for word in ["daily", "track", "log", "record", "drink water"]):
			return 1
		
		# Weekly tasks
		if any(word in lower_text for word in ["weekly", "week", "per week"]):
			return 7
		
		# Practice/habit tasks (recurring concept, shorter deadline)
		if any(word in lower_text for word in ["practice", "exercise", "workout", "meditate"]):
			return 3 if priority == "High" else 7
		
		# Review/feedback tasks (medium timeframe)
		if any(word in lower_text for word in ["review", "feedback", "check", "monitor"]):
			return 7 if priority == "High" else 14
		
		# Documentation/writing tasks (longer timeframe)
		if any(word in lower_text for word in ["document", "write", "draft", "article", "blog"]):
			return 7 if priority == "High" else 21
		
		# Project planning/milestone tasks
		if any(word in lower_text for word in ["plan", "roadmap", "outline", "design", "brainstorm"]):
			return 5 if priority == "High" else 14
		
		# Implementation tasks (medium timeframe)
		if any(word in lower_text for word in ["implement", "build", "create", "develop", "code"]):
			return 14 if priority == "High" else 30
		
		# Testing/quality tasks
		if any(word in lower_text for word in ["test", "debug", "fix", "proofread", "edit"]):
			return 7 if priority == "High" else 14
		
		# Completion/finalization tasks
		if any(word in lower_text for word in ["complete", "finish", "finalize", "publish", "deploy"]):
			return 7 if priority == "High" else 21
		
		# Default deadlines based on priority
		if priority == "High":
			return 7  # 1 week
		elif priority == "Low":
			return 30  # 1 month
		else:
			return 14  # 2 weeks
	
	def _ai_clear_chat(self):
		"""Clear the chat history."""
		self._ai_chat_history = []
		self.ai_chat_display.config(state="normal")
		self.ai_chat_display.delete("1.0", "end")
		self.ai_chat_display.config(state="disabled")
		
		# Clear suggestions
		for widget in self.ai_suggestions_frame.winfo_children():
			widget.destroy()
		self._ai_suggested_tasks = []
		
		# Reset context
		if hasattr(self, '_ai_context'):
			self._ai_context = {"topic": None, "depth": 0}
		
		# Add welcome message back
		self._ai_add_message("assistant", "Chat cleared. Fresh start! What would you like to explore or work on?")
	
	def _ai_quick_start(self):
		"""Provide quick start prompts for common scenarios."""
		prompts = [
			"I want to build a web application",
			"I need to learn Python programming",
			"I want to start a fitness routine",
			"I need to organize my home office",
			"I want to write a blog post",
		]
		
		# Create popup with quick start options
		popup = tk.Toplevel(self.root)
		popup.title("Quick Start Prompts")
		popup.transient(self.root)
		popup.resizable(False, False)
		
		tk.Label(popup, text="Choose a starting point:", font=("", 11, "bold")).pack(pady=10, padx=20)
		
		for prompt in prompts:
			btn = tk.Button(popup, text=prompt, width=40, anchor="w",
						   command=lambda p=prompt: self._ai_use_quick_prompt(p, popup))
			btn.pack(pady=3, padx=20)
		
		tk.Button(popup, text="Cancel", width=15, command=popup.destroy).pack(pady=10)
		
		# Center popup
		popup.update_idletasks()
		x = self.root.winfo_x() + (self.root.winfo_width() - popup.winfo_width()) // 2
		y = self.root.winfo_y() + (self.root.winfo_height() - popup.winfo_height()) // 2
		popup.geometry(f"+{x}+{y}")
	
	def _ai_use_quick_prompt(self, prompt, popup):
		"""Use a quick start prompt and immediately generate tasks."""
		popup.destroy()
		
		# Add user message to history and display
		self._ai_chat_history.append({"role": "user", "content": prompt})
		self._ai_add_message("user", prompt)
		
		# Immediately process and show response with tasks
		response = self._ai_generate_response(prompt)
		self._ai_chat_history.append({"role": "assistant", "content": response})
		self._ai_add_message("assistant", response)
		
		# Extract and display suggested tasks
		self._ai_extract_and_display_tasks(response)
	
	def _load_current_theme_to_editor(self):
		"""Load current theme values into the editor."""
		for key, var in self.theme_color_vars.items():
			var.set(self.current_theme.get(key, "#ffffff"))
	
	def _preview_custom_theme(self):
		"""Apply the custom theme temporarily to preview it."""
		custom_theme = {key: var.get() for key, var in self.theme_color_vars.items()}
		self.current_theme = custom_theme
		self.apply_theme()
		self._refresh_all_category_colors()
		self._update_stats_view()
		self._update_calendar_view()
		messagebox.showinfo("Preview", "Theme preview applied! Use 'Save Theme' to keep it.")
	
	def _save_custom_theme(self):
		"""Save the custom theme to the themes dictionary."""
		theme_name = self.custom_theme_name_var.get().strip()
		if not theme_name:
			messagebox.showwarning("No Name", "Please enter a theme name.")
			return
		
		custom_theme = {key: var.get() for key, var in self.theme_color_vars.items()}
		self.themes[theme_name] = custom_theme
		
		# Update the theme combo box
		self.theme_combo['values'] = list(self.themes.keys())
		self.theme_var.set(theme_name)
		self.current_theme = custom_theme
		self.apply_theme()
		self._refresh_all_category_colors()
		self._update_stats_view()
		self._update_calendar_view()
		
		# Save themes to file
		self._save_themes_to_file()
		
		messagebox.showinfo("Saved", f"Theme '{theme_name}' saved successfully!")
	
	def _delete_custom_theme(self):
		"""Delete a custom theme."""
		theme_name = self.custom_theme_name_var.get().strip()
		if not theme_name:
			messagebox.showwarning("No Name", "Please enter a theme name to delete.")
			return
		
		if theme_name not in self.themes:
			messagebox.showwarning("Not Found", f"Theme '{theme_name}' doesn't exist.")
			return
		
		# Don't allow deleting built-in themes
		built_in = ["Light", "Dark", "Solarized Dark", "Nord", "GitHub Light", "GitHub Dark"]
		if theme_name in built_in:
			messagebox.showwarning("Cannot Delete", "Cannot delete built-in themes.")
			return
		
		if messagebox.askyesno("Confirm Delete", f"Delete theme '{theme_name}'?"):
			del self.themes[theme_name]
			self.theme_combo['values'] = list(self.themes.keys())
			self.theme_var.set("Light")
			self.change_theme()
			self._save_themes_to_file()
			messagebox.showinfo("Deleted", f"Theme '{theme_name}' deleted.")
	
	def _save_themes_to_file(self):
		"""Save custom themes to a JSON file."""
		themes_file = os.path.join(DATA_DIR, "custom_themes.json")
		# Only save non-built-in themes
		built_in = ["Light", "Dark", "Solarized Dark", "Nord", "GitHub Light", "GitHub Dark"]
		custom_themes = {name: theme for name, theme in self.themes.items() if name not in built_in}
		try:
			with open(themes_file, 'w') as f:
				json.dump(custom_themes, f, indent=2)
		except Exception as e:
			messagebox.showerror("Save Error", f"Failed to save themes: {str(e)}")
	
	def _load_themes_from_file(self):
		"""Load custom themes from JSON file."""
		themes_file = os.path.join(DATA_DIR, "custom_themes.json")
		if os.path.exists(themes_file):
			try:
				with open(themes_file, 'r') as f:
					custom_themes = json.load(f)
					self.themes.update(custom_themes)
			except Exception as e:
				print(f"Failed to load custom themes: {str(e)}")
	
	def _import_theme_file(self):
		"""Import themes from a custom_themes.json file."""
		file_path = filedialog.askopenfilename(
			title="Select Theme File",
			filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
			initialdir=DATA_DIR
		)
		
		if not file_path:
			return
		
		try:
			with open(file_path, 'r') as f:
				imported_themes = json.load(f)
			
			# Validate that it's a dictionary of themes
			if not isinstance(imported_themes, dict):
				messagebox.showerror("Invalid File", "Theme file must contain a JSON object with theme definitions.")
				return
			
			# Count how many themes will be imported
			new_count = 0
			updated_count = 0
			built_in = ["Light", "Dark", "Solarized Dark", "Nord", "GitHub Light", "GitHub Dark"]
			
			for theme_name, theme_data in imported_themes.items():
				if theme_name in built_in:
					continue  # Skip built-in theme names
				
				if not isinstance(theme_data, dict):
					continue  # Skip invalid theme data
				
				if theme_name in self.themes:
					updated_count += 1
				else:
					new_count += 1
				
				self.themes[theme_name] = theme_data
			
			if new_count == 0 and updated_count == 0:
				messagebox.showinfo("No Themes Imported", "No valid custom themes found in the file.")
				return
			
			# Update the theme combo box
			self.theme_combo['values'] = list(self.themes.keys())
			
			# Save the merged themes
			self._save_themes_to_file()
			
			# Show success message
			msg = f"Successfully imported {new_count} new theme(s)"
			if updated_count > 0:
				msg += f" and updated {updated_count} existing theme(s)"
			msg += "."
			messagebox.showinfo("Import Successful", msg)
			
		except json.JSONDecodeError:
			messagebox.showerror("Invalid File", "The selected file is not a valid JSON file.")
		except Exception as e:
			messagebox.showerror("Import Error", f"Failed to import themes: {str(e)}")

	def change_theme(self):
		self.current_theme = self.themes[self.theme_var.get()]
		self.apply_theme()
		self._refresh_all_category_colors()  # Refresh category colors with new theme background
		self._apply_alternating_rows()  # Refresh overdue highlights with new theme
		self._update_stats_view()  # Redraw stats graph with new theme colors
		self._update_calendar_view()  # Redraw calendar with new theme colors
		# Re-evaluate min window size in case fonts or paddings changed
		self._update_min_window_size()
	
	def _create_gradient(self, widget, color1, color2=None, vertical=True):
		"""Apply a gradient background to a widget using a canvas."""
		if not color2 or color1 == color2:
			# No gradient, just solid color
			if isinstance(widget, tk.Canvas):
				widget.configure(bg=color1)
			return
		
		# Create or get canvas for gradient
		if not hasattr(widget, '_gradient_canvas'):
			# Store original widget properties
			widget._gradient_canvas = tk.Canvas(widget, highlightthickness=0, bd=0)
			widget._gradient_canvas.place(x=0, y=0, relwidth=1, relheight=1)
			widget._gradient_canvas.lower()  # Send to back
		
		canvas = widget._gradient_canvas
		
		def draw_gradient(event=None):
			canvas.delete("gradient")
			width = canvas.winfo_width() or 1
			height = canvas.winfo_height() or 1
			
			# Parse colors
			r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
			r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
			
			steps = height if vertical else width
			for i in range(steps):
				ratio = i / max(steps - 1, 1)
				r = int(r1 + (r2 - r1) * ratio)
				g = int(g1 + (g2 - g1) * ratio)
				b = int(b1 + (b2 - b1) * ratio)
				color = f'#{r:02x}{g:02x}{b:02x}'
				
				if vertical:
					canvas.create_line(0, i, width, i, fill=color, tags="gradient")
				else:
					canvas.create_line(i, 0, i, height, fill=color, tags="gradient")
		
		canvas.bind("<Configure>", draw_gradient)
		draw_gradient()

	def _draw_canvas_gradient(self, canvas, color1, color2=None, vertical=True):
		"""Draw a gradient directly on a tk.Canvas as its background."""
		if not color2 or color1 == color2:
			# Solid background if no gradient
			canvas.configure(bg=color1)
			return
		# Determine size
		w = canvas.winfo_width() or canvas.winfo_reqwidth() or 300
		h = canvas.winfo_height() or canvas.winfo_reqheight() or 200
		# Parse colors
		r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
		r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
		steps = h if vertical else w
		steps = max(1, steps)
		# Draw gradient lines
		for i in range(steps):
			ratio = i / max(steps - 1, 1)
			r = int(r1 + (r2 - r1) * ratio)
			g = int(g1 + (g2 - g1) * ratio)
			b = int(b1 + (b2 - b1) * ratio)
			color = f'#{r:02x}{g:02x}{b:02x}'
			if vertical:
				canvas.create_line(0, i, w, i, fill=color)
			else:
				canvas.create_line(i, 0, i, h, fill=color)

	def apply_theme(self):
		# Apply theme to root and frames (with gradients if specified)
		bg_color = self.current_theme.get("bg", "#ffffff")
		bg_gradient = self.current_theme.get("bg_gradient")
		
		if bg_gradient and bg_gradient != bg_color:
			# Note: Root window doesn't support canvas gradients, use solid color
			self.root.configure(bg=bg_color)
		else:
			self.root.configure(bg=bg_color)
        
		# Update theme label
		self.theme_label.configure(bg=self.current_theme["bg"],
								 fg=self.current_theme["fg"])
		# Style ttk Treeview to match theme colors
		style = ttk.Style(self.root)
		style.theme_use('clam')  # Use clam theme for better color control
		style.configure('Treeview',
					  background=self.current_theme["listbox_bg"],
					  fieldbackground=self.current_theme["listbox_bg"],
					  foreground=self.current_theme["listbox_fg"],
					  borderwidth=0,
					  rowheight=25)
		
		# Create alternating row color for better readability
		def _hex_to_rgb(h):
			_h = h.lstrip('#')
			return tuple(int(_h[i:i+2], 16) for i in (0, 2, 4))
		
		style.configure('Treeview.Heading',
					  background=self.current_theme["button_bg"],
					  foreground=self.current_theme["button_fg"],
					  borderwidth=1,
					  relief="groove")
		
		bg_rgb = _hex_to_rgb(self.current_theme["listbox_bg"]) if isinstance(self.current_theme.get("listbox_bg"), str) else (255,255,255)
		# Create a slightly different shade for alternating rows (5% lighter/darker)
		alt_rgb = tuple(min(255, int(c * 1.05)) if sum(bg_rgb) < 384 else max(0, int(c * 0.95)) for c in bg_rgb)
		alt_bg = '#{:02x}{:02x}{:02x}'.format(*alt_rgb)
		
		# Configure tag for alternating rows
		self.tree.tag_configure('oddrow', background=alt_bg)
		
		# Configure overdue tag (red highlight for tasks past deadline)
		overdue_bg = self._blend_color_with_bg("#ff0000", 0.25)  # Red with 25% opacity
		self.tree.tag_configure('overdue', background=overdue_bg)
		
		# perceived brightness for selection color
		brightness = (0.299*bg_rgb[0] + 0.587*bg_rgb[1] + 0.114*bg_rgb[2]) / 255.0
		# Choose a strong accent based on background brightness
		accent_bg = "#1976d2" if brightness > 0.5 else "#4a90e2"
		accent_fg = "#ffffff"
		style.map('Treeview',
				 background=[('selected', accent_bg)],
				 foreground=[('selected', accent_fg)])
        
		for frame in self.root.winfo_children():
			if isinstance(frame, tk.Frame):
				frame.configure(bg=self.current_theme["bg"])
				for widget in frame.winfo_children():
					if isinstance(widget, (ttk.Combobox, ttk.Treeview, ttk.Scrollbar, ttk.Notebook)):
						continue  # Skip ttk widgets as they handle styling differently
					elif isinstance(widget, tk.Button):
						widget.configure(bg=self.current_theme["button_bg"],
									  fg=self.current_theme["button_fg"],
									  activebackground=self.current_theme["button_bg"],
									  activeforeground=self.current_theme["button_fg"])
					elif isinstance(widget, tk.Entry):
						widget.configure(bg=self.current_theme["entry_bg"],
									  fg=self.current_theme["entry_fg"],
									  insertbackground=self.current_theme["fg"])
					elif isinstance(widget, tk.Listbox):
						widget.configure(bg=self.current_theme["listbox_bg"],
									  fg=self.current_theme["listbox_fg"],
									  selectbackground=self.current_theme["button_bg"],
									  selectforeground=self.current_theme["button_fg"])
					elif isinstance(widget, tk.Canvas):
						# For canvas widgets, we draw gradients during render functions
						widget.configure(bg=self.current_theme.get("bg", "#ffffff"))
					elif isinstance(widget, tk.Scrollbar):
						widget.configure(bg=self.current_theme["button_bg"],
									  troughcolor=self.current_theme["bg"])
					elif isinstance(widget, tk.Label) and widget != self.theme_label:
						widget.configure(bg=self.current_theme["bg"],
									  fg=self.current_theme["fg"])
		
		# Also apply theme to widgets in notebook tabs
		for tab_frame in [self.tasks_tab, self.daily_tab, self.ai_tasks_tab, self.stats_tab, self.calendar_tab, self.theme_editor_tab, self.settings_tab, self.avatar_room_tab]:
			# Use solid background for tab frames to avoid any overlap issues with content
			tab_bg = self.current_theme.get("bg", "#ffffff")
			# If a previous gradient canvas exists, remove it to prevent covering content
			if hasattr(tab_frame, '_gradient_canvas'):
				try:
					tab_frame._gradient_canvas.destroy()
				except Exception:
					pass
				try:
					delattr(tab_frame, '_gradient_canvas')
				except Exception:
					pass
			tab_frame.configure(bg=tab_bg)
			for widget in tab_frame.winfo_children():
				if isinstance(widget, tk.Frame):
					# Solid background for frames
					frame_bg = self.current_theme.get("bg", "#ffffff")
					widget.configure(bg=frame_bg)
					for child in widget.winfo_children():
						if isinstance(child, (ttk.Combobox, ttk.Treeview, ttk.Scrollbar)):
							continue
						elif isinstance(child, tk.Button):
							child.configure(bg=self.current_theme["button_bg"],
										 fg=self.current_theme["button_fg"],
										 activebackground=self.current_theme["button_bg"],
										 activeforeground=self.current_theme["button_fg"])
						elif isinstance(child, tk.Entry):
							# Keep main task entry white, theme others
							if child != self.entry:
								child.configure(bg=self.current_theme["entry_bg"],
											 fg=self.current_theme["entry_fg"],
											 insertbackground=self.current_theme["fg"])
						elif isinstance(child, tk.Canvas):
							# For canvas widgets, we draw gradients during render functions
							child.configure(bg=self.current_theme.get("bg", "#ffffff"))
						elif isinstance(child, tk.Label):
							child.configure(bg=self.current_theme["bg"],
										 fg=self.current_theme["fg"])
						elif isinstance(child, tk.Radiobutton):
							child.configure(bg=self.current_theme["bg"],
										 fg=self.current_theme["fg"],
										 activebackground=self.current_theme["bg"],
										 activeforeground=self.current_theme["fg"],
										 selectcolor=self.current_theme["button_bg"])
						elif isinstance(child, tk.Checkbutton):
							child.configure(bg=self.current_theme["bg"],
									 fg=self.current_theme["fg"],
									 activebackground=self.current_theme["bg"],
									 activeforeground=self.current_theme["fg"],
									 selectcolor=self.current_theme["button_bg"])
				elif isinstance(widget, tk.Canvas):
					# For canvas widgets, we draw gradients during render functions
					widget.configure(bg=self.current_theme.get("bg", "#ffffff"))
				elif isinstance(widget, tk.Label):
					widget.configure(bg=self.current_theme["bg"],
								  fg=self.current_theme["fg"])
		
		# Style ttk.Notebook tabs
		style.configure('TNotebook', background=self.current_theme["bg"], borderwidth=0)
		style.configure('TNotebook.Tab',
					  background=self.current_theme["button_bg"],
					  foreground=self.current_theme["button_fg"],
					  padding=[10, 2])
		style.map('TNotebook.Tab',
				 background=[('selected', self.current_theme["listbox_bg"])],
				 foreground=[('selected', self.current_theme["fg"])])
		
		# Explicitly theme Calendar navigation widgets
		if hasattr(self, 'cal_prev_btn'):
			self.cal_prev_btn.configure(bg=self.current_theme["button_bg"],
									   fg=self.current_theme["button_fg"],
									   activebackground=self.current_theme["button_bg"],
									   activeforeground=self.current_theme["button_fg"],
									   highlightbackground=self.current_theme["bg"],
									   highlightcolor=self.current_theme["bg"])
		if hasattr(self, 'cal_next_btn'):
			self.cal_next_btn.configure(bg=self.current_theme["button_bg"],
									   fg=self.current_theme["button_fg"],
									   activebackground=self.current_theme["button_bg"],
									   activeforeground=self.current_theme["button_fg"],
									   highlightbackground=self.current_theme["bg"],
									   highlightcolor=self.current_theme["bg"])
		if hasattr(self, 'cal_today_btn'):
			self.cal_today_btn.configure(bg=self.current_theme["button_bg"],
										fg=self.current_theme["button_fg"],
										activebackground=self.current_theme["button_bg"],
										activeforeground=self.current_theme["button_fg"],
										highlightbackground=self.current_theme["bg"],
										highlightcolor=self.current_theme["bg"])
		if hasattr(self, 'cal_date_label'):
			self.cal_date_label.configure(bg=self.current_theme["button_bg"],
										 fg=self.current_theme["button_fg"])
		
		# Theme Calendar frames
		if hasattr(self, 'cal_header'):
			self.cal_header.configure(bg=self.current_theme["bg"])
		if hasattr(self, 'nav_frame'):
			self.nav_frame.configure(bg=self.current_theme["bg"])
		if hasattr(self, 'view_toggle_frame'):
			self.view_toggle_frame.configure(bg=self.current_theme["bg"])
		
		if hasattr(self, 'cal_weekly_radio'):
			self.cal_weekly_radio.configure(bg=self.current_theme["bg"],
										   fg=self.current_theme["fg"],
										   activebackground=self.current_theme["bg"],
										   activeforeground=self.current_theme["fg"],
										   selectcolor=self.current_theme["bg"],
										   highlightbackground=self.current_theme["bg"],
										   highlightcolor=self.current_theme["bg"])
		if hasattr(self, 'cal_monthly_radio'):
			self.cal_monthly_radio.configure(bg=self.current_theme["bg"],
											fg=self.current_theme["fg"],
											activebackground=self.current_theme["bg"],
											activeforeground=self.current_theme["fg"],
											selectcolor=self.current_theme["bg"],
											highlightbackground=self.current_theme["bg"],
											highlightcolor=self.current_theme["bg"])
		
		# Explicitly theme Stats radiobuttons
		if hasattr(self, 'stats_bar_radio'):
			self.stats_bar_radio.configure(bg=self.current_theme["bg"],
										  fg=self.current_theme["fg"],
										  activebackground=self.current_theme["bg"],
										  activeforeground=self.current_theme["fg"],
										  selectcolor=self.current_theme["bg"],
										  highlightbackground=self.current_theme["bg"],
										  highlightcolor=self.current_theme["bg"])
		if hasattr(self, 'stats_line_radio'):
			self.stats_line_radio.configure(bg=self.current_theme["bg"],
										   fg=self.current_theme["fg"],
										   activebackground=self.current_theme["bg"],
										   activeforeground=self.current_theme["fg"],
										   selectcolor=self.current_theme["bg"],
										   highlightbackground=self.current_theme["bg"],
										   highlightcolor=self.current_theme["bg"])
		
		# Theme Stats frames
		if hasattr(self, 'stats_header'):
			self.stats_header.configure(bg=self.current_theme["bg"])
		if hasattr(self, 'stats_type_frame'):
			self.stats_type_frame.configure(bg=self.current_theme["bg"])
		
		# Theme task input widgets (category, priority, deadline)
		# Increase font size to make comboboxes taller (match button height)
		style.configure('TCombobox',
					  fieldbackground=self.current_theme["entry_bg"],
					  background=self.current_theme["button_bg"],
					  foreground=self.current_theme["entry_fg"],
					  arrowcolor=self.current_theme["button_fg"],
					  borderwidth=1,
					  relief="flat",
					  font=("", 9),
					  padding=3)
		style.map('TCombobox',
				 fieldbackground=[('readonly', self.current_theme["entry_bg"])],
				 selectbackground=[('readonly', self.current_theme["button_bg"])],
				 selectforeground=[('readonly', self.current_theme["button_fg"])],
				 foreground=[('readonly', self.current_theme["entry_fg"])])
		
		# Theme deadline button
		if hasattr(self, 'deadline_btn'):
			self.deadline_btn.configure(bg=self.current_theme["button_bg"],
									   fg=self.current_theme["button_fg"],
									   activebackground=self.current_theme["button_bg"],
									   activeforeground=self.current_theme["button_fg"])

	def _ensure_category(self, name, open_state=True, color=None):
		if name in self.categories:
			self._update_category_count(name)
			self._update_category_choices()
			return self.categories[name]
		cat_id = self.tree.insert("", "end", text=name, values=("",), open=open_state)
		self.categories[name] = cat_id
		# Color assignment
		if color:
			self.category_colors[name] = color
		if name not in self.category_colors:
			self.category_colors[name] = self._color_palette[len(self.category_colors) % len(self._color_palette)]
		self._apply_category_tag(name)
		self._update_category_count(name)
		self._update_category_choices()
		return cat_id

	def _apply_category_tag(self, name):
		color = self.category_colors.get(name)
		if not color:
			return
		# Create a lighter background version of the color for better distinction
		# Calculate a semi-transparent effect by blending with theme background
		bg_color = self._blend_color_with_bg(color, 0.25)  # 25% opacity for more visible pastel
		# Color the category row with both foreground and background
		self.tree.tag_configure(f"cat:{name}", foreground=color, background=bg_color)
		cat_id = self.categories.get(name)
		if cat_id:
			self.tree.item(cat_id, tags=(f"cat:{name}",))
	
	def _refresh_all_category_colors(self):
		"""Refresh all category tag colors to ensure consistent 25% opacity."""
		for cat_name in self.category_colors.keys():
			self._apply_category_tag(cat_name)
	
	def _blend_color_with_bg(self, color, alpha):
		"""Blend a color with the current theme's listbox background at given alpha."""
		try:
			# Parse hex colors
			if color.startswith('#'):
				r1, g1, b1 = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
			else:
				return self.current_theme.get("listbox_bg", "#ffffff")
			
			bg = self.current_theme.get("listbox_bg", "#ffffff")
			if bg.startswith('#'):
				r2, g2, b2 = int(bg[1:3], 16), int(bg[3:5], 16), int(bg[5:7], 16)
			else:
				return bg
			
			# Blend: result = color * alpha + bg * (1 - alpha)
			r = int(r1 * alpha + r2 * (1 - alpha))
			g = int(g1 * alpha + g2 * (1 - alpha))
			b = int(b1 * alpha + b2 * (1 - alpha))
			return f"#{r:02x}{g:02x}{b:02x}"
		except:
			return self.current_theme.get("listbox_bg", "#ffffff")

	def _apply_alternating_rows(self):
		"""Apply alternating row colors to all tasks for better readability."""
		today = date.today()
		for cat_id in self.categories.values():
			children = self.tree.get_children(cat_id)
			for idx, child in enumerate(children):
				current_tags = list(self.tree.item(child, "tags"))
				# Remove old oddrow and overdue tags if present
				if 'oddrow' in current_tags:
					current_tags.remove('oddrow')
				if 'overdue' in current_tags:
					current_tags.remove('overdue')
				
				# Check if task is overdue
				deadline_str = self.tree.set(child, "#3")
				status = self.tree.set(child, "#1")
				is_completed = status in ["[x]", "[✓]"]
				is_overdue = False
				
				if deadline_str and not is_completed:
					try:
						deadline_date = date.fromisoformat(deadline_str)
						if deadline_date < today:
							is_overdue = True
					except:
						pass
				
				# Add tags in priority order (overdue takes precedence over oddrow)
				if is_overdue:
					current_tags.append('overdue')
				elif idx % 2 == 1:
					current_tags.append('oddrow')
				
				self.tree.item(child, tags=tuple(current_tags))

	def _update_category_count(self, name):
		cat_id = self.categories.get(name)
		if not cat_id:
			return
		children = self.tree.get_children(cat_id)
		total = len(children)
		done = 0
		for ch in children:
			vals = self.tree.item(ch).get("values") or ["", ""]
			if len(vals) > 0 and vals[0] == "[x]":
				done += 1
		label = f"{name} ({done}/{total})"
		# Keep tag when updating text
		cur_tags = self.tree.item(cat_id, "tags")
		self.tree.item(cat_id, text=label, tags=cur_tags)

	def _update_category_choices(self):
		"""Refresh the category wheel choices from current categories."""
		try:
			choices = sorted(self.categories.keys())
			self.category_combo.configure(values=choices)
			# If current value empty, prefer last used else default
			if (self.category_var.get() or "").strip() == "":
				self.category_var.set(self._last_category or "General")
			# Also update Daily tab category filter
			if hasattr(self, 'daily_cat_combo'):
				self.daily_cat_combo.configure(values=["All"] + choices)
				if self.daily_cat_var.get() not in (["All"] + choices):
					self.daily_cat_var.set("All")
		except Exception:
			pass

	def _on_entry_focus_in(self, event):
		"""Remove placeholder text when entry gains focus."""
		if self.entry_has_placeholder:
			self.entry.delete(0, "end")
			self.entry.config(fg="#000000")
			self.entry_has_placeholder = False
	
	def _on_entry_focus_out(self, event):
		"""Add placeholder text back if entry is empty."""
		if not self.entry.get().strip():
			self.entry.insert(0, self.entry_placeholder)
			self.entry.config(fg="#999999")
			self.entry_has_placeholder = True
	
	def _category_on_mousewheel(self, event):
		"""Scroll through category combobox values with mouse wheel."""
		vals = list(self.category_combo.cget('values')) or []
		if not vals:
			return
		current = self.category_var.get()
		try:
			idx = vals.index(current)
		except ValueError:
			idx = -1
		# On Windows, event.delta positive for up, negative for down
		step = -1 if event.delta > 0 else 1
		new_idx = (idx + step) % len(vals)
		self.category_var.set(vals[new_idx])
		self._last_category = vals[new_idx]

	def _on_tab_press(self, event):
		"""Record which tab was clicked for dragging."""
		try:
			tab_id = self.notebook.index(f"@{event.x},{event.y}")
			self._drag_data["tab"] = tab_id
			self._drag_data["x"] = event.x
		except:
			self._drag_data["tab"] = None
	
	def _on_tab_drag(self, event):
		"""Check if we should swap tabs during drag."""
		if self._drag_data["tab"] is None:
			return
		try:
			# Get the tab under the cursor
			target_tab = self.notebook.index(f"@{event.x},{event.y}")
			source_tab = self._drag_data["tab"]
			
			# If we've dragged over a different tab, swap them
			if target_tab != source_tab and abs(target_tab - source_tab) == 1:
				# Get all current tabs
				all_tabs = []
				for i in range(len(self.notebook.tabs())):
					frame = self.notebook.nametowidget(self.notebook.tabs()[i])
					text = self.notebook.tab(i, "text")
					all_tabs.append((frame, text))
				
				# Swap the two tabs in the list
				all_tabs[source_tab], all_tabs[target_tab] = all_tabs[target_tab], all_tabs[source_tab]
				
				# Remove all tabs
				for i in range(len(self.notebook.tabs()) - 1, -1, -1):
					self.notebook.forget(i)
				
				# Re-add all tabs in new order
				for frame, text in all_tabs:
					self.notebook.add(frame, text=text)
				
				# Update drag data to new position
				self._drag_data["tab"] = target_tab
				self.notebook.select(target_tab)
		except Exception as e:
			pass
	
	def _on_tab_release(self, event):
		"""Clear drag data when mouse is released."""
		self._drag_data["tab"] = None

	def _on_tree_select(self, event):
		"""Sync selected tree category to the category combobox."""
		selection = self.tree.selection()
		if not selection:
			return
		sel = selection[0]
		parent = self.tree.parent(sel)
		if parent:
			cat = self.tree.item(parent, "text").split(" (")[0]
		else:
			cat = self.tree.item(sel, "text").split(" (")[0]
		self.category_var.set(cat)
		self._last_category = cat

	def _on_tree_right_click(self, event):
		"""Show context menu on right-click."""
		# Identify the item under cursor
		item = self.tree.identify_row(event.y)
		if not item:
			return
		# Select the item
		self.tree.selection_set(item)
		# Check if it's a task or category
		parent = self.tree.parent(item)
		
		# Create context menu with theme colors
		context_menu = tk.Menu(self.root, tearoff=0, 
							  bg=self.current_theme["button_bg"], 
							  fg=self.current_theme["button_fg"],
							  activebackground=self.current_theme["listbox_bg"],
							  activeforeground=self.current_theme["listbox_fg"])
		if parent:
			# Task item
			context_menu.add_command(label="Edit", command=self.edit_task)
			context_menu.add_command(label="Toggle Complete", command=self.toggle_complete)
			context_menu.add_separator()
			context_menu.add_command(label="Remove", command=self.remove_task)
		else:
			# Category item
			context_menu.add_command(label="Edit Category", command=self.edit_task)
			context_menu.add_command(label="Change Color", command=self._change_category_color)
			context_menu.add_command(label="Toggle All Tasks", command=self.toggle_complete)
			context_menu.add_separator()
			context_menu.add_command(label="Remove Category", command=self.remove_task)
		
		# Show menu at cursor position
		try:
			context_menu.tk_popup(event.x_root, event.y_root)
		finally:
			context_menu.grab_release()
	
	def _change_category_color(self):
		"""Allow user to pick a custom color for the selected category."""
		from tkinter import colorchooser
		item = self._selected_item()
		if not item or self.tree.parent(item):
			return
		cat_label = self.tree.item(item, "text")
		cat_name = cat_label.split(" (")[0]
		current_color = self.category_colors.get(cat_name, "#000000")
		
		# Open color picker
		color = colorchooser.askcolor(initialcolor=current_color, parent=self.root, title="Choose Category Color")
		if color and color[1]:  # color[1] is the hex string
			self.category_colors[cat_name] = color[1]
			self._apply_category_tag(cat_name)

	def _selected_item(self):
		selection = self.tree.selection()
		if not selection:
			messagebox.showinfo("Select item", "Please select a category or task first.")
			return None
		return selection[0]

	def _priority_symbol(self, priority):
		# Return the priority text directly (Low, Medium, High)
		return priority if priority in ["High", "Medium", "Low"] else "Medium"

	def _priority_order(self, priority):
		order = {"High": 0, "Medium": 1, "Low": 2}
		return order.get(priority, 1)

	def _today_str(self):
		return date.today().isoformat()

	def _inc_daily(self, day_str):
		self.stats_daily[day_str] = self.stats_daily.get(day_str, 0) + 1

	def _dec_daily(self, day_str):
		if day_str in self.stats_daily:
			self.stats_daily[day_str] = max(0, self.stats_daily.get(day_str, 0) - 1)

	def _calendar_prev(self):
		"""Navigate to previous week or month."""
		if self.cal_view_var.get() == "monthly":
			# Go to previous month
			if self.cal_current_date.month == 1:
				self.cal_current_date = date(self.cal_current_date.year - 1, 12, 1)
			else:
				self.cal_current_date = date(self.cal_current_date.year, self.cal_current_date.month - 1, 1)
		else:
			# Go to previous week
			self.cal_current_date = self.cal_current_date - timedelta(days=7)
		self._update_calendar_view()
	
	def _calendar_next(self):
		"""Navigate to next week or month."""
		if self.cal_view_var.get() == "monthly":
			# Go to next month
			if self.cal_current_date.month == 12:
				self.cal_current_date = date(self.cal_current_date.year + 1, 1, 1)
			else:
				self.cal_current_date = date(self.cal_current_date.year, self.cal_current_date.month + 1, 1)
		else:
			# Go to next week
			self.cal_current_date = self.cal_current_date + timedelta(days=7)
		self._update_calendar_view()
	
	def _calendar_today(self):
		"""Reset calendar to today."""
		self.cal_current_date = date.today()
		self._update_calendar_view()
	
	def _update_calendar_view(self):
		"""Render the calendar view based on current settings."""
		if hasattr(self, 'calendar_canvas') and self.calendar_canvas:
			if self.cal_view_var.get() == "monthly":
				self._render_calendar_monthly()
			else:
				self._render_calendar_weekly()

	def _stats_prev_day(self):
		"""Move stats center one day back and refresh graph."""
		self.stats_center_date = getattr(self, 'stats_center_date', date.today()) - timedelta(days=1)
		self._update_stats_view()

	def _stats_next_day(self):
		"""Move stats center one day forward and refresh graph."""
		self.stats_center_date = getattr(self, 'stats_center_date', date.today()) + timedelta(days=1)
		self._update_stats_view()

	def _stats_today(self):
		"""Reset stats center to today and refresh graph."""
		self.stats_center_date = date.today()
		self._update_stats_view()
	
	def _update_stats_view(self):
		# Draw 7-day bar/line graph
		if hasattr(self, 'stats_canvas') and self.stats_canvas:
			self._render_stats_7day_graph()
			# Update nav label with range centered on current center date
			if hasattr(self, 'stats_center_date') and hasattr(self, 'stats_center_label'):
				center = self.stats_center_date
				start = center - timedelta(days=3)
				end = center + timedelta(days=3)
				range_text = f"{start.strftime('%b %d')} - {end.strftime('%b %d, %Y')}"
				self.stats_center_label.config(text=range_text)

	def _render_stats_7day_graph(self):
		"""Render a 7-day graph (bar or line) showing task completions."""
		canvas = self.stats_canvas
		canvas.delete("all")
		# Draw background gradient if configured
		bg = self.current_theme.get("bg", "#ffffff")
		bg_grad = self.current_theme.get("bg_gradient")
		self._draw_canvas_gradient(canvas, bg, bg_grad, vertical=True)
		
		w = canvas.winfo_width() or canvas.winfo_reqwidth()
		h = canvas.winfo_height() or 300
		margin = 44
		inner_w = max(1, w - 2 * margin)
		inner_h = max(1, h - 2 * margin)
		
		# Get 7-day window centered on stats_center_date (center-3 .. center+3)
		center_day = getattr(self, 'stats_center_date', date.today())
		today = date.today()
		days = [center_day + timedelta(days=i) for i in range(-3, 4)]
		
		# Get theme colors
		fg = self.current_theme.get("fg", "#000000")
		accent = self.current_theme.get("button_bg", "#4a90e2")
		grid = self._blend_color_with_bg(fg, 0.15)
		
		# Get data
		vals = [self.stats_daily.get(d.isoformat(), 0) for d in days]
		max_v = max(vals) if vals and max(vals) > 0 else 10
		
		# Draw axes
		canvas.create_line(margin, h - margin, w - margin, h - margin, fill=fg, width=2)
		canvas.create_line(margin, margin, margin, h - margin, fill=fg, width=2)

		# Y-axis ticks and labels (left side)
		# Determine nice step (aim for ~4 ticks)
		if max_v <= 5:
			step = 1
		elif max_v <= 10:
			step = 2
		elif max_v <= 25:
			step = 5
		elif max_v <= 50:
			step = 10
		else:
			step = max(1, (max_v // 5))
		# Extend top to next step for clean headroom
		axis_max = ((max_v + step - 1) // step) * step if max_v > 0 else step
		for yv in range(0, axis_max + 1, step):
			frac = (yv / axis_max) if axis_max > 0 else 0
			y = h - margin - frac * inner_h
			# grid line
			canvas.create_line(margin, y, w - margin, y, fill=grid, width=1, dash=(2,4))
			# tick
			canvas.create_line(margin - 5, y, margin, y, fill=fg, width=1)
			# label
			canvas.create_text(margin - 8, y, text=str(yv), fill=fg, font=("Arial", 9), anchor="e")
		
		spacing = inner_w / len(days)
		graph_type = self.stats_graph_type.get()
		
		if graph_type == "bar":
			# Draw bars
			bar_width = inner_w / (len(days) * 1.5)
			
			for i, (day, val) in enumerate(zip(days, vals)):
				x_center = margin + i * spacing + spacing / 2
				bar_h = (val / max_v) * inner_h if max_v > 0 else 0
				
				x0 = x_center - bar_width / 2
				y0 = h - margin - bar_h
				x1 = x_center + bar_width / 2
				y1 = h - margin
				
				# Draw bar
				color = accent if day == today else self.current_theme.get("listbox_bg", "#cccccc")
				canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=fg, width=1)
				
				# Draw value on top
				if val > 0:
					canvas.create_text(x_center, y0 - 10, text=str(val), fill=fg, font=("Arial", 10, "bold"))
				
				# Draw date label
				label = day.strftime('%m/%d')
				if day == today:
					label = "Today"
				canvas.create_text(x_center, h - margin + 15, text=label, fill=fg, font=("Arial", 9))
		else:
			# Draw line graph
			# Use axis_max for scaling to match y-axis
			points = []
			for i, (day, val) in enumerate(zip(days, vals)):
				x_center = margin + i * spacing + spacing / 2
				frac = (val / axis_max) if axis_max > 0 else 0
				y_val = h - margin - frac * inner_h
				points.append((x_center, y_val))
				# Date label
				label = day.strftime('%m/%d')
				if day == today:
					label = "Today"
				canvas.create_text(x_center, h - margin + 15, text=label, fill=fg, font=("Arial", 9))
				# Optional value labels near points
				if val > 0:
					canvas.create_text(x_center, y_val - 12, text=str(val), fill=fg, font=("Arial", 9))

			# Subtle fill under the line
			if points:
				fill_color = self._blend_color_with_bg(accent, 0.20)
				poly = [(points[0][0], h - margin)] + points + [(points[-1][0], h - margin)]
				# Flatten list for create_polygon
				coords = []
				for x, y in poly:
					coords.extend([x, y])
				canvas.create_polygon(*coords, fill=fill_color, outline="")

			# Dotted line and point markers
			if len(points) > 1:
				for i in range(len(points) - 1):
					canvas.create_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1],
										 fill=accent, width=2, dash=(3, 4), smooth=True)
			# Points on top
			for i, (day, val) in enumerate(zip(days, vals)):
				x, y = points[i]
				r = 4
				pt_color = accent if day == today else fg
				canvas.create_oval(x - r, y - r, x + r, y + r, fill=pt_color, outline=fg, width=1)
	
	def _render_calendar_weekly(self):
		"""Render weekly calendar view with deadlines."""
		canvas = self.calendar_canvas
		canvas.delete("all")
		# Background gradient for calendar
		bg = self.current_theme.get("bg", "#ffffff")
		bg_grad = self.current_theme.get("bg_gradient")
		self._draw_canvas_gradient(canvas, bg, bg_grad, vertical=True)
		# Determine size
		w = canvas.winfo_width() or canvas.winfo_reqwidth()
		h = canvas.winfo_height() or 300
		margin = 20
		inner_w = max(1, w - 2 * margin)
		inner_h = max(1, h - 2 * margin)
		
		# Get week containing cal_current_date
		today = date.today()
		days_since_monday = self.cal_current_date.weekday()
		monday = self.cal_current_date - timedelta(days=days_since_monday)
		week_days = [monday + timedelta(days=i) for i in range(7)]
		day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
		
		# Update date label
		week_str = f"{monday.strftime('%b %d')} - {week_days[-1].strftime('%b %d, %Y')}"
		self.cal_date_label.config(text=week_str)
		
		# Get theme colors
		bg = self.current_theme.get("bg", "#ffffff")
		fg = self.current_theme.get("fg", "#000000")
		cell_bg = self.current_theme.get("entry_bg", "#f0f0f0")
		accent = self.current_theme.get("button_bg", "#4a90e2")
		
		# Calculate cell dimensions
		cell_w = inner_w / 7
		cell_h = inner_h / 2  # Two rows: day names and counts
		
		# Draw grid and data
		for i, (day_name, day_date) in enumerate(zip(day_names, week_days)):
			x = margin + i * cell_w
			# Day name row
			y_name = margin
			# Cell border
			canvas.create_rectangle(x, y_name, x + cell_w, y_name + cell_h, 
								   outline=fg, fill=cell_bg, width=1)
			# Highlight today
			if day_date == today:
				canvas.create_rectangle(x + 2, y_name + 2, x + cell_w - 2, y_name + cell_h - 2,
									   outline=accent, width=2)
			# Day name text
			canvas.create_text(x + cell_w/2, y_name + cell_h/3, 
							  text=day_name[:3],  # Abbreviate to Mon, Tue, etc
							  fill=fg, font=("Arial", 10, "bold"))
			# Date text
			canvas.create_text(x + cell_w/2, y_name + 2*cell_h/3,
							  text=day_date.strftime('%m/%d'),
							  fill=fg, font=("Arial", 8))
			
			# Count row
			y_count = margin + cell_h
			count = self.stats_daily.get(day_date.isoformat(), 0)
			# Cell border
			canvas.create_rectangle(x, y_count, x + cell_w, y_count + cell_h,
								   outline=fg, fill=cell_bg, width=1)
			# Highlight today
			if day_date == today:
				canvas.create_rectangle(x + 2, y_count + 2, x + cell_w - 2, y_count + cell_h - 2,
									   outline=accent, width=2)
			# Count text
			count_color = accent if count > 0 else fg
			canvas.create_text(x + cell_w/2, y_count + cell_h/2,
							  text=str(count),
							  fill=count_color, font=("Arial", 24, "bold"))
	
	def _render_calendar_monthly(self):
		"""Render a monthly calendar showing tasks with deadlines."""
		canvas = self.calendar_canvas
		canvas.delete("all")
		# Background gradient for calendar
		bg = self.current_theme.get("bg", "#ffffff")
		bg_grad = self.current_theme.get("bg_gradient")
		self._draw_canvas_gradient(canvas, bg, bg_grad, vertical=True)
		
		w = canvas.winfo_width() or canvas.winfo_reqwidth()
		h = canvas.winfo_height() or 300
		margin = 20
		inner_w = max(1, w - 2 * margin)
		inner_h = max(1, h - 2 * margin)
		
		# Get month from cal_current_date
		today = date.today()
		year, month = self.cal_current_date.year, self.cal_current_date.month
		from calendar import monthrange
		first_day_weekday = date(year, month, 1).weekday()  # 0=Monday
		num_days = monthrange(year, month)[1]
		
		# Update date label
		month_name = date(year, month, 1).strftime("%B %Y")
		self.cal_date_label.config(text=month_name)
		
		# Theme colors
		fg = self.current_theme.get("fg", "#000000")
		cell_bg = self.current_theme.get("entry_bg", "#f0f0f0")
		accent = self.current_theme.get("button_bg", "#4a90e2")
		
		# Month title (optional, since it's now in the label)
		# canvas.create_text(w/2, margin/2, text=month_name, fill=fg, font=("Arial", 14, "bold"))
		
		# Calendar grid: 7 columns (days of week), up to 6 rows
		cell_w = inner_w / 7
		cell_h = inner_h / 7  # Leave room for title and padding
		
		# Day headers
		day_headers = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
		for i, day in enumerate(day_headers):
			x = margin + i * cell_w
			y = margin
			canvas.create_text(x + cell_w/2, y + cell_h/4, text=day, fill=fg, font=("Arial", 9, "bold"))
		
		# Collect tasks with deadlines for this month
		deadline_tasks = {}  # date_str -> [task_texts]
		for cat_id in self.categories.values():
			for child in self.tree.get_children(cat_id):
				meta = self.task_meta.get(child, {})
				deadline = meta.get("deadline")
				if deadline:
					try:
						deadline_date = date.fromisoformat(deadline)
						if deadline_date.year == year and deadline_date.month == month:
							if deadline not in deadline_tasks:
								deadline_tasks[deadline] = []
							task_text = self.tree.item(child, "text")
							deadline_tasks[deadline].append(task_text[:15])  # Truncate for display
					except:
						pass
		
		# Draw calendar days
		row = 1
		col = first_day_weekday
		for day in range(1, num_days + 1):
			x = margin + col * cell_w
			y = margin + row * cell_h
			
			# Cell background
			canvas.create_rectangle(x, y, x + cell_w, y + cell_h, outline=fg, fill=cell_bg, width=1)
			
			# Highlight today
			if day == today.day:
				canvas.create_rectangle(x + 2, y + 2, x + cell_w - 2, y + cell_h - 2, outline=accent, width=2)
			
			# Day number
			canvas.create_text(x + cell_w/2, y + 12, text=str(day), fill=fg, font=("Arial", 10, "bold"))
			
			# Show tasks due on this day
			day_str = date(year, month, day).isoformat()
			tasks_due = deadline_tasks.get(day_str, [])
			completed_count = self.stats_daily.get(day_str, 0)
			
			# Display task count or truncated task names
			if tasks_due:
				task_info = f"{len(tasks_due)} due"
				canvas.create_text(x + cell_w/2, y + cell_h/2, text=task_info, 
								 fill=accent, font=("Arial", 8))
			if completed_count > 0:
				canvas.create_text(x + cell_w/2, y + cell_h - 10, text=f"✓{completed_count}",
								 fill=fg, font=("Arial", 8))
			
			col += 1
			if col >= 7:
				col = 0
				row += 1

	def add_task(self):
		# Don't add if placeholder text is showing
		if self.entry_has_placeholder:
			return
		text = self.entry.get().strip()
		# Determine category: prefer combobox value; else selected tree category; else last used; fallback to General
		category = (self.category_var.get() or "").strip()
		if not category:
			selection = self.tree.selection()
			if selection:
				sel = selection[0]
				parent = self.tree.parent(sel)
				if parent:  # a task is selected
					cat_label = self.tree.item(parent, "text").split(" (")[0]
					category = cat_label
				else:  # a category is selected
					category = self.tree.item(sel, "text").split(" (")[0]
			elif getattr(self, '_last_category', None):
				category = self._last_category
		if not category:
			category = "General"
		priority = self.priority_var.get() or "Medium"
		if not text:
			return
		cat_id = self._ensure_category(category)
		priority_display = self._priority_symbol(priority)
		deadline_val = self.add_deadline_var.get().strip()
		# Extract actual date if not the default button text
		deadline = deadline_val if deadline_val and deadline_val != "📅 Deadline" else ""
		item = self.tree.insert(cat_id, "end", text=text, values=("[ ]", priority_display, deadline))
		# Store priority and deadline in item tags
		self.tree.set(item, "#1", "[ ]")
		self.tree.set(item, "#2", priority_display)
		self.tree.set(item, "#3", deadline)
		# Store deadline in task metadata
		if deadline:
			if item not in self.task_meta:
				self.task_meta[item] = {}
			self.task_meta[item]["deadline"] = deadline
		# Sort tasks by priority within category
		self._sort_category_by_priority(cat_id)
		# Apply alternating row colors
		self._apply_alternating_rows()
		# Clear inputs, keep last used category for faster subsequent adds
		self.entry.delete(0, "end")
		# Reset placeholder
		self.entry.insert(0, self.entry_placeholder)
		self.entry.config(fg="#999999")
		self.entry_has_placeholder = True
		self._last_category = category
		# Clear deadline after adding
		self.add_deadline_var.set("📅 Deadline")
		# keep category_var as-is to allow rapid multiple entries
		self.priority_var.set("Medium")
		self._update_category_count(category)
		
		# Refresh current view if not in Tree mode
		self._refresh_current_view()

	def _seed_test_tasks(self):
		"""Populate the app with a set of demo categories and tasks, plus sample stats."""
		from datetime import date, timedelta
		# Avoid duplicating on repeated clicks unless user wants to
		if getattr(self, "_demo_seeded", False):
			if not messagebox.askyesno("Demo Data", "Demo tasks already loaded. Load again anyway?"):
				return
		
		cats = {
			"Work": [
				("Design module API", "High", +3, None),
				("Write unit tests", "Medium", +1, None),
				("Refactor utils", "Low", None, None),
				("Fix bug #214", "High", -1, -1),
				("Sprint planning", "Medium", +7, None),
			],
			"Personal": [
				("Workout 30m", "High", None, -2),
				("Read 20 pages", "Medium", None, None),
				("Meditation", "Low", None, None),
				("Call family", "Medium", 0, None),
			],
			"Errands": [
				("Grocery shopping", "Medium", +2, None),
				("Post office", "Low", +1, None),
				("Car wash", "Low", None, None),
			],
			"Ideas": [
				("Research automation", "Medium", None, None),
				("Sketch UI concepts", "Low", None, None),
			]
		}
		
		for cat, items in cats.items():
			cat_id = self._ensure_category(cat)
			for (text, prio, deadline_offset, completed_offset) in items:
				deadline = ""
				if isinstance(deadline_offset, int):
					deadline = (date.today() + timedelta(days=deadline_offset)).isoformat()
				prio_display = self._priority_symbol(prio)
				status = "[ ]"
				if isinstance(completed_offset, int):
					status = "[x]"
				item = self.tree.insert(cat_id, "end", text=text, values=(status, prio_display, deadline))
				# metadata
				if item not in self.task_meta:
					self.task_meta[item] = {}
				if deadline:
					self.task_meta[item]["deadline"] = deadline
				if status == "[x]":
					day_str = (date.today() + timedelta(days=completed_offset)).isoformat()
					self.task_meta[item]["last_completed_date"] = day_str
					self._inc_daily(day_str)
			# Update counts per category after inserts
			self._update_category_count(cat)
		
		# Refresh visuals
		self._apply_alternating_rows()
		self._refresh_all_category_colors()
		self._update_stats_view()
		self._update_calendar_view()
		self._demo_seeded = True

	def _sort_category_by_priority(self, cat_id, reverse=False):
		"""Sort tasks within a category by priority (High -> Medium -> Low, or reverse)"""
		children = list(self.tree.get_children(cat_id))
		if not children:
			return
		# Get task data with priority
		tasks_data = []
		for child in children:
			text = self.tree.item(child, "text")
			vals = self.tree.item(child).get("values") or ["[ ]", "Medium"]
			status = vals[0] if len(vals) > 0 else "[ ]"
			priority = vals[1] if len(vals) > 1 else "Medium"
			# Priority is now text: "High", "Medium", or "Low"
			if priority not in ["High", "Medium", "Low"]:
				priority = "Medium"
			tasks_data.append((child, text, status, priority))
		
		# Sort by priority order
		tasks_data.sort(key=lambda x: self._priority_order(x[3]), reverse=reverse)
		
		# Reinsert in sorted order
		for idx, (child, text, status, priority) in enumerate(tasks_data):
			self.tree.move(child, cat_id, idx)

	def _sort_categories_alphabetically(self):
		"""Toggle between A->Z and Z->A alphabetical category sort"""
		# Toggle sort direction
		self._category_sort_reverse = not self._category_sort_reverse
		
		# Update heading to show current sort state
		if self._category_sort_reverse:
			# Z to A
			self.tree.heading("#0", text="Tasks ▼")
		else:
			# A to Z
			self.tree.heading("#0", text="Tasks ▲")
		
		# Get all categories with their current data
		cat_data = []
		for name, cat_id in list(self.categories.items()):
			# Get category info
			cat_text = self.tree.item(cat_id, "text")
			cat_open = self.tree.item(cat_id, "open")
			
			# Get all tasks in this category
			tasks = []
			for child_id in self.tree.get_children(cat_id):
				task_text = self.tree.item(child_id, "text")
				task_values = self.tree.item(child_id, "values")
				tasks.append((task_text, task_values))
			
			cat_data.append((name, cat_text, cat_open, tasks))
		
		# Sort categories alphabetically by name
		cat_data.sort(key=lambda x: x[0].lower(), reverse=self._category_sort_reverse)
		
		# Delete all categories from tree
		for cat_id in self.categories.values():
			self.tree.delete(cat_id)
		
		# Re-insert categories in alphabetical order
		self.categories.clear()
		for name, cat_text, cat_open, tasks in cat_data:
			cat_id = self.tree.insert("", "end", text=cat_text, values=("",), open=cat_open)
			self.categories[name] = cat_id
			
			# Re-insert all tasks for this category
			for task_text, task_values in tasks:
				self.tree.insert(cat_id, "end", text=task_text, values=task_values)
			
			# Reapply category tag for colors
			self._apply_category_tag(name)
		
		# Apply alternating row colors after rebuilding tree
		self._apply_alternating_rows()
	
	def _sort_all_by_priority(self):
		"""Toggle between High->Low and Low->High priority sort"""
		# Toggle sort direction
		self._priority_sort_reverse = not self._priority_sort_reverse
		
		# Update heading to show current sort state
		if self._priority_sort_reverse:
			# Low to High
			self.tree.heading("priority", text="Priority ▲")
		else:
			# High to Low
			self.tree.heading("priority", text="Priority ▼")
		
		# Sort all categories
		for name, cat_id in self.categories.items():
			self._sort_category_by_priority(cat_id, reverse=self._priority_sort_reverse)
		
		# Apply alternating row colors after sorting
		self._apply_alternating_rows()


	# Removed index-based selection; using Treeview selection via _selected_item

	def remove_task(self):
		item = self._selected_item()
		if not item:
			return
		parent = self.tree.parent(item)
		if not parent:
			# Category node
			label = self.tree.item(item, "text")
			name = label.split(" (")[0]
			if messagebox.askyesno("Remove Category", f"Remove category '{name}' and all its tasks?"):
				self.tree.delete(item)
				self.categories.pop(name, None)
				self.category_colors.pop(name, None)
				self._update_category_choices()
			return
		# Task node
		cat_id = parent
		cat_label = self.tree.item(cat_id, "text").split(" (")[0]
		if messagebox.askyesno("Remove", "Remove selected task?"):
			self.tree.delete(item)
			self._update_category_count(cat_label)
			# Apply alternating rows after removing task
			self._apply_alternating_rows()
			
			# Refresh current view if not in Tree mode
			self._refresh_current_view()

	def _update_deadline_display(self):
		"""Update the deadline button text based on whether a date is selected"""
		current_val = self.add_deadline_var.get()
		# Don't update if we're in the middle of setting it from the picker
		# The picker will set it to the date, and we want to preserve that
		if current_val and current_val != "📅 Deadline":
			# Date is selected, keep showing it
			pass
		elif not current_val:
			# No date selected, show default text
			self.add_deadline_var.set("📅 Deadline")
	
	def _pick_add_deadline(self):
		"""Open date picker for setting deadline when adding a new task"""
		from datetime import date
		import calendar
		
		date_window = tk.Toplevel(self.root)
		date_window.title("Pick Deadline")
		date_window.transient(self.root)
		date_window.grab_set()
		date_window.configure(bg=self.current_theme["bg"])
		
		# Parse current deadline or use today
		try:
			current_val = self.add_deadline_var.get()
			if current_val and current_val != "📅 Deadline":
				current_date = date.fromisoformat(current_val)
			else:
				current_date = date.today()
		except:
			current_date = date.today()
		
		selected_date = [current_date]
		
		def prev_month():
			y, m = selected_date[0].year, selected_date[0].month
			if m == 1:
				y -= 1
				m = 12
			else:
				m -= 1
			selected_date[0] = date(y, m, 1)
			render_calendar()
		
		def next_month():
			y, m = selected_date[0].year, selected_date[0].month
			if m == 12:
				y += 1
				m = 1
			else:
				m += 1
			selected_date[0] = date(y, m, 1)
			render_calendar()
		
		def select_day(day):
			y, m = selected_date[0].year, selected_date[0].month
			selected_date[0] = date(y, m, day)
			self.add_deadline_var.set(selected_date[0].isoformat())
			date_window.destroy()
		
		def clear_date():
			self.add_deadline_var.set("📅 Deadline")
			date_window.destroy()
		
		# Header with navigation
		header = tk.Frame(date_window, bg=self.current_theme["bg"])
		header.pack(pady=5)
		
		tk.Button(header, text="◀", command=prev_month, width=3,
				 bg=self.current_theme["button_bg"], fg=self.current_theme["button_fg"]).pack(side="left", padx=2)
		
		month_label = tk.Label(header, text="", width=20, bg=self.current_theme["bg"], 
							  fg=self.current_theme["fg"])
		month_label.pack(side="left", padx=5)
		
		tk.Button(header, text="▶", command=next_month, width=3,
				 bg=self.current_theme["button_bg"], fg=self.current_theme["button_fg"]).pack(side="left", padx=2)
		
		# Calendar grid
		cal_frame = tk.Frame(date_window, bg=self.current_theme["bg"])
		cal_frame.pack(pady=5, padx=10)
		
		def render_calendar():
			# Clear existing
			for widget in cal_frame.winfo_children():
				widget.destroy()
			
			y, m = selected_date[0].year, selected_date[0].month
			month_label.config(text=f"{calendar.month_name[m]} {y}")
			
			# Day headers
			for i, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
				tk.Label(cal_frame, text=day, width=4, bg=self.current_theme["bg"],
						fg=self.current_theme["fg"], font=("", 8, "bold")).grid(row=0, column=i, padx=1, pady=1)
			
			# Get first day and days in month
			first_weekday, days_in_month = calendar.monthrange(y, m)
			first_weekday = (first_weekday + 1) % 7  # Convert to Mon=0
			
			row = 1
			col = first_weekday
			
			for day in range(1, days_in_month + 1):
				day_date = date(y, m, day)
				is_today = (day_date == date.today())
				
				btn = tk.Button(cal_frame, text=str(day), width=4, 
							   command=lambda d=day: select_day(d),
							   bg=self.current_theme["button_bg"] if not is_today else "#4CAF50",
							   fg=self.current_theme["button_fg"])
				btn.grid(row=row, column=col, padx=1, pady=1)
				
				col += 1
				if col > 6:
					col = 0
					row += 1
		
		render_calendar()
		
		# Clear button at bottom
		btn_frame = tk.Frame(date_window, bg=self.current_theme["bg"])
		btn_frame.pack(pady=10)
		tk.Button(btn_frame, text="Clear", command=clear_date, width=10,
				 bg=self.current_theme["button_bg"], fg=self.current_theme["button_fg"]).pack()
	
	def edit_task(self):
		item = self._selected_item()
		if not item:
			return
		parent = self.tree.parent(item)
		if not parent:
			# Edit category name only
			old_label = self.tree.item(item, "text")
			old_name = old_label.split(" (")[0]
			new_name = simpledialog.askstring("Edit category", "New category name:", initialvalue=old_name, parent=self.root)
			if new_name:
				new_name = new_name.strip() or old_name
				# Update mapping
				self.categories.pop(old_name, None)
				self.categories[new_name] = item
				# Preserve color
				if old_name in self.category_colors:
					self.category_colors[new_name] = self.category_colors.pop(old_name)
				# Update label and tags/colors
				self._apply_category_tag(new_name)
				self._update_category_count(new_name)
				self._update_category_choices()
			return
		
		# Editing a task - unified dialog with all fields
		old_text = self.tree.item(item, "text")
		cat_label = self.tree.item(parent, "text")
		old_cat = cat_label.split(" (")[0]
		vals = self.tree.item(item).get("values") or ["[ ]", "Medium", ""]
		old_priority = vals[1] if len(vals) > 1 else "Medium"
		# Priority is now stored as text directly ("High", "Medium", "Low")
		if old_priority not in ["High", "Medium", "Low"]:
			# Handle legacy arrow symbols if any exist
			priority_map = {"⬆️": "High", "➡️": "Medium", "⬇️": "Low"}
			old_priority = priority_map.get(old_priority, "Medium")
		old_deadline = vals[2] if len(vals) > 2 else ""
		
		# Create unified edit dialog
		edit_window = tk.Toplevel(self.root)
		edit_window.title("Edit Task")
		edit_window.geometry("450x360")
		edit_window.transient(self.root)
		edit_window.grab_set()
		
		# Apply theme to dialog
		edit_window.configure(bg=self.current_theme["bg"])
		
		# Task text
		label1 = tk.Label(edit_window, text="Task:", bg=self.current_theme["bg"], fg=self.current_theme["fg"])
		label1.pack(pady=(10, 0))
		text_entry = tk.Entry(edit_window, width=50, bg=self.current_theme["entry_bg"], 
							 fg=self.current_theme["entry_fg"], insertbackground=self.current_theme["fg"])
		text_entry.insert(0, old_text)
		text_entry.pack(pady=5)
		text_entry.focus_set()
		
		# Category with ability to add new
		label2 = tk.Label(edit_window, text="Category:", bg=self.current_theme["bg"], fg=self.current_theme["fg"])
		label2.pack(pady=(10, 0))
		cat_frame = tk.Frame(edit_window, bg=self.current_theme["bg"])
		cat_frame.pack(pady=5)
		
		cat_var = tk.StringVar(value=old_cat)
		cat_choices = sorted(self.categories.keys()) if self.categories else ["General"]
		cat_combo = ttk.Combobox(cat_frame, textvariable=cat_var, values=cat_choices, width=30)
		cat_combo.pack(side="left", padx=(0, 5))
		
		def add_new_category():
			new_cat_name = simpledialog.askstring("New Category", "Enter new category name:", parent=edit_window)
			if new_cat_name and new_cat_name.strip():
				new_cat_name = new_cat_name.strip()
				if new_cat_name not in self.categories:
					# Add to choices and select it
					current_choices = list(cat_combo['values'])
					current_choices.append(new_cat_name)
					cat_combo['values'] = sorted(current_choices)
					cat_var.set(new_cat_name)
		
		add_cat_btn = tk.Button(cat_frame, text="+", command=add_new_category, width=3,
							   bg=self.current_theme["button_bg"], fg=self.current_theme["button_fg"])
		add_cat_btn.pack(side="left")
		
		# Priority
		label3 = tk.Label(edit_window, text="Priority:", bg=self.current_theme["bg"], fg=self.current_theme["fg"])
		label3.pack(pady=(10, 0))
		priority_var = tk.StringVar(value=old_priority)
		priority_combo = ttk.Combobox(edit_window, textvariable=priority_var, 
									values=["High", "Medium", "Low"], state="readonly", width=30)
		priority_combo.pack(pady=5)
		
		# Deadline
		label4 = tk.Label(edit_window, text="Deadline (optional):", bg=self.current_theme["bg"], fg=self.current_theme["fg"])
		label4.pack(pady=(10, 0))
		
		deadline_frame = tk.Frame(edit_window, bg=self.current_theme["bg"])
		deadline_frame.pack(pady=5)
		
		deadline_var = tk.StringVar(master=edit_window, value=old_deadline)
		deadline_display = tk.Label(deadline_frame, textvariable=deadline_var, width=15,
								   bg=self.current_theme["entry_bg"], fg=self.current_theme["entry_fg"],
								   relief="sunken", bd=1, anchor="w")
		deadline_display.pack(side="left", padx=(0, 5))
		
		def pick_date():
			"""Open a date picker dialog"""
			date_window = tk.Toplevel(edit_window)
			date_window.title("Pick Date")
			date_window.transient(edit_window)
			date_window.grab_set()
			date_window.configure(bg=self.current_theme["bg"])
			
			from datetime import date, timedelta
			
			# Parse current deadline or use today
			try:
				if deadline_var.get():
					current_date = date.fromisoformat(deadline_var.get())
				else:
					current_date = date.today()
			except:
				current_date = date.today()
			
			selected_date = [current_date]
			
			def prev_month():
				y, m = selected_date[0].year, selected_date[0].month
				if m == 1:
					y -= 1
					m = 12
				else:
					m -= 1
				selected_date[0] = date(y, m, 1)
				render_calendar()
			
			def next_month():
				y, m = selected_date[0].year, selected_date[0].month
				if m == 12:
					y += 1
					m = 1
				else:
					m += 1
				selected_date[0] = date(y, m, 1)
				render_calendar()
			
			def select_day(day):
				y, m = selected_date[0].year, selected_date[0].month
				selected_date[0] = date(y, m, day)
				deadline_var.set(selected_date[0].isoformat())
				date_window.destroy()
			
			def clear_date():
				deadline_var.set("")
				date_window.destroy()
			
			# Header with navigation
			header = tk.Frame(date_window, bg=self.current_theme["bg"])
			header.pack(pady=5)
			
			tk.Button(header, text="◀", command=prev_month, width=3,
					 bg=self.current_theme["button_bg"], fg=self.current_theme["button_fg"]).pack(side="left", padx=2)
			
			month_label = tk.Label(header, text="", width=20, bg=self.current_theme["bg"], 
								  fg=self.current_theme["fg"])
			month_label.pack(side="left", padx=5)
			
			tk.Button(header, text="▶", command=next_month, width=3,
					 bg=self.current_theme["button_bg"], fg=self.current_theme["button_fg"]).pack(side="left", padx=2)
			
			# Calendar grid
			cal_frame = tk.Frame(date_window, bg=self.current_theme["bg"])
			cal_frame.pack(pady=5, padx=10)
			
			def render_calendar():
				# Clear existing
				for widget in cal_frame.winfo_children():
					widget.destroy()
				
				import calendar
				y, m = selected_date[0].year, selected_date[0].month
				month_label.config(text=f"{calendar.month_name[m]} {y}")
				
				# Day headers
				for i, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
					tk.Label(cal_frame, text=day, width=4, bg=self.current_theme["bg"],
							fg=self.current_theme["fg"], font=("", 8, "bold")).grid(row=0, column=i, padx=1, pady=1)
				
				# Get first day and days in month
				first_weekday, days_in_month = calendar.monthrange(y, m)
				first_weekday = (first_weekday + 1) % 7  # Convert to Mon=0
				
				row = 1
				col = first_weekday
				
				for day in range(1, days_in_month + 1):
					day_date = date(y, m, day)
					is_today = (day_date == date.today())
					
					btn = tk.Button(cal_frame, text=str(day), width=4, 
								   command=lambda d=day: select_day(d),
								   bg=self.current_theme["button_bg"] if not is_today else "#4CAF50",
								   fg=self.current_theme["button_fg"])
					btn.grid(row=row, column=col, padx=1, pady=1)
					
					col += 1
					if col > 6:
						col = 0
						row += 1
			
			render_calendar()
			
			# Clear button at bottom
			btn_frame = tk.Frame(date_window, bg=self.current_theme["bg"])
			btn_frame.pack(pady=10)
			tk.Button(btn_frame, text="Clear", command=clear_date, width=10,
					 bg=self.current_theme["button_bg"], fg=self.current_theme["button_fg"]).pack()
		
		tk.Button(deadline_frame, text="Pick Date", command=pick_date, width=10,
				 bg=self.current_theme["button_bg"], fg=self.current_theme["button_fg"]).pack(side="left")
		
		tk.Button(deadline_frame, text="Clear", command=lambda: deadline_var.set(""), width=8,
				 bg=self.current_theme["button_bg"], fg=self.current_theme["button_fg"]).pack(side="left", padx=5)
		
		# Buttons
		confirmed = [False]
		result_data = {}
		
		def confirm():
			# Get values BEFORE destroying window
			result_data['text'] = text_entry.get().strip()
			result_data['category'] = cat_var.get().strip() or old_cat
			result_data['priority'] = priority_var.get() or old_priority
			result_data['deadline'] = deadline_var.get().strip()
			confirmed[0] = True
			edit_window.destroy()
		
		def cancel():
			edit_window.destroy()
		
		btn_frame = tk.Frame(edit_window, bg=self.current_theme["bg"])
		btn_frame.pack(pady=20)
		tk.Button(btn_frame, text="OK", command=confirm, width=10,
				 bg=self.current_theme["button_bg"], fg=self.current_theme["button_fg"]).pack(side="left", padx=5)
		tk.Button(btn_frame, text="Cancel", command=cancel, width=10,
				 bg=self.current_theme["button_bg"], fg=self.current_theme["button_fg"]).pack(side="left", padx=5)
		
		# Bind Enter key to confirm
		edit_window.bind('<Return>', lambda e: confirm())
		edit_window.bind('<Escape>', lambda e: cancel())
		
		edit_window.wait_window()
		
		if not confirmed[0]:
			return
		
		# Get values from result_data dictionary
		new_text = result_data.get('text', '')
		if not new_text:
			return
		
		new_cat = result_data.get('category', old_cat)
		new_priority = result_data.get('priority', old_priority)
		new_priority_symbol = self._priority_symbol(new_priority)
		new_deadline = result_data.get('deadline', '')
		
		# Validate deadline format if provided
		if new_deadline:
			try:
				from datetime import datetime
				datetime.strptime(new_deadline, "%Y-%m-%d")
			except:
				messagebox.showerror("Invalid Date", "Deadline must be in YYYY-MM-DD format")
				return
		
		# Update text, priority, and deadline
		self.tree.item(item, text=new_text)
		current_vals = list(self.tree.item(item).get("values") or ["[ ]", "➡️", ""])
		while len(current_vals) < 3:
			current_vals.append("")
		current_vals[1] = new_priority_symbol
		current_vals[2] = new_deadline
		self.tree.item(item, values=tuple(current_vals))
		
		# Store deadline in task metadata
		if item not in self.task_meta:
			self.task_meta[item] = {}
		self.task_meta[item]["deadline"] = new_deadline if new_deadline else None
		
		# Move category if changed
		if new_cat != old_cat:
			new_cat_id = self._ensure_category(new_cat)
			self.tree.move(item, new_cat_id, "end")
			self._sort_category_by_priority(new_cat_id)
			self._update_category_count(old_cat)
			self._update_category_count(new_cat)
			self._update_category_choices()
		else:
			# Re-sort if priority changed
			self._sort_category_by_priority(parent)
			self._update_category_count(old_cat)
		
		# Apply alternating rows after editing
		self._apply_alternating_rows()
		
		# Refresh stats and calendar views to show updated deadlines
		self._update_stats_view()
		self._update_calendar_view()

	def toggle_complete(self):
		# Track XP gains
		xp_gained = 0
		
		selection = self.tree.selection()
		if not selection:
			return
		
		def set_status_and_stats(it, new_val):
			# Update tree values - preserve all columns including deadline
			vals = self.tree.item(it).get("values") or ["[ ]", "➡️", ""]
			priority = vals[1] if len(vals) > 1 else "➡️"
			deadline = vals[2] if len(vals) > 2 else ""
			self.tree.item(it, values=(new_val, priority, deadline))
			# Stats adjustment
			if new_val == "[x]":
				# Award XP for completing task
				nonlocal xp_gained
				xp_gained += self.XP_PER_TASK
				# mark completion today
				meta = self.task_meta.setdefault(it, {"last_completed_date": None})
				# If previously completed on another day and now re-completing, we don't auto-decrement past day here
				# We only set the new completed date and increment today's count
				meta["last_completed_date"] = self._today_str()
				self._inc_daily(meta["last_completed_date"])
			else:
				# un-completing: decrement the day it was last completed
				meta = self.task_meta.get(it)
				if meta and meta.get("last_completed_date"):
					self._dec_daily(meta["last_completed_date"])
					meta["last_completed_date"] = None

		categories_to_update = set()
		for item in selection:
			parent = self.tree.parent(item)
			if not parent:
				# category node
				cat_label = self.tree.item(item, "text").split(" (")[0]
				children = self.tree.get_children(item)
				any_incomplete = any((self.tree.item(ch).get("values") or ["[ ]"])[0] == "[ ]" for ch in children)
				new_val = "[x]" if any_incomplete else "[ ]"
				for ch in children:
					set_status_and_stats(ch, new_val)
				categories_to_update.add(cat_label)
			else:
				# task node
				cur = (self.tree.item(item).get("values") or ["[ ]"])[0]
				new_val = "[x]" if cur == "[ ]" else "[ ]"
				set_status_and_stats(item, new_val)
				cat_label = self.tree.item(parent, "text").split(" (")[0]
				categories_to_update.add(cat_label)
		
		for cat in categories_to_update:
			self._update_category_count(cat)

		# Award XP and check for level up
		if xp_gained > 0:
			self._award_xp(xp_gained)
		self._update_stats_view()
		# Apply alternating rows after toggling tasks
		self._apply_alternating_rows()
		
		# Refresh current view if not in Tree mode
		self._refresh_current_view()

	def clear_completed(self):
		if not messagebox.askyesno("Clear", "Remove all completed tasks?"):
			return
		# Iterate categories
		for name, cat_id in list(self.categories.items()):
			for child in list(self.tree.get_children(cat_id)):
				vals = self.tree.item(child).get("values") or [""]
				if vals[0] == "[x]":
					self.tree.delete(child)
			self._update_category_count(name)
			# Remove empty category
			if not self.tree.get_children(cat_id):
				self.tree.delete(cat_id)
				self.categories.pop(name, None)
				self.category_colors.pop(name, None)
		self._update_category_choices()

	def save_tasks(self, path=None, show_error=True):
		if path is None:
			path = filedialog.asksaveasfilename(defaultextension=".json",
											  filetypes=[("JSON files","*.json"),("All files","*.*")],
											  initialfile=TASKS_FILE)
			if not path:
				return False

		try:
			# Collect tasks by category from tree
			tasks_by_category = {}
			categories_meta = []
			for name, cat_id in self.categories.items():
				clean_name = name  # internal key name
				# derive original name from label
				clean_name = name
				# read open state
				open_state = bool(self.tree.item(cat_id, 'open'))
				categories_meta.append({
					"name": clean_name,
					"open": open_state,
					"color": self.category_colors.get(clean_name)
				})
				items = []
				for child in self.tree.get_children(cat_id):
					text = self.tree.item(child, "text")
					vals = self.tree.item(child).get("values") or ["[ ]", "➡️", ""]
					priority_symbol = vals[1] if len(vals) > 1 else "➡️"
					deadline = vals[2] if len(vals) > 2 else ""
					priority_map = {"⬆️": "High", "➡️": "Medium", "⬇️": "Low"}
					priority = priority_map.get(priority_symbol, "Medium")
					item_data = {
						"text": text,
						"done": vals[0] == "[x]",
						"priority": priority,
						"deadline": deadline if deadline else None
					}
					# Persist last completed date if available
					meta = self.task_meta.get(child)
					if meta and meta.get("last_completed_date") and item_data["done"]:
						item_data["completed_date"] = meta["last_completed_date"]
					items.append(item_data)
				tasks_by_category[clean_name] = items
			data = {
				"theme": self.theme_var.get(),
				"tasks_by_category": tasks_by_category,
				"categories": categories_meta,
				"stats": {"daily_counts": self.stats_daily}
			}
			with open(path, "w", encoding="utf-8") as f:
				json.dump(data, f, ensure_ascii=False, indent=2)
			return True
		except Exception as e:
			if show_error:
				messagebox.showerror("Error", f"Failed to save: {e}")
			return False

	def load_tasks(self, startup=False):
		def populate_from_tasks_list(tasks_list):
			# Backward compatibility: list of tasks with optional category
			for t in tasks_list:
				name = t.get("category", "General")
				cat_id = self._ensure_category(name)
				status = "[x]" if bool(t.get("done", False)) else "[ ]"
				priority = t.get("priority", "Medium")
				priority_symbol = self._priority_symbol(priority)
				child = self.tree.insert(cat_id, "end", text=t.get("text", ""), values=(status, priority_symbol))
				completed_date = t.get("completed_date")
				if completed_date:
					self.task_meta[child] = {"last_completed_date": completed_date}
				self._update_category_count(name)
		def clear_tree():
			for it in self.tree.get_children(""):
				self.tree.delete(it)
			self.categories.clear()
			self.category_colors = {}
			self.task_meta = {}
		if startup:
			try:
				with open(TASKS_FILE, "r", encoding="utf-8") as f:
					data = json.load(f)
					clear_tree()
					if isinstance(data, dict):
						# New hierarchical format
						if "tasks_by_category" in data:
							for cat in data.get("categories", []):
								name = cat.get("name", "General")
								open_state = bool(cat.get("open", True))
								color = cat.get("color")
								self._ensure_category(name, open_state=open_state, color=color)
							for name, items in data.get("tasks_by_category", {}).items():
								cat_id = self._ensure_category(name)
								for it in items:
									status = "[x]" if bool(it.get("done", False)) else "[ ]"
									priority = it.get("priority", "Medium")
									priority_symbol = self._priority_symbol(priority)
									deadline = it.get("deadline", "")
									child = self.tree.insert(cat_id, "end", text=it.get("text", ""), 
														   values=(status, priority_symbol, deadline))
									# Restore metadata
									if child not in self.task_meta:
										self.task_meta[child] = {}
									comp = it.get("completed_date")
									if comp:
										self.task_meta[child]["last_completed_date"] = comp
									if deadline:
										self.task_meta[child]["deadline"] = deadline
								self._sort_category_by_priority(cat_id)
								self._update_category_count(name)
						elif "tasks" in data:
							populate_from_tasks_list(data.get("tasks", []))
						# Apply alternating row colors after loading
						self._apply_alternating_rows()
						# Theme
						theme = data.get("theme", DEFAULT_THEME)
						if theme in self.themes:
							self.theme_var.set(theme)
							self.change_theme()
						# Stats
						stats = data.get("stats", {})
						self.stats_daily = dict(stats.get("daily_counts", {}))
					elif isinstance(data, list):
						populate_from_tasks_list(data)
			except Exception:
				# Start with empty
				clear_tree()
			self._update_category_choices()
			self._update_stats_view()
			return

		path = filedialog.askopenfilename(defaultextension=".json",
										  filetypes=[("JSON files","*.json"),("All files","*.*")])
		if not path:
			return
		try:
			with open(path, "r", encoding="utf-8") as f:
				data = json.load(f)
				clear_tree()
				if isinstance(data, dict):
					if "tasks_by_category" in data:
						for cat in data.get("categories", []):
							name = cat.get("name", "General")
							open_state = bool(cat.get("open", True))
							color = cat.get("color")
							self._ensure_category(name, open_state=open_state, color=color)
						for name, items in data.get("tasks_by_category", {}).items():
							cat_id = self._ensure_category(name)
							for it in items:
								status = "[x]" if bool(it.get("done", False)) else "[ ]"
								priority = it.get("priority", "Medium")
								priority_symbol = self._priority_symbol(priority)
								deadline = it.get("deadline", "")
								child = self.tree.insert(cat_id, "end", text=it.get("text", ""), 
													   values=(status, priority_symbol, deadline))
								# Restore metadata
								if child not in self.task_meta:
									self.task_meta[child] = {}
								comp = it.get("completed_date")
								if comp:
									self.task_meta[child]["last_completed_date"] = comp
								if deadline:
									self.task_meta[child]["deadline"] = deadline
							self._sort_category_by_priority(cat_id)
							self._update_category_count(name)
					elif "tasks" in data:
						populate_from_tasks_list(data.get("tasks", []))
					# Theme
					theme = (data.get("theme") if isinstance(data, dict) else DEFAULT_THEME) or DEFAULT_THEME
					if theme in self.themes:
						self.theme_var.set(theme)
						self.change_theme()
					# Stats
					stats = data.get("stats", {})
					self.stats_daily = dict(stats.get("daily_counts", {}))
				elif isinstance(data, list):
					populate_from_tasks_list(data)
		except Exception as e:
			messagebox.showerror("Error", f"Failed to load: {e}")
		self._update_category_choices()
		self._update_stats_view()

	def on_closing(self):
		"""Handle window closing event"""
		# Automatically save to the default tasks file
		if self.save_tasks(TASKS_FILE, show_error=False):
			self.root.destroy()
		else:
			# If auto-save fails, ask user if they want to quit anyway
			if messagebox.askyesno("Save Failed", 
								"Failed to save tasks automatically. Quit anyway?"):
				self.root.destroy()

	# --- Drag & drop handlers ---
	def _on_tree_press(self, event):
		# record item under cursor
		row = self.tree.identify_row(event.y)
		self._drag_item = row if row else None
		self._drag_over = None

	def _on_tree_motion(self, event):
		if not self._drag_item:
			return
		row = self.tree.identify_row(event.y)
		self._drag_over = row

	def _on_tree_release(self, event):
		if not self._drag_item:
			return
		source = self._drag_item
		target = self._drag_over or self.tree.identify_row(event.y)
		self._drag_item = None
		self._drag_over = None
		if not target or source == target:
			return
		s_parent = self.tree.parent(source)
		t_parent = self.tree.parent(target)
		# If dropping onto a task, use its parent as the target category
		if t_parent:
			target_cat_id = t_parent
		else:
			target_cat_id = target
		# Source is category
		if not s_parent:
			# Only allow reordering among top-level
			if not t_parent:
				index = self.tree.index(target)
				self.tree.move(source, "", index)
			return
		# Source is task; move under target category
		cat_label = self.tree.item(target_cat_id, "text").split(" (")[0]
		self.tree.move(source, target_cat_id, "end")
		# Tasks keep theme text color (do not tag tasks with category color)
		# Update counts for both categories
		if s_parent:
			old_cat = self.tree.item(s_parent, "text").split(" (")[0]
			self._update_category_count(old_cat)
		self._update_category_count(cat_label)

if __name__ == "__main__":
	root = tk.Tk()
	# Set minimum window size to ensure all buttons are visible
	root.minsize(600, 400)
	app = TodoApp(root)
	# Set default window size
	root.geometry("600x400")
	# Make the window resizable
	root.resizable(True, True)
	root.mainloop()
 