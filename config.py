"""
Configuration and Constants for Conic Section Visualizer
"""

# Window Configuration - 16:9 Aspect Ratio
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Conic Section 3D Visualizer"

# Layout Configuration - 3D viewport on left, UI panel on right
VIEWPORT_WIDTH = 820  # Width for 3D rendering area
UI_PANEL_WIDTH = 460  # Width for right side UI panel
UI_PANEL_MARGIN = 12
UI_ELEMENT_HEIGHT = 28
UI_ELEMENT_SPACING = 32
UI_LABEL_WIDTH = 120
UI_INPUT_WIDTH = 130

# Dialog Box Heights (will be calculated dynamically in UI manager)
DIALOG_BOX_1_HEIGHT = 120  # Cone Parameters
DIALOG_BOX_2_HEIGHT = 160  # Plane Parameters
DIALOG_BOX_3_HEIGHT = 300  # Results Display

# OpenGL Settings
BACKGROUND_COLOR = (0.12, 0.12, 0.15, 1.0)  # Dark background
FOV = 45  # Field of view
NEAR_CLIP = 0.1
FAR_CLIP = 100.0

# Color Schemes
COLORS = {
    'cone': (0.85, 0.88, 0.95, 0.8),         # Light blue-gray
    'plane': (0.2, 0.55, 0.9, 0.35),          # Semi-transparent blue
    'intersection': (1.0, 0.15, 0.1),         # Bright red
    'axis_x': (1.0, 0.2, 0.2),                # Red
    'axis_y': (0.2, 1.0, 0.2),                # Green
    'axis_z': (0.2, 0.2, 1.0),                # Blue
}

# Default Parameters
DEFAULT_CONE_K = 1.0
DEFAULT_CONE_HEIGHT = 5.0
DEFAULT_CONE_AXIS_ANGLE = 45.0
DEFAULT_PLANE_A = 0.0
DEFAULT_PLANE_B = 0.0
DEFAULT_PLANE_C = 1.0
DEFAULT_PLANE_D = -2.0

# Camera Settings
DEFAULT_ROTATION_X = 30
DEFAULT_ROTATION_Y = 45
DEFAULT_ZOOM = -15
ZOOM_SPEED = 0.5
ROTATION_SPEED = 0.5

# Rendering Settings
CONE_SEGMENTS = 48
CONE_LAYERS = 24
PLANE_SIZE = 10
PLANE_DIVISIONS = 20
INTERSECTION_LINE_WIDTH = 6
INTERSECTION_POINT_SIZE = 10
AXIS_LINE_WIDTH = 2
AXIS_LENGTH = 3

# Computation Settings
INTERSECTION_SAMPLES = 120
INTERSECTION_TOLERANCE = 0.08
ANGLE_TOLERANCE = 2.0  # degrees