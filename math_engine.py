"""
Mathematical Engine for Conic Section Calculations
PARAMETRIC EQUATIONS with proper inside-cone filtering for hyperbola
"""

import numpy as np
from config import *


class MathEngine:
    def __init__(self):
        self.cone_k = DEFAULT_CONE_K
        self.cone_height = DEFAULT_CONE_HEIGHT
        self.plane_A = DEFAULT_PLANE_A
        self.plane_B = DEFAULT_PLANE_B
        self.plane_C = DEFAULT_PLANE_C
        self.plane_D = DEFAULT_PLANE_D
        
        self.intersection_points = []
        self.conic_type = ""
        self.eccentricity = 0.0
        self.angle_deg = 0.0
        self.description = ""
    
    def update_cone_params(self, k, height):
        if k > 0 and height > 0:
            self.cone_k = k
            self.cone_height = height
            return True
        return False
    
    def update_plane_params(self, A, B, C, D):
        if abs(A) < 1e-10 and abs(B) < 1e-10 and abs(C) < 1e-10:
            return False
        self.plane_A = A
        self.plane_B = B
        self.plane_C = C
        self.plane_D = D
        return True
    
    def compute_intersection(self):
        """
        PARAMETRIC EQUATIONS with inside-cone check
        
        For hyperbola: only show points where the plane enters the cone volume
        (not where it exits through the outer surface)
        """
        self.intersection_points = []
        points = []
        
        k = self.cone_k
        A, B, C, D = self.plane_A, self.plane_B, self.plane_C, self.plane_D
        
        num_samples = 720
        
        # Determine if this will be a hyperbola (plane shallower than cone)
        normal = np.array([A, B, C])
        norm_len = np.linalg.norm(normal)
        if norm_len > 1e-10:
            normal = normal / norm_len
        axis = np.array([0, 0, 1])
        cos_angle = abs(np.dot(normal, axis))
        plane_angle = 90.0 - np.degrees(np.arccos(np.clip(cos_angle, 0, 1)))
        cone_half_angle = np.degrees(np.arctan(k))
        is_hyperbola = plane_angle < cone_half_angle - 2.0
        
        # UPPER NAPPE (z >= 0)
        for i in range(num_samples):
            theta = 2 * np.pi * i / num_samples
            cos_t = np.cos(theta)
            sin_t = np.sin(theta)
            
            denom = A * k * cos_t + B * k * sin_t + C
            if abs(denom) < 1e-10:
                continue
            
            z = -D / denom
            if z < 0 or z > self.cone_height:
                continue
            
            x = k * z * cos_t
            y = k * z * sin_t
            
            # Verify on plane
            if abs(A*x + B*y + C*z + D) > 0.1:
                continue
            
            points.append([x, y, z])
        
        # LOWER NAPPE (z <= 0)
        for i in range(num_samples):
            theta = 2 * np.pi * i / num_samples
            cos_t = np.cos(theta)
            sin_t = np.sin(theta)
            
            denom = -A * k * cos_t - B * k * sin_t + C
            if abs(denom) < 1e-10:
                continue
            
            z = -D / denom
            if z > 0 or z < -self.cone_height:
                continue
            
            x = -k * z * cos_t
            y = -k * z * sin_t
            
            # Verify on plane
            if abs(A*x + B*y + C*z + D) > 0.1:
                continue
            
            # For hyperbola: check if plane goes INTO cone
            if is_hyperbola:
                scale = 0.95
                xi, yi = x * scale, y * scale
                if abs(C) > 1e-10:
                    zi = (-A*xi - B*yi - D) / C
                else:
                    zi = z * scale
                # For lower nappe, use abs(zi) in cone equation
                if xi**2 + yi**2 > (k * abs(zi))**2:
                    continue
            
            points.append([x, y, z])
        
        # Sort for continuous curve
        if len(points) > 0:
            center = np.mean(points, axis=0)
            points = sorted(points, key=lambda p: np.arctan2(p[1]-center[1], p[0]-center[0]))
        
        self.intersection_points = points
        print(f"[CALC] {len(points)} points")
        return points
    
    def classify_conic(self):
        normal = np.array([self.plane_A, self.plane_B, self.plane_C])
        norm_len = np.linalg.norm(normal)
        if norm_len < 1e-10:
            self.conic_type = "Invalid"
            return
        normal = normal / norm_len
        
        axis = np.array([0, 0, 1])
        cos_normal_axis = abs(np.dot(normal, axis))
        normal_axis_angle = np.degrees(np.arccos(np.clip(cos_normal_axis, 0, 1)))
        plane_angle = 90.0 - normal_axis_angle
        self.angle_deg = plane_angle
        cone_half_angle = np.degrees(np.arctan(self.cone_k))
        
        print(f"[DEBUG] Plane: {plane_angle:.2f}°, Cone: {cone_half_angle:.2f}°")
        
        if plane_angle > 90 - ANGLE_TOLERANCE:
            self.conic_type = "Circle"
            self.eccentricity = 0.0
            self.description = "CIRCLE: e=0"
        elif plane_angle > cone_half_angle + ANGLE_TOLERANCE:
            self.conic_type = "Ellipse"
            self.eccentricity = np.cos(np.radians(plane_angle)) / np.cos(np.radians(cone_half_angle))
            if self.eccentricity >= 1.0: self.eccentricity = 0.9
            self.description = f"ELLIPSE: e={self.eccentricity:.3f}"
        elif abs(plane_angle - cone_half_angle) <= ANGLE_TOLERANCE:
            self.conic_type = "Parabola"
            self.eccentricity = 1.0
            self.description = "PARABOLA: e=1.0"
        else:
            self.conic_type = "Hyperbola"
            if abs(np.cos(np.radians(plane_angle))) > 1e-10:
                self.eccentricity = np.cos(np.radians(cone_half_angle)) / np.cos(np.radians(plane_angle))
            else:
                self.eccentricity = 2.0
            if self.eccentricity <= 1.0: self.eccentricity = 1.5
            self.description = f"HYPERBOLA: e={self.eccentricity:.3f}"
    
    def get_results(self):
        return {
            'conic_type': self.conic_type,
            'angle': self.angle_deg,
            'eccentricity': self.eccentricity,
            'description': self.description,
            'point_count': len(self.intersection_points)
        }
