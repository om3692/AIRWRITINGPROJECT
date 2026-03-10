import numpy as np
import cv2
from collections import deque

class VirtualCanvas:
    def __init__(self, width, height):
        # We now store a list of dictionary objects. 
        # Each stroke remembers its own color, thickness, and chronological points.
        self.strokes = [{'color': (255, 0, 0), 'thickness': 10, 'points': deque(maxlen=1024)}]
        self.paint_window = np.zeros((height, width, 3), dtype=np.uint8)

    def update_canvas(self, frame):
        """Draws all strokes chronologically and merges them with the live frame."""
        # 1. Clear the internal canvas every frame to prevent infinite overlapping
        self.paint_window[:] = 0

        # 2. Redraw all strokes in chronological order
        for stroke in self.strokes:
            color = stroke['color']
            thickness = stroke['thickness']
            points = stroke['points']
            
            for i in range(1, len(points)):
                if points[i - 1] is None or points[i] is None:
                    continue
                # Draw the line segments on the black internal canvas
                cv2.line(self.paint_window, points[i - 1], points[i], color, thickness)

        # 3. Merge Logic: Create a mask of where the paint is
        img_gray = cv2.cvtColor(self.paint_window, cv2.COLOR_BGR2GRAY)
        _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
        img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
        
        # Combine the clean frame and the paint
        frame = cv2.bitwise_and(frame, img_inv)
        frame = cv2.bitwise_or(frame, self.paint_window)
        
        return frame

    def add_point(self, point, color=(255, 0, 0), thickness=10):
        """Adds a coordinate to the current stroke, or starts a new one if tools changed."""
        # If the user switches tools (e.g., Draw -> Erase), start a new stroke block automatically
        if not self.strokes or self.strokes[-1]['color'] != color or self.strokes[-1]['thickness'] != thickness:
            self.lift_pen(color, thickness)
            
        self.strokes[-1]['points'].appendleft(point)

    def lift_pen(self, color=(255, 0, 0), thickness=10):
        """Creates a break in the line so we don't connect points when hovering."""
        # Only append a new stroke dictionary if the current one isn't empty
        if self.strokes and len(self.strokes[-1]['points']) == 0:
            self.strokes[-1]['color'] = color
            self.strokes[-1]['thickness'] = thickness
        else:
            self.strokes.append({'color': color, 'thickness': thickness, 'points': deque(maxlen=1024)})

    def clear(self):
        """Wipes the entire stroke history and clears the canvas."""
        self.strokes = [{'color': (255, 0, 0), 'thickness': 10, 'points': deque(maxlen=1024)}]
        self.paint_window[:] = 0