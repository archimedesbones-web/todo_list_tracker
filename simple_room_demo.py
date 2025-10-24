import tkinter as tk
import math

class SimpleRoomDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple /-----\\ Room Demo")
        
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white')
        self.canvas.pack()
        
        # Simple button to show different views
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        
        tk.Button(button_frame, text="Show Correct Room Shape", 
                 command=self.draw_correct_room).pack(side=tk.LEFT, padx=5)
        
        self.draw_correct_room()
        
    def draw_correct_room(self):
        self.canvas.delete("all")
        
        # Draw what the /-----\ room should actually look like in 3D
        self.canvas.create_text(400, 50, text="/-----\\ Room Shape (What You Should See)", 
                               font=("Arial", 16, "bold"))
        
        # Center point for drawing
        cx, cy = 400, 300
        
        # Define SYMMETRICAL TRAPEZOID floor first, then build walls straight up
        # Trapezoid: wide front edge, narrow back edge, perfectly symmetrical
        
        # FLOOR TRAPEZOID POINTS (all at ground level z=0)
        front_left = (-120, -80, 0)    # Wide front left
        front_right = (120, -80, 0)    # Wide front right (symmetrical)
        back_left = (-40, 120, 0)      # Narrow back left
        back_right = (40, 120, 0)      # Narrow back right (symmetrical)
        
        # This creates a symmetrical trapezoid floor:
        # Front edge: 240 units wide (120 - (-120))
        # Back edge: 80 units wide (40 - (-40))  
        # Perfectly centered and symmetrical
        
        # Wall height
        height = 150
        
        # Convert 3D to simple 2D (basic isometric view)
        def simple_3d_to_2d(x, y, z):
            # Simple isometric projection
            screen_x = cx + x * 0.8 - y * 0.4
            screen_y = cy - z - y * 0.2
            return (screen_x, screen_y)
        
        # Draw the floor outline first 
        floor_points = [
            simple_3d_to_2d(*front_left),   # front-left 
            simple_3d_to_2d(*front_right),  # front-right 
            simple_3d_to_2d(*back_right),   # back-right 
            simple_3d_to_2d(*back_left)     # back-left 
        ]
        self.canvas.create_polygon(floor_points, fill='lightgray', outline='black', width=2)
        
        # Back wall - BLUE (the "-----" part)
        back_wall_bottom = [simple_3d_to_2d(*back_left), simple_3d_to_2d(*back_right)]
        back_wall_top = [simple_3d_to_2d(back_left[0], back_left[1], height), 
                        simple_3d_to_2d(back_right[0], back_right[1], height)]
        
        back_wall_points = [back_wall_bottom[0], back_wall_bottom[1], 
                           back_wall_top[1], back_wall_top[0]]
        self.canvas.create_polygon(back_wall_points, fill='blue', outline='darkblue', width=2)
        
        # LEFT WALL - RED (the "/" part - diagonal across the room)
        # For "/" it should go from front-left to back-center-right to create the "/" slope
        # Let me try connecting front-left to a point that creates proper "/" angle
        left_connect_x = -10  # Slightly left of center at back
        left_wall_points = [
            simple_3d_to_2d(*front_left),                              # front-left floor
            simple_3d_to_2d(left_connect_x, back_left[1], 0),         # back connection floor
            simple_3d_to_2d(left_connect_x, back_left[1], height),    # back connection ceiling
            simple_3d_to_2d(front_left[0], front_left[1], height)     # front-left ceiling
        ]
        self.canvas.create_polygon(left_wall_points, fill='red', outline='darkred', width=2)
        
        # RIGHT WALL - GREEN (the "\" part - diagonal across the room) 
        # For "\" it should go from front-right to back-center-left to create the "\" slope
        right_connect_x = 10   # Slightly right of center at back
        right_wall_points = [
            simple_3d_to_2d(*front_right),                             # front-right floor
            simple_3d_to_2d(right_connect_x, back_right[1], 0),       # back connection floor
            simple_3d_to_2d(right_connect_x, back_right[1], height),  # back connection ceiling
            simple_3d_to_2d(front_right[0], front_right[1], height)   # front-right ceiling
        ]
        self.canvas.create_polygon(right_wall_points, fill='green', outline='darkgreen', width=2)
        
        # Add labels
        self.canvas.create_text(cx - 120, cy - 50, text="RED\n/", 
                               font=("Arial", 14, "bold"), fill='darkred')
        self.canvas.create_text(cx, cy - 80, text="BLUE -----", 
                               font=("Arial", 14, "bold"), fill='darkblue')
        self.canvas.create_text(cx + 120, cy - 50, text="GREEN\n\\", 
                               font=("Arial", 14, "bold"), fill='darkgreen')
        
        # Add explanation
        self.canvas.create_text(400, 550, 
                               text="SYMMETRICAL TRAPEZOID /-----\\ room: Floor is perfect trapezoid, walls built straight up!\nFront: 240 wide, Back: 80 wide, perfectly centered and symmetrical",
                               font=("Arial", 12), justify=tk.CENTER)

if __name__ == "__main__":
    app = SimpleRoomDemo()
    app.root.mainloop()