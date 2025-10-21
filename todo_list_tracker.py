import json
import os
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox, ttk

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Create data directory if it doesn't exist
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
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
        
		top_frame = tk.Frame(root)
		top_frame.pack(padx=8, pady=6, fill="x")

		self.entry = tk.Entry(top_frame)
		self.entry.pack(side="left", expand=True, fill="x", padx=(0,6))
		self.entry.bind("<Return>", lambda e: self.add_task())

		add_btn = tk.Button(top_frame, text="Add", width=10, command=self.add_task)
		add_btn.pack(side="left")

		list_frame = tk.Frame(root)
		list_frame.pack(padx=8, pady=(0,6), fill="both", expand=True)

		self.listbox = tk.Listbox(list_frame, selectmode="browse")
		self.listbox.pack(side="left", fill="both", expand=True)
		self.listbox.bind("<Double-Button-1>", lambda e: self.toggle_complete())
		self.listbox.bind("<Delete>", lambda e: self.remove_task())

		scrollbar = tk.Scrollbar(list_frame, command=self.listbox.yview)
		scrollbar.pack(side="right", fill="y")
		self.listbox.config(yscrollcommand=scrollbar.set)

		btn_frame = tk.Frame(root)
		btn_frame.pack(padx=8, pady=(0,8), fill="x")

		tk.Button(btn_frame, text="Edit", width=10, command=self.edit_task).pack(side="left")
		tk.Button(btn_frame, text="Remove", width=10, command=self.remove_task).pack(side="left", padx=6)
		tk.Button(btn_frame, text="Toggle Complete", width=14, command=self.toggle_complete).pack(side="left")
		tk.Button(btn_frame, text="Clear Completed", width=14, command=self.clear_completed).pack(side="left", padx=6)
		tk.Button(btn_frame, text="Save", width=10, command=self.save_tasks).pack(side="right")
		tk.Button(btn_frame, text="Load", width=10, command=self.load_tasks).pack(side="right", padx=(0,6))

		self.tasks = []
		self.load_tasks(startup=True)
		self.apply_theme()

	def change_theme(self):
		self.current_theme = self.themes[self.theme_var.get()]
		self.apply_theme()

	def apply_theme(self):
		# Apply theme to root and frames
		self.root.configure(bg=self.current_theme["bg"])
        
		# Update theme label
		self.theme_label.configure(bg=self.current_theme["bg"],
								 fg=self.current_theme["fg"])
        
		for frame in self.root.winfo_children():
			if isinstance(frame, tk.Frame):
				frame.configure(bg=self.current_theme["bg"])
				for widget in frame.winfo_children():
					if isinstance(widget, ttk.Combobox):
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
					elif isinstance(widget, tk.Scrollbar):
						widget.configure(bg=self.current_theme["button_bg"],
									  troughcolor=self.current_theme["bg"])
					elif isinstance(widget, tk.Label) and widget != self.theme_label:
						widget.configure(bg=self.current_theme["bg"],
									  fg=self.current_theme["fg"])

	def display_text(self, task):
		return ("[x] " if task["done"] else "[ ] ") + task["text"]

	def refresh_listbox(self):
		self.listbox.delete(0, "end")
		for t in self.tasks:
			self.listbox.insert("end", self.display_text(t))

	def add_task(self):
		text = self.entry.get().strip()
		if not text:
			return
		self.tasks.append({"text": text, "done": False})
		self.entry.delete(0, "end")
		self.refresh_listbox()

	def get_selected_index(self):
		sel = self.listbox.curselection()
		if not sel:
			messagebox.showinfo("Select item", "Please select a task first.")
			return None
		return sel[0]

	def remove_task(self):
		idx = self.get_selected_index()
		if idx is None:
			return
		if messagebox.askyesno("Remove", "Remove selected task?"):
			self.tasks.pop(idx)
			self.refresh_listbox()

	def edit_task(self):
		idx = self.get_selected_index()
		if idx is None:
			return
		current = self.tasks[idx]["text"]
		new = simpledialog.askstring("Edit task", "Modify task text:", initialvalue=current, parent=self.root)
		if new is None:
			return
		new = new.strip()
		if new:
			self.tasks[idx]["text"] = new
			self.refresh_listbox()

	def toggle_complete(self):
		idx = self.get_selected_index()
		if idx is None:
			return
		self.tasks[idx]["done"] = not self.tasks[idx]["done"]
		self.refresh_listbox()
		# Restore the selection
		self.listbox.selection_set(idx)
		# Ensure the selected item is visible
		self.listbox.see(idx)

	def clear_completed(self):
		if messagebox.askyesno("Clear", "Remove all completed tasks?"):
			self.tasks = [t for t in self.tasks if not t["done"]]
			self.refresh_listbox()

	def save_tasks(self, path=None, show_error=True):
		if path is None:
			path = filedialog.asksaveasfilename(defaultextension=".json",
											  filetypes=[("JSON files","*.json"),("All files","*.*")],
											  initialfile=TASKS_FILE)
			if not path:
				return False

		try:
			data = {
				"tasks": self.tasks,
				"theme": self.theme_var.get()
			}
			with open(path, "w", encoding="utf-8") as f:
				json.dump(data, f, ensure_ascii=False, indent=2)
			return True
		except Exception as e:
			if show_error:
				messagebox.showerror("Error", f"Failed to save: {e}")
			return False

	def load_tasks(self, startup=False):
		if startup:
			try:
				with open(TASKS_FILE, "r", encoding="utf-8") as f:
					data = json.load(f)
					if isinstance(data, dict):
						# New format with tasks and theme
						self.tasks = [{"text": t.get("text",""), "done": bool(t.get("done",False))} 
									for t in data.get("tasks", [])]
						theme = data.get("theme", DEFAULT_THEME)
						if theme in self.themes:
							self.theme_var.set(theme)
							self.change_theme()
					elif isinstance(data, list):
						# Old format (backward compatibility)
						self.tasks = [{"text": t.get("text",""), "done": bool(t.get("done",False))} 
									for t in data]
			except Exception:
				self.tasks = []
			self.refresh_listbox()
			return

		path = filedialog.askopenfilename(defaultextension=".json",
										  filetypes=[("JSON files","*.json"),("All files","*.*")])
		if not path:
			return
		try:
			with open(path, "r", encoding="utf-8") as f:
				data = json.load(f)
				if isinstance(data, dict):
					# New format with tasks and theme
					self.tasks = [{"text": t.get("text",""), "done": bool(t.get("done",False))} 
								for t in data.get("tasks", [])]
					theme = data.get("theme", DEFAULT_THEME)
					if theme in self.themes:
						self.theme_var.set(theme)
						self.change_theme()
				elif isinstance(data, list):
					# Old format (backward compatibility)
					self.tasks = [{"text": t.get("text",""), "done": bool(t.get("done",False))} 
								for t in data]
				self.refresh_listbox()
		except Exception as e:
			messagebox.showerror("Error", f"Failed to load: {e}")
    
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
 