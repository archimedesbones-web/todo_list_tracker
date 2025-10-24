"""
Ultra-Simple 3D Avatar System
No threading, minimal Panda3D usage to avoid conflicts
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

class MockAvatar3DWidget(tk.Frame):
    """Mock 3D widget that simulates 3D avatar functionality"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.avatar_state = {
            "x": 0, "y": 0,
            "shirt": "t_shirt_blue",
            "pants": "jeans_blue",
            "hat": "none"
        }
        self.pets = []
        self.is_initialized = False
        self.setup_ui()
        
    def setup_ui(self):
        """Set up a mock 3D interface with enhanced 2.5D graphics"""
        # Title
        title = tk.Label(self, text="🎮 Enhanced Claymation Avatar", 
                        font=("Arial", 12, "bold"))
        title.pack(pady=5)
        
        # Canvas for enhanced 2.5D avatar
        self.canvas = tk.Canvas(self, width=400, height=300, bg="#f5f5dc")
        self.canvas.pack(pady=10)
        
        # Control panel
        controls = tk.Frame(self)
        controls.pack(pady=5)
        
        # Initialize button
        self.init_btn = tk.Button(controls, text="Initialize Enhanced Avatar", 
                                 command=self.initialize_enhanced,
                                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.init_btn.pack(side="left", padx=5)
        
        # Movement controls
        move_frame = tk.Frame(controls)
        move_frame.pack(side="left", padx=20)
        
        tk.Button(move_frame, text="↑", width=3, 
                 command=lambda: self.move_avatar("up")).grid(row=0, column=1)
        tk.Button(move_frame, text="←", width=3,
                 command=lambda: self.move_avatar("left")).grid(row=1, column=0)
        tk.Button(move_frame, text="↓", width=3,
                 command=lambda: self.move_avatar("down")).grid(row=1, column=1)
        tk.Button(move_frame, text="→", width=3,
                 command=lambda: self.move_avatar("right")).grid(row=1, column=2)
        
        # Status
        self.status_label = tk.Label(self, text="Ready to initialize enhanced claymation avatar",
                                    fg="#666")
        self.status_label.pack()
        
        # Draw initial scene
        self.draw_enhanced_scene()
        
    def initialize_enhanced(self):
        """Initialize the enhanced 2.5D avatar system"""
        self.init_btn.config(text="Initializing...", state="disabled")
        self.status_label.config(text="Creating enhanced claymation experience...", fg="orange")
        self.update()
        
        # Simulate initialization
        self.after(1500, self._complete_initialization)
        
    def _complete_initialization(self):
        """Complete the initialization process"""
        self.is_initialized = True
        self.init_btn.config(text="✨ Enhanced Avatar Active", bg="#2E7D32", state="disabled")
        self.status_label.config(text="🎭 Enhanced Claymation Avatar Ready!", fg="green")
        
        # Add some flair to the scene
        self.draw_enhanced_scene()
        self._add_animation_effects()
        
    def draw_enhanced_scene(self):
        """Draw an enhanced 2.5D claymation-style scene"""
        self.canvas.delete("all")
        
        # Enhanced background with gradient effect
        for i in range(300):
            color_intensity = 245 - (i // 10)
            color = f"#{color_intensity:02x}{color_intensity-10:02x}{color_intensity-20:02x}"
            self.canvas.create_line(0, i, 400, i, fill=color, width=1)
        
        # Draw enhanced floor with clay texture pattern
        for x in range(0, 400, 20):
            for y in range(250, 300, 20):
                # Clay tile effect
                self.canvas.create_rectangle(x, y, x+18, y+18, 
                                           fill="#e8dcc0", outline="#d4c5a9", width=1)
                # Add slight texture variation
                if (x + y) % 40 == 0:
                    self.canvas.create_oval(x+7, y+7, x+11, y+11, 
                                          fill="#d4c5a9", outline="")
        
        # Enhanced avatar with clay-like styling
        self.draw_clay_avatar()
        
        # Draw any pets with enhanced style
        self.draw_clay_pets()
        
        # Add depth and lighting effects
        self.add_lighting_effects()
        
    def draw_clay_avatar(self):
        """Draw an enhanced claymation-style avatar"""
        x = 200 + self.avatar_state["x"] * 5
        y = 180 + self.avatar_state["y"] * 5
        
        # Get clothing colors
        shirt_colors = {
            "t_shirt_blue": "#4169e1",
            "t_shirt_red": "#dc143c", 
            "hoodie_green": "#32cd32",
            "polo_yellow": "#ffd700",
            "sweater_purple": "#9370db",
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
            "pants_camo": "#556b2f",
            "pants_rainbow": "#ff69b4",
            "pants_gold": "#b8860b"
        }
        
        shirt_color = shirt_colors.get(self.avatar_state["shirt"], "#4169e1")
        pants_color = pants_colors.get(self.avatar_state["pants"], "#1e90ff")
        
        # Shadow with clay-like softness
        for i in range(3):
            shadow_alpha = 50 - i * 15
            self.canvas.create_oval(x-20+i, y+45+i, x+20-i, y+55-i, 
                                  fill="#888888", outline="", stipple="gray50")
        
        # Enhanced legs with clay texture
        self.draw_clay_shape(x-10, y+10, x-2, y+45, pants_color, "leg")
        self.draw_clay_shape(x+2, y+10, x+10, y+45, pants_color, "leg")
        
        # Enhanced body with clay shading
        self.draw_clay_shape(x-15, y-5, x+15, y+15, shirt_color, "body")
        
        # Arms with clay texture
        self.draw_clay_shape(x-20, y-2, x-15, y+12, shirt_color, "arm")
        self.draw_clay_shape(x+15, y-2, x+20, y+12, shirt_color, "arm") 
        
        # Hands
        self.canvas.create_oval(x-22, y+10, x-16, y+16, 
                              fill="#fdbcb4", outline="#e8a68c", width=2)
        self.canvas.create_oval(x+16, y+10, x+22, y+16,
                              fill="#fdbcb4", outline="#e8a68c", width=2)
        
        # Enhanced head with clay features
        self.canvas.create_oval(x-12, y-25, x+12, y-5, 
                              fill="#fdbcb4", outline="#e8a68c", width=2)
        
        # Clay-style facial features
        # Eyes
        self.canvas.create_oval(x-6, y-20, x-2, y-16, fill="#000000")
        self.canvas.create_oval(x+2, y-20, x+6, y-16, fill="#000000")
        # Eye highlights
        self.canvas.create_oval(x-5, y-19, x-3, y-17, fill="#ffffff")
        self.canvas.create_oval(x+3, y-19, x+5, y-17, fill="#ffffff")
        
        # Nose
        self.canvas.create_oval(x-2, y-16, x+2, y-12, 
                              fill="#f0a898", outline="#e8a68c")
        
        # Mouth
        self.canvas.create_arc(x-4, y-14, x+4, y-8, 
                             start=0, extent=180, fill="#d87878", width=2, style="pieslice")
        
        # Enhanced hat rendering
        self.draw_clay_hat(x, y)
        
        # Feet
        self.canvas.create_oval(x-12, y+43, x-6, y+48, fill="#000000")
        self.canvas.create_oval(x+6, y+43, x+12, y+48, fill="#000000")
        
    def draw_clay_shape(self, x1, y1, x2, y2, color, shape_type):
        """Draw a shape with clay-like texture and shading"""
        # Main shape
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", width=0)
        
        # Add clay texture with stippling
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="", outline=color, 
                                   stipple="gray25", width=1)
        
        # Add highlights and shadows for clay effect
        highlight_color = self._lighten_color(color, 1.2)
        shadow_color = self._darken_color(color, 0.8)
        
        # Top highlight
        self.canvas.create_line(x1, y1, x2, y1, fill=highlight_color, width=2)
        # Left highlight  
        self.canvas.create_line(x1, y1, x1, y2, fill=highlight_color, width=2)
        # Bottom shadow
        self.canvas.create_line(x1, y2, x2, y2, fill=shadow_color, width=2)
        # Right shadow
        self.canvas.create_line(x2, y1, x2, y2, fill=shadow_color, width=2)
        
    def draw_clay_hat(self, x, y):
        """Draw enhanced clay-style hats"""
        hat = self.avatar_state.get("hat", "none")
        
        if hat == "baseball_cap":
            # Cap with clay shading
            self.canvas.create_arc(x-13, y-30, x+13, y-15, 
                                 start=0, extent=180, fill="#ff4500", 
                                 outline="#cc3300", width=2, style="pieslice")
            # Bill with clay texture
            self.canvas.create_polygon(x-13, y-22, x-20, y-20, x-20, y-18, x-13, y-20,
                                     fill="#ff4500", outline="#cc3300", width=2)
            
        elif hat == "wizard_hat":
            # Wizard hat with clay texture
            self.canvas.create_polygon(x-8, y-25, x, y-40, x+8, y-25,
                                     fill="#6a0dad", outline="#4b0082", width=2)
            # Brim
            self.canvas.create_oval(x-12, y-27, x+12, y-23, 
                                  fill="#4b0082", outline="#301934", width=2)
            
        # Add more hats as needed...
        
    def draw_clay_pets(self):
        """Draw enhanced clay-style pets"""
        pet_positions = [(100, 200), (300, 220), (150, 240), (250, 190)]
        
        for i, pet_type in enumerate(self.pets):
            if i >= len(pet_positions):
                break
                
            px, py = pet_positions[i]
            
            if pet_type == "pet_cat":
                self.draw_clay_cat(px, py)
            elif pet_type == "pet_dog":
                self.draw_clay_dog(px, py)
            elif pet_type == "pet_bird":
                self.draw_clay_bird(px, py)
            elif pet_type == "pet_dragon":
                self.draw_clay_dragon(px, py)
                
    def draw_clay_cat(self, x, y):
        """Draw enhanced claymation cat"""
        # Body
        self.canvas.create_oval(x-15, y-8, x+15, y+8, 
                              fill="#ffa500", outline="#ff8c00", width=2)
        # Head
        self.canvas.create_oval(x+10, y-10, x+25, y+5, 
                              fill="#ffa500", outline="#ff8c00", width=2)
        # Ears
        self.canvas.create_polygon(x+12, y-10, x+16, y-16, x+20, y-10,
                                 fill="#ffb84d", outline="#ff8c00", width=1)
        self.canvas.create_polygon(x+15, y-10, x+19, y-16, x+23, y-10,
                                 fill="#ffb84d", outline="#ff8c00", width=1)
        # Tail
        self.canvas.create_arc(x-25, y-15, x-5, y+5, 
                             start=200, extent=140, outline="#ff8c00", width=3, style="arc")
        # Eyes
        self.canvas.create_oval(x+14, y-6, x+16, y-4, fill="#000000")
        self.canvas.create_oval(x+19, y-6, x+21, y-4, fill="#000000")
        
    def draw_clay_dog(self, x, y):
        """Draw enhanced claymation dog"""
        # Body (larger than cat)
        self.canvas.create_oval(x-18, y-10, x+18, y+10, 
                              fill="#8b4513", outline="#654321", width=2)
        # Head
        self.canvas.create_oval(x+12, y-12, x+30, y+6, 
                              fill="#a0522d", outline="#654321", width=2)
        # Muzzle
        self.canvas.create_oval(x+25, y-2, x+35, y+6, 
                              fill="#d2b48c", outline="#8b4513", width=2)
        # Ears (floppy)
        self.canvas.create_oval(x+10, y-10, x+18, y-2, 
                              fill="#654321", outline="#4a2f1a", width=1)
        self.canvas.create_oval(x+24, y-10, x+32, y-2, 
                              fill="#654321", outline="#4a2f1a", width=1)
        # Eyes
        self.canvas.create_oval(x+16, y-6, x+18, y-4, fill="#000000")
        self.canvas.create_oval(x+22, y-6, x+24, y-4, fill="#000000")
        
    def draw_clay_bird(self, x, y):
        """Draw enhanced claymation bird"""
        # Body
        self.canvas.create_oval(x-8, y-8, x+8, y+8, 
                              fill="#87ceeb", outline="#4682b4", width=2)
        # Head
        self.canvas.create_oval(x+6, y-10, x+16, y, 
                              fill="#b0e0e6", outline="#4682b4", width=2)
        # Beak
        self.canvas.create_polygon(x+16, y-5, x+22, y-3, x+16, y-1,
                                 fill="#ffa500", outline="#ff8c00", width=1)
        # Wings
        self.canvas.create_arc(x-12, y-6, x+4, y+6, 
                             start=90, extent=180, outline="#4682b4", width=3, style="arc")
        # Eye
        self.canvas.create_oval(x+8, y-6, x+10, y-4, fill="#000000")
        
    def draw_clay_dragon(self, x, y):
        """Draw enhanced claymation dragon"""
        # Body (majestic)
        self.canvas.create_oval(x-20, y-12, x+20, y+12, 
                              fill="#228b22", outline="#006400", width=2)
        # Head
        self.canvas.create_oval(x+15, y-15, x+35, y+5, 
                              fill="#32cd32", outline="#006400", width=2)
        # Wings
        self.canvas.create_arc(x-25, y-20, x+5, y+5, 
                             start=45, extent=90, outline="#006400", width=4, style="arc")
        self.canvas.create_arc(x-5, y-20, x+25, y+5, 
                             start=45, extent=90, outline="#006400", width=4, style="arc")
        # Eyes (glowing)
        self.canvas.create_oval(x+20, y-10, x+22, y-8, fill="#ff0000")
        self.canvas.create_oval(x+26, y-10, x+28, y-8, fill="#ff0000")
        # Spikes
        for spike_x in range(x-15, x+15, 6):
            self.canvas.create_polygon(spike_x, y-12, spike_x+3, y-18, spike_x+6, y-12,
                                     fill="#006400", outline="#004400", width=1)
        
    def add_lighting_effects(self):
        """Add clay-style lighting and depth effects"""
        # Soft ambient lighting overlay
        for i in range(5):
            alpha = 20 - i * 3
            self.canvas.create_rectangle(50 + i*2, 50 + i*2, 
                                       350 - i*2, 250 - i*2, 
                                       fill="", outline="#ffffff", stipple="gray12")
        
    def _add_animation_effects(self):
        """Add subtle animation effects to enhance the clay feel"""
        # This could add gentle breathing animation, eye blinks, etc.
        self._animate_breathing()
        
    def _animate_breathing(self):
        """Subtle breathing animation for clay avatar"""
        if not self.is_initialized:
            return
            
        # Subtle scale changes could be added here
        # For now, we'll just refresh the scene periodically
        self.after(3000, self._animate_breathing)
        
    def _lighten_color(self, color, factor):
        """Lighten a hex color for highlights"""
        try:
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            rgb = tuple(min(255, int(c * factor)) for c in rgb)
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        except:
            return "#ffffff"
            
    def _darken_color(self, color, factor):
        """Darken a hex color for shadows"""
        try:
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            rgb = tuple(max(0, int(c * factor)) for c in rgb)
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        except:
            return "#000000"
    
    # Interface methods to match expected API
    def move_avatar(self, direction):
        """Move avatar with enhanced animation"""
        if direction == "left":
            self.avatar_state["x"] -= 1
        elif direction == "right":
            self.avatar_state["x"] += 1
        elif direction == "up":
            self.avatar_state["y"] -= 1
        elif direction == "down":
            self.avatar_state["y"] += 1
            
        # Redraw with new position
        self.draw_enhanced_scene()
        
        # Show movement feedback
        if self.is_initialized:
            self.status_label.config(text=f"🎭 Avatar moved {direction}!", fg="green")
            self.after(1000, lambda: self.status_label.config(
                text="🎭 Enhanced Claymation Avatar Ready!", fg="green"))
    
    def update_avatar_state(self, state_dict):
        """Update avatar appearance"""
        self.avatar_state.update(state_dict)
        if self.is_initialized:
            self.draw_enhanced_scene()
            self.status_label.config(text="🎨 Avatar appearance updated!", fg="green")
            self.after(1000, lambda: self.status_label.config(
                text="🎭 Enhanced Claymation Avatar Ready!", fg="green"))
    
    def add_pet(self, pet_type):
        """Add a pet to the scene"""
        if pet_type not in self.pets:
            self.pets.append(pet_type)
            if self.is_initialized:
                self.draw_enhanced_scene()
                self.status_label.config(text=f"🐾 Added {pet_type}!", fg="green")
                self.after(1500, lambda: self.status_label.config(
                    text="🎭 Enhanced Claymation Avatar Ready!", fg="green"))
    
    def remove_pet(self, pet_type):
        """Remove a pet from the scene"""
        if pet_type in self.pets:
            self.pets.remove(pet_type)
            if self.is_initialized:
                self.draw_enhanced_scene()
                self.status_label.config(text=f"🐾 Removed {pet_type}!", fg="orange")
                self.after(1500, lambda: self.status_label.config(
                    text="🎭 Enhanced Claymation Avatar Ready!", fg="green"))


# Test the enhanced avatar
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Enhanced Claymation Avatar")
    root.geometry("500x400")
    
    avatar = MockAvatar3DWidget(root)
    avatar.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Auto-initialize for testing
    root.after(500, avatar.initialize_enhanced)
    
    root.mainloop()