"""
Simplified 3D Claymation Avatar System
Uses basic Panda3D primitives without external model dependencies
"""

import tkinter as tk
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import CardMaker, Material, AmbientLight, DirectionalLight, NodePath
from direct.gui.DirectGui import *
import threading
import queue
import time

class SimpleAvatar3DEngine:
    """Simplified 3D rendering engine for claymation-style avatars"""
    
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
            return True
            
        try:
            self.render_thread = threading.Thread(target=self._run_panda3d, daemon=True)
            self.render_thread.start()
            
            # Wait for initialization with timeout
            start_time = time.time()
            while not self.is_initialized and time.time() - start_time < 5:
                time.sleep(0.1)
                
            return self.is_initialized
        except Exception as e:
            print(f"3D Engine initialization failed: {e}")
            return False
            
    def _run_panda3d(self):
        """Run Panda3D in separate thread"""
        try:
            self.app = SimpleClayAvatar3D(self)
            self.is_initialized = True
            self.app.run()
        except Exception as e:
            print(f"3D Engine Error: {e}")
            self.is_initialized = False
            
    def update_avatar_state(self, state_dict):
        """Update avatar appearance and position"""
        if self.is_initialized:
            self.command_queue.put(("update_avatar", state_dict))
        
    def move_avatar(self, direction):
        """Move avatar in specified direction"""
        if self.is_initialized:
            self.command_queue.put(("move_avatar", direction))
        
    def add_pet(self, pet_type, position=None):
        """Add a pet to the scene"""
        if self.is_initialized:
            if position is None:
                position = (2, 2, 0)
            self.command_queue.put(("add_pet", {"type": pet_type, "pos": position}))
        
    def remove_pet(self, pet_type):
        """Remove pet from scene"""
        if self.is_initialized:
            self.command_queue.put(("remove_pet", pet_type))


class SimpleClayAvatar3D(ShowBase):
    """Simplified Panda3D application for claymation avatar"""
    
    def __init__(self, engine):
        try:
            ShowBase.__init__(self)
            self.engine = engine
            self.avatar_node = None
            self.pets_nodes = {}
            
            # Set up the simplified 3D environment
            self.setup_simple_scene()
            self.create_simple_avatar()
            self.setup_simple_lighting()
            self.setup_camera()
            
            # Start command processing task
            self.taskMgr.add(self.process_commands, "process_commands")
        except Exception as e:
            print(f"SimpleClayAvatar3D init error: {e}")
            raise
        
    def setup_simple_scene(self):
        """Set up a basic 3D scene without complex geometry"""
        try:
            # Disable default mouse controls
            self.disableMouse()
            
            # Set background color
            self.setBackgroundColor(0.9, 0.85, 0.75, 1)
            
            # Create simple floor using CardMaker
            cm = CardMaker("floor")
            cm.setFrame(-5, 5, -5, 5)
            floor = NodePath(cm.generate())
            floor.setPos(0, 0, -1)
            floor.setColor(0.8, 0.7, 0.6, 1)
            floor.reparentTo(self.render)
        except Exception as e:
            print(f"Scene setup error: {e}")
        
    def create_simple_avatar(self):
        """Create a very simple avatar using basic shapes"""
        try:
            self.avatar_node = self.render.attachNewNode("avatar")
            
            # Head (using CardMaker card)
            cm_head = CardMaker("head")
            cm_head.setFrame(-0.5, 0.5, -0.5, 0.5)
            head = NodePath(cm_head.generate())
            head.setPos(0, 0, 2)
            head.setColor(0.95, 0.8, 0.7, 1)  # Skin color
            head.reparentTo(self.avatar_node)
            
            # Body
            cm_body = CardMaker("body")
            cm_body.setFrame(-0.8, 0.8, -1, 1)
            body = NodePath(cm_body.generate())
            body.setPos(0, 0, 0.5)
            body.setColor(0.3, 0.5, 0.8, 1)  # Blue shirt
            body.reparentTo(self.avatar_node)
            self.body_node = body
            
            # Legs
            cm_leg = CardMaker("leg")
            cm_leg.setFrame(-0.3, 0.3, -1, 1)
            
            leg_left = NodePath(cm_leg.generate())
            leg_left.setPos(-0.4, 0, -1)
            leg_left.setColor(0.2, 0.3, 0.6, 1)  # Blue jeans
            leg_left.reparentTo(self.avatar_node)
            
            leg_right = NodePath(cm_leg.generate())
            leg_right.setPos(0.4, 0, -1)
            leg_right.setColor(0.2, 0.3, 0.6, 1)
            leg_right.reparentTo(self.avatar_node)
            
            # Store references for updates
            self.head_node = head
            self.legs_left = leg_left
            self.legs_right = leg_right
            
        except Exception as e:
            print(f"Avatar creation error: {e}")
        
    def setup_simple_lighting(self):
        """Set up basic lighting"""
        try:
            # Ambient light
            ambient_light = AmbientLight('ambient_light')
            ambient_light.setColor(0.4, 0.4, 0.4, 1)
            self.render.setLight(self.render.attachNewNode(ambient_light))
            
            # Main light
            main_light = DirectionalLight('main_light')
            main_light.setColor(0.8, 0.8, 0.8, 1)
            main_light.setDirection(-1, -1, -1)
            self.render.setLight(self.render.attachNewNode(main_light))
        except Exception as e:
            print(f"Lighting setup error: {e}")
        
    def setup_camera(self):
        """Position camera for avatar view"""
        try:
            self.camera.setPos(0, -6, 2)
            self.camera.lookAt(0, 0, 1)
        except Exception as e:
            print(f"Camera setup error: {e}")
        
    def process_commands(self, task):
        """Process commands from the main thread"""
        try:
            while not self.engine.command_queue.empty():
                command, data = self.engine.command_queue.get_nowait()
                
                if command == "update_avatar":
                    self.update_avatar_appearance(data)
                elif command == "move_avatar":
                    self.move_avatar_direction(data)
                elif command == "add_pet":
                    self.add_simple_pet(data)
                elif command == "remove_pet":
                    self.remove_simple_pet(data)
                    
        except queue.Empty:
            pass
        except Exception as e:
            print(f"Command processing error: {e}")
            
        return task.cont
        
    def update_avatar_appearance(self, state):
        """Update avatar clothing colors"""
        try:
            if "shirt" in state and self.body_node:
                # Simple color mapping for shirts
                shirt_colors = {
                    "t_shirt_blue": (0.3, 0.5, 0.8, 1),
                    "t_shirt_red": (0.8, 0.2, 0.2, 1),
                    "hoodie_green": (0.2, 0.6, 0.2, 1),
                }
                color = shirt_colors.get(state["shirt"], (0.5, 0.5, 0.5, 1))
                self.body_node.setColor(*color)
                
            if "pants" in state and hasattr(self, 'legs_left'):
                # Simple color mapping for pants
                pants_colors = {
                    "jeans_blue": (0.2, 0.3, 0.6, 1),
                    "jeans_black": (0.1, 0.1, 0.1, 1),
                    "khaki": (0.7, 0.6, 0.4, 1),
                }
                color = pants_colors.get(state["pants"], (0.3, 0.3, 0.3, 1))
                self.legs_left.setColor(*color)
                self.legs_right.setColor(*color)
                
        except Exception as e:
            print(f"Appearance update error: {e}")
        
    def move_avatar_direction(self, direction):
        """Move avatar with simple translation"""
        try:
            if not self.avatar_node:
                return
                
            pos = self.avatar_node.getPos()
            step = 0.5
            
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
                
            self.avatar_node.setPos(*new_pos)
        except Exception as e:
            print(f"Movement error: {e}")
        
    def add_simple_pet(self, pet_data):
        """Add a simple pet shape"""
        try:
            pet_type = pet_data["type"]
            pos = pet_data["pos"]
            
            if pet_type in self.pets_nodes:
                return
                
            # Create simple pet using CardMaker
            cm = CardMaker(pet_type)
            cm.setFrame(-0.3, 0.3, -0.3, 0.3)
            pet = NodePath(cm.generate())
            pet.setPos(*pos)
            
            # Simple pet colors
            if pet_type == "pet_cat":
                pet.setColor(0.9, 0.7, 0.4, 1)  # Orange
            elif pet_type == "pet_dog":
                pet.setColor(0.6, 0.4, 0.2, 1)  # Brown
            elif pet_type == "pet_bird":
                pet.setColor(0.4, 0.6, 0.9, 1)  # Blue
            elif pet_type == "pet_dragon":
                pet.setColor(0.2, 0.7, 0.3, 1)  # Green
            else:
                pet.setColor(0.5, 0.5, 0.5, 1)  # Gray
                
            pet.reparentTo(self.render)
            self.pets_nodes[pet_type] = pet
        except Exception as e:
            print(f"Pet creation error: {e}")
        
    def remove_simple_pet(self, pet_type):
        """Remove pet from scene"""
        try:
            if pet_type in self.pets_nodes:
                self.pets_nodes[pet_type].removeNode()
                del self.pets_nodes[pet_type]
        except Exception as e:
            print(f"Pet removal error: {e}")


class SimpleTkinterAvatar3DWidget(tk.Frame):
    """Simplified Tkinter widget for 3D avatar"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.engine = SimpleAvatar3DEngine()
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI for the 3D avatar widget"""
        # Info label
        info_label = tk.Label(self, text="🎮 Simple 3D Claymation Avatar", 
                             font=("Arial", 12, "bold"))
        info_label.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(self, text="3D Engine: Not Initialized", 
                                    fg="red", font=("Arial", 10))
        self.status_label.pack(pady=5)
        
        # Controls frame
        controls_frame = tk.Frame(self)
        controls_frame.pack(pady=10)
        
        # Initialize button
        self.init_btn = tk.Button(controls_frame, text="Initialize 3D Avatar", 
                                 command=self.initialize_3d, bg="#4CAF50", fg="white",
                                 font=("Arial", 10, "bold"))
        self.init_btn.pack(side="left", padx=5)
        
        # Movement buttons
        move_frame = tk.Frame(controls_frame)
        move_frame.pack(side="left", padx=20)
        
        tk.Button(move_frame, text="↑", width=3, 
                 command=lambda: self.move_avatar("up")).grid(row=0, column=1, padx=2)
        tk.Button(move_frame, text="←", width=3,
                 command=lambda: self.move_avatar("left")).grid(row=1, column=0, padx=2)
        tk.Button(move_frame, text="↓", width=3,
                 command=lambda: self.move_avatar("down")).grid(row=1, column=1, padx=2)
        tk.Button(move_frame, text="→", width=3,
                 command=lambda: self.move_avatar("right")).grid(row=1, column=2, padx=2)
        
        # Info text
        info_text = tk.Label(self, text="Click 'Initialize 3D Avatar' to start the claymation system.\nUse arrow buttons to move your avatar around!",
                           justify="center", wraplength=400)
        info_text.pack(pady=10)
        
    def initialize_3d(self):
        """Initialize the 3D engine"""
        self.status_label.config(text="Initializing 3D Engine...", fg="orange")
        self.init_btn.config(state="disabled", text="Initializing...")
        self.update()
        
        try:
            success = self.engine.initialize_3d_system()
            if success:
                self.status_label.config(text="✅ 3D Engine: Running Successfully!", fg="green")
                self.init_btn.config(text="3D Avatar Active", bg="#2E7D32")
            else:
                self.status_label.config(text="❌ 3D Engine: Failed to Initialize", fg="red")
                self.init_btn.config(state="normal", text="Try Again", bg="#f44336")
        except Exception as e:
            self.status_label.config(text=f"❌ 3D Error: {str(e)[:30]}...", fg="red")
            self.init_btn.config(state="normal", text="Try Again", bg="#f44336")
            
    def move_avatar(self, direction):
        """Move the 3D avatar"""
        if self.engine.is_initialized:
            self.engine.move_avatar(direction)
        else:
            self.status_label.config(text="Please initialize 3D engine first", fg="orange")
        
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


# Test the simplified 3D avatar system
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simple 3D Claymation Avatar Test")
    root.geometry("500x400")
    
    avatar_widget = SimpleTkinterAvatar3DWidget(root)
    avatar_widget.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Auto-initialize for testing
    root.after(1000, avatar_widget.initialize_3d)
    
    root.mainloop()