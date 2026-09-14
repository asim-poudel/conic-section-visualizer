"""
UI Manager - Dark Grey Theme
"""

import pygame
import pygame.freetype
from OpenGL.GL import *
from config import *


# Dark Grey Theme Colors
COL_MAIN_BG = (0.169, 0.180, 0.200, 1.0)      # #2B2E33 - Warm dark grey
COL_BOX_BG = (0.200, 0.227, 0.259, 1.0)       # #333A42 - Soft blue-tinted dark grey
COL_HEADER_BG = (0.247, 0.290, 0.333, 1.0)    # #3F4A55 - Muted steel blue
COL_HEADER_TEXT = (230, 235, 240)              # #E6EBF0 - Soft off-white
COL_BODY_TEXT = (201, 209, 217)                # #C9D1D9 - Light cool gray
COL_BUTTON = (0.357, 0.498, 0.651, 1.0)       # #5B7FA6 - Blue-Gray
COL_BUTTON_TEXT = (255, 255, 255)              # #FFFFFF
COL_HIGHLIGHT = (63, 182, 178)                 # #3FB6B2 - Soft Teal
COL_BORDER = (0.259, 0.290, 0.325, 1.0)       # #424A53 - Border


class UIManager:
    def __init__(self, width, height, math_engine):
        self.width = width
        self.height = height
        self.math = math_engine
        
        pygame.freetype.init()
        self.font = pygame.freetype.SysFont('Arial', 14)
        self.title_font = pygame.freetype.SysFont('Arial', 16, bold=True)
        self.bold_font = pygame.freetype.SysFont('Arial', 18, bold=True)
        self.result_font = pygame.freetype.SysFont('Arial', 13)
        self.small_font = pygame.freetype.SysFont('Arial', 12)
        
        # Input values
        self.cone_k_value = str(DEFAULT_CONE_K)
        self.cone_h_value = str(DEFAULT_CONE_HEIGHT)
        self.plane_A_value = str(DEFAULT_PLANE_A)
        self.plane_B_value = str(DEFAULT_PLANE_B)
        self.plane_C_value = str(DEFAULT_PLANE_C)
        self.plane_D_value = str(DEFAULT_PLANE_D)
        
        self.active_field = None
        self.input_fields = {}
        
        self.h_slider_value = DEFAULT_ROTATION_Y
        self.v_slider_value = DEFAULT_ROTATION_X
        self.dragging_h_slider = False
        self.dragging_v_slider = False
        
        # Layout
        self.panel_x = VIEWPORT_WIDTH + 10
        self.panel_width = UI_PANEL_WIDTH - 20
        
        self.box1_height = 150
        self.box2_height = 200
        self.box3_height = 280
        
        total_boxes_height = self.box1_height + self.box2_height + self.box3_height + 20
        available_height = height - 80
        start_y = max(8, (available_height - total_boxes_height) // 2)
        
        self.box1_y = start_y
        self.box2_y = self.box1_y + self.box1_height + 8
        self.box3_y = self.box2_y + self.box2_height + 8
        
        self.setup_fields()
    
    def setup_fields(self):
        fw, fx = 120, self.panel_x + 100
        
        y = self.box1_y + 42
        self.input_fields['cone_k'] = pygame.Rect(fx, y, fw, 26)
        self.input_fields['cone_h'] = pygame.Rect(fx, y + 32, fw, 26)
        # Button with more spacing (moved up from bottom)
        self.cone_btn_rect = pygame.Rect(self.panel_x + 15, self.box1_y + self.box1_height - 42, self.panel_width - 30, 32)
        
        y = self.box2_y + 40
        self.input_fields['plane_A'] = pygame.Rect(fx, y, fw, 26)
        self.input_fields['plane_B'] = pygame.Rect(fx, y + 28, fw, 26)
        self.input_fields['plane_C'] = pygame.Rect(fx, y + 56, fw, 26)
        self.input_fields['plane_D'] = pygame.Rect(fx, y + 84, fw, 26)
        # Button with more spacing
        self.plane_btn_rect = pygame.Rect(self.panel_x + 15, self.box2_y + self.box2_height - 42, self.panel_width - 30, 32)
        
        sy = self.height - 40
        self.h_slider_rect = pygame.Rect(20, sy, 380, 16)
        self.v_slider_rect = pygame.Rect(440, sy, 380, 16)
    
    def get_cone_params(self):
        try: return float(self.cone_k_value), float(self.cone_h_value)
        except: return None, None
    
    def get_plane_params(self):
        try: return float(self.plane_A_value), float(self.plane_B_value), float(self.plane_C_value), float(self.plane_D_value)
        except: return None, None, None, None
    
    def handle_mouse_down(self, pos):
        x, y = pos
        for name, rect in self.input_fields.items():
            if rect.collidepoint(x, y):
                self.active_field = name
                return None
        if self.cone_btn_rect.collidepoint(x, y):
            self.active_field = None
            return 'update_cone'
        if self.plane_btn_rect.collidepoint(x, y):
            self.active_field = None
            return 'update_plane'
        if self.h_slider_rect.collidepoint(x, y):
            self.dragging_h_slider = True
            self.update_h_slider(x)
        if self.v_slider_rect.collidepoint(x, y):
            self.dragging_v_slider = True
            self.update_v_slider(x)
        self.active_field = None
        return None
    
    def handle_mouse_up(self):
        self.dragging_h_slider = self.dragging_v_slider = False
    
    def handle_mouse_motion(self, pos):
        if self.dragging_h_slider: self.update_h_slider(pos[0])
        if self.dragging_v_slider: self.update_v_slider(pos[0])
    
    def update_h_slider(self, x):
        r = max(0, min(x - self.h_slider_rect.x, self.h_slider_rect.width))
        self.h_slider_value = (r / self.h_slider_rect.width) * 360
    
    def update_v_slider(self, x):
        r = max(0, min(x - self.v_slider_rect.x, self.v_slider_rect.width))
        self.v_slider_value = (r / self.v_slider_rect.width) * 360
    
    def handle_key(self, event):
        if not self.active_field: return
        val = getattr(self, f'{self.active_field}_value')
        if event.key == pygame.K_BACKSPACE: val = val[:-1]
        elif event.key in (pygame.K_RETURN, pygame.K_TAB, pygame.K_ESCAPE): self.active_field = None; return
        elif event.unicode in '0123456789.-': val += event.unicode
        setattr(self, f'{self.active_field}_value', val)
    
    def get_slider_values(self): return self.h_slider_value, self.v_slider_value
    
    # Drawing
    def rect(self, x, y, w, h, c):
        glColor4f(*c); glBegin(GL_QUADS)
        glVertex2f(x,y); glVertex2f(x+w,y); glVertex2f(x+w,y+h); glVertex2f(x,y+h)
        glEnd()
    
    def shadow(self, x, y, w, h):
        """Draw subtle shadow"""
        glColor4f(0, 0, 0, 0.4)
        glBegin(GL_QUADS)
        glVertex2f(x+3, y+3); glVertex2f(x+w+3, y+3); glVertex2f(x+w+3, y+h+3); glVertex2f(x+3, y+h+3)
        glEnd()
    
    def outline(self, x, y, w, h, c=COL_BORDER, lw=1):
        glColor4f(*c); glLineWidth(lw)
        glBegin(GL_LINE_LOOP); glVertex2f(x,y); glVertex2f(x+w,y); glVertex2f(x+w,y+h); glVertex2f(x,y+h); glEnd()
        glLineWidth(1)
    
    def txt_tex(self, text, font, color=(255,255,255)):
        if not text: text = " "
        s, r = font.render(text, color)
        if r.width == 0: return None, 0, 0
        rgba = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
        rgba.blit(s, (0, 0))
        flip = pygame.transform.flip(rgba, False, True)
        data = pygame.image.tostring(flip, "RGBA", False)
        tid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tid)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, r.width, r.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        return tid, r.width, r.height
    
    def txt(self, t, x, y, font=None, color=COL_BODY_TEXT):
        if font is None: font = self.font
        tid, w, h = self.txt_tex(t, font, color)
        if not tid: return
        glEnable(GL_TEXTURE_2D); glBindTexture(GL_TEXTURE_2D, tid); glColor4f(1,1,1,1)
        glBegin(GL_QUADS)
        glTexCoord2f(0,1); glVertex2f(x, y); glTexCoord2f(1,1); glVertex2f(x+w, y)
        glTexCoord2f(1,0); glVertex2f(x+w, y+h); glTexCoord2f(0,0); glVertex2f(x, y+h)
        glEnd()
        glDisable(GL_TEXTURE_2D); glDeleteTextures([tid])
    
    def input(self, name, label, y, val):
        self.txt(label, self.panel_x + 10, y + 5, color=COL_BODY_TEXT)
        r = self.input_fields[name]
        act = self.active_field == name
        # Dark input background
        self.rect(r.x, r.y, r.width, r.height, (0.15, 0.17, 0.20, 1.0))
        border_col = (0.4, 0.55, 0.75, 1.0) if act else COL_BORDER
        self.outline(r.x, r.y, r.width, r.height, border_col, 2 if act else 1)
        self.txt(val + ("|" if act else ""), r.x + 6, r.y + 4, color=(240, 245, 250))
    
    def btn(self, r, t):
        self.shadow(r.x, r.y, r.width, r.height)
        self.rect(r.x, r.y, r.width, r.height, COL_BUTTON)
        self.outline(r.x, r.y, r.width, r.height, (0.45, 0.58, 0.75, 1.0))
        tid, tw, th = self.txt_tex(t, self.font, COL_BUTTON_TEXT)
        if tid:
            tx, ty = r.x + (r.width-tw)//2, r.y + (r.height-th)//2
            glEnable(GL_TEXTURE_2D); glBindTexture(GL_TEXTURE_2D, tid); glColor4f(1,1,1,1)
            glBegin(GL_QUADS)
            glTexCoord2f(0,1); glVertex2f(tx, ty); glTexCoord2f(1,1); glVertex2f(tx+tw, ty)
            glTexCoord2f(1,0); glVertex2f(tx+tw, ty+th); glTexCoord2f(0,0); glVertex2f(tx, ty+th)
            glEnd()
            glDisable(GL_TEXTURE_2D); glDeleteTextures([tid])
    
    def slider(self, r, val, label, ly):
        self.txt(label, r.x, ly, self.small_font, (160, 165, 175))
        self.rect(r.x, r.y, r.width, r.height, (0.15, 0.17, 0.2, 1.0))
        fw = (val/360) * r.width
        self.rect(r.x, r.y, fw, r.height, (0.35, 0.5, 0.65, 0.8))
        hx = r.x + (val/360) * (r.width - 12)
        self.rect(hx, r.y-3, 12, r.height+6, (0.45, 0.6, 0.8, 1.0))
        self.txt(f"{int(val)}°", r.x + r.width + 10, r.y, self.small_font, (150, 155, 165))
    
    def panel(self, y, h, title):
        # Shadow
        self.shadow(self.panel_x, y, self.panel_width, h)
        # Box background
        self.rect(self.panel_x, y, self.panel_width, h, COL_BOX_BG)
        self.outline(self.panel_x, y, self.panel_width, h)
        # Header bar
        self.rect(self.panel_x, y, self.panel_width, 30, COL_HEADER_BG)
        # Header text
        self.txt(title, self.panel_x + 12, y + 7, self.title_font, COL_HEADER_TEXT)
    
    def draw(self):
        # Main panel background
        self.rect(VIEWPORT_WIDTH, 0, UI_PANEL_WIDTH, self.height, COL_MAIN_BG)
        
        # Box 1: Cone
        self.panel(self.box1_y, self.box1_height, "CONE PARAMETERS")
        y = self.box1_y + 42
        self.input('cone_k', 'k (slope):', y, self.cone_k_value)
        self.input('cone_h', 'Height:', y + 34, self.cone_h_value)
        self.btn(self.cone_btn_rect, "Update Cone")
        
        # Box 2: Plane
        self.panel(self.box2_y, self.box2_height, "PLANE EQUATION (Ax+By+Cz+D=0)")
        y = self.box2_y + 40
        self.input('plane_A', 'A:', y, self.plane_A_value)
        self.input('plane_B', 'B:', y + 30, self.plane_B_value)
        self.input('plane_C', 'C:', y + 60, self.plane_C_value)
        self.input('plane_D', 'D:', y + 90, self.plane_D_value)
        self.btn(self.plane_btn_rect, "Update Plane")
        
        # Box 3: Results
        self.panel(self.box3_y, self.box3_height, "CONIC SECTION RESULTS")
        y = self.box3_y + 42
        
        # Conic type - BOLD with teal highlight
        ctype = self.math.conic_type if self.math.conic_type else "Calculating..."
        self.txt("Type:", self.panel_x + 12, y, color=COL_BODY_TEXT)
        self.txt(ctype, self.panel_x + 65, y, self.bold_font, COL_HIGHLIGHT)
        y += 32
        
        # Angle
        self.txt(f"Plane Angle: {self.math.angle_deg:.2f}°", self.panel_x + 12, y, color=COL_BODY_TEXT)
        y += 26
        
        # Eccentricity
        ecc = self.math.eccentricity
        ecc_str = f"Eccentricity: {ecc:.4f}" if ecc < 100 else "Eccentricity: N/A"
        self.txt(ecc_str, self.panel_x + 12, y, color=COL_BODY_TEXT)
        y += 32
        
        # Description header
        self.txt("Description:", self.panel_x + 12, y, self.font, (140, 180, 220))
        y += 24
        
        # Description text
        desc = self.math.description if self.math.description else "Update parameters to see results"
        words = desc.split()
        line = ""
        for w in words:
            if len(line + w) > 42:
                self.txt(line.strip(), self.panel_x + 12, y, self.result_font, (180, 185, 195))
                y += 18
                line = w + " "
            else:
                line += w + " "
        if line:
            self.txt(line.strip(), self.panel_x + 12, y, self.result_font, (180, 185, 195))
        y += 28
        
        # Point count
        pts = len(self.math.intersection_points)
        self.txt(f"Intersection Points: {pts}", self.panel_x + 12, y, color=COL_BODY_TEXT)
        
        # Sliders
        sly = self.height - 58
        self.slider(self.h_slider_rect, self.h_slider_value, "Horizontal Rotation", sly)
        self.slider(self.v_slider_rect, self.v_slider_value, "Vertical Rotation", sly)