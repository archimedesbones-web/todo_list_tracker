import tkinter as tk
import math

class TestRoomShape:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Room Shape Test - /-----\\")
        
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white')
        self.canvas.pack()
        
        # Draw the room shape from top-down view first
        self.draw_top_down_view()
        
        # Then draw the 3D perspective view
        self.draw_3d_view()
        
    def draw_top_down_view(self):
        # Draw top-down view on the left side
        self.canvas.create_text(200, 50, text="Top-Down View (Bird's Eye)", font=("Arial", 14, "bold"))
        
        # Room coordinates (scaled for display)
        scale = 20
        offset_x, offset_y = 200, 200
        
        # Define room points
        back_left = (-3, 4)
        back_right = (3, 4)
        front_left = (-6, -2)
        front_right = (6, -2)
        
        # Convert to screen coordinates
        def to_screen(x, y):
            return (offset_x + x * scale, offset_y - y * scale)  # Flip Y for screen coords
        
        # Draw the room outline
        points = [
            to_screen(*front_left),   # Front left
            to_screen(*back_left),    # Back left  
            to_screen(*back_right),   # Back right
            to_screen(*front_right),  # Front right
            to_screen(*front_left)    # Close the shape
        ]
        
        # Draw the room outline
        for i in range(len(points)-1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            self.canvas.create_line(x1, y1, x2, y2, width=3, fill='blue')
            
        # Label the walls
        self.canvas.create_text(offset_x - 60, offset_y + 40, text="/", font=("Arial", 20, "bold"), fill='red')
        self.canvas.create_text(offset_x, offset_y + 80, text="-----", font=("Arial", 12, "bold"), fill='red')
        self.canvas.create_text(offset_x + 60, offset_y + 40, text="\\", font=("Arial", 20, "bold"), fill='red')
        
        # Add coordinate labels
        self.canvas.create_text(*to_screen(*front_left), text=f"FL{front_left}", anchor="nw")
        self.canvas.create_text(*to_screen(*back_left), text=f"BL{back_left}", anchor="sw")
        self.canvas.create_text(*to_screen(*back_right), text=f"BR{back_right}", anchor="se")
        self.canvas.create_text(*to_screen(*front_right), text=f"FR{front_right}", anchor="ne")
        
    def draw_3d_view(self):
        # Draw 3D perspective view on the right side
        self.canvas.create_text(600, 50, text="3D Perspective View", font=("Arial", 14, "bold"))
        
        offset_x, offset_y = 600, 400
        
        # Simple isometric projection
        def project_3d(x, y, z):
            # Basic isometric projection
            screen_x = offset_x + (x - y) * 15
            screen_y = offset_y - z * 20 - (x + y) * 8
            return (screen_x, screen_y)
        
        # Room coordinates
        back_left = (-3, 4, 0)
        back_right = (3, 4, 0)  
        front_left = (-6, -2, 0)
        front_right = (6, -2, 0)
        
        wall_height = 3
        back_left_top = (-3, 4, wall_height)
        back_right_top = (3, 4, wall_height)
        front_left_top = (-6, -2, wall_height)
        front_right_top = (6, -2, wall_height)
        
        # Draw floor outline
        floor_points = [
            project_3d(*front_left),
            project_3d(*back_left),
            project_3d(*back_right),
            project_3d(*front_right)
        ]
        
        self.canvas.create_polygon(floor_points, fill='lightgray', outline='black', width=2)
        
        # Draw walls
        # Back wall
        back_wall = [
            project_3d(*back_left),
            project_3d(*back_right),
            project_3d(*back_right_top),
            project_3d(*back_left_top)
        ]
        self.canvas.create_polygon(back_wall, fill='lightblue', outline='black', width=2)
        
        # Left wall (/)
        left_wall = [
            project_3d(*front_left),
            project_3d(*back_left),
            project_3d(*back_left_top),
            project_3d(*front_left_top)
        ]
        self.canvas.create_polygon(left_wall, fill='lightgreen', outline='black', width=2)
        
        # Right wall (\)
        right_wall = [
            project_3d(*back_right),
            project_3d(*front_right),
            project_3d(*front_right_top),
            project_3d(*back_right_top)
        ]
        self.canvas.create_polygon(right_wall, fill='lightyellow', outline='black', width=2)
        
        # Add labels
        self.canvas.create_text(offset_x - 50, offset_y - 100, text="/", font=("Arial", 16, "bold"), fill='green')
        self.canvas.create_text(offset_x, offset_y - 120, text="-----", font=("Arial", 12, "bold"), fill='blue')
        self.canvas.create_text(offset_x + 50, offset_y - 100, text="\\", font=("Arial", 16, "bold"), fill='orange')

if __name__ == "__main__":
    app = TestRoomShape()
    app.root.mainloop()