"""
Camera Controller for 3D View Navigation
Handles rotation, zoom, and pan operations
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from config import *


class Camera:
    """Manages camera position and orientation"""
    
    def __init__(self):
        self.rotation_x = DEFAULT_ROTATION_X
        self.rotation_y = DEFAULT_ROTATION_Y
        self.zoom = DEFAULT_ZOOM
        
        self.mouse_down = False
        self.last_mouse_pos = (0, 0)
    
    def handle_mouse_down(self, pos, button):
        """Handle mouse button press"""
        if button == 1:  # Left click
            self.mouse_down = True
            self.last_mouse_pos = pos
    
    def handle_mouse_up(self, button):
        """Handle mouse button release"""
        if button == 1:
            self.mouse_down = False
    
    def handle_mouse_motion(self, pos):
        """Handle mouse movement for rotation"""
        if self.mouse_down:
            dx = pos[0] - self.last_mouse_pos[0]
            dy = pos[1] - self.last_mouse_pos[1]
            
            self.rotation_y += dx * ROTATION_SPEED
            self.rotation_x += dy * ROTATION_SPEED
            
            self.last_mouse_pos = pos
    
    def handle_scroll(self, direction):
        """Handle mouse scroll for zoom"""
        if direction == 'up':
            self.zoom += ZOOM_SPEED
        elif direction == 'down':
            self.zoom -= ZOOM_SPEED
    
    def set_rotation_x(self, value):
        """Set rotation around X axis"""
        self.rotation_x = value
    
    def set_rotation_y(self, value):
        """Set rotation around Y axis"""
        self.rotation_y = value
    
    def apply_transformation(self):
        """Apply camera transformation to OpenGL matrix"""
        glTranslatef(0, 0, self.zoom)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
    
    def reset(self):
        """Reset camera to default position"""
        self.rotation_x = DEFAULT_ROTATION_X
        self.rotation_y = DEFAULT_ROTATION_Y
        self.zoom = DEFAULT_ZOOM