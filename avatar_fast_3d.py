"""
Fast 3D Claymation Avatar System - Optimized for Performance
Uses tkinter Canvas with fast 3D projection math for real-time 3D rendering
"""

import tkinter as tk
from tkinter import messagebox
import math
import time

class Fast3DClayAvatar(tk.Frame):
    """Fast 3D Claymation Avatar using optimized canvas 3D projection"""
    
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
        
        # 3D Camera settings - positioned to look at chibi avatar properly
        self.camera_x = 0
        self.camera_y = 8   # Behind the chibi avatar (closer for better view)
        self.camera_z = 2   # Lower to frame the shorter chibi better
        self.camera_rotation_y = 0   # Looking forward
        self.camera_rotation_x = -5  # Looking slightly down at cute chibi
        
        # Animation
        self.animation_time = 0
        self.animation_running = False
        
        # Performance settings
        self.canvas_width = 600
        self.canvas_height = 500
        self.center_x = self.canvas_width // 2
        self.center_y = self.canvas_height // 2
        self.scale_3d = 40  # 3D to 2D scaling factor
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI with fast 3D canvas"""
        # Title with chibi style indicator
        title = tk.Label(self, text="🌟 Chibi 3D Claymation Avatar (Animal Crossing Style)", 
                        font=("Arial", 14, "bold"), fg="#e67e22")
        title.pack(pady=(0, 10))
        
        # Create high-performance canvas
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, 
                               bg="#87ceeb", highlightthickness=2, highlightbackground="#2c3e50")
        self.canvas.pack(pady=(0, 10))
        
        # Bind mouse events for camera control
        self.canvas.bind("<Button-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Button-3>", self.reset_camera)  # Right click to reset
        
        # Controls
        self.setup_controls()
        
        # Draw initial scene
        self.draw_3d_scene()
        
    def setup_controls(self):
        """Set up control interface"""
        controls_frame = tk.Frame(self)
        controls_frame.pack(fill="x", pady=(0, 10))
        
        # Initialize button
        self.init_btn = tk.Button(controls_frame, 
                                 text="🌟 Initialize Chibi 3D Avatar",
                                 command=self.initialize_3d, 
                                 bg="#e67e22", fg="white", font=("Arial", 11, "bold"))
        self.init_btn.pack(pady=5)
        
        # Movement controls
        move_frame = tk.LabelFrame(controls_frame, text="Avatar Movement (3D)")
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
        
        # Camera controls
        camera_frame = tk.LabelFrame(controls_frame, text="Camera (Drag mouse)")
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
        
        # Quick customization
        custom_frame = tk.LabelFrame(controls_frame, text="Quick Customize")
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
                                    text="Ready for chibi 3D adventure! Just like Animal Crossing GameCube!",
                                    fg="#2c3e50")
        self.status_label.pack(pady=5)
        
    def initialize_3d(self):
        """Initialize the fast 3D avatar system"""
        self.init_btn.config(text="Initializing...", state="disabled", bg="#95a5a6")
        self.status_label.config(text="Setting up fast 3D claymation world...", fg="#f39c12")
        self.update()
        
        # Quick initialization
        self.after(500, self._complete_3d_initialization)
        
    def _complete_3d_initialization(self):
        """Complete 3D initialization"""
        self.is_initialized = True
        
        self.init_btn.config(text="🌟 Chibi 3D Avatar Active!", bg="#27ae60", state="disabled")
        self.status_label.config(text="🌟 Adorable Chibi Avatar Ready! Animal Crossing vibes!", fg="#27ae60")
        
        # Start smooth animation
        self.start_animation()
        self.draw_3d_scene()
        
    def project_3d_to_2d(self, x, y, z):
        """Fast 3D to 2D projection with corrected orientation"""
        # Translate to camera position first
        x_cam = x - self.camera_x
        y_cam = y - self.camera_y  
        z_cam = z - self.camera_z
        
        # Apply camera rotations (Y rotation first, then X)
        cos_y = math.cos(math.radians(self.camera_rotation_y))
        sin_y = math.sin(math.radians(self.camera_rotation_y))
        cos_x = math.cos(math.radians(self.camera_rotation_x))
        sin_x = math.sin(math.radians(self.camera_rotation_x))
        
        # Rotate around Y axis (left/right camera rotation)
        x_rot1 = x_cam * cos_y + y_cam * sin_y
        y_rot1 = -x_cam * sin_y + y_cam * cos_y
        z_rot1 = z_cam
        
        # Rotate around X axis (up/down camera rotation)
        x_final = x_rot1
        y_final = y_rot1 * cos_x - z_rot1 * sin_x
        z_final = y_rot1 * sin_x + z_rot1 * cos_x
        
        # Prevent objects behind camera
        if z_final <= 0.1:
            z_final = 0.1
            
        # Proper perspective projection
        focal_length = 500  # Virtual camera focal length
        screen_x = self.center_x + (x_final * focal_length / z_final)
        screen_y = self.center_y - (z_rot1 * focal_length / z_final)  # Use original z for height
        
        return screen_x, screen_y, z_final
        
    def draw_3d_scene(self):
        """Draw the complete 3D scene with optimized rendering"""
        # Clear canvas efficiently
        self.canvas.delete("all")
        
        # Sky gradient background
        for i in range(0, self.canvas_height, 10):
            intensity = int(135 + (i / self.canvas_height) * 120)
            color = f"#{intensity:02x}{min(255, intensity + 20):02x}{255:02x}"
            self.canvas.create_rectangle(0, i, self.canvas_width, i + 10, 
                                       fill=color, outline="")
        
        # Draw 3D elements in depth order
        all_objects = []
        
        # Add floor
        floor_points = self.get_3d_floor()
        all_objects.extend(floor_points)
        
        # Add avatar if initialized
        if self.is_initialized:
            avatar_objects = self.get_3d_avatar()
            all_objects.extend(avatar_objects)
            
            # Add pets
            pet_objects = self.get_3d_pets()
            all_objects.extend(pet_objects)
        
        # Sort by depth (z-coordinate) for proper rendering
        all_objects.sort(key=lambda obj: obj['depth'], reverse=True)
        
        # Render all objects
        for obj in all_objects:
            self.render_3d_object(obj)
            
    def get_3d_floor(self):
        """Generate 3D floor grid objects - properly oriented"""
        objects = []
        
        # Create floor at ground level (z=0)
        for x in range(-8, 9, 2):
            for y in range(-8, 9, 2):
                # Floor tile corners (flat on ground, z=0)
                corners = [
                    (x, y, 0), (x+2, y, 0), (x+2, y+2, 0), (x, y+2, 0)
                ]
                
                projected_corners = []
                depths = []
                valid_corners = True
                
                for corner in corners:
                    px, py, depth = self.project_3d_to_2d(*corner)
                    projected_corners.append((px, py))
                    depths.append(depth)
                    # Skip tiles that are behind camera or too far
                    if depth <= 0.1 or depth > 50:
                        valid_corners = False
                        break
                
                if valid_corners and len(projected_corners) >= 3:
                    avg_depth = sum(depths) / len(depths)
                    
                    objects.append({
                        'type': 'polygon',
                        'points': projected_corners,
                        'fill': '#d2b48c' if (x + y) % 4 == 0 else '#c9a876',
                        'outline': '#b8965f',
                        'depth': avg_depth
                    })
                
        return objects
        
    def get_3d_avatar(self):
        """Generate 3D avatar objects"""
        objects = []
        
        # Avatar position with breathing animation - avatar stands upright on floor
        ax = self.avatar_state["x"]
        ay = self.avatar_state["y"]
        az = self.avatar_state["z"]
        
        breath = 0.05 * math.sin(self.animation_time * 2)
        base_height = 0  # Avatar feet on the floor (z=0)
        
        # Get colors
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
        
        # Chibi Avatar parts - Animal Crossing GameCube style with big head and small body
        
        # Big round head (oversized like Animal Crossing chibi style)
        head_center = (ax, ay, base_height + 3.2 + breath)
        objects.extend(self.create_3d_sphere(head_center, 1.2, '#f4a460'))  # Much bigger head
        
        # Large cute eyes (Animal Crossing style)
        eye_left = (ax - 0.4, ay - 1.0, base_height + 3.4 + breath)
        eye_right = (ax + 0.4, ay - 1.0, base_height + 3.4 + breath)
        objects.extend(self.create_3d_sphere(eye_left, 0.25, '#000000'))  # Bigger eyes
        objects.extend(self.create_3d_sphere(eye_right, 0.25, '#000000'))
        
        # Eye highlights for that chibi sparkle
        eye_highlight_left = (ax - 0.35, ay - 1.1, base_height + 3.5 + breath)
        eye_highlight_right = (ax + 0.35, ay - 1.1, base_height + 3.5 + breath)
        objects.extend(self.create_3d_sphere(eye_highlight_left, 0.08, '#ffffff'))
        objects.extend(self.create_3d_sphere(eye_highlight_right, 0.08, '#ffffff'))
        
        # Tiny cute nose
        nose_center = (ax, ay - 1.0, base_height + 3.1 + breath)
        objects.extend(self.create_3d_sphere(nose_center, 0.06, '#e19950'))
        
        # Small chibi body (much smaller proportionally)
        body_center = (ax, ay, base_height + 1.8 + breath)
        objects.extend(self.create_3d_box(body_center, (1.0, 0.8, 1.6), shirt_color))  # Smaller body
        
        # Tiny stubby arms (Animal Crossing style)
        arm_left = (ax - 0.8, ay, base_height + 2.1 + breath)
        arm_right = (ax + 0.8, ay, base_height + 2.1 + breath)
        objects.extend(self.create_3d_box(arm_left, (0.4, 0.4, 1.0), shirt_color))  # Stubby arms
        objects.extend(self.create_3d_box(arm_right, (0.4, 0.4, 1.0), shirt_color))
        
        # Cute little hands
        hand_left = (ax - 1.1, ay, base_height + 2.0 + breath)
        hand_right = (ax + 1.1, ay, base_height + 2.0 + breath)
        objects.extend(self.create_3d_sphere(hand_left, 0.2, '#f4a460'))
        objects.extend(self.create_3d_sphere(hand_right, 0.2, '#f4a460'))
        
        # Short chibi legs
        leg_left = (ax - 0.3, ay, base_height + 0.8 + breath)
        leg_right = (ax + 0.3, ay, base_height + 0.8 + breath)
        objects.extend(self.create_3d_box(leg_left, (0.5, 0.5, 1.5), pants_color))  # Shorter legs
        objects.extend(self.create_3d_box(leg_right, (0.5, 0.5, 1.5), pants_color))
        
        # Cute rounded feet (on the ground)
        foot_left = (ax - 0.3, ay + 0.2, base_height + 0.15)
        foot_right = (ax + 0.3, ay + 0.2, base_height + 0.15)
        objects.extend(self.create_3d_sphere(foot_left, 0.3, '#2c3e50'))  # Round feet
        objects.extend(self.create_3d_sphere(foot_right, 0.3, '#2c3e50'))
        
        # Hat (on top of big chibi head)
        if self.avatar_state.get("hat", "none") != "none":
            hat_objects = self.create_3d_hat((ax, ay, base_height + 4.6 + breath))  # Adjusted for bigger head
            objects.extend(hat_objects)
        
        return objects
        
    def get_3d_pets(self):
        """Generate 3D pet objects - positioned on floor around avatar"""
        objects = []
        
        pet_positions = [(3, 2, 0.5), (-3, 2, 0.5), (2, -3, 0.5), (-2, -3, 0.5)]
        
        for i, pet_type in enumerate(self.pets[:4]):
            px, py, base_pz = pet_positions[i]
            
            # Pet animation (gentle bobbing on the ground)
            pet_bob = 0.1 * math.sin(self.animation_time * 3 + i)
            pz = base_pz + pet_bob  # Pets stay near ground level
            
            if pet_type == "pet_cat":
                objects.extend(self.create_3d_cat((px, py, pz)))
            elif pet_type == "pet_dog":
                objects.extend(self.create_3d_dog((px, py, pz)))
            elif pet_type == "pet_bird":
                objects.extend(self.create_3d_bird((px, py, pz)))
            elif pet_type == "pet_dragon":
                objects.extend(self.create_3d_dragon((px, py, pz)))
                
        return objects
        
    def create_3d_sphere(self, center, radius, color):
        """Create 3D sphere using optimized circles"""
        objects = []
        
        # Multiple circles at different heights for sphere effect
        for i in range(5):
            height_offset = (i - 2) * radius * 0.4
            circle_radius = radius * math.sqrt(1 - (height_offset/radius)**2) if abs(height_offset) < radius else 0
            
            if circle_radius > 0.1:
                circle_center = (center[0], center[1], center[2] + height_offset)
                px, py, depth = self.project_3d_to_2d(*circle_center)
                
                objects.append({
                    'type': 'circle',
                    'center': (px, py),
                    'radius': circle_radius * self.scale_3d / (1 + depth * 0.1),
                    'fill': color,
                    'outline': self.darken_color(color),
                    'depth': depth
                })
                
        return objects
        
    def create_3d_box(self, center, dimensions, color):
        """Create optimized 3D box"""
        objects = []
        dx, dy, dz = [d/2 for d in dimensions]
        
        # Box faces (front, back, top, bottom, left, right)
        faces = [
            # Front face
            [(center[0]-dx, center[1]-dy, center[2]-dz), (center[0]+dx, center[1]-dy, center[2]-dz),
             (center[0]+dx, center[1]-dy, center[2]+dz), (center[0]-dx, center[1]-dy, center[2]+dz)],
            # Back face  
            [(center[0]-dx, center[1]+dy, center[2]-dz), (center[0]-dx, center[1]+dy, center[2]+dz),
             (center[0]+dx, center[1]+dy, center[2]+dz), (center[0]+dx, center[1]+dy, center[2]-dz)],
            # Top face
            [(center[0]-dx, center[1]-dy, center[2]+dz), (center[0]+dx, center[1]-dy, center[2]+dz),
             (center[0]+dx, center[1]+dy, center[2]+dz), (center[0]-dx, center[1]+dy, center[2]+dz)],
        ]
        
        for i, face in enumerate(faces):
            projected_face = []
            depths = []
            
            for vertex in face:
                px, py, depth = self.project_3d_to_2d(*vertex)
                projected_face.append((px, py))
                depths.append(depth)
            
            avg_depth = sum(depths) / len(depths)
            
            # Color variation for different faces
            face_color = color
            if i == 1:  # Back face darker
                face_color = self.darken_color(color)
            elif i == 2:  # Top face lighter
                face_color = self.lighten_color(color)
            
            objects.append({
                'type': 'polygon',
                'points': projected_face,
                'fill': face_color,
                'outline': self.darken_color(face_color),
                'depth': avg_depth
            })
            
        return objects
        
    def create_3d_hat(self, center):
        """Create 3D hat - sized for chibi head"""
        objects = []
        hat_type = self.avatar_state.get("hat", "none")
        
        if hat_type == "baseball_cap":
            # Cute oversized baseball cap
            objects.extend(self.create_3d_sphere(center, 0.9, '#e67e22'))  # Bigger for chibi head
            # Visor
            visor_center = (center[0], center[1] - 0.8, center[2] - 0.2)
            objects.extend(self.create_3d_box(visor_center, (1.4, 0.4, 0.1), '#d35400'))
        elif hat_type == "wizard_hat":
            # Adorable wizard hat
            objects.extend(self.create_3d_box(center, (1.0, 1.0, 1.8), '#8e44ad'))
            # Wizard hat tip
            tip_center = (center[0], center[1], center[2] + 1.2)
            objects.extend(self.create_3d_sphere(tip_center, 0.2, '#8e44ad'))
        elif hat_type == "crown":
            # Royal chibi crown
            objects.extend(self.create_3d_box((center[0], center[1], center[2] + 0.3), (1.2, 1.2, 0.6), '#f1c40f'))
            # Crown jewels
            for i, pos in enumerate([(-0.4, 0), (0, 0), (0.4, 0)]):
                jewel_center = (center[0] + pos[0], center[1] - 0.8, center[2] + 0.7)
                colors = ['#e74c3c', '#3498db', '#e74c3c']
                objects.extend(self.create_3d_sphere(jewel_center, 0.1, colors[i]))
        elif hat_type == "beanie":
            # Cute beanie
            objects.extend(self.create_3d_sphere(center, 0.85, '#95a5a6'))
            
        return objects
        
    def create_3d_cat(self, center):
        """Create 3D chibi cat - Animal Crossing style"""
        objects = []
        # Round chibi cat body
        objects.extend(self.create_3d_sphere((center[0], center[1], center[2] + 0.4), 0.5, '#ff9500'))
        # Big round head
        objects.extend(self.create_3d_sphere((center[0], center[1] - 0.3, center[2] + 0.8), 0.4, '#ff9500'))
        # Cute triangle ears
        objects.extend(self.create_3d_box((center[0] - 0.2, center[1] - 0.4, center[2] + 1.1), (0.15, 0.1, 0.3), '#ff9500'))
        objects.extend(self.create_3d_box((center[0] + 0.2, center[1] - 0.4, center[2] + 1.1), (0.15, 0.1, 0.3), '#ff9500'))
        # Tiny eyes
        objects.extend(self.create_3d_sphere((center[0] - 0.15, center[1] - 0.5, center[2] + 0.85), 0.06, '#000000'))
        objects.extend(self.create_3d_sphere((center[0] + 0.15, center[1] - 0.5, center[2] + 0.85), 0.06, '#000000'))
        return objects
        
    def create_3d_dog(self, center):
        """Create 3D chibi dog - Animal Crossing style"""
        objects = []
        # Round chibi dog body (slightly bigger than cat)
        objects.extend(self.create_3d_sphere((center[0], center[1], center[2] + 0.5), 0.6, '#8b4513'))
        # Big round head
        objects.extend(self.create_3d_sphere((center[0], center[1] - 0.4, center[2] + 0.9), 0.45, '#8b4513'))
        # Floppy ears
        objects.extend(self.create_3d_sphere((center[0] - 0.3, center[1] - 0.3, center[2] + 1.0), 0.2, '#654321'))
        objects.extend(self.create_3d_sphere((center[0] + 0.3, center[1] - 0.3, center[2] + 1.0), 0.2, '#654321'))
        # Tiny eyes
        objects.extend(self.create_3d_sphere((center[0] - 0.15, center[1] - 0.6, center[2] + 0.95), 0.06, '#000000'))
        objects.extend(self.create_3d_sphere((center[0] + 0.15, center[1] - 0.6, center[2] + 0.95), 0.06, '#000000'))
        # Cute nose
        objects.extend(self.create_3d_sphere((center[0], center[1] - 0.65, center[2] + 0.9), 0.04, '#000000'))
        return objects
        
    def create_3d_bird(self, center):
        """Create 3D chibi bird - Animal Crossing style"""
        objects = []
        # Round chibi bird body
        objects.extend(self.create_3d_sphere((center[0], center[1], center[2] + 1.2), 0.35, '#3498db'))
        # Tiny wings
        objects.extend(self.create_3d_sphere((center[0] - 0.3, center[1], center[2] + 1.2), 0.15, '#2980b9'))
        objects.extend(self.create_3d_sphere((center[0] + 0.3, center[1], center[2] + 1.2), 0.15, '#2980b9'))
        # Tiny beak
        objects.extend(self.create_3d_box((center[0], center[1] - 0.4, center[2] + 1.2), (0.1, 0.2, 0.1), '#f39c12'))
        # Tiny eyes
        objects.extend(self.create_3d_sphere((center[0] - 0.1, center[1] - 0.25, center[2] + 1.3), 0.05, '#000000'))
        objects.extend(self.create_3d_sphere((center[0] + 0.1, center[1] - 0.25, center[2] + 1.3), 0.05, '#000000'))
        return objects
        
    def create_3d_dragon(self, center):
        """Create 3D chibi dragon - Animal Crossing style"""
        objects = []
        # Round chibi dragon body
        objects.extend(self.create_3d_sphere((center[0], center[1], center[2] + 0.6), 0.7, '#27ae60'))
        # Big round head
        objects.extend(self.create_3d_sphere((center[0], center[1] - 0.5, center[2] + 1.0), 0.5, '#27ae60'))
        # Cute little wings
        objects.extend(self.create_3d_sphere((center[0] - 0.6, center[1], center[2] + 1.0), 0.3, '#229954'))
        objects.extend(self.create_3d_sphere((center[0] + 0.6, center[1], center[2] + 1.0), 0.3, '#229954'))
        # Dragon eyes (slightly bigger for majesty)
        objects.extend(self.create_3d_sphere((center[0] - 0.2, center[1] - 0.7, center[2] + 1.1), 0.08, '#e74c3c'))
        objects.extend(self.create_3d_sphere((center[0] + 0.2, center[1] - 0.7, center[2] + 1.1), 0.08, '#e74c3c'))
        # Tiny horns
        objects.extend(self.create_3d_box((center[0] - 0.15, center[1] - 0.4, center[2] + 1.4), (0.1, 0.1, 0.3), '#f39c12'))
        objects.extend(self.create_3d_box((center[0] + 0.15, center[1] - 0.4, center[2] + 1.4), (0.1, 0.1, 0.3), '#f39c12'))
        return objects
        
    def render_3d_object(self, obj):
        """Render a 3D object on the canvas"""
        if obj['type'] == 'polygon':
            if len(obj['points']) >= 3:
                flat_points = [coord for point in obj['points'] for coord in point]
                self.canvas.create_polygon(flat_points, fill=obj['fill'], outline=obj['outline'])
        elif obj['type'] == 'circle':
            x, y = obj['center']
            r = obj['radius']
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=obj['fill'], outline=obj['outline'])
            
    def lighten_color(self, color):
        """Lighten a color"""
        try:
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            rgb = tuple(min(255, int(c * 1.3)) for c in rgb)
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        except:
            return "#ffffff"
            
    def darken_color(self, color):
        """Darken a color"""
        try:
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            rgb = tuple(max(0, int(c * 0.7)) for c in rgb)
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        except:
            return "#000000"
    
    # Control methods
    def move_avatar(self, direction):
        """Move avatar in 3D space - intuitive movement"""
        step = 0.8
        
        if direction == "forward":
            self.avatar_state["y"] -= step  # Move away from camera
        elif direction == "backward":
            self.avatar_state["y"] += step  # Move toward camera
        elif direction == "left":
            self.avatar_state["x"] -= step  # Move left
        elif direction == "right":
            self.avatar_state["x"] += step  # Move right
        elif direction == "up":
            self.avatar_state["z"] += step  # Jump up
        elif direction == "down":
            self.avatar_state["z"] = max(0, self.avatar_state["z"] - step)  # Come down (but don't go below ground)
            
        self.draw_3d_scene()
        
        if self.is_initialized:
            self.status_label.config(text=f"⚡ Avatar moved {direction} in fast 3D!", fg="#27ae60")
            self.after(1000, lambda: self.status_label.config(
                text="⚡ Fast 3D Avatar Ready! Smooth real-time rendering!", fg="#27ae60"))
    
    def rotate_camera(self, direction):
        """Rotate camera"""
        angle_step = 15
        
        if direction == "left":
            self.camera_rotation_y -= angle_step
        elif direction == "right":
            self.camera_rotation_y += angle_step
        elif direction == "up":
            self.camera_rotation_x = min(80, self.camera_rotation_x + angle_step)
        elif direction == "down":
            self.camera_rotation_x = max(-80, self.camera_rotation_x - angle_step)
        elif direction == "spin":
            self.camera_rotation_y += 45
            
        self.draw_3d_scene()
        
    def reset_camera(self, event=None):
        """Reset camera to default position - good view of chibi avatar"""
        self.camera_rotation_y = 0    # Looking straight
        self.camera_rotation_x = -5   # Looking slightly down at chibi
        self.camera_x = 0             # Centered on chibi avatar
        self.camera_y = 8             # Behind the chibi avatar
        self.camera_z = 2             # Lower for better chibi framing
        self.draw_3d_scene()
    
    def cycle_shirt(self):
        """Cycle through shirt options"""
        shirts = ["t_shirt_blue", "t_shirt_red", "hoodie_green", "polo_yellow", "sweater_purple"]
        current_idx = shirts.index(self.avatar_state.get("shirt", "t_shirt_blue"))
        next_idx = (current_idx + 1) % len(shirts)
        self.avatar_state["shirt"] = shirts[next_idx]
        self.draw_3d_scene()
        
    def cycle_pants(self):
        """Cycle through pants options"""
        pants = ["jeans_blue", "jeans_black", "khaki", "joggers_gray", "shorts_red"]
        current_idx = pants.index(self.avatar_state.get("pants", "jeans_blue"))
        next_idx = (current_idx + 1) % len(pants)
        self.avatar_state["pants"] = pants[next_idx]
        self.draw_3d_scene()
        
    def cycle_hat(self):
        """Cycle through hat options"""
        hats = ["none", "baseball_cap", "wizard_hat", "crown"]
        current_idx = hats.index(self.avatar_state.get("hat", "none"))
        next_idx = (current_idx + 1) % len(hats)
        self.avatar_state["hat"] = hats[next_idx]
        self.draw_3d_scene()
        
    def add_random_pet(self):
        """Add a random pet"""
        pets = ["pet_cat", "pet_dog", "pet_bird", "pet_dragon"]
        if len(self.pets) < 4:
            import random
            new_pet = random.choice(pets)
            if new_pet not in self.pets:
                self.pets.append(new_pet)
                self.draw_3d_scene()
                self.status_label.config(text=f"🐾 Added {new_pet} in fast 3D!", fg="#27ae60")
                self.after(1000, lambda: self.status_label.config(
                    text="⚡ Fast 3D Avatar Ready! Smooth real-time rendering!", fg="#27ae60"))
    
    def update_avatar_state(self, state_dict):
        """Update avatar appearance"""
        self.avatar_state.update(state_dict)
        self.draw_3d_scene()
        
    def add_pet(self, pet_type):
        """Add a pet to the scene"""
        if pet_type not in self.pets and len(self.pets) < 4:
            self.pets.append(pet_type)
            self.draw_3d_scene()
            
    def remove_pet(self, pet_type):
        """Remove a pet from the scene"""
        if pet_type in self.pets:
            self.pets.remove(pet_type)
            self.draw_3d_scene()
    
    # Animation system
    def start_animation(self):
        """Start smooth animation loop"""
        if not self.animation_running:
            self.animation_running = True
            self.animate_loop()
            
    def animate_loop(self):
        """Fast animation loop"""
        if self.animation_running and self.is_initialized:
            self.animation_time += 0.1
            self.draw_3d_scene()
            self.after(50, self.animate_loop)  # 20 FPS for smooth animation
    
    # Mouse interaction
    def on_mouse_press(self, event):
        """Handle mouse press"""
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
        
    def on_mouse_drag(self, event):
        """Handle mouse drag for camera rotation"""
        if hasattr(self, 'last_mouse_x'):
            dx = event.x - self.last_mouse_x
            dy = event.y - self.last_mouse_y
            
            self.camera_rotation_y += dx * 0.5
            self.camera_rotation_x += dy * 0.5
            self.camera_rotation_x = max(-80, min(80, self.camera_rotation_x))
            
            self.last_mouse_x = event.x
            self.last_mouse_y = event.y
            
            self.draw_3d_scene()
            
    def on_mouse_wheel(self, event):
        """Handle mouse wheel for zooming - move camera closer/further"""
        zoom_step = 1.5
        if event.delta > 0:
            # Zoom in - move camera closer
            self.camera_y -= zoom_step
        else:
            # Zoom out - move camera further
            self.camera_y += zoom_step
            
        # Limit camera distance
        self.camera_y = max(5, min(25, self.camera_y))
        self.draw_3d_scene()


# Test the fast 3D avatar
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Fast 3D Claymation Avatar")
    root.geometry("800x700")
    
    avatar = Fast3DClayAvatar(root)
    avatar.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Auto-initialize
    root.after(1000, avatar.initialize_3d)
    
    root.mainloop()