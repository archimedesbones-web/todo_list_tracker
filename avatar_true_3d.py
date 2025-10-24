"""
True 3D Claymation Avatar System - OpenGL Integration
Uses OpenGL directly with Tkinter for real 3D claymation rendering
"""

import tkinter as tk
from tkinter import messagebox
import math
import time

# Try to import OpenGL - if not available, we'll fall back gracefully
try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
    try:
        import tkinter.opengl as tkogl
        OPENGL_TKINTER_AVAILABLE = True
    except ImportError:
        # Alternative: use pyopengl with tkinter
        try:
            from OpenGL.Tk import *
            OPENGL_TKINTER_AVAILABLE = True
        except ImportError:
            OPENGL_TKINTER_AVAILABLE = False
    OPENGL_AVAILABLE = True
except ImportError:
    OPENGL_AVAILABLE = False
    OPENGL_TKINTER_AVAILABLE = False

class True3DClayAvatar(tk.Frame):
    """Real 3D Claymation Avatar using OpenGL"""
    
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
        self.camera_angle_x = 0
        self.camera_angle_y = 0
        self.camera_distance = 10
        self.animation_time = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI with 3D OpenGL widget or fallback"""
        # Title
        title = tk.Label(self, text="🎮 True 3D Claymation Avatar", 
                        font=("Arial", 14, "bold"))
        title.pack(pady=(0, 10))
        
        # Check if we can use real 3D
        if OPENGL_AVAILABLE and OPENGL_TKINTER_AVAILABLE:
            self.setup_true_3d()
        else:
            self.setup_3d_fallback()
            
    def setup_true_3d(self):
        """Set up real OpenGL 3D rendering"""
        try:
            # Create OpenGL widget
            self.gl_frame = tk.Frame(self)
            self.gl_frame.pack(fill="both", expand=True, pady=(0, 10))
            
            # Try to create OpenGL context
            from OpenGL.Tk import Opengl
            self.opengl = Opengl(self.gl_frame, width=500, height=400, double=1, depth=1)
            self.opengl.pack(fill="both", expand=True)
            
            # Bind OpenGL events
            self.opengl.bind('<Button-1>', self.on_mouse_click)
            self.opengl.bind('<B1-Motion>', self.on_mouse_drag)
            self.opengl.bind('<MouseWheel>', self.on_mouse_wheel)
            
            # Set up OpenGL
            self.opengl.redraw = self.redraw_3d
            self.opengl.redraw()
            
            self.is_3d_mode = True
            
            # Controls
            controls = self.setup_3d_controls()
            
            # Start animation loop
            self.animate_3d()
            
        except Exception as e:
            print(f"3D setup failed: {e}")
            self.setup_3d_fallback()
            
    def setup_3d_fallback(self):
        """Set up enhanced pseudo-3D as fallback"""
        self.is_3d_mode = False
        
        # Info message
        info = tk.Label(self, text="🎨 Enhanced Pseudo-3D Mode\n(True 3D requires OpenGL)", 
                       justify="center", fg="#666")
        info.pack(pady=(0, 10))
        
        # Create enhanced canvas with 3D-like effects
        self.canvas = tk.Canvas(self, width=500, height=400, bg="#2c3e50")
        self.canvas.pack(pady=(0, 10))
        
        # Controls
        controls = self.setup_3d_controls()
        
        # Draw initial scene
        self.draw_pseudo_3d()
        
    def setup_3d_controls(self):
        """Set up control interface for 3D avatar"""
        controls_frame = tk.Frame(self)
        controls_frame.pack(fill="x", pady=(0, 10))
        
        # Initialize button
        self.init_btn = tk.Button(controls_frame, 
                                 text="🎮 Initialize 3D Avatar" if self.is_3d_mode else "🎨 Initialize Enhanced Avatar",
                                 command=self.initialize_3d, 
                                 bg="#e74c3c", fg="white", font=("Arial", 11, "bold"))
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
        
        # Camera controls (3D only)
        if self.is_3d_mode:
            camera_frame = tk.LabelFrame(controls_frame, text="Camera")
            camera_frame.pack(side="left", padx=5)
            
            tk.Button(camera_frame, text="🔄", width=3,
                     command=lambda: self.rotate_camera("left")).grid(row=0, column=0, padx=2)
            tk.Button(camera_frame, text="↕", width=3,
                     command=lambda: self.rotate_camera("up")).grid(row=0, column=1, padx=2)
            tk.Button(camera_frame, text="🔄", width=3,
                     command=lambda: self.rotate_camera("right")).grid(row=0, column=2, padx=2)
            tk.Button(camera_frame, text="🔍+", width=3,
                     command=lambda: self.zoom_camera("in")).grid(row=1, column=0, padx=2)
            tk.Button(camera_frame, text="🎯", width=3,
                     command=self.reset_camera).grid(row=1, column=1, padx=2)
            tk.Button(camera_frame, text="🔍-", width=3,
                     command=lambda: self.zoom_camera("out")).grid(row=1, column=2, padx=2)
        
        # Status
        self.status_label = tk.Label(controls_frame, 
                                    text="Ready for 3D claymation experience" if self.is_3d_mode else "Enhanced pseudo-3D ready",
                                    fg="#34495e")
        self.status_label.pack(pady=5)
        
        return controls_frame
        
    def initialize_3d(self):
        """Initialize the 3D avatar system"""
        self.init_btn.config(text="Initializing...", state="disabled", bg="#95a5a6")
        self.status_label.config(text="Setting up 3D claymation world...", fg="#f39c12")
        self.update()
        
        # Simulate initialization process
        self.after(1000, self._complete_3d_initialization)
        
    def _complete_3d_initialization(self):
        """Complete 3D initialization"""
        self.is_initialized = True
        
        if self.is_3d_mode:
            self.init_btn.config(text="🎮 3D Avatar Active!", bg="#27ae60", state="disabled")
            self.status_label.config(text="🎭 True 3D Claymation Avatar Ready!", fg="#27ae60")
            self.redraw_3d()
        else:
            self.init_btn.config(text="🎨 Enhanced Avatar Active!", bg="#27ae60", state="disabled") 
            self.status_label.config(text="🎨 Enhanced Pseudo-3D Avatar Ready!", fg="#27ae60")
            self.draw_pseudo_3d()
            
        # Start animation
        self.animate_avatar()
        
    def redraw_3d(self):
        """Redraw the true 3D scene using OpenGL"""
        if not hasattr(self, 'opengl'):
            return
            
        try:
            # Clear and set up
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            
            # Set up camera
            gluLookAt(
                self.camera_distance * math.cos(self.camera_angle_y) * math.cos(self.camera_angle_x),
                self.camera_distance * math.sin(self.camera_angle_x),
                self.camera_distance * math.sin(self.camera_angle_y) * math.cos(self.camera_angle_x),
                0, 0, 0,  # Look at origin
                0, 1, 0   # Up vector
            )
            
            # Enable lighting for clay effect
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glEnable(GL_DEPTH_TEST)
            
            # Set up clay-like lighting
            light_pos = [2.0, 2.0, 2.0, 1.0]
            light_ambient = [0.4, 0.4, 0.3, 1.0]
            light_diffuse = [0.8, 0.7, 0.6, 1.0]
            
            glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
            glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
            glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
            
            # Draw 3D scene
            self.draw_3d_environment()
            self.draw_3d_avatar()
            self.draw_3d_pets()
            
            # Swap buffers
            self.opengl.tkSwapBuffers()
            
        except Exception as e:
            print(f"3D rendering error: {e}")
            
    def draw_3d_environment(self):
        """Draw 3D environment (floor, walls)"""
        # Clay-colored floor
        glColor3f(0.8, 0.7, 0.6)
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glVertex3f(-5, -1, -5)
        glVertex3f(5, -1, -5) 
        glVertex3f(5, -1, 5)
        glVertex3f(-5, -1, 5)
        glEnd()
        
    def draw_3d_avatar(self):
        """Draw the 3D claymation avatar"""
        if not self.is_initialized:
            return
            
        # Save matrix state
        glPushMatrix()
        
        # Move to avatar position
        glTranslatef(self.avatar_state["x"], self.avatar_state["y"], self.avatar_state["z"])
        glRotatef(self.avatar_state["rotation"], 0, 1, 0)
        
        # Add subtle breathing animation
        breath_scale = 1.0 + 0.02 * math.sin(self.animation_time * 2)
        glScalef(breath_scale, breath_scale, breath_scale)
        
        # Get clothing colors
        shirt_colors = {
            "t_shirt_blue": (0.2, 0.4, 0.8),
            "t_shirt_red": (0.8, 0.2, 0.2),
            "hoodie_green": (0.2, 0.6, 0.2),
            "polo_yellow": (0.9, 0.9, 0.2),
            "sweater_purple": (0.6, 0.2, 0.8)
        }
        
        pants_colors = {
            "jeans_blue": (0.1, 0.2, 0.6),
            "jeans_black": (0.1, 0.1, 0.1),
            "khaki": (0.7, 0.6, 0.4),
            "joggers_gray": (0.5, 0.5, 0.5),
            "shorts_red": (0.8, 0.3, 0.3)
        }
        
        shirt_color = shirt_colors.get(self.avatar_state["shirt"], (0.2, 0.4, 0.8))
        pants_color = pants_colors.get(self.avatar_state["pants"], (0.1, 0.2, 0.6))
        
        # Draw head (clay-colored sphere)
        glPushMatrix()
        glTranslatef(0, 1.7, 0)
        glColor3f(0.95, 0.8, 0.7)  # Clay skin color
        self.draw_sphere(0.4, 16, 16)
        
        # Eyes
        glColor3f(0.1, 0.1, 0.1)
        glPushMatrix()
        glTranslatef(-0.15, 0.1, -0.35)
        self.draw_sphere(0.05, 8, 8)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0.15, 0.1, -0.35)
        self.draw_sphere(0.05, 8, 8)
        glPopMatrix()
        
        # Nose
        glColor3f(0.9, 0.75, 0.65)
        glPushMatrix()
        glTranslatef(0, 0, -0.4)
        self.draw_sphere(0.08, 8, 8)
        glPopMatrix()
        
        glPopMatrix()  # End head
        
        # Draw body (shirt colored)
        glPushMatrix()
        glTranslatef(0, 0.5, 0)
        glColor3f(*shirt_color)
        glScalef(0.8, 1.2, 0.6)
        self.draw_cube()
        glPopMatrix()
        
        # Draw arms
        glColor3f(*shirt_color)
        # Left arm
        glPushMatrix()
        glTranslatef(-0.8, 0.8, 0)
        glScalef(0.3, 1.0, 0.3)
        self.draw_cube()
        glPopMatrix()
        
        # Right arm
        glPushMatrix()
        glTranslatef(0.8, 0.8, 0)
        glScalef(0.3, 1.0, 0.3)
        self.draw_cube()
        glPopMatrix()
        
        # Draw legs (pants colored)
        glColor3f(*pants_color)
        # Left leg
        glPushMatrix()
        glTranslatef(-0.3, -0.8, 0)
        glScalef(0.35, 1.2, 0.35)
        self.draw_cube()
        glPopMatrix()
        
        # Right leg  
        glPushMatrix()
        glTranslatef(0.3, -0.8, 0)
        glScalef(0.35, 1.2, 0.35)
        self.draw_cube()
        glPopMatrix()
        
        # Draw feet
        glColor3f(0.1, 0.1, 0.1)  # Black shoes
        # Left foot
        glPushMatrix()
        glTranslatef(-0.3, -1.6, 0.2)
        glScalef(0.4, 0.2, 0.8)
        self.draw_cube()
        glPopMatrix()
        
        # Right foot
        glPushMatrix()
        glTranslatef(0.3, -1.6, 0.2)
        glScalef(0.4, 0.2, 0.8)
        self.draw_cube()
        glPopMatrix()
        
        # Draw hat if applicable
        self.draw_3d_hat()
        
        glPopMatrix()  # End avatar
        
    def draw_3d_hat(self):
        """Draw 3D hat based on avatar state"""
        hat = self.avatar_state.get("hat", "none")
        
        if hat == "baseball_cap":
            glColor3f(0.8, 0.2, 0.0)  # Orange cap
            glPushMatrix()
            glTranslatef(0, 2.0, 0)
            glScalef(0.5, 0.2, 0.5)
            self.draw_sphere(0.8, 12, 12)
            glPopMatrix()
            
        elif hat == "wizard_hat":
            glColor3f(0.4, 0.0, 0.6)  # Purple wizard hat
            glPushMatrix()
            glTranslatef(0, 2.2, 0)
            glRotatef(-90, 1, 0, 0)
            self.draw_cone(0.3, 1.0, 12)
            glPopMatrix()
            
    def draw_3d_pets(self):
        """Draw 3D pets"""
        pet_positions = [(2, -1, 1), (-2, -1, 1), (1, -1, -2), (-1, -1, -2)]
        
        for i, pet_type in enumerate(self.pets):
            if i >= len(pet_positions):
                break
                
            pos = pet_positions[i]
            
            glPushMatrix()
            glTranslatef(*pos)
            
            # Add subtle pet animation
            pet_bob = 0.1 * math.sin(self.animation_time * 3 + i)
            glTranslatef(0, pet_bob, 0)
            
            if pet_type == "pet_cat":
                self.draw_3d_cat()
            elif pet_type == "pet_dog":
                self.draw_3d_dog()
            elif pet_type == "pet_bird":
                self.draw_3d_bird()
            elif pet_type == "pet_dragon":
                self.draw_3d_dragon()
                
            glPopMatrix()
            
    def draw_3d_cat(self):
        """Draw 3D claymation cat"""
        glColor3f(0.9, 0.6, 0.2)  # Orange cat
        
        # Body
        glPushMatrix()
        glScalef(0.8, 0.4, 0.4)
        self.draw_sphere(0.5, 12, 12)
        glPopMatrix()
        
        # Head
        glPushMatrix()
        glTranslatef(0.6, 0.1, 0)
        self.draw_sphere(0.3, 10, 10)
        glPopMatrix()
        
        # Ears
        glPushMatrix()
        glTranslatef(0.7, 0.3, -0.15)
        self.draw_cone(0.1, 0.2, 6)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0.7, 0.3, 0.15)
        self.draw_cone(0.1, 0.2, 6)
        glPopMatrix()
        
    def draw_3d_dog(self):
        """Draw 3D claymation dog"""
        glColor3f(0.6, 0.4, 0.2)  # Brown dog
        
        # Body (larger than cat)
        glPushMatrix()
        glScalef(1.0, 0.5, 0.5)
        self.draw_sphere(0.6, 12, 12)
        glPopMatrix()
        
        # Head
        glPushMatrix()
        glTranslatef(0.8, 0.1, 0)
        glScalef(0.8, 0.6, 0.6)
        self.draw_sphere(0.4, 10, 10)
        glPopMatrix()
        
    def draw_3d_bird(self):
        """Draw 3D claymation bird"""
        glColor3f(0.2, 0.6, 0.9)  # Blue bird
        
        # Body
        glPushMatrix()
        glScalef(0.4, 0.4, 0.6)
        self.draw_sphere(0.3, 10, 10)
        glPopMatrix()
        
        # Wings
        glColor3f(0.1, 0.5, 0.8)
        glPushMatrix()
        glTranslatef(0, 0, -0.4)
        glScalef(0.6, 0.1, 0.3)
        self.draw_sphere(0.3, 8, 8)
        glPopMatrix()
        
    def draw_3d_dragon(self):
        """Draw 3D claymation dragon"""
        glColor3f(0.2, 0.7, 0.3)  # Green dragon
        
        # Body (majestic)
        glPushMatrix()
        glScalef(1.2, 0.6, 0.8)
        self.draw_sphere(0.7, 12, 12)
        glPopMatrix()
        
        # Wings
        glColor3f(0.1, 0.6, 0.2)
        glPushMatrix()
        glTranslatef(0, 0.3, -0.8)
        glScalef(1.0, 0.1, 0.6)
        self.draw_sphere(0.5, 8, 8)
        glPopMatrix()
        
    def draw_sphere(self, radius, slices, stacks):
        """Draw a sphere with given parameters"""
        try:
            glutSolidSphere(radius, slices, stacks)
        except:
            # Fallback if GLUT not available
            self.draw_cube()
            
    def draw_cube(self):
        """Draw a unit cube"""
        glBegin(GL_QUADS)
        
        # Front face
        glNormal3f(0, 0, 1)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        
        # Back face
        glNormal3f(0, 0, -1)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        
        # Top face
        glNormal3f(0, 1, 0)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, -0.5)
        
        # Bottom face
        glNormal3f(0, -1, 0)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        
        # Right face
        glNormal3f(1, 0, 0)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        
        # Left face
        glNormal3f(-1, 0, 0)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        
        glEnd()
        
    def draw_cone(self, base_radius, height, slices):
        """Draw a cone"""
        try:
            glutSolidCone(base_radius, height, slices, 2)
        except:
            # Fallback
            self.draw_cube()
            
    def draw_pseudo_3d(self):
        """Draw enhanced pseudo-3D scene as fallback"""
        if not hasattr(self, 'canvas'):
            return
            
        self.canvas.delete("all")
        
        # Enhanced 3D-like background
        for i in range(400):
            intensity = int(44 + i * 0.1)  # Gradient from dark to lighter
            color = f"#{intensity:02x}{intensity+10:02x}{intensity+20:02x}"
            self.canvas.create_line(0, i, 500, i, fill=color, width=1)
        
        # 3D-like floor grid
        for x in range(0, 500, 30):
            # Perspective lines
            self.canvas.create_line(x, 350, 250, 400, fill="#34495e", width=1)
        for y in range(350, 400, 10):
            self.canvas.create_line(0, y, 500, y, fill="#34495e", width=1)
        
        # Draw pseudo-3D avatar
        if self.is_initialized:
            self.draw_pseudo_3d_avatar()
            
    def draw_pseudo_3d_avatar(self):
        """Draw avatar with enhanced 3D-like effects"""
        cx, cy = 250 + self.avatar_state["x"] * 20, 200 + self.avatar_state["y"] * 20
        
        # Enhanced shadow with multiple layers
        for i in range(5):
            alpha = 50 - i * 8
            shadow_offset = i * 2
            self.canvas.create_oval(
                cx - 30 + shadow_offset, cy + 80 + shadow_offset,
                cx + 30 - shadow_offset, cy + 90 - shadow_offset,
                fill="#2c3e50", outline="", stipple="gray25"
            )
        
        # 3D-style body with depth
        colors = {
            "t_shirt_blue": "#3498db",
            "t_shirt_red": "#e74c3c", 
            "hoodie_green": "#27ae60"
        }
        shirt_color = colors.get(self.avatar_state["shirt"], "#3498db")
        
        # Body with 3D shading
        self.draw_3d_rect(cx-25, cy-10, cx+25, cy+30, shirt_color)
        
        # Head with 3D shading  
        self.draw_3d_circle(cx, cy-40, 20, "#f39c12")
        
        # Arms with depth
        self.draw_3d_rect(cx-40, cy-5, cx-25, cy+20, shirt_color)
        self.draw_3d_rect(cx+25, cy-5, cx+40, cy+20, shirt_color)
        
        # Legs with 3D effect
        pants_colors = {"jeans_blue": "#2980b9", "jeans_black": "#34495e"}
        pants_color = pants_colors.get(self.avatar_state["pants"], "#2980b9")
        
        self.draw_3d_rect(cx-20, cy+30, cx-5, cy+70, pants_color)
        self.draw_3d_rect(cx+5, cy+30, cx+20, cy+70, pants_color)
        
        # 3D facial features
        # Eyes with depth
        self.canvas.create_oval(cx-12, cy-45, cx-8, cy-41, fill="#2c3e50", outline="#1a252f", width=2)
        self.canvas.create_oval(cx+8, cy-45, cx+12, cy-41, fill="#2c3e50", outline="#1a252f", width=2)
        # Eye highlights
        self.canvas.create_oval(cx-11, cy-44, cx-9, cy-42, fill="#ecf0f1")
        self.canvas.create_oval(cx+9, cy-44, cx+11, cy-42, fill="#ecf0f1")
        
    def draw_3d_rect(self, x1, y1, x2, y2, base_color):
        """Draw a rectangle with 3D shading effect"""
        # Main face
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=base_color, outline="")
        
        # Top highlight
        highlight = self.lighten_color(base_color, 1.3)
        self.canvas.create_line(x1, y1, x2, y1, fill=highlight, width=3)
        
        # Left highlight
        self.canvas.create_line(x1, y1, x1, y2, fill=highlight, width=2)
        
        # Right shadow
        shadow = self.darken_color(base_color, 0.7)
        self.canvas.create_line(x2, y1, x2, y2, fill=shadow, width=3)
        
        # Bottom shadow
        self.canvas.create_line(x1, y2, x2, y2, fill=shadow, width=3)
        
    def draw_3d_circle(self, cx, cy, radius, base_color):
        """Draw a circle with 3D shading effect"""
        # Main circle
        self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, 
                              fill=base_color, outline="")
        
        # Highlight
        highlight = self.lighten_color(base_color, 1.4)
        self.canvas.create_oval(cx-radius+3, cy-radius+3, cx-2, cy-2, 
                              fill=highlight, outline="")
        
        # Shadow
        shadow = self.darken_color(base_color, 0.6)
        self.canvas.create_oval(cx+2, cy+2, cx+radius-3, cy+radius-3, 
                              fill=shadow, outline="")
                              
    def lighten_color(self, color, factor):
        """Lighten a hex color"""
        try:
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            rgb = tuple(min(255, int(c * factor)) for c in rgb)
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        except:
            return "#ffffff"
            
    def darken_color(self, color, factor):
        """Darken a hex color"""
        try:
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            rgb = tuple(max(0, int(c * factor)) for c in rgb)
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        except:
            return "#000000"
    
    # Avatar control methods
    def move_avatar(self, direction):
        """Move avatar in 3D space"""
        step = 0.5
        
        if direction == "forward":
            self.avatar_state["z"] -= step
        elif direction == "backward":  
            self.avatar_state["z"] += step
        elif direction == "left":
            self.avatar_state["x"] -= step
        elif direction == "right":
            self.avatar_state["x"] += step
            
        self.update_display()
        
        if self.is_initialized:
            self.status_label.config(text=f"🎭 Avatar moved {direction}!", fg="#27ae60")
            self.after(1000, lambda: self.status_label.config(
                text="🎮 True 3D Avatar Ready!" if self.is_3d_mode else "🎨 Enhanced Avatar Ready!", fg="#27ae60"))
    
    def rotate_camera(self, direction):
        """Rotate camera around avatar (3D only)"""
        if not self.is_3d_mode:
            return
            
        angle_step = 0.2
        
        if direction == "left":
            self.camera_angle_y -= angle_step
        elif direction == "right":
            self.camera_angle_y += angle_step
        elif direction == "up":
            self.camera_angle_x += angle_step
        elif direction == "down":
            self.camera_angle_x -= angle_step
            
        self.update_display()
        
    def zoom_camera(self, direction):
        """Zoom camera in/out (3D only)"""
        if not self.is_3d_mode:
            return
            
        if direction == "in":
            self.camera_distance = max(3, self.camera_distance - 1)
        elif direction == "out":
            self.camera_distance = min(20, self.camera_distance + 1)
            
        self.update_display()
        
    def reset_camera(self):
        """Reset camera to default position"""
        if not self.is_3d_mode:
            return
            
        self.camera_angle_x = 0
        self.camera_angle_y = 0
        self.camera_distance = 10
        self.update_display()
    
    def update_avatar_state(self, state_dict):
        """Update avatar appearance"""
        self.avatar_state.update(state_dict)
        self.update_display()
        
        if self.is_initialized:
            self.status_label.config(text="🎨 Avatar updated!", fg="#27ae60")
            self.after(1000, lambda: self.status_label.config(
                text="🎮 True 3D Avatar Ready!" if self.is_3d_mode else "🎨 Enhanced Avatar Ready!", fg="#27ae60"))
    
    def add_pet(self, pet_type):
        """Add a pet to the scene"""
        if pet_type not in self.pets:
            self.pets.append(pet_type)
            self.update_display()
            
            if self.is_initialized:
                self.status_label.config(text=f"🐾 Added {pet_type}!", fg="#27ae60")
                self.after(1500, lambda: self.status_label.config(
                    text="🎮 True 3D Avatar Ready!" if self.is_3d_mode else "🎨 Enhanced Avatar Ready!", fg="#27ae60"))
    
    def remove_pet(self, pet_type):
        """Remove a pet from the scene"""
        if pet_type in self.pets:
            self.pets.remove(pet_type)
            self.update_display()
            
    def update_display(self):
        """Update the display (3D or pseudo-3D)"""
        if self.is_3d_mode and hasattr(self, 'opengl'):
            self.redraw_3d()
        elif hasattr(self, 'canvas'):
            self.draw_pseudo_3d()
            
    def animate_3d(self):
        """Animation loop for 3D effects"""
        if self.is_initialized:
            self.animation_time += 0.05
            self.update_display()
        self.after(50, self.animate_3d)
        
    def animate_avatar(self):
        """Start avatar animation"""
        self.animate_3d()
        
    # Mouse interaction for 3D mode
    def on_mouse_click(self, event):
        """Handle mouse click for camera control"""
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
        
    def on_mouse_drag(self, event):
        """Handle mouse drag for camera rotation"""
        if hasattr(self, 'last_mouse_x'):
            dx = event.x - self.last_mouse_x
            dy = event.y - self.last_mouse_y
            
            self.camera_angle_y += dx * 0.01
            self.camera_angle_x += dy * 0.01
            
            self.last_mouse_x = event.x
            self.last_mouse_y = event.y
            
            self.update_display()
            
    def on_mouse_wheel(self, event):
        """Handle mouse wheel for zooming"""
        if event.delta > 0:
            self.zoom_camera("in")
        else:
            self.zoom_camera("out")


# Test the true 3D avatar
if __name__ == "__main__":
    root = tk.Tk()
    root.title("True 3D Claymation Avatar")
    root.geometry("600x600")
    
    avatar = True3DClayAvatar(root)
    avatar.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Auto-initialize
    root.after(1000, avatar.initialize_3d)
    
    root.mainloop()