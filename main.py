"""
Conic Section 3D Visualizer - Main Application
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *

from config import *
from math_engine import MathEngine
from graphics_engine import GraphicsEngine
from camera import Camera
from ui_manager import UIManager


class ConicVisualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
        pygame.display.set_caption(WINDOW_TITLE)
        
        self.math_engine = MathEngine()
        self.graphics_engine = GraphicsEngine(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.camera = Camera()
        
        # Pass math_engine reference to UI manager
        self.ui_manager = UIManager(WINDOW_WIDTH, WINDOW_HEIGHT, self.math_engine)
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initial calculation
        self.do_calculation()
    
    def do_calculation(self):
        """Perform intersection and classification"""
        self.math_engine.compute_intersection()
        self.math_engine.classify_conic()
        print(f"[CALC] {self.math_engine.conic_type}, Angle={self.math_engine.angle_deg:.2f}°, Ecc={self.math_engine.eccentricity:.4f}")
    
    def handle_events(self):
        self.clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                return
            
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if event.button == 1:
                    # Check if in UI area
                    if x >= VIEWPORT_WIDTH or y > self.ui_manager.height - 70:
                        action = self.ui_manager.handle_mouse_down(event.pos)
                        print(f"[CLICK] UI area, action={action}")
                        if action == 'update_cone':
                            k, h = self.ui_manager.get_cone_params()
                            print(f"[CONE] k={k}, h={h}")
                            if k and h and k > 0 and h > 0:
                                self.math_engine.cone_k = k
                                self.math_engine.cone_height = h
                                self.do_calculation()
                        elif action == 'update_plane':
                            A, B, C, D = self.ui_manager.get_plane_params()
                            print(f"[PLANE] A={A}, B={B}, C={C}, D={D}")
                            if A is not None:
                                if abs(A) > 1e-10 or abs(B) > 1e-10 or abs(C) > 1e-10:
                                    self.math_engine.plane_A = float(A)
                                    self.math_engine.plane_B = float(B)
                                    self.math_engine.plane_C = float(C)
                                    self.math_engine.plane_D = float(D)
                                    self.do_calculation()
                                    print(f"[DONE] Recalculated with {len(self.math_engine.intersection_points)} points")
                    else:
                        self.camera.handle_mouse_down(event.pos, 1)
                elif event.button == 4 and x < VIEWPORT_WIDTH:
                    self.camera.handle_scroll('up')
                elif event.button == 5 and x < VIEWPORT_WIDTH:
                    self.camera.handle_scroll('down')
            
            if event.type == MOUSEBUTTONUP and event.button == 1:
                self.camera.handle_mouse_up(1)
                self.ui_manager.handle_mouse_up()
            
            if event.type == MOUSEMOTION:
                self.ui_manager.handle_mouse_motion(event.pos)
                h, v = self.ui_manager.get_slider_values()
                self.camera.set_rotation_y(h)
                self.camera.set_rotation_x(v)
                if event.pos[0] < VIEWPORT_WIDTH:
                    self.camera.handle_mouse_motion(event.pos)
            
            if event.type == KEYDOWN:
                self.ui_manager.handle_key(event)
    
    def render(self):
        self.graphics_engine.clear_screen()
        self.camera.apply_transformation()
        
        self.graphics_engine.draw_axes()
        self.graphics_engine.draw_cone(self.math_engine.cone_k, self.math_engine.cone_height)
        self.graphics_engine.draw_plane(
            self.math_engine.plane_A, self.math_engine.plane_B,
            self.math_engine.plane_C, self.math_engine.plane_D
        )
        self.graphics_engine.draw_intersection(self.math_engine.intersection_points)
        
        self.graphics_engine.switch_to_2d()
        self.ui_manager.draw()
        self.graphics_engine.switch_to_3d()
        
        pygame.display.flip()
    
    def run(self):
        print("=== Conic Section Visualizer ===")
        print(f"Window: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        print("Running...")
        
        while self.running:
            self.handle_events()
            self.render()
        
        pygame.quit()


if __name__ == "__main__":
    ConicVisualizer().run()