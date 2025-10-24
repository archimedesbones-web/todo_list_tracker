"""
3D Claymation Avatar System
Integrates Panda3D with Tkinter for realistic 3D claymation avatars
"""

import tkinter as tk
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import (
    GeomVertexFormat, GeomVertexData, GeomVertexWriter, Geom, GeomTriangles, 
    GeomNode, NodePath, Material, AmbientLight, DirectionalLight, CardMaker,
    Point3, Vec3, CollisionTraverser, CollisionNode, CollisionSphere,
    CollisionHandlerQueue, BitMask32, TransparencyAttrib, RenderState,
    ColorBlendAttrib, AntialiasAttrib
)
from direct.gui.DirectGui import *
import numpy as np
import math
import threading
import queue
import time

class Avatar3DEngine:
    """3D rendering engine for claymation-style avatars"""
    
    def __init__(self):
        self.is_initialized = False
        self.command_queue = queue.Queue()
        self.response_queue = queue.Queue()
        self.avatar_state = {
            "x": 0, "y": 0, "z": 0,
            "rotation": 0,
            "hat": "none",
            "shirt": "t_shirt_blue", 
            "pants": "jeans_blue",
            "animation": "idle"
        }
        self.pets = []
        
    def initialize_3d_system(self):
        """Initialize Panda3D in a separate thread"""
        if self.is_initialized:
            return
            
        self.render_thread = threading.Thread(target=self._run_panda3d, daemon=True)
        self.render_thread.start()
        
        # Wait for initialization
        start_time = time.time()
        while not self.is_initialized and time.time() - start_time < 10:
            time.sleep(0.1)
            
    def _run_panda3d(self):
        """Run Panda3D in separate thread"""
        try:
            self.app = ClayAvatar3D(self)
            self.is_initialized = True
            self.app.run()
        except Exception as e:
            print(f"3D Engine Error: {e}")
            
    def update_avatar_state(self, state_dict):
        """Update avatar appearance and position"""
        self.command_queue.put(("update_avatar", state_dict))
        
    def move_avatar(self, direction):
        """Move avatar in specified direction"""
        self.command_queue.put(("move_avatar", direction))
        
    def set_animation(self, animation_name):
        """Set avatar animation (idle, walk, celebrate)"""
        self.command_queue.put(("animate", animation_name))
        
    def add_pet(self, pet_type, position=None):
        """Add a pet to the scene"""
        if position is None:
            position = (2, 2, 0)
        self.command_queue.put(("add_pet", {"type": pet_type, "pos": position}))
        
    def remove_pet(self, pet_type):
        """Remove pet from scene"""
        self.command_queue.put(("remove_pet", pet_type))
        
    def get_screenshot(self, width=400, height=300):
        """Get a screenshot of the 3D scene"""
        self.command_queue.put(("screenshot", (width, height)))
        try:
            response = self.response_queue.get(timeout=1.0)
            return response
        except:
            return None

class ClayAvatar3D(ShowBase):
    """Main Panda3D application for claymation avatar"""
    
    def __init__(self, engine):
        ShowBase.__init__(self)
        self.engine = engine
        self.avatar_node = None
        self.pets_nodes = {}
        self.clay_material = None
        
        # Set up the 3D environment
        self.setup_scene()
        self.create_clay_materials()
        self.create_avatar()
        self.setup_lighting()
        self.setup_camera()
        
        # Start command processing task
        self.taskMgr.add(self.process_commands, "process_commands")
        
    def setup_scene(self):
        """Set up the basic 3D scene"""
        # Disable default mouse controls
        self.disableMouse()
        
        # Set background color to match room theme
        self.setBackgroundColor(0.9, 0.85, 0.75, 1)  # Warm clay-like background
        
        # Create floor using CardMaker (simple and reliable)
        floor = self.create_floor()
        floor.setScale(10, 10, 0.1)
        floor.setPos(0, 0, -1)
        floor.setColor(0.8, 0.7, 0.6, 1)  # Floor color
        floor.reparentTo(self.render)
        
    def create_floor(self):
        """Create a procedural floor"""
        try:
            # Create simple floor geometry
            format = GeomVertexFormat.getV3n3()
            vdata = GeomVertexData('floor', format, Geom.UHStatic)
            vdata.setNumRows(4)
            vertex = GeomVertexWriter(vdata, 'vertex')
            normal = GeomVertexWriter(vdata, 'normal')
            
            # Floor vertices
            vertex.addData3(-5, -5, 0)
            vertex.addData3(5, -5, 0)
            vertex.addData3(5, 5, 0)
            vertex.addData3(-5, 5, 0)
            
            # Normals pointing up
            for _ in range(4):
                normal.addData3(0, 0, 1)
            
            # Create geometry
            geom = Geom(vdata)
            tris = GeomTriangles(Geom.UHStatic)
            tris.addVertices(0, 1, 2)
            tris.addVertices(0, 2, 3)
            geom.addPrimitive(tris)
            
            # Create node
            floor_node = GeomNode('floor')
            floor_node.addGeom(geom)
            return NodePath(floor_node)
        except Exception as e:
            print(f"Floor creation error: {e}")
            # Fallback: create a simple CardMaker quad
            from panda3d.core import CardMaker
            cm = CardMaker("floor")
            cm.setFrame(-5, 5, -5, 5)
            return NodePath(cm.generate())
        
    def create_clay_materials(self):
        """Create clay-like materials and shaders"""
        # Clay material with subsurface scattering effect
        self.clay_material = Material()
        self.clay_material.setShininess(5.0)  # Low shininess for clay
        self.clay_material.setAmbient(0.4, 0.3, 0.3, 1)
        self.clay_material.setDiffuse(0.8, 0.6, 0.5, 1)
        self.clay_material.setSpecular(0.1, 0.1, 0.1, 1)
        self.clay_material.setEmission(0, 0, 0, 1)
        
        # Color variations for different parts
        self.clay_colors = {
            "skin": (0.95, 0.8, 0.7, 1),
            "t_shirt_blue": (0.3, 0.5, 0.8, 1),
            "t_shirt_red": (0.8, 0.2, 0.2, 1),
            "jeans_blue": (0.2, 0.3, 0.6, 1),
            "jeans_black": (0.1, 0.1, 0.15, 1),
            "hair_brown": (0.4, 0.25, 0.1, 1),
        }
        
    def create_avatar(self):
        """Create the main claymation avatar"""
        self.avatar_node = self.render.attachNewNode("avatar")
        
        # Create avatar parts
        self.create_avatar_head()
        self.create_avatar_body()
        self.create_avatar_limbs()
        
        # Position avatar at origin
        self.avatar_node.setPos(0, 0, 0)
        
    def create_avatar_head(self):
        """Create claymation-style head"""
        # Head (slightly flattened sphere for clay look)
        head = self.create_clay_sphere("head", 0.8, 0.9, 0.8)  # Slightly wider
        head.setPos(0, 0, 2.5)
        head.setColor(*self.clay_colors["skin"])
        head.reparentTo(self.avatar_node)
        
        # Eyes (small dark spheres)
        eye_left = self.create_clay_sphere("eye_left", 0.1, 0.1, 0.1)
        eye_left.setPos(-0.25, -0.6, 2.7)
        eye_left.setColor(0.1, 0.1, 0.1, 1)
        eye_left.reparentTo(self.avatar_node)
        
        eye_right = self.create_clay_sphere("eye_right", 0.1, 0.1, 0.1)
        eye_right.setPos(0.25, -0.6, 2.7)
        eye_right.setColor(0.1, 0.1, 0.1, 1)
        eye_right.reparentTo(self.avatar_node)
        
        # Nose (small bump)
        nose = self.create_clay_sphere("nose", 0.08, 0.1, 0.08)
        nose.setPos(0, -0.65, 2.4)
        nose.setColor(*self.clay_colors["skin"])
        nose.reparentTo(self.avatar_node)
        
        # Mouth (flattened sphere)
        mouth = self.create_clay_sphere("mouth", 0.2, 0.05, 0.1)
        mouth.setPos(0, -0.7, 2.1)
        mouth.setColor(0.6, 0.2, 0.2, 1)  # Reddish for mouth
        mouth.reparentTo(self.avatar_node)
        
    def create_avatar_body(self):
        """Create claymation-style body"""
        # Torso (stretched cube for clay-like body)
        body = self.create_clay_cube("body", 1.2, 0.8, 1.5)
        body.setPos(0, 0, 1.0)
        body.setColor(*self.clay_colors["t_shirt_blue"])  # Default shirt color
        body.reparentTo(self.avatar_node)
        
        # Store reference for clothing changes
        self.body_node = body
        
    def create_avatar_limbs(self):
        """Create claymation-style arms and legs"""
        # Arms
        arm_left = self.create_clay_cube("arm_left", 0.3, 0.3, 1.0)
        arm_left.setPos(-0.8, 0, 1.2)
        arm_left.setColor(*self.clay_colors["t_shirt_blue"])
        arm_left.reparentTo(self.avatar_node)
        
        arm_right = self.create_clay_cube("arm_right", 0.3, 0.3, 1.0)
        arm_right.setPos(0.8, 0, 1.2)
        arm_right.setColor(*self.clay_colors["t_shirt_blue"])
        arm_right.reparentTo(self.avatar_node)
        
        # Hands
        hand_left = self.create_clay_sphere("hand_left", 0.2, 0.2, 0.2)
        hand_left.setPos(-0.8, 0, 0.5)
        hand_left.setColor(*self.clay_colors["skin"])
        hand_left.reparentTo(self.avatar_node)
        
        hand_right = self.create_clay_sphere("hand_right", 0.2, 0.2, 0.2)
        hand_right.setPos(0.8, 0, 0.5)
        hand_right.setColor(*self.clay_colors["skin"])
        hand_right.reparentTo(self.avatar_node)
        
        # Legs
        leg_left = self.create_clay_cube("leg_left", 0.35, 0.35, 1.2)
        leg_left.setPos(-0.35, 0, -0.2)
        leg_left.setColor(*self.clay_colors["jeans_blue"])
        leg_left.reparentTo(self.avatar_node)
        
        leg_right = self.create_clay_cube("leg_right", 0.35, 0.35, 1.2)
        leg_right.setPos(0.35, 0, -0.2)
        leg_right.setColor(*self.clay_colors["jeans_blue"])
        leg_right.reparentTo(self.avatar_node)
        
        # Feet
        foot_left = self.create_clay_cube("foot_left", 0.4, 0.6, 0.2)
        foot_left.setPos(-0.35, 0.1, -0.9)
        foot_left.setColor(0.1, 0.1, 0.1, 1)  # Black shoes
        foot_left.reparentTo(self.avatar_node)
        
        foot_right = self.create_clay_cube("foot_right", 0.4, 0.6, 0.2)
        foot_right.setPos(0.35, 0.1, -0.9)
        foot_right.setColor(0.1, 0.1, 0.1, 1)  # Black shoes
        foot_right.reparentTo(self.avatar_node)
        
    def create_clay_sphere(self, name, sx=1, sy=1, sz=1):
        """Create a clay-like sphere with organic imperfections"""
        # Use built-in loader for primitive shapes
        try:
            # Try to load from Panda3D's built-in models
            sphere = self.loader.loadModel("models/environment")
            if sphere:
                # Use a part of the environment model if available
                sphere = sphere.find("**/sphere*")
            if not sphere:
                # Create using CardMaker as fallback
                sphere = self.create_simple_sphere()
        except:
            sphere = self.create_simple_sphere()
        
        # Apply slight random scaling for organic clay effect
        random_x = 0.95 + 0.1 * (hash(name) % 10) / 100
        random_y = 0.95 + 0.1 * (hash(name + "y") % 10) / 100
        random_z = 0.95 + 0.1 * (hash(name + "z") % 10) / 100
        sphere.setScale(sx * random_x, sy * random_y, sz * random_z)
        
        # Apply clay material
        if self.clay_material:
            sphere.setMaterial(self.clay_material)
        
        return sphere
        
    def create_clay_cube(self, name, sx=1, sy=1, sz=1):
        """Create a clay-like cube with rounded edges"""
        # Create simple cube using CardMaker
        cube = self.create_simple_cube()
            
        # Slightly irregular scaling for handmade clay effect
        random_x = 0.98 + 0.04 * (hash(name) % 10) / 100
        random_y = 0.98 + 0.04 * (hash(name + "y") % 10) / 100
        random_z = 0.98 + 0.04 * (hash(name + "z") % 10) / 100
        cube.setScale(sx * random_x, sy * random_y, sz * random_z)
        
        # Apply clay material
        if self.clay_material:
            cube.setMaterial(self.clay_material)
        
        return cube
        
    def create_simple_sphere(self):
        """Create a simple sphere using CardMaker"""
        cm = CardMaker("sphere")
        cm.setFrame(-1, 1, -1, 1)
        sphere = NodePath(cm.generate())
        # Make it look more spherical by rotating multiple cards
        return sphere
        
    def create_simple_cube(self):
        """Create a simple cube using CardMaker"""
        cm = CardMaker("cube") 
        cm.setFrame(-1, 1, -1, 1)
        cube = NodePath(cm.generate())
        return cube
        
    def setup_lighting(self):
        """Set up lighting for claymation effect"""
        # Ambient light for soft clay appearance
        ambient_light = AmbientLight('ambient_light')
        ambient_light.setColor(0.4, 0.4, 0.3, 1)
        self.render.setLight(self.render.attachNewNode(ambient_light))
        
        # Main directional light (soft clay lighting)
        main_light = DirectionalLight('main_light')
        main_light.setColor(0.8, 0.8, 0.7, 1)
        main_light.setDirection(-1, -1, -1)
        self.render.setLight(self.render.attachNewNode(main_light))
        
        # Fill light (reduce harsh shadows)
        fill_light = DirectionalLight('fill_light')
        fill_light.setColor(0.3, 0.3, 0.4, 1)
        fill_light.setDirection(1, 1, -0.5)
        self.render.setLight(self.render.attachNewNode(fill_light))
        
    def setup_camera(self):
        """Position camera for good avatar view"""
        self.camera.setPos(0, -8, 3)
        self.camera.lookAt(0, 0, 1)
        
    def process_commands(self, task):
        """Process commands from the main thread"""
        try:
            while not self.engine.command_queue.empty():
                command, data = self.engine.command_queue.get_nowait()
                
                if command == "update_avatar":
                    self.update_avatar_appearance(data)
                elif command == "move_avatar":
                    self.move_avatar_direction(data)
                elif command == "animate":
                    self.set_avatar_animation(data)
                elif command == "add_pet":
                    self.add_pet_to_scene(data)
                elif command == "remove_pet":
                    self.remove_pet_from_scene(data)
                elif command == "screenshot":
                    self.take_screenshot(data)
                    
        except queue.Empty:
            pass
        except Exception as e:
            print(f"Command processing error: {e}")
            
        return task.cont
        
    def update_avatar_appearance(self, state):
        """Update avatar clothing and appearance"""
        # Update clothing colors based on state
        if "shirt" in state and hasattr(self, 'body_node'):
            shirt_color = self.clay_colors.get(state["shirt"], (0.5, 0.5, 0.5, 1))
            self.body_node.setColor(*shirt_color)
            
        # Store state for reference
        self.engine.avatar_state.update(state)
        
    def move_avatar_direction(self, direction):
        """Move avatar with clay-like animation"""
        if not self.avatar_node:
            return
            
        # Get current position
        pos = self.avatar_node.getPos()
        step = 0.5
        
        # Calculate new position
        if direction == "left":
            new_pos = (pos.x - step, pos.y, pos.z)
        elif direction == "right":
            new_pos = (pos.x + step, pos.y, pos.z)
        elif direction == "up":
            new_pos = (pos.x, pos.y + step, pos.z)
        elif direction == "down":
            new_pos = (pos.x, pos.y - step, pos.z)
        else:
            return
            
        # Animate movement with clay-like squash and stretch
        self.animate_clay_movement(new_pos)
        
    def animate_clay_movement(self, target_pos):
        """Animate movement with clay-like squash and stretch"""
        if not self.avatar_node:
            return
            
        # Simple movement for now (can be enhanced with proper animation)
        self.avatar_node.setPos(*target_pos)
        
        # Add slight "bounce" effect
        original_scale = self.avatar_node.getScale()
        
        # Squash slightly during movement
        self.avatar_node.setScale(original_scale.x * 0.95, 
                                 original_scale.y * 1.05, 
                                 original_scale.z)
        
        # Return to normal scale after brief delay
        def restore_scale(task):
            if self.avatar_node:
                self.avatar_node.setScale(original_scale)
            return task.done
            
        self.taskMgr.doMethodLater(0.1, restore_scale, "restore_scale")
        
    def set_avatar_animation(self, animation):
        """Set avatar animation state"""
        # Placeholder for animation system
        # Can implement idle breathing, walking cycles, etc.
        pass
        
    def add_pet_to_scene(self, pet_data):
        """Add a 3D pet to the scene"""
        pet_type = pet_data["type"]
        pos = pet_data["pos"]
        
        if pet_type in self.pets_nodes:
            return  # Pet already exists
            
        # Create simple pet geometry
        if pet_type == "pet_cat":
            pet_node = self.create_clay_cat()
        elif pet_type == "pet_dog":
            pet_node = self.create_clay_dog()
        elif pet_type == "pet_bird":
            pet_node = self.create_clay_bird()
        elif pet_type == "pet_dragon":
            pet_node = self.create_clay_dragon()
        else:
            pet_node = self.create_clay_sphere("generic_pet", 0.3, 0.3, 0.3)
            
        pet_node.setPos(*pos)
        pet_node.reparentTo(self.render)
        self.pets_nodes[pet_type] = pet_node
        
    def create_clay_cat(self):
        """Create a claymation-style cat"""
        cat = self.render.attachNewNode("cat")
        
        # Body
        body = self.create_clay_sphere("cat_body", 0.8, 0.4, 0.4)
        body.setColor(0.9, 0.7, 0.4, 1)  # Orange cat
        body.reparentTo(cat)
        
        # Head  
        head = self.create_clay_sphere("cat_head", 0.4, 0.4, 0.4)
        head.setPos(0.6, 0, 0.1)
        head.setColor(0.9, 0.7, 0.4, 1)
        head.reparentTo(cat)
        
        # Ears
        ear1 = self.create_clay_sphere("cat_ear1", 0.1, 0.1, 0.2)
        ear1.setPos(0.7, -0.2, 0.3)
        ear1.setColor(0.8, 0.6, 0.3, 1)
        ear1.reparentTo(cat)
        
        ear2 = self.create_clay_sphere("cat_ear2", 0.1, 0.1, 0.2)
        ear2.setPos(0.7, 0.2, 0.3)
        ear2.setColor(0.8, 0.6, 0.3, 1)
        ear2.reparentTo(cat)
        
        # Tail
        tail = self.create_clay_sphere("cat_tail", 0.1, 0.1, 0.6)
        tail.setPos(-0.8, 0, 0.3)
        tail.setHpr(0, 45, 0)
        tail.setColor(0.9, 0.7, 0.4, 1)
        tail.reparentTo(cat)
        
        return cat
        
    def create_clay_dog(self):
        """Create a claymation-style dog"""
        dog = self.render.attachNewNode("dog")
        
        # Body (larger than cat)
        body = self.create_clay_sphere("dog_body", 1.0, 0.5, 0.5)
        body.setColor(0.6, 0.4, 0.2, 1)  # Brown dog
        body.reparentTo(dog)
        
        # Head
        head = self.create_clay_sphere("dog_head", 0.5, 0.4, 0.4)
        head.setPos(0.7, 0, 0.1)
        head.setColor(0.7, 0.5, 0.3, 1)
        head.reparentTo(dog)
        
        # Muzzle
        muzzle = self.create_clay_sphere("dog_muzzle", 0.3, 0.2, 0.2)
        muzzle.setPos(0.9, 0, -0.1)
        muzzle.setColor(0.8, 0.6, 0.4, 1)
        muzzle.reparentTo(dog)
        
        return dog
        
    def create_clay_bird(self):
        """Create a claymation-style bird"""
        bird = self.render.attachNewNode("bird")
        
        # Body
        body = self.create_clay_sphere("bird_body", 0.3, 0.3, 0.4)
        body.setColor(0.4, 0.6, 0.9, 1)  # Blue bird
        body.reparentTo(bird)
        
        # Head
        head = self.create_clay_sphere("bird_head", 0.2, 0.2, 0.2)
        head.setPos(0.3, 0, 0.2)
        head.setColor(0.5, 0.7, 1.0, 1)
        head.reparentTo(bird)
        
        # Wings (flattened spheres)
        wing1 = self.create_clay_sphere("bird_wing1", 0.4, 0.1, 0.2)
        wing1.setPos(0, -0.3, 0.1)
        wing1.setColor(0.3, 0.5, 0.8, 1)
        wing1.reparentTo(bird)
        
        wing2 = self.create_clay_sphere("bird_wing2", 0.4, 0.1, 0.2)
        wing2.setPos(0, 0.3, 0.1)
        wing2.setColor(0.3, 0.5, 0.8, 1)
        wing2.reparentTo(bird)
        
        return bird
        
    def create_clay_dragon(self):
        """Create a claymation-style dragon"""
        dragon = self.render.attachNewNode("dragon")
        
        # Body (larger and more majestic)
        body = self.create_clay_sphere("dragon_body", 1.2, 0.6, 0.6)
        body.setColor(0.2, 0.7, 0.3, 1)  # Green dragon
        body.reparentTo(dragon)
        
        # Head
        head = self.create_clay_sphere("dragon_head", 0.6, 0.5, 0.5)
        head.setPos(0.8, 0, 0.2)
        head.setColor(0.3, 0.8, 0.4, 1)
        head.reparentTo(dragon)
        
        # Wings
        wing1 = self.create_clay_sphere("dragon_wing1", 0.8, 0.1, 0.6)
        wing1.setPos(0, -0.7, 0.3)
        wing1.setColor(0.1, 0.6, 0.2, 1)
        wing1.reparentTo(dragon)
        
        wing2 = self.create_clay_sphere("dragon_wing2", 0.8, 0.1, 0.6)
        wing2.setPos(0, 0.7, 0.3)
        wing2.setColor(0.1, 0.6, 0.2, 1)
        wing2.reparentTo(dragon)
        
        return dragon
        
    def remove_pet_from_scene(self, pet_type):
        """Remove pet from scene"""
        if pet_type in self.pets_nodes:
            self.pets_nodes[pet_type].removeNode()
            del self.pets_nodes[pet_type]
            
    def take_screenshot(self, size):
        """Take a screenshot of the 3D scene"""
        width, height = size
        try:
            # This is a placeholder - actual screenshot functionality
            # would require setting up a texture and rendering to it
            self.engine.response_queue.put("screenshot_data_placeholder")
        except Exception as e:
            print(f"Screenshot error: {e}")
            self.engine.response_queue.put(None)


class TkinterAvatar3DWidget(tk.Frame):
    """Tkinter widget that embeds the 3D avatar"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.engine = Avatar3DEngine()
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI for the 3D avatar widget"""
        # Info label
        info_label = tk.Label(self, text="3D Claymation Avatar", 
                             font=("Arial", 12, "bold"))
        info_label.pack(pady=10)
        
        # Controls frame
        controls_frame = tk.Frame(self)
        controls_frame.pack(pady=10)
        
        # Initialize 3D button
        init_btn = tk.Button(controls_frame, text="Initialize 3D Avatar", 
                            command=self.initialize_3d)
        init_btn.pack(side="left", padx=5)
        
        # Movement buttons
        tk.Button(controls_frame, text="↑", width=3, 
                 command=lambda: self.move_avatar("up")).pack(side="left", padx=2)
        tk.Button(controls_frame, text="↓", width=3,
                 command=lambda: self.move_avatar("down")).pack(side="left", padx=2) 
        tk.Button(controls_frame, text="←", width=3,
                 command=lambda: self.move_avatar("left")).pack(side="left", padx=2)
        tk.Button(controls_frame, text="→", width=3,
                 command=lambda: self.move_avatar("right")).pack(side="left", padx=2)
        
        # Status label
        self.status_label = tk.Label(self, text="3D Engine: Not Initialized", 
                                    fg="red")
        self.status_label.pack(pady=5)
        
    def initialize_3d(self):
        """Initialize the 3D engine"""
        self.status_label.config(text="Initializing 3D Engine...", fg="orange")
        self.update()
        
        try:
            self.engine.initialize_3d_system()
            if self.engine.is_initialized:
                self.status_label.config(text="3D Engine: Running", fg="green")
            else:
                self.status_label.config(text="3D Engine: Failed to Initialize", fg="red")
        except Exception as e:
            self.status_label.config(text=f"3D Error: {str(e)[:50]}...", fg="red")
            
    def move_avatar(self, direction):
        """Move the 3D avatar"""
        if self.engine.is_initialized:
            self.engine.move_avatar(direction)
        
    def update_avatar_state(self, state_dict):
        """Update avatar appearance"""
        if self.engine.is_initialized:
            self.engine.update_avatar_state(state_dict)
            
    def add_pet(self, pet_type):
        """Add a pet to the 3D scene"""
        if self.engine.is_initialized:
            self.engine.add_pet(pet_type)
            
    def remove_pet(self, pet_type):
        """Remove a pet from the 3D scene"""
        if self.engine.is_initialized:
            self.engine.remove_pet(pet_type)


# Test the 3D avatar system
if __name__ == "__main__":
    root = tk.Tk()
    root.title("3D Claymation Avatar Test")
    root.geometry("600x400")
    
    avatar_widget = TkinterAvatar3DWidget(root)
    avatar_widget.pack(fill="both", expand=True, padx=20, pady=20)
    
    root.mainloop()