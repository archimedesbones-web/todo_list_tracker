"""
Real 3D Claymation Avatar System - Alternative Implementation
Uses matplotlib's 3D plotting for true 3D claymation without OpenGL complexity
"""

import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import math
import time

# Check matplotlib availability
try:
    import matplotlib
    matplotlib.use('TkAgg')
    MATPLOTLIB_3D_AVAILABLE = True
except ImportError:
    MATPLOTLIB_3D_AVAILABLE = False

class Real3DClayAvatar(tk.Frame):
    """Real 3D Claymation Avatar using matplotlib's 3D engine"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.avatar_state = {
            "x": 0, "y": 0, "z": 0,
            "rotation": 0,
            "shirt": "t_shirt_blue",
            "pants": "jeans_blue", 
            "hat": "none"
        }
        self.pets = []
        self.is_initialized = False
        self.camera_elevation = 15
        self.camera_azimuth = 45
        self.animation_time = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI with 3D matplotlib widget or fallback"""
        # Title
        title = tk.Label(self, text="🎮 Real 3D Claymation Avatar", 
                        font=("Arial", 14, "bold"), fg="#e74c3c")
        title.pack(pady=(0, 10))
        
        # Check if we can use real 3D
        if MATPLOTLIB_3D_AVAILABLE:
            self.setup_real_3d()
        else:
            self.setup_3d_fallback()
            
    def setup_real_3d(self):
        """Set up real matplotlib 3D rendering"""
        try:
            # Create matplotlib figure for 3D
            self.fig = Figure(figsize=(8, 6), dpi=80)
            self.ax = self.fig.add_subplot(111, projection='3d')
            
            # Create tkinter canvas
            self.canvas_3d = FigureCanvasTkAgg(self.fig, self)
            self.canvas_3d.get_tk_widget().pack(fill="both", expand=True, pady=(0, 10))
            
            # Set up 3D scene
            self.setup_3d_scene()
            
            self.is_3d_mode = True
            
            # Controls
            self.setup_3d_controls()
            
            # Bind mouse events for camera control
            self.canvas_3d.mpl_connect('button_press_event', self.on_mouse_press)
            self.canvas_3d.mpl_connect('motion_notify_event', self.on_mouse_motion)
            self.canvas_3d.mpl_connect('scroll_event', self.on_scroll)
            
            self.mouse_pressed = False
            
        except Exception as e:
            print(f"3D setup failed: {e}")
            self.setup_3d_fallback()
            
    def setup_3d_fallback(self):
        """Set up info message as fallback"""
        self.is_3d_mode = False
        
        # Info message
        info = tk.Label(self, text="📋 3D Avatar requires matplotlib\nPlease install: pip install matplotlib", 
                       justify="center", fg="#e74c3c", font=("Arial", 11))
        info.pack(pady=50)
        
        # Basic controls still
        self.setup_3d_controls()
        
    def setup_3d_scene(self):
        """Set up the 3D scene properties"""
        # Set background color to clay-like
        self.ax.set_facecolor('#f4e4bc')
        
        # Set axis limits
        self.ax.set_xlim([-5, 5])
        self.ax.set_ylim([-5, 5])
        self.ax.set_zlim([0, 8])
        
        # Set labels
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        
        # Set initial camera position
        self.ax.view_init(elev=self.camera_elevation, azim=self.camera_azimuth)
        
        # Remove axis for cleaner look (optional)
        # self.ax.set_axis_off()
        
    def setup_3d_controls(self):
        """Set up control interface for 3D avatar"""
        controls_frame = tk.Frame(self)
        controls_frame.pack(fill="x", pady=(0, 10))
        
        # Initialize button
        self.init_btn = tk.Button(controls_frame, 
                                 text="🎮 Initialize Real 3D Avatar" if self.is_3d_mode else "📋 3D Not Available",
                                 command=self.initialize_3d, 
                                 bg="#e74c3c", fg="white", font=("Arial", 11, "bold"),
                                 state="normal" if self.is_3d_mode else "disabled")
        self.init_btn.pack(pady=5)
        
        # Movement controls
        move_frame = tk.LabelFrame(controls_frame, text="Avatar Movement")
        move_frame.pack(side="left", padx=5)
        
        tk.Button(move_frame, text="↑", width=3, 
                 command=lambda: self.move_avatar("forward")).grid(row=0, column=1, padx=2, pady=2)
        tk.Button(move_frame, text="←", width=3,
                 command=lambda: self.move_avatar("left")).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(move_frame, text="↓", width=3,
                 command=lambda: self.move_avatar("backward")).grid(row=1, column=1, padx=2, pady=2)
        tk.Button(move_frame, text="→", width=3,
                 command=lambda: self.move_avatar("right")).grid(row=1, column=2, padx=2, pady=2)
        
        tk.Button(move_frame, text="⬆", width=3,
                 command=lambda: self.move_avatar("up")).grid(row=0, column=3, padx=2, pady=2)
        tk.Button(move_frame, text="⬇", width=3,
                 command=lambda: self.move_avatar("down")).grid(row=1, column=3, padx=2, pady=2)
        
        # Camera controls (3D only)
        if self.is_3d_mode:
            camera_frame = tk.LabelFrame(controls_frame, text="3D Camera")
            camera_frame.pack(side="left", padx=5)
            
            tk.Button(camera_frame, text="🔄⬅", width=4,
                     command=lambda: self.rotate_camera("left")).grid(row=0, column=0, padx=2)
            tk.Button(camera_frame, text="⬆", width=4,
                     command=lambda: self.rotate_camera("up")).grid(row=0, column=1, padx=2)
            tk.Button(camera_frame, text="🔄➡", width=4,
                     command=lambda: self.rotate_camera("right")).grid(row=0, column=2, padx=2)
            tk.Button(camera_frame, text="🎯", width=4,
                     command=self.reset_camera).grid(row=1, column=0, padx=2)
            tk.Button(camera_frame, text="⬇", width=4,
                     command=lambda: self.rotate_camera("down")).grid(row=1, column=1, padx=2)
            tk.Button(camera_frame, text="🔄", width=4,
                     command=lambda: self.rotate_camera("spin")).grid(row=1, column=2, padx=2)
        
        # Customization controls
        custom_frame = tk.LabelFrame(controls_frame, text="Appearance")
        custom_frame.pack(side="left", padx=5)
        
        tk.Button(custom_frame, text="👕", width=3,
                 command=self.cycle_shirt).grid(row=0, column=0, padx=2)
        tk.Button(custom_frame, text="👖", width=3,
                 command=self.cycle_pants).grid(row=0, column=1, padx=2)
        tk.Button(custom_frame, text="🎩", width=3,
                 command=self.cycle_hat).grid(row=1, column=0, padx=2)
        tk.Button(custom_frame, text="🐾", width=3,
                 command=self.add_random_pet).grid(row=1, column=1, padx=2)
        
        # Status
        self.status_label = tk.Label(controls_frame, 
                                    text="Ready for REAL 3D claymation experience!" if self.is_3d_mode else "Install matplotlib for 3D",
                                    fg="#e74c3c" if self.is_3d_mode else "#95a5a6")
        self.status_label.pack(pady=5)
        
    def initialize_3d(self):
        """Initialize the 3D avatar system"""
        if not self.is_3d_mode:
            return
            
        self.init_btn.config(text="Initializing Real 3D...", state="disabled", bg="#95a5a6")
        self.status_label.config(text="Setting up real 3D claymation world...", fg="#f39c12")
        self.update()
        
        # Simulate initialization process
        self.after(1500, self._complete_3d_initialization)
        
    def _complete_3d_initialization(self):
        """Complete 3D initialization"""
        self.is_initialized = True
        
        if self.is_3d_mode:
            self.init_btn.config(text="🎮 REAL 3D Avatar Active!", bg="#27ae60", state="disabled")
            self.status_label.config(text="🎭 REAL 3D Claymation Avatar Ready! Drag mouse to rotate camera!", fg="#27ae60")
            self.draw_3d_scene()
        else:
            self.init_btn.config(text="📋 3D Not Available", bg="#95a5a6", state="disabled") 
            self.status_label.config(text="Install matplotlib for real 3D", fg="#95a5a6")
            
        # Start animation
        if self.is_3d_mode:
            self.animate_3d()
        
    def draw_3d_scene(self):
        """Draw the complete 3D scene"""
        if not self.is_3d_mode or not hasattr(self, 'ax'):
            return
            
        # Clear the axes
        self.ax.clear()
        self.setup_3d_scene()
        
        # Draw environment
        self.draw_3d_floor()
        
        # Draw avatar if initialized
        if self.is_initialized:
            self.draw_3d_avatar()
            self.draw_3d_pets()
        
        # Refresh canvas
        self.canvas_3d.draw()
        
    def draw_3d_floor(self):
        """Draw 3D clay floor"""
        # Create floor mesh
        x = np.linspace(-4, 4, 20)
        y = np.linspace(-4, 4, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        # Clay floor color
        self.ax.plot_surface(X, Y, Z, color='#d2b48c', alpha=0.6, linewidth=0, antialiased=True)
        
        # Floor grid lines for clay texture
        for i in range(len(x)):
            self.ax.plot([x[i], x[i]], [y[0], y[-1]], [0, 0], 'k-', alpha=0.1, linewidth=0.5)
        for i in range(len(y)):
            self.ax.plot([x[0], x[-1]], [y[i], y[i]], [0, 0], 'k-', alpha=0.1, linewidth=0.5)
            
    def draw_3d_avatar(self):
        """Draw the 3D claymation avatar"""
        if not self.is_initialized:
            return
            
        # Avatar position
        x, y, z = self.avatar_state["x"], self.avatar_state["y"], self.avatar_state["z"]
        
        # Breathing animation
        breath = 0.05 * math.sin(self.animation_time * 2)
        
        # Get clothing colors
        shirt_colors = {
            "t_shirt_blue": '#3498db',
            "t_shirt_red": '#e74c3c',
            "hoodie_green": '#27ae60',
            "polo_yellow": '#f1c40f',
            "sweater_purple": '#9b59b6'
        }
        
        pants_colors = {
            "jeans_blue": '#2980b9',
            "jeans_black": '#2c3e50',
            "khaki": '#d35400',
            "joggers_gray": '#7f8c8d',
            "shorts_red": '#c0392b'
        }
        
        shirt_color = shirt_colors.get(self.avatar_state["shirt"], '#3498db')
        pants_color = pants_colors.get(self.avatar_state["pants"], '#2980b9')
        
        # Draw head (clay-colored sphere)
        head_center = [x, y, z + 6 + breath]
        self.draw_3d_sphere(head_center, 0.8, '#f4a460')  # Sandy brown (clay)
        
        # Eyes
        eye_left = [x - 0.3, y - 0.6, z + 6.2 + breath]
        eye_right = [x + 0.3, y - 0.6, z + 6.2 + breath]
        self.draw_3d_sphere(eye_left, 0.15, '#000000')
        self.draw_3d_sphere(eye_right, 0.15, '#000000')
        
        # Nose
        nose_center = [x, y - 0.7, z + 6 + breath]
        self.draw_3d_sphere(nose_center, 0.2, '#e19950')
        
        # Body (shirt colored)
        body_center = [x, y, z + 3.5 + breath]
        self.draw_3d_box(body_center, [1.6, 1.0, 2.5], shirt_color)
        
        # Arms
        arm_left = [x - 1.5, y, z + 4 + breath]
        arm_right = [x + 1.5, y, z + 4 + breath]
        self.draw_3d_box(arm_left, [0.6, 0.6, 2.0], shirt_color)
        self.draw_3d_box(arm_right, [0.6, 0.6, 2.0], shirt_color)
        
        # Legs (pants colored)
        leg_left = [x - 0.5, y, z + 1 + breath]
        leg_right = [x + 0.5, y, z + 1 + breath]
        self.draw_3d_box(leg_left, [0.7, 0.7, 2.5], pants_color)
        self.draw_3d_box(leg_right, [0.7, 0.7, 2.5], pants_color)
        
        # Feet (black shoes)
        foot_left = [x - 0.5, y + 0.4, z + 0.2]
        foot_right = [x + 0.5, y + 0.4, z + 0.2]
        self.draw_3d_box(foot_left, [0.8, 1.2, 0.4], '#2c3e50')
        self.draw_3d_box(foot_right, [0.8, 1.2, 0.4], '#2c3e50')
        
        # Hat if applicable
        self.draw_3d_hat(x, y, z + 7.2 + breath)
        
    def draw_3d_hat(self, x, y, z):
        """Draw 3D hat based on avatar state"""
        hat = self.avatar_state.get("hat", "none")
        
        if hat == "baseball_cap":
            # Baseball cap
            self.draw_3d_sphere([x, y, z], 0.6, '#e67e22')  # Orange cap
            self.draw_3d_box([x, y - 0.8, z - 0.2], [1.2, 0.4, 0.1], '#e67e22')  # Visor
            
        elif hat == "wizard_hat":
            # Wizard hat (cone)
            self.draw_3d_cone([x, y, z], 0.5, 1.5, '#8e44ad')  # Purple cone
            
        elif hat == "crown":
            # Simple crown
            self.draw_3d_box([x, y, z + 0.3], [1.0, 1.0, 0.6], '#f1c40f')  # Gold crown
            
    def draw_3d_pets(self):
        """Draw 3D pets around the avatar"""
        if not self.pets:
            return
            
        pet_positions = [
            [3, 2, 0.5], [-3, 2, 0.5], [2, -3, 0.5], [-2, -3, 0.5]
        ]
        
        for i, pet_type in enumerate(self.pets[:4]):  # Max 4 pets
            pos = pet_positions[i]
            
            # Add pet animation (gentle bobbing)
            pet_bob = 0.1 * math.sin(self.animation_time * 3 + i)
            pos[2] += pet_bob
            
            if pet_type == "pet_cat":
                self.draw_3d_cat(pos)
            elif pet_type == "pet_dog":
                self.draw_3d_dog(pos)
            elif pet_type == "pet_bird":
                self.draw_3d_bird(pos)
            elif pet_type == "pet_dragon":
                self.draw_3d_dragon(pos)
                
    def draw_3d_cat(self, pos):
        """Draw 3D cat"""
        x, y, z = pos
        
        # Cat body (orange)
        self.draw_3d_box([x, y, z + 0.3], [1.2, 0.6, 0.6], '#ff9500')
        # Cat head
        self.draw_3d_sphere([x + 0.8, y, z + 0.5], 0.4, '#ff9500')
        # Ears
        self.draw_3d_cone([x + 0.9, y - 0.2, z + 0.8], 0.1, 0.3, '#ff9500')
        self.draw_3d_cone([x + 0.9, y + 0.2, z + 0.8], 0.1, 0.3, '#ff9500')
        
    def draw_3d_dog(self, pos):
        """Draw 3D dog"""
        x, y, z = pos
        
        # Dog body (brown, larger than cat)
        self.draw_3d_box([x, y, z + 0.4], [1.5, 0.8, 0.8], '#8b4513')
        # Dog head
        self.draw_3d_box([x + 1.0, y, z + 0.6], [0.8, 0.6, 0.6], '#8b4513')
        
    def draw_3d_bird(self, pos):
        """Draw 3D bird"""
        x, y, z = pos
        
        # Bird body (blue)
        self.draw_3d_sphere([x, y, z + 1.0], 0.3, '#3498db')
        # Wings
        self.draw_3d_box([x, y - 0.5, z + 1.0], [0.1, 0.8, 0.4], '#2980b9')
        
    def draw_3d_dragon(self, pos):
        """Draw 3D dragon"""
        x, y, z = pos
        
        # Dragon body (green, majestic)
        self.draw_3d_box([x, y, z + 0.5], [2.0, 1.0, 1.0], '#27ae60')
        # Dragon head
        self.draw_3d_box([x + 1.5, y, z + 0.8], [1.0, 0.8, 0.8], '#27ae60')
        # Wings
        self.draw_3d_box([x, y - 1.0, z + 1.2], [0.2, 1.5, 0.8], '#229954')
        self.draw_3d_box([x, y + 1.0, z + 1.2], [0.2, 1.5, 0.8], '#229954')
        
    def draw_3d_sphere(self, center, radius, color):
        """Draw a 3D sphere"""
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        x = center[0] + radius * np.outer(np.cos(u), np.sin(v))
        y = center[1] + radius * np.outer(np.sin(u), np.sin(v))
        z = center[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        self.ax.plot_surface(x, y, z, color=color, alpha=0.8, linewidth=0, antialiased=True)
        
    def draw_3d_box(self, center, dimensions, color):
        """Draw a 3D box"""
        dx, dy, dz = [d/2 for d in dimensions]
        
        # Define the vertices of a box
        r = [-dx, dx]
        s = [-dy, dy] 
        t = [-dz, dz]
        
        # Generate faces
        for i in [0, 1]:
            for j in [0, 1]:
                for k in [0, 1]:
                    # Create each face of the box
                    if i == 0:  # Left face
                        x = [center[0] + r[i]] * 4
                        y = [center[1] + s[0], center[1] + s[0], center[1] + s[1], center[1] + s[1]]
                        z = [center[2] + t[0], center[2] + t[1], center[2] + t[1], center[2] + t[0]]
                        self.ax.plot_surface(np.array([x, x]), np.array([y, y]), np.array([z, z]), color=color, alpha=0.8)
        
        # Simplified box using scatter points for better performance
        x_range = np.linspace(center[0] - dx, center[0] + dx, 5)
        y_range = np.linspace(center[1] - dy, center[1] + dy, 5)
        z_range = np.linspace(center[2] - dz, center[2] + dz, 5)
        
        X, Y, Z = np.meshgrid(x_range, y_range, z_range)
        self.ax.scatter(X, Y, Z, c=color, s=20, alpha=0.6)
        
    def draw_3d_cone(self, center, radius, height, color):
        """Draw a 3D cone"""
        # Simplified cone as pyramid
        self.draw_3d_box([center[0], center[1], center[2] + height/2], [radius*2, radius*2, height], color)
        
    # Avatar control methods
    def move_avatar(self, direction):
        """Move avatar in 3D space"""
        step = 0.5
        
        if direction == "forward":
            self.avatar_state["y"] -= step
        elif direction == "backward":  
            self.avatar_state["y"] += step
        elif direction == "left":
            self.avatar_state["x"] -= step
        elif direction == "right":
            self.avatar_state["x"] += step
        elif direction == "up":
            self.avatar_state["z"] += step
        elif direction == "down":
            self.avatar_state["z"] = max(0, self.avatar_state["z"] - step)
            
        self.update_display()
        
        if self.is_initialized:
            self.status_label.config(text=f"🎭 Avatar moved {direction} in REAL 3D!", fg="#27ae60")
            self.after(1500, lambda: self.status_label.config(
                text="🎮 REAL 3D Avatar Ready! Drag mouse to rotate camera!", fg="#27ae60"))
    
    def rotate_camera(self, direction):
        """Rotate camera around avatar (3D only)"""
        if not self.is_3d_mode:
            return
            
        angle_step = 15
        
        if direction == "left":
            self.camera_azimuth -= angle_step
        elif direction == "right":
            self.camera_azimuth += angle_step
        elif direction == "up":
            self.camera_elevation = min(90, self.camera_elevation + angle_step)
        elif direction == "down":
            self.camera_elevation = max(-90, self.camera_elevation - angle_step)
        elif direction == "spin":
            self.camera_azimuth += 45
            
        if hasattr(self, 'ax'):
            self.ax.view_init(elev=self.camera_elevation, azim=self.camera_azimuth)
            self.update_display()
        
    def reset_camera(self):
        """Reset camera to default position"""
        if not self.is_3d_mode:
            return
            
        self.camera_elevation = 15
        self.camera_azimuth = 45
        
        if hasattr(self, 'ax'):
            self.ax.view_init(elev=self.camera_elevation, azim=self.camera_azimuth)
            self.update_display()
    
    def cycle_shirt(self):
        """Cycle through shirt options"""
        shirts = ["t_shirt_blue", "t_shirt_red", "hoodie_green", "polo_yellow", "sweater_purple"]
        current_idx = shirts.index(self.avatar_state.get("shirt", "t_shirt_blue"))
        next_idx = (current_idx + 1) % len(shirts)
        self.avatar_state["shirt"] = shirts[next_idx]
        self.update_display()
        
    def cycle_pants(self):
        """Cycle through pants options"""
        pants = ["jeans_blue", "jeans_black", "khaki", "joggers_gray", "shorts_red"]
        current_idx = pants.index(self.avatar_state.get("pants", "jeans_blue"))
        next_idx = (current_idx + 1) % len(pants)
        self.avatar_state["pants"] = pants[next_idx]
        self.update_display()
        
    def cycle_hat(self):
        """Cycle through hat options"""
        hats = ["none", "baseball_cap", "wizard_hat", "crown"]
        current_idx = hats.index(self.avatar_state.get("hat", "none"))
        next_idx = (current_idx + 1) % len(hats)
        self.avatar_state["hat"] = hats[next_idx]
        self.update_display()
        
    def add_random_pet(self):
        """Add a random pet"""
        pets = ["pet_cat", "pet_dog", "pet_bird", "pet_dragon"]
        if len(self.pets) < 4:
            import random
            new_pet = random.choice(pets)
            if new_pet not in self.pets:
                self.pets.append(new_pet)
                self.update_display()
                self.status_label.config(text=f"🐾 Added {new_pet} in REAL 3D!", fg="#27ae60")
                self.after(1500, lambda: self.status_label.config(
                    text="🎮 REAL 3D Avatar Ready! Drag mouse to rotate camera!", fg="#27ae60"))
    
    def update_avatar_state(self, state_dict):
        """Update avatar appearance"""
        self.avatar_state.update(state_dict)
        self.update_display()
        
    def add_pet(self, pet_type):
        """Add a pet to the scene"""
        if pet_type not in self.pets and len(self.pets) < 4:
            self.pets.append(pet_type)
            self.update_display()
            
    def remove_pet(self, pet_type):
        """Remove a pet from the scene"""
        if pet_type in self.pets:
            self.pets.remove(pet_type)
            self.update_display()
            
    def update_display(self):
        """Update the 3D display"""
        if self.is_3d_mode:
            self.draw_3d_scene()
            
    def animate_3d(self):
        """Animation loop for 3D effects"""
        if self.is_initialized and self.is_3d_mode:
            self.animation_time += 0.05
            self.draw_3d_scene()
        self.after(100, self.animate_3d)
        
    # Mouse interaction for 3D mode
    def on_mouse_press(self, event):
        """Handle mouse press for camera control"""
        self.mouse_pressed = True
        self.last_mouse_x = event.xdata
        self.last_mouse_y = event.ydata
        
    def on_mouse_motion(self, event):
        """Handle mouse motion for camera rotation"""
        if self.mouse_pressed and event.xdata and event.ydata:
            if hasattr(self, 'last_mouse_x') and self.last_mouse_x:
                dx = event.xdata - self.last_mouse_x
                dy = event.ydata - self.last_mouse_y
                
                self.camera_azimuth += dx * 2
                self.camera_elevation += dy * 2
                self.camera_elevation = max(-90, min(90, self.camera_elevation))
                
                if hasattr(self, 'ax'):
                    self.ax.view_init(elev=self.camera_elevation, azim=self.camera_azimuth)
                    self.canvas_3d.draw_idle()
                
            self.last_mouse_x = event.xdata
            self.last_mouse_y = event.ydata
            
    def on_scroll(self, event):
        """Handle mouse scroll for zooming"""
        if hasattr(self, 'ax'):
            # Adjust axis limits for zoom
            scale = 0.9 if event.step > 0 else 1.1
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
            zlim = self.ax.get_zlim()
            
            center_x = (xlim[0] + xlim[1]) / 2
            center_y = (ylim[0] + ylim[1]) / 2
            center_z = (zlim[0] + zlim[1]) / 2
            
            width_x = (xlim[1] - xlim[0]) * scale / 2
            width_y = (ylim[1] - ylim[0]) * scale / 2
            width_z = (zlim[1] - zlim[0]) * scale / 2
            
            self.ax.set_xlim([center_x - width_x, center_x + width_x])
            self.ax.set_ylim([center_y - width_y, center_y + width_y])
            self.ax.set_zlim([center_z - width_z, center_z + width_z])
            
            self.canvas_3d.draw_idle()


# Test the real 3D avatar
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Real 3D Claymation Avatar")
    root.geometry("800x700")
    
    if MATPLOTLIB_3D_AVAILABLE:
        avatar = Real3DClayAvatar(root)
        avatar.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Auto-initialize
        root.after(1000, avatar.initialize_3d)
    else:
        label = tk.Label(root, text="Please install matplotlib:\npip install matplotlib", 
                        font=("Arial", 16), fg="red")
        label.pack(expand=True)
    
    root.mainloop()