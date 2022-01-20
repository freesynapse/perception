
import numpy as np
from OpenGL.GL import *


class OpenGLObject(object):
    vertices = []
    indices = []
    colors = []
    
    pos = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    scale = np.array([1.0, 1.0, 1.0], dtype=np.float64)
    rot = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    theta = 0.0
    
#----------------------------------------------------------------------------------------
class Quad(OpenGLObject):
    def __init__(self, position=np.array([0.0, 0.0, 0.0]), size=1.0):
        self.side = size / 2
        self.vertices = [np.array([-self.side, -self.side,  0.0]),
                         np.array([ self.side, -self.side,  0.0]),
                         np.array([ self.side,  self.side,  0.0]),
                         np.array([-self.side,  self.side,  0.0])]
        self.indices = [0, 1, 2, 2, 3, 0]
        self.pos = position
        self.color = np.array([1.0, 1.0, 1.0])
        
    #------------------------------------------------------------------------------------
    def render(self, wireframe=False):
        glPushMatrix()
        glTranslate(*self.pos)
        glScale(*self.scale)
        glRotate(self.theta, *self.rot)
        glBegin(GL_TRIANGLES)
        for idx in self.indices:
            glColor3fv(self.color)
            glVertex3fv(self.vertices[idx])
        glEnd()
        glPopMatrix()

#----------------------------------------------------------------------------------------
class Cube(OpenGLObject):
    def __init__(self, position=[0.0,0.0,0.0], scale=[1.0,1.0,1.0], rotation=[0.0,1.0,0.0], theta=0.0, size=0.5):
        self.vertices = []
        self.colors = []
        self.size = size
        self.pos = np.array(position, dtype=np.float64)
        self.scale = np.array(scale, dtype=np.float64)
        self.rot = np.array(rotation, dtype=np.float64)
        self.theta = theta
        self.setup_vertices_()
        self.selection_color = np.array([0, 0, 0])
    #------------------------------------------------------------------------------------
    def move(self, delta):
        self.pos += np.array(delta, dtype=np.float64)

    #------------------------------------------------------------------------------------
    def render(self, translation=np.array([0.0, 0.0, 0.0]), wireframe=False):

        if wireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            
        glPushMatrix()
        
        tpos = self.pos + translation
        
        glTranslate(*tpos)
        glScale(*self.scale)
        glRotate(self.theta, self.rot[0], self.rot[1], self.rot[2])

        glBegin(GL_TRIANGLES)
        for i in range(36):
            glColor3fv(self.colors[i] + self.selection_color)
            glVertex3fv(self.vertices[i])
        glEnd()
        
        glPopMatrix()
        
        if wireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    #------------------------------------------------------------------------------------
    def setup_vertices_(self):
        x0 = self.pos[0] - self.size
        x1 = self.pos[0] + self.size
        y0 = self.pos[1] - self.size
        y1 = self.pos[1] + self.size
        z0 = self.pos[2] - self.size
        z1 = self.pos[2] + self.size

        # top
        self.vertices.append(np.array([x0, y1, z0])), self.colors.append(np.array([0.8, 0.8, 0.8]))
        self.vertices.append(np.array([x0, y1, z1])), self.colors.append(np.array([0.8, 0.8, 0.8]))
        self.vertices.append(np.array([x1, y1, z1])), self.colors.append(np.array([0.8, 0.8, 0.8]))
        self.vertices.append(np.array([x1, y1, z0])), self.colors.append(np.array([0.8, 0.8, 0.8]))
        self.vertices.append(np.array([x0, y1, z0])), self.colors.append(np.array([0.8, 0.8, 0.8]))
        self.vertices.append(np.array([x1, y1, z1])), self.colors.append(np.array([0.8, 0.8, 0.8]))

        # bottom
        self.vertices.append(np.array([x1, y0, z1])), self.colors.append(np.array([0.3, 0.3, 0.3]))
        self.vertices.append(np.array([x0, y0, z1])), self.colors.append(np.array([0.3, 0.3, 0.3]))
        self.vertices.append(np.array([x0, y0, z0])), self.colors.append(np.array([0.3, 0.3, 0.3]))
        self.vertices.append(np.array([x1, y0, z0])), self.colors.append(np.array([0.3, 0.3, 0.3]))
        self.vertices.append(np.array([x1, y0, z1])), self.colors.append(np.array([0.3, 0.3, 0.3]))
        self.vertices.append(np.array([x0, y0, z0])), self.colors.append(np.array([0.3, 0.3, 0.3]))

        # right?
        self.vertices.append(np.array([x1, y1, z0])), self.colors.append(np.array([0.5, 0.5, 0.5]))
        self.vertices.append(np.array([x1, y1, z1])), self.colors.append(np.array([0.5, 0.5, 0.5]))
        self.vertices.append(np.array([x1, y0, z1])), self.colors.append(np.array([0.5, 0.5, 0.5]))
        self.vertices.append(np.array([x1, y0, z0])), self.colors.append(np.array([0.5, 0.5, 0.5]))
        self.vertices.append(np.array([x1, y1, z0])), self.colors.append(np.array([0.5, 0.5, 0.5]))
        self.vertices.append(np.array([x1, y0, z1])), self.colors.append(np.array([0.5, 0.5, 0.5]))

        # front
        self.vertices.append(np.array([x1, y1, z1])), self.colors.append(np.array([0.4, 0.4, 0.4]))
        self.vertices.append(np.array([x0, y1, z1])), self.colors.append(np.array([0.4, 0.4, 0.4]))
        self.vertices.append(np.array([x0, y0, z1])), self.colors.append(np.array([0.4, 0.4, 0.4]))
        self.vertices.append(np.array([x1, y0, z1])), self.colors.append(np.array([0.4, 0.4, 0.4]))
        self.vertices.append(np.array([x1, y1, z1])), self.colors.append(np.array([0.4, 0.4, 0.4]))
        self.vertices.append(np.array([x0, y0, z1])), self.colors.append(np.array([0.4, 0.4, 0.4]))

        # left
        self.vertices.append(np.array([x0, y0, z0])), self.colors.append(np.array([0.6, 0.6, 0.6]))
        self.vertices.append(np.array([x0, y0, z1])), self.colors.append(np.array([0.6, 0.6, 0.6]))
        self.vertices.append(np.array([x0, y1, z0])), self.colors.append(np.array([0.6, 0.6, 0.6]))
        self.vertices.append(np.array([x0, y0, z1])), self.colors.append(np.array([0.6, 0.6, 0.6]))
        self.vertices.append(np.array([x0, y1, z1])), self.colors.append(np.array([0.6, 0.6, 0.6]))
        self.vertices.append(np.array([x0, y1, z0])), self.colors.append(np.array([0.6, 0.6, 0.6]))

        # back
        self.vertices.append(np.array([x1, y0, z0])), self.colors.append(np.array([0.2, 0.2, 0.2]))
        self.vertices.append(np.array([x0, y0, z0])), self.colors.append(np.array([0.2, 0.2, 0.2]))
        self.vertices.append(np.array([x0, y1, z0])), self.colors.append(np.array([0.2, 0.2, 0.2]))
        self.vertices.append(np.array([x1, y1, z0])), self.colors.append(np.array([0.2, 0.2, 0.2]))
        self.vertices.append(np.array([x1, y0, z0])), self.colors.append(np.array([0.2, 0.2, 0.2]))
        self.vertices.append(np.array([x0, y1, z0])), self.colors.append(np.array([0.2, 0.2, 0.2]))

        assert len(self.vertices) == 36
