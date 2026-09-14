"""
Graphics Engine for 3D Rendering with Anti-Aliasing and Smooth Shading
"""

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from config import *


class GraphicsEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.viewport_width = VIEWPORT_WIDTH
        self.quadric = None
        self.setup_opengl()
    
    def setup_opengl(self):
        # Enable anti-aliasing
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        
        # Depth and blending
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(*BACKGROUND_COLOR)
        
        # Gouraud shading (smooth interpolation)
        glShadeModel(GL_SMOOTH)
        
        # Lighting setup
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 10.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.9, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        
        glLightfv(GL_LIGHT1, GL_POSITION, [-5.0, -3.0, 5.0, 1.0])
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.5, 0.5, 0.6, 1.0])
        
        # Quadric for cone
        self.quadric = gluNewQuadric()
        gluQuadricNormals(self.quadric, GLU_SMOOTH)
        gluQuadricDrawStyle(self.quadric, GLU_FILL)
        
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glViewport(0, 0, self.viewport_width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOV, self.viewport_width / self.height, NEAR_CLIP, FAR_CLIP)
        glMatrixMode(GL_MODELVIEW)
    
    def clear_screen(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glViewport(0, 0, self.viewport_width, self.height)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    def draw_axes(self):
        glDisable(GL_LIGHTING)
        glLineWidth(AXIS_LINE_WIDTH)
        glBegin(GL_LINES)
        glColor3f(*COLORS['axis_x']); glVertex3f(0,0,0); glVertex3f(AXIS_LENGTH,0,0)
        glColor3f(*COLORS['axis_y']); glVertex3f(0,0,0); glVertex3f(0,AXIS_LENGTH,0)
        glColor3f(*COLORS['axis_z']); glVertex3f(0,0,0); glVertex3f(0,0,AXIS_LENGTH)
        glEnd()
        glLineWidth(1)
        glEnable(GL_LIGHTING)
    
    def draw_cone(self, k, height):
        """Solid WHITE cone"""
        glEnable(GL_LIGHTING)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glColor4f(0.95, 0.95, 0.97, 0.85)
        
        base_radius = height * k
        
        glPushMatrix()
        gluCylinder(self.quadric, 0.001, base_radius, height, CONE_SEGMENTS, CONE_LAYERS)
        glPopMatrix()
        
        glPushMatrix()
        glRotatef(180, 1, 0, 0)
        gluCylinder(self.quadric, 0.001, base_radius, height, CONE_SEGMENTS, CONE_LAYERS)
        glPopMatrix()
    
    def draw_plane(self, A, B, C, D):
        """DARK GREY plane"""
        glEnable(GL_LIGHTING)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glColor4f(0.25, 0.28, 0.32, 0.5)
        
        normal = np.array([A, B, C])
        nlen = np.linalg.norm(normal)
        if nlen > 0: normal = normal / nlen
        glNormal3f(*normal)
        
        size, div = PLANE_SIZE, PLANE_DIVISIONS
        
        glBegin(GL_QUADS)
        for i in range(div):
            for j in range(div):
                u1, u2 = (i/div-0.5)*size, ((i+1)/div-0.5)*size
                v1, v2 = (j/div-0.5)*size, ((j+1)/div-0.5)*size
                pts = []
                for u, v in [(u1,v1),(u2,v1),(u2,v2),(u1,v2)]:
                    if abs(C) > 1e-10:
                        x,y = u,v; z = (-A*x-B*y-D)/C
                    elif abs(B) > 1e-10:
                        x,z = u,v; y = (-A*x-C*z-D)/B
                    elif abs(A) > 1e-10:
                        y,z = u,v; x = (-B*y-C*z-D)/A
                    else: continue
                    pts.append((x,y,z))
                if len(pts) == 4:
                    for p in pts: glVertex3f(*p)
        glEnd()
    
    def draw_intersection(self, points):
        """3D SOLID conic section from analytical parametric curve"""
        if len(points) < 3:
            return
        
        # Points are already ordered by angle from parametric computation
        # No sorting needed - continuous ordered polyline
        pts = [np.array(p) for p in points]
        n_pts = len(pts)
        center = np.mean(pts, axis=0)
        
        # Calculate surface normal
        v1 = np.array(pts[1]) - np.array(pts[0])
        v2 = np.array(pts[n_pts//2]) - np.array(pts[0])
        normal = np.cross(v1, v2)
        nlen = np.linalg.norm(normal)
        if nlen > 1e-10:
            normal = normal / nlen
        else:
            normal = np.array([0.0, 0.0, 1.0])
        
        # Enable anti-aliasing and smooth rendering
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        
        # Z-buffer
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glDepthMask(GL_TRUE)
        
        # Two-sided Gouraud shading
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
        glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
        glDisable(GL_CULL_FACE)
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glShadeModel(GL_SMOOTH)  # Gouraud shading
        
        # Bright yellow material with specular highlights
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.5, 0.5, 0.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1.0, 1.0, 0.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 0.9, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 120.0)
        glColor4f(1.0, 1.0, 0.0, 1.0)
        
        # 3D thickness
        thickness = 0.05
        center_top = center + normal * thickness
        center_bot = center - normal * thickness
        pts_top = [np.array(p) + normal * thickness for p in pts]
        pts_bot = [np.array(p) - normal * thickness for p in pts]
        
        # Calculate smooth vertex normals (outward from center)
        edge_normals = []
        for i in range(n_pts):
            outward = np.array(pts[i]) - center
            out_len = np.linalg.norm(outward)
            if out_len > 1e-10:
                edge_normals.append(outward / out_len)
            else:
                edge_normals.append(np.array([1.0, 0.0, 0.0]))
        
        # Draw top surface with smooth shading
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(*normal)
        glVertex3f(*center_top)
        for i in range(n_pts):
            glVertex3f(*pts_top[i])
        glVertex3f(*pts_top[0])
        glEnd()
        
        # Draw bottom surface
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(*(-normal))
        glVertex3f(*center_bot)
        for i in range(n_pts - 1, -1, -1):
            glVertex3f(*pts_bot[i])
        glVertex3f(*pts_bot[n_pts - 1])
        glEnd()
        
        # Draw smooth edge strip with per-vertex normals
        glBegin(GL_QUAD_STRIP)
        for i in range(n_pts + 1):
            idx = i % n_pts
            glNormal3f(*edge_normals[idx])
            glVertex3f(*pts_top[idx])
            glVertex3f(*pts_bot[idx])
        glEnd()
        
        # Restore
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE)
        glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_FALSE)
        glEnable(GL_LIGHTING)
    
    def switch_to_2d(self):
        glDisable(GL_LIGHTING)
        glDisable(GL_POLYGON_SMOOTH)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
    
    def switch_to_3d(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glViewport(0, 0, self.viewport_width, self.height)