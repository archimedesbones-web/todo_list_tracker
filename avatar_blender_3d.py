"""
Blender-Style 3D Avatar System - Mesh-Based 3D Rendering
Creates proper 3D meshes with smooth surfaces like Blender models
"""

import tkinter as tk
from tkinter import messagebox
import math
import time
import numpy as np

class BlenderStyle3DAvatar(tk.Frame):
    """Blender-style 3D Avatar with proper mesh generation and smooth surfaces"""
    
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
        
        # 3D Camera settings for Blender-style view
        self.camera_x = 0
        self.camera_y = 8
        self.camera_z = 3
        self.camera_rotation_y = 0
        self.camera_rotation_x = -15
        
        # Animation and lighting
        self.animation_time = 0
        self.animation_running = False
        self.light_angle = 0
        
        # Mesh resolution settings
        self.sphere_resolution = 24  # Higher resolution for smooth spheres
        self.mesh_detail = 16        # Mesh subdivision level
        
        # Canvas settings
        self.canvas_width = 700
        self.canvas_height = 600
        self.center_x = self.canvas_width // 2
        self.center_y = self.canvas_height // 2
        self.scale_3d = 60
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI with Blender-style 3D canvas"""
        # Title
        title = tk.Label(self, text="🎯 Blender-Style 3D Avatar", 
                        font=("Arial", 16, "bold"), fg="#2980b9")
        title.pack(pady=(0, 10))
        
        subtitle = tk.Label(self, text="Mesh-based 3D rendering with smooth surfaces", 
                           font=("Arial", 10), fg="#7f8c8d")
        subtitle.pack(pady=(0, 15))
        
        # Create high-resolution canvas with better background
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, 
                               bg="#1e1e1e", highlightthickness=2, highlightbackground="#34495e")
        self.canvas.pack(pady=(0, 15))
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Button-3>", self.reset_camera)
        
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
                                 text="🎯 Initialize Blender-Style Avatar",
                                 command=self.initialize_3d, 
                                 bg="#2980b9", fg="white", font=("Arial", 12, "bold"))
        self.init_btn.pack(pady=8)
        
        # Control panels
        controls_row = tk.Frame(controls_frame)
        controls_row.pack(fill="x", pady=5)
        
        # Movement controls
        move_frame = tk.LabelFrame(controls_row, text="3D Movement", font=("Arial", 10, "bold"))
        move_frame.pack(side="left", padx=10, pady=5)
        
        tk.Button(move_frame, text="↑", width=4, height=2, font=("Arial", 12, "bold"),
                 command=lambda: self.move_avatar("forward")).grid(row=0, column=1, padx=3, pady=2)
        tk.Button(move_frame, text="←", width=4, height=2, font=("Arial", 12, "bold"),
                 command=lambda: self.move_avatar("left")).grid(row=1, column=0, padx=3, pady=2)
        tk.Button(move_frame, text="↓", width=4, height=2, font=("Arial", 12, "bold"),
                 command=lambda: self.move_avatar("backward")).grid(row=1, column=1, padx=3, pady=2)
        tk.Button(move_frame, text="→", width=4, height=2, font=("Arial", 12, "bold"),
                 command=lambda: self.move_avatar("right")).grid(row=1, column=2, padx=3, pady=2)
        
        tk.Button(move_frame, text="⬆", width=4, height=1, font=("Arial", 10, "bold"),
                 command=lambda: self.move_avatar("up")).grid(row=0, column=3, padx=3, pady=2)
        tk.Button(move_frame, text="⬇", width=4, height=1, font=("Arial", 10, "bold"),
                 command=lambda: self.move_avatar("down")).grid(row=1, column=3, padx=3, pady=2)
        
        # Camera controls
        camera_frame = tk.LabelFrame(controls_row, text="Camera & Lighting", font=("Arial", 10, "bold"))
        camera_frame.pack(side="left", padx=10, pady=5)
        
        tk.Button(camera_frame, text="🔄⬅", width=5,
                 command=lambda: self.rotate_camera("left")).grid(row=0, column=0, padx=2)
        tk.Button(camera_frame, text="⬆", width=5,
                 command=lambda: self.rotate_camera("up")).grid(row=0, column=1, padx=2)
        tk.Button(camera_frame, text="🔄➡", width=5,
                 command=lambda: self.rotate_camera("right")).grid(row=0, column=2, padx=2)
        tk.Button(camera_frame, text="🎯", width=5,
                 command=self.reset_camera).grid(row=1, column=0, padx=2)
        tk.Button(camera_frame, text="⬇", width=5,
                 command=lambda: self.rotate_camera("down")).grid(row=1, column=1, padx=2)
        tk.Button(camera_frame, text="💡", width=5,
                 command=self.toggle_lighting).grid(row=1, column=2, padx=2)
        
        # Mesh quality controls
        quality_frame = tk.LabelFrame(controls_row, text="Mesh Quality", font=("Arial", 10, "bold"))
        quality_frame.pack(side="left", padx=10, pady=5)
        
        tk.Button(quality_frame, text="🔺", width=5, 
                 command=lambda: self.adjust_quality("up")).grid(row=0, column=0, padx=2)
        tk.Label(quality_frame, text="Detail", font=("Arial", 9)).grid(row=0, column=1, padx=2)
        tk.Button(quality_frame, text="🔻", width=5,
                 command=lambda: self.adjust_quality("down")).grid(row=0, column=2, padx=2)
        
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
                                    text="Ready for Blender-style 3D rendering! Drag mouse to orbit camera",
                                    fg="#2c3e50", font=("Arial", 10))
        self.status_label.pack(pady=8)
        
        # Quality indicator
        self.quality_label = tk.Label(controls_frame,
                                     text=f"Mesh Resolution: {self.sphere_resolution} | Detail Level: {self.mesh_detail}",
                                     fg="#7f8c8d", font=("Arial", 9))
        self.quality_label.pack()
        
    def initialize_3d(self):
        """Initialize the Blender-style 3D avatar system"""
        self.init_btn.config(text="Initializing Blender-style 3D...", state="disabled", bg="#95a5a6")
        self.status_label.config(text="Generating high-quality 3D meshes...", fg="#f39c12")
        self.update()
        
        self.after(800, self._complete_3d_initialization)
        
    def _complete_3d_initialization(self):
        """Complete 3D initialization"""
        self.is_initialized = True
        
        self.init_btn.config(text="🎯 Blender-Style Avatar Active!", bg="#27ae60", state="disabled")
        self.status_label.config(text="🎯 High-Quality 3D Avatar Ready! Professional mesh rendering!", fg="#27ae60")
        
        self.start_animation()
        self.draw_3d_scene()
        
    def project_3d_to_2d(self, x, y, z):
        """Enhanced 3D to 2D projection with improved perspective"""
        # Camera transformations
        x_cam = x - self.camera_x
        y_cam = y - self.camera_y  
        z_cam = z - self.camera_z
        
        # Rotation matrices
        cos_y = math.cos(math.radians(self.camera_rotation_y))
        sin_y = math.sin(math.radians(self.camera_rotation_y))
        cos_x = math.cos(math.radians(self.camera_rotation_x))
        sin_x = math.sin(math.radians(self.camera_rotation_x))
        
        # Y rotation
        x_rot1 = x_cam * cos_y + y_cam * sin_y
        y_rot1 = -x_cam * sin_y + y_cam * cos_y
        z_rot1 = z_cam
        
        # X rotation
        x_final = x_rot1
        y_final = y_rot1 * cos_x - z_rot1 * sin_x
        z_final = y_rot1 * sin_x + z_rot1 * cos_x
        
        # Enhanced perspective with realistic focal length
        if z_final <= 0.1:
            z_final = 0.1
            
        focal_length = 800
        screen_x = self.center_x + (x_final * focal_length / z_final)
        screen_y = self.center_y - (z_rot1 * focal_length / z_final)
        
        return screen_x, screen_y, z_final
        
    def generate_sphere_mesh(self, center, radius, resolution=None):
        """Generate high-quality sphere mesh with proper vertices and faces"""
        if resolution is None:
            resolution = self.sphere_resolution
            
        vertices = []
        faces = []
        
        # Generate sphere vertices using UV sphere method (like Blender)
        for i in range(resolution + 1):
            lat = math.pi * i / resolution - math.pi / 2  # -π/2 to π/2
            for j in range(resolution * 2 + 1):
                lon = 2 * math.pi * j / (resolution * 2)  # 0 to 2π
                
                x = center[0] + radius * math.cos(lat) * math.cos(lon)
                y = center[1] + radius * math.cos(lat) * math.sin(lon) 
                z = center[2] + radius * math.sin(lat)
                
                vertices.append((x, y, z))
        
        # Generate faces (quads converted to triangles)
        for i in range(resolution):
            for j in range(resolution * 2):
                # Current quad vertices
                v0 = i * (resolution * 2 + 1) + j
                v1 = v0 + 1
                v2 = (i + 1) * (resolution * 2 + 1) + j
                v3 = v2 + 1
                
                # Skip if at the edge
                if j == resolution * 2:
                    continue
                    
                # Create two triangles from quad
                if i > 0:  # Skip top cap
                    faces.append([v0, v2, v1])
                if i < resolution - 1:  # Skip bottom cap
                    faces.append([v1, v2, v3])
        
        return vertices, faces
        
    def generate_cylinder_mesh(self, center, radius, height, resolution=None):
        """Generate cylinder mesh for body parts"""
        if resolution is None:
            resolution = self.mesh_detail
            
        vertices = []
        faces = []
        
        # Generate vertices for top and bottom circles
        for layer in range(2):  # Top and bottom
            z_pos = center[2] + (height/2 if layer == 1 else -height/2)
            for i in range(resolution):
                angle = 2 * math.pi * i / resolution
                x = center[0] + radius * math.cos(angle)
                y = center[1] + radius * math.sin(angle)
                vertices.append((x, y, z_pos))
        
        # Generate side faces
        for i in range(resolution):
            next_i = (i + 1) % resolution
            
            # Bottom face vertices
            v0 = i
            v1 = next_i
            # Top face vertices  
            v2 = i + resolution
            v3 = next_i + resolution
            
            # Two triangles for each side face
            faces.append([v0, v2, v1])
            faces.append([v1, v2, v3])
            
        return vertices, faces
        
    def render_mesh(self, vertices, faces, color, lighting=True):
        """Render a 3D mesh with proper lighting and shading"""
        rendered_faces = []
        
        for face in faces:
            if len(face) < 3:
                continue
                
            # Project vertices to screen
            projected_verts = []
            depths = []
            
            for vertex_idx in face:
                if vertex_idx >= len(vertices):
                    continue
                    
                vertex = vertices[vertex_idx]
                px, py, depth = self.project_3d_to_2d(*vertex)
                projected_verts.append((px, py))
                depths.append(depth)
            
            if len(projected_verts) < 3:
                continue
                
            avg_depth = sum(depths) / len(depths)
            
            # Calculate face normal for lighting
            if len(projected_verts) >= 3 and lighting:
                # Get world space vertices for normal calculation
                v1 = np.array(vertices[face[0]])
                v2 = np.array(vertices[face[1]]) 
                v3 = np.array(vertices[face[2]])
                
                # Calculate normal
                edge1 = v2 - v1
                edge2 = v3 - v1
                normal = np.cross(edge1, edge2)
                
                # Normalize
                length = np.linalg.norm(normal)
                if length > 0:
                    normal = normal / length
                
                # Simple lighting calculation
                light_dir = np.array([0.5, -0.5, -1])  # Light from top-front
                light_intensity = max(0.2, min(1.0, -np.dot(normal, light_dir)))
                
                # Apply lighting to color
                shade_color = self.shade_color(color, light_intensity)
            else:
                shade_color = color
            
            rendered_faces.append({
                'points': projected_verts,
                'color': shade_color,
                'depth': avg_depth,
                'original_color': color
            })
        
        return rendered_faces
        
    def shade_color(self, color, intensity):
        """Apply lighting intensity to color"""
        try:
            # Parse hex color
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            
            # Apply intensity
            shaded_rgb = tuple(int(c * intensity) for c in rgb)
            shaded_rgb = tuple(max(0, min(255, c)) for c in shaded_rgb)
            
            return f"#{shaded_rgb[0]:02x}{shaded_rgb[1]:02x}{shaded_rgb[2]:02x}"
        except:
            return color
            
    def draw_3d_scene(self):
        """Draw the complete Blender-style 3D scene"""
        self.canvas.delete("all")
        
        # Dark Blender-style background with subtle gradient
        for i in range(0, self.canvas_height, 8):
            intensity = int(30 + (i / self.canvas_height) * 15)
            color = f"#{intensity:02x}{intensity:02x}{intensity:02x}"
            self.canvas.create_rectangle(0, i, self.canvas_width, i + 8, 
                                       fill=color, outline="")
        
        # Collect all mesh objects
        all_objects = []
        
        # Generate floor grid with mesh-based tiles
        floor_objects = self.generate_floor_mesh()
        all_objects.extend(floor_objects)
        
        # Generate avatar meshes if initialized
        if self.is_initialized:
            avatar_objects = self.generate_avatar_mesh()
            all_objects.extend(avatar_objects)
            
            # Generate pet meshes
            pet_objects = self.generate_pet_meshes()
            all_objects.extend(pet_objects)
        
        # Sort by depth and render
        all_objects.sort(key=lambda obj: obj['depth'], reverse=True)
        
        for obj in all_objects:
            self.render_mesh_object(obj)
            
    def generate_avatar_mesh(self):
        """Generate high-quality avatar using proper 3D meshes"""
        objects = []
        
        # Avatar position with animation
        ax = self.avatar_state["x"]
        ay = self.avatar_state["y"] 
        az = self.avatar_state["z"]
        
        breath = 0.03 * math.sin(self.animation_time * 2)
        base_height = 0
        
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
        
        # Generate mesh-based body parts
        
        # Head (high-resolution sphere)
        head_center = (ax, ay, base_height + 5.5 + breath)
        head_vertices, head_faces = self.generate_sphere_mesh(head_center, 1.1, self.sphere_resolution)
        objects.extend(self.render_mesh(head_vertices, head_faces, '#f4a460'))
        
        # Eyes (smaller high-res spheres)
        eye_left = (ax - 0.4, ay - 0.8, base_height + 5.7 + breath)
        eye_right = (ax + 0.4, ay - 0.8, base_height + 5.7 + breath)
        
        eye_left_verts, eye_left_faces = self.generate_sphere_mesh(eye_left, 0.2, 12)
        eye_right_verts, eye_right_faces = self.generate_sphere_mesh(eye_right, 0.2, 12)
        objects.extend(self.render_mesh(eye_left_verts, eye_left_faces, '#000000'))
        objects.extend(self.render_mesh(eye_right_verts, eye_right_faces, '#000000'))
        
        # Eye highlights
        highlight_left = (ax - 0.35, ay - 0.9, base_height + 5.8 + breath)
        highlight_right = (ax + 0.35, ay - 0.9, base_height + 5.8 + breath)
        
        hl_left_verts, hl_left_faces = self.generate_sphere_mesh(highlight_left, 0.06, 8)
        hl_right_verts, hl_right_faces = self.generate_sphere_mesh(highlight_right, 0.06, 8)
        objects.extend(self.render_mesh(hl_left_verts, hl_left_faces, '#ffffff'))
        objects.extend(self.render_mesh(hl_right_verts, hl_right_faces, '#ffffff'))
        
        # Body (cylinder mesh)
        body_center = (ax, ay, base_height + 3.2 + breath)
        body_vertices, body_faces = self.generate_cylinder_mesh(body_center, 0.9, 2.4)
        objects.extend(self.render_mesh(body_vertices, body_faces, shirt_color))
        
        # Arms (cylinder meshes)
        arm_left_center = (ax - 1.3, ay, base_height + 3.8 + breath)
        arm_right_center = (ax + 1.3, ay, base_height + 3.8 + breath)
        
        arm_left_verts, arm_left_faces = self.generate_cylinder_mesh(arm_left_center, 0.3, 1.8)
        arm_right_verts, arm_right_faces = self.generate_cylinder_mesh(arm_right_center, 0.3, 1.8)
        objects.extend(self.render_mesh(arm_left_verts, arm_left_faces, shirt_color))
        objects.extend(self.render_mesh(arm_right_verts, arm_right_faces, shirt_color))
        
        # Hands (small spheres)
        hand_left = (ax - 1.3, ay, base_height + 2.7 + breath)
        hand_right = (ax + 1.3, ay, base_height + 2.7 + breath)
        
        hand_left_verts, hand_left_faces = self.generate_sphere_mesh(hand_left, 0.25, 12)
        hand_right_verts, hand_right_faces = self.generate_sphere_mesh(hand_right, 0.25, 12)
        objects.extend(self.render_mesh(hand_left_verts, hand_left_faces, '#f4a460'))
        objects.extend(self.render_mesh(hand_right_verts, hand_right_faces, '#f4a460'))
        
        # Legs (cylinder meshes)
        leg_left_center = (ax - 0.4, ay, base_height + 1.2 + breath)
        leg_right_center = (ax + 0.4, ay, base_height + 1.2 + breath)
        
        leg_left_verts, leg_left_faces = self.generate_cylinder_mesh(leg_left_center, 0.35, 2.2)
        leg_right_verts, leg_right_faces = self.generate_cylinder_mesh(leg_right_center, 0.35, 2.2)
        objects.extend(self.render_mesh(leg_left_verts, leg_left_faces, pants_color))
        objects.extend(self.render_mesh(leg_right_verts, leg_right_faces, pants_color))
        
        # Feet (rounded)
        foot_left = (ax - 0.4, ay + 0.3, base_height + 0.2)
        foot_right = (ax + 0.4, ay + 0.3, base_height + 0.2)
        
        foot_left_verts, foot_left_faces = self.generate_sphere_mesh(foot_left, 0.4, 10)
        foot_right_verts, foot_right_faces = self.generate_sphere_mesh(foot_right, 0.4, 10)
        objects.extend(self.render_mesh(foot_left_verts, foot_left_faces, '#2c3e50'))
        objects.extend(self.render_mesh(foot_right_verts, foot_right_faces, '#2c3e50'))
        
        return objects
        
    def generate_floor_mesh(self):
        """Generate floor using mesh-based tiles"""
        objects = []
        
        for x in range(-6, 7, 2):
            for y in range(-6, 7, 2):
                # Create a slightly raised floor tile
                tile_center = (x, y, -0.1)
                tile_vertices, tile_faces = self.generate_cylinder_mesh(tile_center, 0.9, 0.1)
                
                # Alternate tile colors
                color = '#d2b48c' if (x + y) % 4 == 0 else '#c9a876'
                rendered_faces = self.render_mesh(tile_vertices, tile_faces, color)
                objects.extend(rendered_faces)
                
        return objects
        
    def generate_pet_meshes(self):
        """Generate pet meshes"""
        objects = []
        
        pet_positions = [(3, 2, 0.5), (-3, 2, 0.5), (2, -3, 0.5), (-2, -3, 0.5)]
        
        for i, pet_type in enumerate(self.pets[:4]):
            px, py, base_pz = pet_positions[i]
            pet_bob = 0.1 * math.sin(self.animation_time * 3 + i)
            pz = base_pz + pet_bob
            
            if pet_type == "pet_cat":
                objects.extend(self.generate_cat_mesh((px, py, pz)))
            elif pet_type == "pet_dog": 
                objects.extend(self.generate_dog_mesh((px, py, pz)))
                
        return objects
        
    def generate_cat_mesh(self, center):
        """Generate mesh-based cat"""
        objects = []
        
        # Cat body
        body_verts, body_faces = self.generate_sphere_mesh(center, 0.4, 12)
        objects.extend(self.render_mesh(body_verts, body_faces, '#ff9500'))
        
        # Cat head
        head_center = (center[0], center[1] - 0.5, center[2] + 0.3)
        head_verts, head_faces = self.generate_sphere_mesh(head_center, 0.3, 12)
        objects.extend(self.render_mesh(head_verts, head_faces, '#ff9500'))
        
        return objects
        
    def generate_dog_mesh(self, center):
        """Generate mesh-based dog"""
        objects = []
        
        # Dog body (larger than cat)
        body_verts, body_faces = self.generate_sphere_mesh(center, 0.5, 12)
        objects.extend(self.render_mesh(body_verts, body_faces, '#8b4513'))
        
        # Dog head
        head_center = (center[0], center[1] - 0.6, center[2] + 0.4)
        head_verts, head_faces = self.generate_sphere_mesh(head_center, 0.35, 12)
        objects.extend(self.render_mesh(head_verts, head_faces, '#8b4513'))
        
        return objects
        
    def render_mesh_object(self, obj):
        """Render a mesh object to canvas"""
        if len(obj['points']) >= 3:
            flat_points = [coord for point in obj['points'] for coord in point]
            
            # Add outline for better definition
            outline_color = self.darken_color(obj['color'])
            
            self.canvas.create_polygon(flat_points, 
                                     fill=obj['color'], 
                                     outline=outline_color,
                                     width=1,
                                     smooth=True)
            
    def darken_color(self, color):
        """Darken color for outlines"""
        try:
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            rgb = tuple(max(0, int(c * 0.6)) for c in rgb)
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        except:
            return "#000000"
    
    # Control methods (same as before but with mesh updates)
    def move_avatar(self, direction):
        """Move avatar in 3D space"""
        step = 0.6
        
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
            
        self.draw_3d_scene()
        
        if self.is_initialized:
            self.status_label.config(text=f"🎯 Avatar moved {direction} with mesh precision!", fg="#27ae60")
            self.after(1200, self._reset_status)
    
    def _reset_status(self):
        """Reset status message"""
        self.status_label.config(text="🎯 High-Quality 3D Avatar Ready! Professional mesh rendering!", fg="#27ae60")
    
    def rotate_camera(self, direction):
        """Rotate camera"""
        angle_step = 12
        
        if direction == "left":
            self.camera_rotation_y -= angle_step
        elif direction == "right":
            self.camera_rotation_y += angle_step
        elif direction == "up":
            self.camera_rotation_x = min(70, self.camera_rotation_x + angle_step)
        elif direction == "down":
            self.camera_rotation_x = max(-70, self.camera_rotation_x - angle_step)
            
        self.draw_3d_scene()
        
    def reset_camera(self, event=None):
        """Reset camera"""
        self.camera_rotation_y = 0
        self.camera_rotation_x = -15
        self.camera_x = 0
        self.camera_y = 8
        self.camera_z = 3
        self.draw_3d_scene()
        
    def adjust_quality(self, direction):
        """Adjust mesh quality"""
        if direction == "up":
            self.sphere_resolution = min(32, self.sphere_resolution + 4)
            self.mesh_detail = min(24, self.mesh_detail + 2)
        else:
            self.sphere_resolution = max(8, self.sphere_resolution - 4)
            self.mesh_detail = max(8, self.mesh_detail - 2)
            
        self.quality_label.config(text=f"Mesh Resolution: {self.sphere_resolution} | Detail Level: {self.mesh_detail}")
        
        if self.is_initialized:
            self.draw_3d_scene()
            
    def toggle_lighting(self):
        """Toggle lighting effects"""
        self.light_angle += 45
        if self.is_initialized:
            self.draw_3d_scene()
    
    def cycle_shirt(self):
        """Cycle shirt colors"""
        shirts = ["t_shirt_blue", "t_shirt_red", "hoodie_green", "polo_yellow", "sweater_purple"]
        current = shirts.index(self.avatar_state.get("shirt", "t_shirt_blue"))
        self.avatar_state["shirt"] = shirts[(current + 1) % len(shirts)]
        if self.is_initialized:
            self.draw_3d_scene()
        
    def cycle_pants(self):
        """Cycle pants colors"""
        pants = ["jeans_blue", "jeans_black", "khaki", "joggers_gray", "shorts_red"]
        current = pants.index(self.avatar_state.get("pants", "jeans_blue"))
        self.avatar_state["pants"] = pants[(current + 1) % len(pants)]
        if self.is_initialized:
            self.draw_3d_scene()
        
    def cycle_hat(self):
        """Cycle hats"""
        hats = ["none", "baseball_cap", "wizard_hat", "crown"]
        current = hats.index(self.avatar_state.get("hat", "none"))
        self.avatar_state["hat"] = hats[(current + 1) % len(hats)]
        if self.is_initialized:
            self.draw_3d_scene()
        
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
                self.status_label.config(text=f"🐾 Added {new_pet} with mesh precision!", fg="#27ae60")
                self.after(1200, self._reset_status)
    
    def start_animation(self):
        """Start animation"""
        if not self.animation_running:
            self.animation_running = True
            self.animate_loop()
            
    def animate_loop(self):
        """Animation loop"""
        if self.animation_running and self.is_initialized:
            self.animation_time += 0.08
            self.draw_3d_scene()
            self.after(60, self.animate_loop)  # ~16 FPS for smooth mesh rendering
    
    # Mouse interaction
    def on_mouse_press(self, event):
        """Mouse press"""
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
        
    def on_mouse_drag(self, event):
        """Mouse drag camera"""
        if hasattr(self, 'last_mouse_x'):
            dx = event.x - self.last_mouse_x
            dy = event.y - self.last_mouse_y
            
            self.camera_rotation_y += dx * 0.4
            self.camera_rotation_x += dy * 0.4
            self.camera_rotation_x = max(-70, min(70, self.camera_rotation_x))
            
            self.last_mouse_x = event.x
            self.last_mouse_y = event.y
            
            self.draw_3d_scene()
            
    def on_mouse_wheel(self, event):
        """Mouse wheel zoom"""
        zoom_step = 1.2
        if event.delta > 0:
            self.camera_y -= zoom_step
        else:
            self.camera_y += zoom_step
            
        self.camera_y = max(4, min(20, self.camera_y))
        self.draw_3d_scene()


# Test the Blender-style avatar
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Blender-Style 3D Avatar")
    root.geometry("900x800")
    root.configure(bg="#2c3e50")
    
    avatar = BlenderStyle3DAvatar(root)
    avatar.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Auto-initialize
    root.after(1000, avatar.initialize_3d)
    
    root.mainloop()