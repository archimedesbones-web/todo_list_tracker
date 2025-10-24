import tkinter as tk
import math

class SimpleOBJViewer:
    def __init__(self, obj_file):
        self.root = tk.Tk()
        self.root.title("OBJ File Viewer - " + obj_file)
        self.root.geometry("800x600")
        
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='black')
        self.canvas.pack()
        
        # Camera settings
        self.camera_x = 0
        self.camera_y = -1
        self.camera_z = -5
        self.rotation_y = 0
        
        # Load OBJ file
        self.vertices = []
        self.faces = []
        self.load_obj(obj_file)
        
        # Bind keys for camera control
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
        
        self.render()
        
    def load_obj(self, filename):
        """Load vertices and faces from OBJ file"""
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('v '):  # Vertex
                        parts = line.split()
                        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                        self.vertices.append([x, y, z])
                    elif line.startswith('f '):  # Face
                        parts = line.split()
                        # Handle different face formats (v, v/vt, v/vt/vn, v//vn)
                        face_vertices = []
                        for part in parts[1:]:
                            vertex_index = int(part.split('//')[0].split('/')[0]) - 1  # OBJ is 1-indexed
                            face_vertices.append(vertex_index)
                        if len(face_vertices) >= 3:
                            self.faces.append(face_vertices)
            
            print(f"Loaded {len(self.vertices)} vertices and {len(self.faces)} faces")
            
        except Exception as e:
            print(f"Error loading OBJ file: {e}")
    
    def project_3d_to_2d(self, x, y, z):
        """Project 3D coordinates to 2D screen coordinates"""
        # Apply camera rotation around Y axis
        cos_y = math.cos(self.rotation_y)
        sin_y = math.sin(self.rotation_y)
        
        # Rotate around Y axis
        rotated_x = x * cos_y - z * sin_y
        rotated_z = x * sin_y + z * cos_y
        
        # Apply camera translation
        world_x = rotated_x - self.camera_x
        world_y = y - self.camera_y
        world_z = rotated_z - self.camera_z
        
        # Simple perspective projection
        if world_z > -0.1:  # Prevent division by zero/negative
            world_z = -0.1
            
        scale = 200  # Projection scale
        screen_x = 400 + (world_x * scale) / (-world_z)
        screen_y = 300 - (world_y * scale) / (-world_z)  # Flip Y for screen coordinates
        
        return screen_x, screen_y
    
    def render(self):
        """Render the 3D model"""
        self.canvas.delete("all")
        
        # Project all vertices
        projected_vertices = []
        for vertex in self.vertices:
            x, y = self.project_3d_to_2d(vertex[0], vertex[1], vertex[2])
            projected_vertices.append((x, y))
        
        # Draw faces
        for i, face in enumerate(self.faces):
            if len(face) >= 3:
                # Get face vertices
                face_points = []
                for vertex_index in face:
                    if 0 <= vertex_index < len(projected_vertices):
                        face_points.extend(projected_vertices[vertex_index])
                
                if len(face_points) >= 6:  # At least 3 points (x,y pairs)
                    # Different colors for different faces
                    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
                    color = colors[i % len(colors)]
                    
                    # Draw the face
                    self.canvas.create_polygon(face_points, fill=color, outline='white', width=2)
        
        # Draw vertex points for reference
        for i, (x, y) in enumerate(projected_vertices):
            if 0 <= x <= 800 and 0 <= y <= 600:  # Only draw if on screen
                self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='yellow', outline='red')
                self.canvas.create_text(x+10, y-10, text=str(i+1), fill='white', font=('Arial', 8))
        
        # Draw instructions
        instructions = [
            "Controls:",
            "A/D - Rotate left/right",
            "W/S - Move forward/back", 
            "Q/E - Move up/down",
            "Arrow keys - Move around"
        ]
        
        for i, instruction in enumerate(instructions):
            self.canvas.create_text(10, 10 + i*15, text=instruction, anchor='nw', fill='white', font=('Arial', 10))
    
    def on_key_press(self, event):
        """Handle keyboard input for camera control"""
        step = 0.5
        rotation_step = 0.1
        
        if event.keysym == 'w':
            self.camera_z += step
        elif event.keysym == 's':
            self.camera_z -= step
        elif event.keysym == 'a':
            self.rotation_y -= rotation_step
        elif event.keysym == 'd':
            self.rotation_y += rotation_step
        elif event.keysym == 'q':
            self.camera_y += step
        elif event.keysym == 'e':
            self.camera_y -= step
        elif event.keysym == 'Left':
            self.camera_x -= step
        elif event.keysym == 'Right':
            self.camera_x += step
        elif event.keysym == 'Up':
            self.camera_z += step
        elif event.keysym == 'Down':
            self.camera_z -= step
        
        self.render()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    viewer = SimpleOBJViewer("simple_room.obj")
    viewer.run()