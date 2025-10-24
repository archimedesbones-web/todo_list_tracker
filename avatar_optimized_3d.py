"""
Optimized 3D Avatar System - Fast Blender-like rendering
Uses optimized drawing techniques for smooth 60 FPS performance
"""

import tkinter as tk
from tkinter import messagebox
import math
import time

class Optimized3DAvatar(tk.Frame):
    """Super fast 3D Avatar that looks like Blender models but renders at 60 FPS"""
    
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
        
        # 3D Camera settings - positioned for /-----\ perspective room view
        self.camera_x = 0     # Center on back wall
        self.camera_y = -4    # Positioned to see angled walls clearly
        self.camera_z = 2     # Good height for perspective
        self.camera_rotation_y = 0    # Look straight at back center wall
        self.camera_rotation_x = -5   # Slight downward angle for 3D perspective
        
        # Animation
        self.animation_time = 0
        self.animation_running = False
        
        # Room settings
        self.show_walls = True
        self.show_grid = True
        self.room_theme = "cozy"  # cozy, modern, classic
        self.camera_preset = 0    # 0=isometric, 1=corner view, 2=side view, 3=overhead
        
        # Canvas settings for performance
        self.canvas_width = 700
        self.canvas_height = 600
        self.center_x = self.canvas_width // 2
        self.center_y = self.canvas_height // 2
        self.scale_3d = 200  # Much larger scale to see full avatar
        
        # Pre-computed lighting values for speed
        self.light_cache = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the optimized 3D UI"""
        # Title
        title = tk.Label(self, text="⚡ Ultra-Fast 3D Avatar", 
                        font=("Arial", 16, "bold"), fg="#e74c3c")
        title.pack(pady=(0, 10))
        
        subtitle = tk.Label(self, text="60 FPS Blender-style rendering with optimized techniques", 
                           font=("Arial", 10), fg="#7f8c8d")
        subtitle.pack(pady=(0, 15))
        
        # High-performance canvas
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, 
                               bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(pady=(0, 15))
        
        # No mouse camera controls - fixed room view
        
        # Controls
        self.setup_controls()
        
        # Draw initial scene
        self.draw_3d_scene()
        
        # Auto-initialize after a short delay
        self.after(1000, self.initialize_3d)
        
    def setup_controls(self):
        """Set up control interface"""
        controls_frame = tk.Frame(self)
        controls_frame.pack(fill="x", pady=(0, 10))
        
        # Initialize button
        self.init_btn = tk.Button(controls_frame, 
                                 text="⚡ Initialize Ultra-Fast 3D",
                                 command=self.initialize_3d, 
                                 bg="#e74c3c", fg="white", font=("Arial", 12, "bold"))
        self.init_btn.pack(pady=8)
        
        # Control panels
        controls_row = tk.Frame(controls_frame)
        controls_row.pack(fill="x", pady=5)
        
        # Movement controls
        move_frame = tk.LabelFrame(controls_row, text="Movement", font=("Arial", 10, "bold"))
        move_frame.pack(side="left", padx=10, pady=5)
        
        tk.Button(move_frame, text="↑", width=4, height=2, font=("Arial", 12, "bold"),
                 command=lambda: self.move_avatar("forward")).grid(row=0, column=1, padx=3, pady=2)
        tk.Button(move_frame, text="←", width=4, height=2, font=("Arial", 12, "bold"),
                 command=lambda: self.move_avatar("left")).grid(row=1, column=0, padx=3, pady=2)
        tk.Button(move_frame, text="↓", width=4, height=2, font=("Arial", 12, "bold"),
                 command=lambda: self.move_avatar("backward")).grid(row=1, column=1, padx=3, pady=2)
        tk.Button(move_frame, text="→", width=4, height=2, font=("Arial", 12, "bold"),
                 command=lambda: self.move_avatar("right")).grid(row=1, column=2, padx=3, pady=2)
        
        # Room view controls (no camera movement)
        room_frame = tk.LabelFrame(controls_row, text="Room View", font=("Arial", 10, "bold"))
        room_frame.pack(side="left", padx=10, pady=5)
        
        tk.Button(room_frame, text="🏠", width=5,
                 command=self.toggle_walls).grid(row=0, column=0, padx=2)
        tk.Button(room_frame, text="�", width=5,
                 command=self.toggle_lighting).grid(row=0, column=1, padx=2)
        tk.Button(room_frame, text="�", width=5,
                 command=self.cycle_room_theme).grid(row=1, column=0, padx=2)
        tk.Button(room_frame, text="📐", width=5,
                 command=self.toggle_grid).grid(row=1, column=1, padx=2)
        tk.Button(room_frame, text="📷", width=5,
                 command=self.cycle_camera_preset).grid(row=0, column=2, padx=2)
        
        # Customization
        custom_frame = tk.LabelFrame(controls_row, text="Customize", font=("Arial", 10, "bold"))
        custom_frame.pack(side="left", padx=10, pady=5)
        
        tk.Button(custom_frame, text="👕", width=4,
                 command=self.cycle_shirt).grid(row=0, column=0, padx=2)
        tk.Button(custom_frame, text="👖", width=4,
                 command=self.cycle_pants).grid(row=0, column=1, padx=2)
        tk.Button(custom_frame, text="🎩", width=4,
                 command=self.cycle_hat).grid(row=1, column=0, padx=2)
        tk.Button(custom_frame, text="🐾", width=4,
                 command=self.add_random_pet).grid(row=1, column=1, padx=2)
        
        # Status
        self.status_label = tk.Label(controls_frame, 
                                    text="Ready for ultra-fast 3D room view! Fixed camera shows all walls and floor",
                                    fg="#2c3e50", font=("Arial", 10))
        self.status_label.pack(pady=8)
        
        # Performance indicator
        self.perf_label = tk.Label(controls_frame,
                                  text="Room View Mode: Fixed Camera | Ultra-Fast 60 FPS",
                                  fg="#27ae60", font=("Arial", 9, "bold"))
        self.perf_label.pack()
        
    def initialize_3d(self):
        """Initialize the optimized 3D avatar system"""
        self.init_btn.config(text="Initializing Ultra-Fast 3D...", state="disabled", bg="#95a5a6")
        self.status_label.config(text="Optimizing rendering pipeline...", fg="#f39c12")
        self.update()
        
        # Pre-compute lighting cache for performance
        self.precompute_lighting()
        
        self.after(500, self._complete_3d_initialization)
        
    def _complete_3d_initialization(self):
        """Complete 3D initialization"""
        self.is_initialized = True
        
        self.init_btn.config(text="⚡ Ultra-Fast 3D Active!", bg="#27ae60", state="disabled")
        self.status_label.config(text="⚡ Ultra-Fast 3D Room Ready! Fixed camera view of 3 walls and floor!", fg="#27ae60")
        
        # Debug: Print avatar position
        print(f"Avatar initialized at position: x={self.avatar_state['x']}, y={self.avatar_state['y']}, z={self.avatar_state['z']}")
        print(f"Camera position: x={self.camera_x}, y={self.camera_y}, z={self.camera_z}")
        print(f"Camera rotation: x={self.camera_rotation_x}, y={self.camera_rotation_y}")
        print("3D Avatar system initialized successfully!")
        
        self.start_animation()
        self.draw_3d_scene()
        
    def precompute_lighting(self):
        """Pre-compute lighting values for better performance"""
        # Get lighting intensity based on mode
        lighting_modes = [0.7, 1.0, 0.4]  # Normal, Bright, Dramatic
        base_intensity = lighting_modes[getattr(self, 'lighting_mode', 0)]
        
        # Cache common lighting calculations
        for angle in range(0, 360, 5):
            rad = math.radians(angle)
            normal_x = math.cos(rad)
            normal_z = math.sin(rad)
            
            # Light direction from top-right (room lighting)
            light_x, light_y, light_z = 0.4, -0.8, -0.3
            
            # Dot product for diffuse lighting
            dot = normal_x * light_x + normal_z * light_z
            intensity = max(0.3, min(1.0, base_intensity * (0.4 + dot * 0.6)))
            
            self.light_cache[angle] = intensity
        
    def project_3d_to_2d(self, x, y, z):
        """Simple and reliable 3D to 2D projection"""
        # Simple isometric-style projection
        # Translate relative to camera
        dx = x - self.camera_x
        dy = y - self.camera_y
        dz = z - self.camera_z
        
        # Simple orthographic projection with perspective hint
        # This creates a reliable isometric-like view
        screen_x = self.center_x + dx * 40 - dy * 20
        screen_y = self.center_y - dz * 60 - dy * 10
        
        # Simple depth calculation
        depth = dy + 10  # Simple depth for sorting
        
        return screen_x, screen_y, depth
        
    def draw_optimized_sphere(self, center, radius, color, segments=12):
        """Draw sphere using optimized circle drawing instead of complex mesh"""
        rendered_objects = []
        
        # Draw multiple circles to create 3D sphere illusion
        for i in range(segments):
            # Latitude angle
            lat = (i / segments - 0.5) * math.pi
            circle_y = center[2] + radius * math.sin(lat)
            circle_radius = radius * math.cos(lat) * 0.8
            
            if circle_radius > 0.1:
                # Get lighting intensity based on position
                angle_key = int((i / segments) * 360) // 5 * 5
                intensity = self.light_cache.get(angle_key, 0.7)
                
                # Apply lighting to color
                lit_color = self.apply_lighting(color, intensity)
                
                # Project circle center
                px, py, depth = self.project_3d_to_2d(center[0], center[1], circle_y)
                
                # Draw circle with proper depth and lighting
                screen_radius = max(1, circle_radius * self.scale_3d / depth)
                
                rendered_objects.append({
                    'type': 'circle',
                    'x': px, 'y': py, 'radius': screen_radius,
                    'color': lit_color, 'depth': depth
                })
                
        return rendered_objects
        
    def draw_optimized_cylinder(self, center, radius, height, color, segments=8):
        """Draw cylinder using optimized rectangles"""
        rendered_objects = []
        
        # Draw vertical strips to simulate cylinder
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi
            next_angle = ((i + 1) / segments) * 2 * math.pi
            
            # Calculate positions
            x1 = center[0] + radius * math.cos(angle)
            y1 = center[1] + radius * math.sin(angle)
            x2 = center[0] + radius * math.cos(next_angle)
            y2 = center[1] + radius * math.sin(next_angle)
            
            # Top and bottom points
            z_top = center[2] + height / 2
            z_bottom = center[2] - height / 2
            
            # Project corners
            p1_top = self.project_3d_to_2d(x1, y1, z_top)
            p1_bottom = self.project_3d_to_2d(x1, y1, z_bottom)
            p2_top = self.project_3d_to_2d(x2, y2, z_top)
            p2_bottom = self.project_3d_to_2d(x2, y2, z_bottom)
            
            # Get lighting
            face_angle = int(math.degrees(angle)) // 5 * 5
            intensity = self.light_cache.get(face_angle, 0.7)
            lit_color = self.apply_lighting(color, intensity)
            
            avg_depth = (p1_top[2] + p1_bottom[2] + p2_top[2] + p2_bottom[2]) / 4
            
            rendered_objects.append({
                'type': 'quad',
                'points': [p1_top[:2], p2_top[:2], p2_bottom[:2], p1_bottom[:2]],
                'color': lit_color,
                'depth': avg_depth
            })
            
        return rendered_objects
        
    def apply_lighting(self, color, intensity):
        """Apply lighting intensity to color (optimized)"""
        try:
            # Fast hex color parsing
            r = int(color[1:3], 16)
            g = int(color[3:5], 16) 
            b = int(color[5:7], 16)
            
            # Apply intensity
            r = max(0, min(255, int(r * intensity)))
            g = max(0, min(255, int(g * intensity)))
            b = max(0, min(255, int(b * intensity)))
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color
            
    def draw_3d_scene(self):
        """Draw the complete optimized 3D scene"""
        self.canvas.delete("all")
        
        # Fast gradient background
        gradient_steps = 6
        for i in range(gradient_steps):
            y_start = i * self.canvas_height // gradient_steps
            y_end = (i + 1) * self.canvas_height // gradient_steps
            intensity = int(20 + (i / gradient_steps) * 25)
            color = f"#{intensity:02x}{intensity:02x}{intensity:02x}"
            self.canvas.create_rectangle(0, y_start, self.canvas_width, y_end, 
                                       fill=color, outline="")
        
        # Collect all objects for depth sorting
        all_objects = []
        
        # Room elements
        if self.show_grid:
            all_objects.extend(self.draw_room_floor())
        if self.show_walls:
            all_objects.extend(self.draw_room_walls())
        
        # Avatar if initialized
        if self.is_initialized:
            all_objects.extend(self.draw_optimized_avatar())
            all_objects.extend(self.draw_optimized_pets())
        else:
            # Show a simple placeholder even before initialization
            placeholder_objects = self.draw_optimized_sphere((0, 0, 1), 0.8, '#ff0000', 8)
            all_objects.extend(placeholder_objects)
        
        # Sort by depth and render
        all_objects.sort(key=lambda obj: obj['depth'], reverse=True)
        
        # Fast rendering
        for obj in all_objects:
            self.render_optimized_object(obj)
            
    def draw_room_floor(self):
        """Draw perspective room floor to match /-----\\ wall layout"""
        objects = []
        
        # Extended floor to match the angled walls
        floor_width = 8
        floor_depth = 8
        
        # Floor tiles in perspective room
        for x in range(-floor_width//2, floor_width//2):
            for y in range(-floor_depth//2, floor_depth//2):
                # Project tile corners
                corners = [
                    self.project_3d_to_2d(x, y, 0),
                    self.project_3d_to_2d(x+1, y, 0),
                    self.project_3d_to_2d(x+1, y+1, 0),
                    self.project_3d_to_2d(x, y+1, 0)
                ]
                
                avg_depth = sum(c[2] for c in corners) / 4
                
                # Floor color based on theme
                if self.room_theme == "cozy":
                    color = '#8b7355' if (x + y) % 2 == 0 else '#9d8568'
                elif self.room_theme == "modern":
                    color = '#e8e8e8' if (x + y) % 2 == 0 else '#f0f0f0'
                else:  # classic
                    color = '#d2b48c' if (x + y) % 2 == 0 else '#deb887'
                
                objects.append({
                    'type': 'quad',
                    'points': [c[:2] for c in corners],
                    'color': color,
                    'depth': avg_depth
                })
                
        return objects
        
    def draw_room_walls(self):
        """Draw angled perspective walls like /-----\\ shape"""
        objects = []
        
        # Get wall colors based on theme
        if self.room_theme == "cozy":
            wall_color = '#d4c4a0'
            accent_color = '#b8a082'
        elif self.room_theme == "modern":
            wall_color = '#f5f5f5'
            accent_color = '#e0e0e0'
        else:  # classic
            wall_color = '#f0e68c'
            accent_color = '#daa520'
        
        # Define room layout from bird's eye view: /-----\
        # Key points for the angled room shape
        wall_height = 5
        
        # Room corners (looking from above, Y increases away from camera)
        # Back wall endpoints
        back_left = (-3, 4)
        back_right = (3, 4)
        
        # Front wall endpoints (where angled walls meet)
        # For /-----\ shape: left wall goes from front-left to back-left
        # Right wall goes from back-right to front-right  
        front_left = (-4, 0)   # Left front point
        front_right = (4, 0)   # Right front point
        
        # Debug: Print the coordinates to understand the shape
        if not hasattr(self, '_debug_printed'):
            print(f"Room shape coordinates:")
            print(f"  Back left: {back_left}, Back right: {back_right}")
            print(f"  Front left: {front_left}, Front right: {front_right}")
            print(f"  Left wall: {front_left} -> {back_left} (should create '/')")
            print(f"  Right wall: {back_right} -> {front_right} (should create '\\')")
            self._debug_printed = True
        
        # Back wall (straight horizontal line) - the "-----" part (BRIGHT BLUE for testing)
        back_wall_corners = [
            self.project_3d_to_2d(back_left[0], back_left[1], 0),
            self.project_3d_to_2d(back_right[0], back_right[1], 0),
            self.project_3d_to_2d(back_right[0], back_right[1], wall_height),
            self.project_3d_to_2d(back_left[0], back_left[1], wall_height)
        ]
        
        avg_depth = sum(c[2] for c in back_wall_corners) / 4
        objects.append({
            'type': 'quad',
            'points': [c[:2] for c in back_wall_corners],
            'color': '#0000FF',  # BRIGHT BLUE - you should definitely see this!
            'depth': avg_depth
        })
        
        # Left angled wall - the "/" part (BRIGHT RED for testing)
        # For proper "/" angle: front-left to back-left (left to right, front to back)
        left_wall_corners = [
            self.project_3d_to_2d(front_left[0], front_left[1], 0),      # front-left bottom
            self.project_3d_to_2d(back_left[0], back_left[1], 0),       # back-left bottom
            self.project_3d_to_2d(back_left[0], back_left[1], wall_height),   # back-left top
            self.project_3d_to_2d(front_left[0], front_left[1], wall_height)  # front-left top
        ]
        
        avg_depth = sum(c[2] for c in left_wall_corners) / 4
        objects.append({
            'type': 'quad',
            'points': [c[:2] for c in left_wall_corners],
            'color': '#FF0000',  # BRIGHT RED - you should definitely see this!
            'depth': avg_depth
        })
        
        # Right angled wall - the "\" part (BRIGHT GREEN for testing)
        # Connects back_right to front_right
        right_wall_corners = [
            self.project_3d_to_2d(back_right[0], back_right[1], 0),
            self.project_3d_to_2d(front_right[0], front_right[1], 0),
            self.project_3d_to_2d(front_right[0], front_right[1], wall_height),
            self.project_3d_to_2d(back_right[0], back_right[1], wall_height)
        ]
        
        avg_depth = sum(c[2] for c in right_wall_corners) / 4
        objects.append({
            'type': 'quad',
            'points': [c[:2] for c in right_wall_corners],
            'color': '#00FF00',  # BRIGHT GREEN - you should definitely see this!
            'depth': avg_depth
        })
        
        # Add wall trim/molding for better definition
        trim_height = 0.2
        
        # Back wall trim
        back_trim_corners = [
            self.project_3d_to_2d(back_left[0], back_left[1], 0),
            self.project_3d_to_2d(back_right[0], back_right[1], 0),
            self.project_3d_to_2d(back_right[0], back_right[1], trim_height),
            self.project_3d_to_2d(back_left[0], back_left[1], trim_height)
        ]
        
        avg_depth = sum(c[2] for c in back_trim_corners) / 4
        objects.append({
            'type': 'quad',
            'points': [c[:2] for c in back_trim_corners],
            'color': accent_color,
            'depth': avg_depth - 0.1
        })
        
        # Corner trim where walls meet
        # Left corner trim
        left_corner_corners = [
            self.project_3d_to_2d(back_left[0]-0.1, back_left[1], 0),
            self.project_3d_to_2d(back_left[0]+0.1, back_left[1], 0),
            self.project_3d_to_2d(back_left[0]+0.1, back_left[1], wall_height),
            self.project_3d_to_2d(back_left[0]-0.1, back_left[1], wall_height)
        ]
        
        avg_depth = sum(c[2] for c in left_corner_corners) / 4
        objects.append({
            'type': 'quad',
            'points': [c[:2] for c in left_corner_corners],
            'color': accent_color,
            'depth': avg_depth - 0.05
        })
        
        # Right corner trim  
        right_corner_corners = [
            self.project_3d_to_2d(back_right[0]-0.1, back_right[1], 0),
            self.project_3d_to_2d(back_right[0]+0.1, back_right[1], 0),
            self.project_3d_to_2d(back_right[0]+0.1, back_right[1], wall_height),
            self.project_3d_to_2d(back_right[0]-0.1, back_right[1], wall_height)
        ]
        
        avg_depth = sum(c[2] for c in right_corner_corners) / 4
        objects.append({
            'type': 'quad',
            'points': [c[:2] for c in right_corner_corners],
            'color': accent_color,
            'depth': avg_depth - 0.05
        })
        
        return objects
        
    def draw_optimized_avatar(self):
        """Draw avatar using optimized 3D shapes"""
        objects = []
        
        # Avatar position (centered in room)
        ax = self.avatar_state["x"]
        ay = self.avatar_state["y"] 
        az = self.avatar_state["z"]
        
        # Breathing animation
        breath = 0.03 * math.sin(self.animation_time * 2)
        
        # Ensure avatar is visible (debug positioning)
        if ax == 0 and ay == 0 and az == 0:
            # Center avatar in room if at origin
            ax = 0
            ay = 0
            az = 0
        
        # Colors
        shirt_colors = {
            "t_shirt_blue": '#3498db', "t_shirt_red": '#e74c3c',
            "hoodie_green": '#27ae60', "polo_yellow": '#f1c40f',
            "sweater_purple": '#9b59b6'
        }
        pants_colors = {
            "jeans_blue": '#2980b9', "jeans_black": '#2c3e50',
            "khaki": '#d35400', "joggers_gray": '#7f8c8d',
            "shorts_red": '#c0392b'
        }
        
        shirt_color = shirt_colors.get(self.avatar_state["shirt"], '#3498db')
        pants_color = pants_colors.get(self.avatar_state["pants"], '#2980b9')
        
        # Head (optimized sphere) - Positioned at ground level
        head_center = (ax, ay, 1.8 + breath)  # Much lower position - head at 1.8 units
        objects.extend(self.draw_optimized_sphere(head_center, 0.8, '#f4a460', 16))  # Normal sized head
        
        # Eyes (small spheres)
        eye_left = (ax - 0.3, ay - 0.6, 1.9 + breath)  # Adjusted for new head position
        eye_right = (ax + 0.3, ay - 0.6, 1.9 + breath)
        objects.extend(self.draw_optimized_sphere(eye_left, 0.1, '#000000', 6))
        objects.extend(self.draw_optimized_sphere(eye_right, 0.1, '#000000', 6))
        
        # Eye highlights
        highlight_left = (ax - 0.25, ay - 0.65, 1.95 + breath)
        highlight_right = (ax + 0.25, ay - 0.65, 1.95 + breath)
        objects.extend(self.draw_optimized_sphere(highlight_left, 0.04, '#ffffff', 4))
        objects.extend(self.draw_optimized_sphere(highlight_right, 0.04, '#ffffff', 4))
        
        # Body (optimized cylinder) - Normal size at ground level
        body_center = (ax, ay, 0.8 + breath)  # Body center at 0.8 units
        objects.extend(self.draw_optimized_cylinder(body_center, 0.6, 1.4, shirt_color, 12))
        
        # Arms (cylinders) - Normal size at proper height
        arm_left = (ax - 0.8, ay, 1.0 + breath)
        arm_right = (ax + 0.8, ay, 1.0 + breath)
        objects.extend(self.draw_optimized_cylinder(arm_left, 0.2, 1.0, shirt_color, 8))
        objects.extend(self.draw_optimized_cylinder(arm_right, 0.2, 1.0, shirt_color, 8))
        
        # Hands (small spheres)
        hand_left = (ax - 0.8, ay, 0.4 + breath)
        hand_right = (ax + 0.8, ay, 0.4 + breath)
        objects.extend(self.draw_optimized_sphere(hand_left, 0.15, '#f4a460', 8))
        objects.extend(self.draw_optimized_sphere(hand_right, 0.15, '#f4a460', 8))
        
        # Legs (cylinders) - From body down to ground
        leg_left = (ax - 0.25, ay, 0.3 + breath)
        leg_right = (ax + 0.25, ay, 0.3 + breath)
        objects.extend(self.draw_optimized_cylinder(leg_left, 0.2, 0.6, pants_color, 8))
        objects.extend(self.draw_optimized_cylinder(leg_right, 0.2, 0.6, pants_color, 8))
        
        # Feet (on the ground)
        foot_left = (ax - 0.25, ay + 0.2, 0.1)  # Just above ground level
        foot_right = (ax + 0.25, ay + 0.2, 0.1)
        objects.extend(self.draw_optimized_sphere(foot_left, 0.2, '#2c3e50', 8))
        objects.extend(self.draw_optimized_sphere(foot_right, 0.2, '#2c3e50', 8))
        
        return objects
        
    def draw_optimized_pets(self):
        """Draw pets using optimized shapes"""
        objects = []
        
        pet_positions = [(3, 2, 0.4), (-3, 2, 0.4), (2, -3, 0.4), (-2, -3, 0.4)]
        
        for i, pet_type in enumerate(self.pets[:4]):
            if i >= len(pet_positions):
                break
                
            px, py, base_pz = pet_positions[i]
            pet_bob = 0.1 * math.sin(self.animation_time * 3 + i)
            pz = base_pz + pet_bob
            
            if pet_type == "pet_cat":
                # Cat body and head
                objects.extend(self.draw_optimized_sphere((px, py, pz), 0.3, '#ff9500', 8))
                objects.extend(self.draw_optimized_sphere((px, py - 0.4, pz + 0.25), 0.2, '#ff9500', 6))
            elif pet_type == "pet_dog":
                # Dog body and head  
                objects.extend(self.draw_optimized_sphere((px, py, pz), 0.4, '#8b4513', 8))
                objects.extend(self.draw_optimized_sphere((px, py - 0.5, pz + 0.3), 0.25, '#8b4513', 6))
                
        return objects
        
    def render_optimized_object(self, obj):
        """Render object to canvas with optimized drawing"""
        if obj['type'] == 'circle':
            self.canvas.create_oval(
                obj['x'] - obj['radius'], obj['y'] - obj['radius'],
                obj['x'] + obj['radius'], obj['y'] + obj['radius'],
                fill=obj['color'], outline="", width=0
            )
        elif obj['type'] == 'quad' and len(obj['points']) >= 3:
            flat_points = []
            for point in obj['points']:
                flat_points.extend(point)
            
            self.canvas.create_polygon(flat_points, 
                                     fill=obj['color'], 
                                     outline="", 
                                     width=0,
                                     smooth=False)  # Disable smoothing for speed
    
    # Control methods
    def move_avatar(self, direction):
        """Move avatar"""
        step = 0.6
        
        if direction == "forward":
            self.avatar_state["y"] -= step
        elif direction == "backward":
            self.avatar_state["y"] += step
        elif direction == "left":
            self.avatar_state["x"] -= step
        elif direction == "right":
            self.avatar_state["x"] += step
            
        if self.is_initialized:
            self.draw_3d_scene()
            self.status_label.config(text=f"⚡ Avatar moved {direction} at 60 FPS!", fg="#27ae60")
            self.after(1000, self._reset_status)
    
    def _reset_status(self):
        self.status_label.config(text="⚡ Ultra-Fast 3D Room Ready! Fixed camera view of 3 walls and floor!", fg="#27ae60")
    
    def toggle_walls(self):
        """Toggle room walls visibility"""
        self.show_walls = not self.show_walls
        if self.is_initialized:
            self.draw_3d_scene()
            self.status_label.config(text=f"⚡ Room walls {'shown' if self.show_walls else 'hidden'}!", fg="#27ae60")
            self.after(1000, self._reset_status)
            
    def toggle_grid(self):
        """Toggle floor grid visibility"""
        self.show_grid = not self.show_grid
        if self.is_initialized:
            self.draw_3d_scene()
            self.status_label.config(text=f"⚡ Floor grid {'shown' if self.show_grid else 'hidden'}!", fg="#27ae60")
            self.after(1000, self._reset_status)
            
    def cycle_room_theme(self):
        """Cycle through room themes"""
        themes = ["cozy", "modern", "classic"]
        current = themes.index(self.room_theme)
        self.room_theme = themes[(current + 1) % len(themes)]
        if self.is_initialized:
            self.draw_3d_scene()
            self.status_label.config(text=f"⚡ Room theme: {self.room_theme.title()}!", fg="#27ae60")
            self.after(1000, self._reset_status)
            
    def toggle_lighting(self):
        """Toggle lighting effects"""
        # Cycle through lighting intensities
        if not hasattr(self, 'lighting_mode'):
            self.lighting_mode = 0
        self.lighting_mode = (self.lighting_mode + 1) % 3
        
        # Rebuild lighting cache with new intensity
        self.precompute_lighting()
        
        if self.is_initialized:
            self.draw_3d_scene()
            modes = ["Normal", "Bright", "Dramatic"]
            self.status_label.config(text=f"⚡ Lighting: {modes[self.lighting_mode]}!", fg="#27ae60")
            self.after(1000, self._reset_status)
            
    def cycle_camera_preset(self):
        """Cycle through different camera presets"""
        self.camera_preset = (self.camera_preset + 1) % 4
        
        # Camera presets - positioned to look at back center wall with /-----\ perspective
        presets = {
            0: {"x": 0, "y": -4, "z": 2, "rot_x": -5, "rot_y": 0, "name": "Center Perspective"},
            1: {"x": -2, "y": -3, "z": 2.5, "rot_x": -10, "rot_y": 15, "name": "Left Angle View"},
            2: {"x": 2, "y": -3, "z": 2.5, "rot_x": -10, "rot_y": -15, "name": "Right Angle View"},
            3: {"x": 0, "y": -2, "z": 5, "rot_x": -35, "rot_y": 0, "name": "Overhead View"}
        }
        
        preset = presets[self.camera_preset]
        self.camera_x = preset["x"]
        self.camera_y = preset["y"]
        self.camera_z = preset["z"]
        self.camera_rotation_x = preset["rot_x"]
        self.camera_rotation_y = preset["rot_y"]
        
        if self.is_initialized:
            self.draw_3d_scene()
            self.status_label.config(text=f"⚡ Camera: {preset['name']}!", fg="#27ae60")
            self.after(1500, self._reset_status)
    
    def cycle_shirt(self):
        """Cycle shirt"""
        shirts = ["t_shirt_blue", "t_shirt_red", "hoodie_green", "polo_yellow", "sweater_purple"]
        current = shirts.index(self.avatar_state.get("shirt", "t_shirt_blue"))
        self.avatar_state["shirt"] = shirts[(current + 1) % len(shirts)]
        if self.is_initialized:
            self.draw_3d_scene()
        
    def cycle_pants(self):
        """Cycle pants"""
        pants = ["jeans_blue", "jeans_black", "khaki", "joggers_gray", "shorts_red"]
        current = pants.index(self.avatar_state.get("pants", "jeans_blue"))
        self.avatar_state["pants"] = pants[(current + 1) % len(pants)]
        if self.is_initialized:
            self.draw_3d_scene()
        
    def cycle_hat(self):
        """Cycle hat"""
        # Hat functionality can be added here
        pass
        
    def add_random_pet(self):
        """Add pet"""
        pets = ["pet_cat", "pet_dog"]
        if len(self.pets) < 4:
            import random
            new_pet = random.choice(pets)
            if new_pet not in self.pets:
                self.pets.append(new_pet)
                if self.is_initialized:
                    self.draw_3d_scene()
                self.status_label.config(text=f"🐾 Added {new_pet} at blazing speed!", fg="#27ae60")
                self.after(1000, self._reset_status)
    
    def start_animation(self):
        """Start optimized animation loop"""
        if not self.animation_running:
            self.animation_running = True
            self.animate_loop()
            
    def animate_loop(self):
        """Optimized animation loop targeting 60 FPS"""
        if self.animation_running and self.is_initialized:
            self.animation_time += 0.05
            self.draw_3d_scene()
            # Target 60 FPS = ~16ms per frame
            self.after(16, self.animate_loop)
    
    # No mouse camera controls - fixed room view only


# Test the optimized avatar
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ultra-Fast 3D Avatar")
    root.geometry("900x800")
    root.configure(bg="#2c3e50")
    
    avatar = Optimized3DAvatar(root)
    avatar.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Auto-initialize
    root.after(800, avatar.initialize_3d)
    
    root.mainloop()