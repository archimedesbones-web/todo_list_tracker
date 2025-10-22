import os
import sys
import json
import os
import sys
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
os.makedirs(DATA_DIR, exist_ok=True)

# Default paths
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")
DEFAULT_THEME = "Light"

class TodoApp:
	def __init__(self, root):
		self.root = root
		root.title("To-Do List Tracker")
        
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
		self.notebook.add(self.tasks_tab, text="Tasks")
		self.notebook.add(self.stats_tab, text="Stats")

		# Top input row (Tasks tab)
		top_frame = tk.Frame(self.tasks_tab)
		top_frame.pack(padx=8, pady=6, fill="x")

		self.entry = tk.Entry(top_frame)
		self.entry.pack(side="left", expand=True, fill="x", padx=(0,6))
		self.entry.bind("<Return>", lambda e: self.add_task())

		self.category_var = tk.StringVar()
		# Use a Combobox as a scrollable wheel for categories; allow typing new ones
		self.category_combo = ttk.Combobox(top_frame, textvariable=self.category_var, width=16, state="normal")
		self.category_combo.pack(side="left", padx=(0,6))
		self.category_var.set("General")
		# Scroll through categories with mouse wheel
		self.category_combo.bind("<MouseWheel>", self._category_on_mousewheel)

		self.priority_var = tk.StringVar(value="Medium")
		self.priority_combo = ttk.Combobox(top_frame, textvariable=self.priority_var, 
									  values=["High", "Medium", "Low"], state="readonly", width=8)
		self.priority_combo.pack(side="left", padx=(0,6))

		add_btn = tk.Button(top_frame, text="Add", width=10, command=self.add_task)
		add_btn.pack(side="left")

		# Treeview for categories and tasks (Tasks tab)
		tree_frame = tk.Frame(self.tasks_tab)
		tree_frame.pack(padx=8, pady=(0,6), fill="both", expand=True)

		self.tree = ttk.Treeview(tree_frame, columns=("status", "priority"), show="tree headings", selectmode="extended")
		self.tree.heading("#0", text="Tasks")
		self.tree.heading("status", text="Status")
		self.tree.heading("priority", text="Priority")
		self.tree.column("status", width=70, anchor="center")
		self.tree.column("priority", width=80, anchor="center")
		self.tree.pack(side="left", fill="both", expand=True)

		scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
		scrollbar.pack(side="right", fill="y")
		self.tree.configure(yscrollcommand=scrollbar.set)

		# Buttons row (Tasks tab)
		btn_frame = tk.Frame(self.tasks_tab)
		btn_frame.pack(padx=8, pady=(0,8), fill="x")

		tk.Button(btn_frame, text="Edit", width=10, command=self.edit_task).pack(side="left")
		tk.Button(btn_frame, text="Remove", width=10, command=self.remove_task).pack(side="left", padx=6)
		tk.Button(btn_frame, text="Toggle Complete", width=16, command=self.toggle_complete).pack(side="left")
		tk.Button(btn_frame, text="Clear Completed", width=16, command=self.clear_completed).pack(side="left", padx=6)
		tk.Button(btn_frame, text="Save", width=10, command=self.save_tasks).pack(side="right")
		tk.Button(btn_frame, text="Load", width=10, command=self.load_tasks).pack(side="right", padx=(0,6))

		# Bindings
		self.tree.bind("<Double-1>", lambda e: self.toggle_complete())
		self.tree.bind("<Delete>", lambda e: self.remove_task())
		self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)
		# Drag & drop
		self.tree.bind("<ButtonPress-1>", self._on_tree_press)
		self.tree.bind("<B1-Motion>", self._on_tree_motion)
		self.tree.bind("<ButtonRelease-1>", self._on_tree_release)

		# Category tracking and colors
		self.categories = {}  # name -> tree item id
		self.category_colors = {}  # name -> color
		self._last_category = "General"  # remember last used category
		self._priority_sort_reverse = False  # False=High->Low, True=Low->High
		# Stats tracking
		self.stats_daily = {}  # date_str -> count
		self.task_meta = {}    # tree item id -> {"last_completed_date": str|None}
		self._color_palette = [
			"#e6194B", "#3cb44b", "#ffe119", "#0082c8", "#f58231",
			"#911eb4", "#46f0f0", "#f032e6", "#d2f53c", "#fabebe",
			"#008080", "#e6beff", "#aa6e28", "#800000", "#aaffc3",
			"#808000", "#ffd8b1", "#000080", "#808080", "#FFFFFF"
		]
		self._drag_item = None
		self._drag_over = None

		# --- Stats tab UI ---
		stats_header = tk.Frame(self.stats_tab)
		stats_header.pack(padx=8, pady=8, fill="x")
		self.today_label = tk.Label(stats_header, text="Today's completed: 0")
		self.today_label.pack(side="left")
		self.stats_canvas = tk.Canvas(self.stats_tab, height=220, highlightthickness=0)
		self.stats_canvas.pack(padx=8, pady=(0,8), fill="both", expand=True)

		# Initial load and theme
		self.load_tasks(startup=True)
		self.apply_theme()
		self.tree.heading("priority", command=self._sort_all_by_priority)
		self._update_stats_view()

	def change_theme(self):
		self.current_theme = self.themes[self.theme_var.get()]
		self.apply_theme()

	def apply_theme(self):
		# Apply theme to root and frames
		self.root.configure(bg=self.current_theme["bg"])
        
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
					  borderwidth=0)
		style.configure('Treeview.Heading',
					  background=self.current_theme["button_bg"],
					  foreground=self.current_theme["button_fg"])
		# Compute a high-contrast selection color for better visibility
		def _hex_to_rgb(h):
			_h = h.lstrip('#')
			return tuple(int(_h[i:i+2], 16) for i in (0, 2, 4))
		bg_rgb = _hex_to_rgb(self.current_theme["listbox_bg"]) if isinstance(self.current_theme.get("listbox_bg"), str) else (255,255,255)
		# perceived brightness
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
					if isinstance(widget, (ttk.Combobox, ttk.Treeview, ttk.Scrollbar)):
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
						widget.configure(bg=self.current_theme["bg"]) 
					elif isinstance(widget, tk.Scrollbar):
						widget.configure(bg=self.current_theme["button_bg"],
									  troughcolor=self.current_theme["bg"])
					elif isinstance(widget, tk.Label) and widget != self.theme_label:
						widget.configure(bg=self.current_theme["bg"],
									  fg=self.current_theme["fg"])

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
		# Color only the category row to keep task text using theme colors
		self.tree.tag_configure(f"cat:{name}", foreground=color)
		cat_id = self.categories.get(name)
		if cat_id:
			self.tree.item(cat_id, tags=(f"cat:{name}",))

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
		except Exception:
			pass

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

	def _selected_item(self):
		selection = self.tree.selection()
		if not selection:
			messagebox.showinfo("Select item", "Please select a category or task first.")
			return None
		return selection[0]

	def _priority_symbol(self, priority):
		symbols = {"High": "⬆️", "Medium": "➡️", "Low": "⬇️"}
		return symbols.get(priority, "➡️")

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

	def _update_stats_view(self):
		# Update today's label
		today = self._today_str()
		cnt = self.stats_daily.get(today, 0)
		if hasattr(self, 'today_label') and self.today_label:
			self.today_label.configure(text=f"Today's completed: {cnt}")
		# Draw graph
		if hasattr(self, 'stats_canvas') and self.stats_canvas:
			self._render_stats_graph()

	def _render_stats_graph(self):
		canvas = self.stats_canvas
		canvas.delete("all")
		# Determine size
		w = canvas.winfo_width() or canvas.winfo_reqwidth()
		h = canvas.winfo_height() or 220
		margin_left, margin_right, margin_top, margin_bottom = 36, 10, 10, 26
		inner_w = max(1, w - margin_left - margin_right)
		inner_h = max(1, h - margin_top - margin_bottom)
		# Prepare data for last 14 days
		days = 14
		day_list = [date.today() - timedelta(days=i) for i in range(days-1, -1, -1)]
		vals = [self.stats_daily.get(d.isoformat(), 0) for d in day_list]
		max_v = max(vals) if vals else 0
		step = inner_w / max(1, len(day_list))
		bar_w = step * 0.6
		bar_color = self.current_theme.get("button_bg", "#4a90e2")
		fg = self.current_theme.get("fg", "#000000")
		# Draw axes baseline
		canvas.create_line(margin_left, h - margin_bottom, w - margin_right, h - margin_bottom, fill=fg)
		# Draw bars and labels
		for i, d in enumerate(day_list):
			x_center = margin_left + i * step + step / 2
			val = vals[i]
			ratio = (val / max_v) if max_v > 0 else 0
			bar_h = ratio * inner_h
			x0 = x_center - bar_w/2
			y0 = (margin_top + inner_h) - bar_h
			x1 = x_center + bar_w/2
			y1 = margin_top + inner_h
			canvas.create_rectangle(x0, y0, x1, y1, fill=bar_color, outline=bar_color)
			# Label every other day to avoid clutter
			if i % 2 == 0:
				label = d.strftime('%m-%d')
				canvas.create_text(x_center, h - margin_bottom + 10, text=label, fill=fg, font=(None, 8))

	def add_task(self):
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
		item = self.tree.insert(cat_id, "end", text=text, values=("[ ]", priority_display))
		# Store priority in item tags for sorting
		self.tree.set(item, "#1", "[ ]")
		self.tree.set(item, "#2", priority_display)
		# Sort tasks by priority within category
		self._sort_category_by_priority(cat_id)
		# Clear inputs, keep last used category for faster subsequent adds
		self.entry.delete(0, "end")
		self._last_category = category
		# keep category_var as-is to allow rapid multiple entries
		self.priority_var.set("Medium")
		self._update_category_count(category)

	def _sort_category_by_priority(self, cat_id, reverse=False):
		"""Sort tasks within a category by priority (High -> Medium -> Low, or reverse)"""
		children = list(self.tree.get_children(cat_id))
		if not children:
			return
		# Get task data with priority
		tasks_data = []
		for child in children:
			text = self.tree.item(child, "text")
			vals = self.tree.item(child).get("values") or ["[ ]", "➡️"]
			status = vals[0] if len(vals) > 0 else "[ ]"
			priority_symbol = vals[1] if len(vals) > 1 else "➡️"
			# Map symbol back to priority
			priority_map = {"⬆️": "High", "➡️": "Medium", "⬇️": "Low"}
			priority = priority_map.get(priority_symbol, "Medium")
			tasks_data.append((child, text, status, priority, priority_symbol))
		
		# Sort by priority order
		tasks_data.sort(key=lambda x: self._priority_order(x[3]), reverse=reverse)
		
		# Reinsert in sorted order
		for idx, (child, text, status, priority, priority_symbol) in enumerate(tasks_data):
			self.tree.move(child, cat_id, idx)

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

	def edit_task(self):
		item = self._selected_item()
		if not item:
			return
		parent = self.tree.parent(item)
		if not parent:
			# Edit category name and color
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
		# Editing a task
		old_text = self.tree.item(item, "text")
		cat_label = self.tree.item(parent, "text")
		old_cat = cat_label.split(" (")[0]
		vals = self.tree.item(item).get("values") or ["[ ]", "➡️"]
		old_priority_symbol = vals[1] if len(vals) > 1 else "➡️"
		priority_map = {"⬆️": "High", "➡️": "Medium", "⬇️": "Low"}
		old_priority = priority_map.get(old_priority_symbol, "Medium")
		
		new_text = simpledialog.askstring("Edit task", "Modify task text:", initialvalue=old_text, parent=self.root)
		new_cat = simpledialog.askstring("Edit category", "Modify category:", initialvalue=old_cat, parent=self.root)
		if new_text is None:
			return
		new_text = new_text.strip()
		if not new_text:
			return
		
		# Ask for new priority
		priority_window = tk.Toplevel(self.root)
		priority_window.title("Select Priority")
		priority_window.geometry("250x100")
		tk.Label(priority_window, text="Select priority:").pack(pady=10)
		new_priority_var = tk.StringVar(value=old_priority)
		priority_combo = ttk.Combobox(priority_window, textvariable=new_priority_var, 
								   values=["High", "Medium", "Low"], state="readonly", width=12)
		priority_combo.pack(pady=5)
		
		confirmed = [False]
		def confirm():
			confirmed[0] = True
			priority_window.destroy()
		tk.Button(priority_window, text="OK", command=confirm).pack(pady=5)
		priority_window.wait_window()
		
		if not confirmed[0]:
			return
			
		new_priority = new_priority_var.get() or old_priority
		new_priority_symbol = self._priority_symbol(new_priority)
		
		# Update text and priority
		self.tree.item(item, text=new_text)
		current_vals = list(self.tree.item(item).get("values") or ["[ ]", "➡️"])
		current_vals[1] = new_priority_symbol
		self.tree.item(item, values=tuple(current_vals))
		
		# Move category if changed
		new_cat = (new_cat or old_cat).strip() or old_cat
		if new_cat != old_cat:
			new_cat_id = self._ensure_category(new_cat)
			self.tree.move(item, new_cat_id, "end")
			self._sort_category_by_priority(new_cat_id)
			self._update_category_count(old_cat)
			self._update_category_count(new_cat)
		else:
			# Re-sort if priority changed
			self._sort_category_by_priority(parent)
			self._update_category_count(old_cat)

	def toggle_complete(self):
		selection = self.tree.selection()
		if not selection:
			return
		
		def set_status_and_stats(it, new_val):
			# Update tree values
			vals = self.tree.item(it).get("values") or ["[ ]", "➡️"]
			priority = vals[1] if len(vals) > 1 else "➡️"
			self.tree.item(it, values=(new_val, priority))
			# Stats adjustment
			if new_val == "[x]":
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
		self._update_stats_view()

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
					vals = self.tree.item(child).get("values") or ["[ ]", "➡️"]
					priority_symbol = vals[1] if len(vals) > 1 else "➡️"
					priority_map = {"⬆️": "High", "➡️": "Medium", "⬇️": "Low"}
					priority = priority_map.get(priority_symbol, "Medium")
					item_data = {
						"text": text,
						"done": vals[0] == "[x]",
						"priority": priority
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
									child = self.tree.insert(cat_id, "end", text=it.get("text", ""), values=(status, priority_symbol))
									comp = it.get("completed_date")
									if comp:
										self.task_meta[child] = {"last_completed_date": comp}
								self._sort_category_by_priority(cat_id)
								self._update_category_count(name)
						elif "tasks" in data:
							populate_from_tasks_list(data.get("tasks", []))
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
								child = self.tree.insert(cat_id, "end", text=it.get("text", ""), values=(status, priority_symbol))
								comp = it.get("completed_date")
								if comp:
									self.task_meta[child] = {"last_completed_date": comp}
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
 