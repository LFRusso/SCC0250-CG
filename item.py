import numpy as np

class Item:
    def __init__(self, vertices, edges=None, colors=None, action=None):
        self.vertices = np.array(vertices, np.float32)
        self.edges = np.array(edges, np.float32)
        self.colors = colors
        self.action = action

        self.Rz = lambda x: np.array([  np.cos(x), -np.sin(x), 0.0, 0.0, 
                                        np.sin(x),  np.cos(x), 0.0, 0.0, 
                                        0.0,      0.0, 1.0, 0.0, 
                                        0.0,      0.0, 0.0, 1.0], np.float32)
        
        self.Rx = lambda x: np.array([     1.0,   0.0,    0.0, 0.0, 
                                        0.0, np.cos(x), -np.sin(x), 0.0, 
                                        0.0, np.sin(x),  np.cos(x), 0.0, 
                                        0.0,   0.0,    0.0, 1.0], np.float32)
        
        self.Ry = lambda x: np.array([   np.cos(x),     0.0,  np.sin(x),    0.0, 
                                               0.0,     1.0,        0.0,    0.0, 
                                        -np.sin(x),     0.0,  np.cos(x),    0.0, 
                                               0.0,     0.0,        0.0,    1.0], np.float32)

        self.T = lambda x,y,z: np.array([   1.0,   0.0,    0.0,     x, 
                                            0.0,   1.0,    0.0,     y, 
                                            0.0,   0.0,    1.0,     z, 
                                            0.0,   0.0,    0.0,     1.0], np.float32)
        
        self.S = lambda x,y,z: np.array([     x,    0.0,    0.0, 0.0, 
                                            0.0,      y,    0.0, 0.0, 
                                            0.0,    0.0,      z, 0.0, 
                                            0.0,    0.0,    0.0, 1.0], np.float32)

    def _mat_mul(self, a, b):
        m_a = a.reshape(4,4)
        m_b = b.reshape(4,4)
        m_c = np.dot(m_a,m_b)
        c = m_c.reshape(1,16)

        return
        
    def action(self, args=None):
        self.action(*args)
        return

    def translate(self, v):
        new_vertices = np.dot(self.T(*v).reshape(4,4),self.vertices.T)
        self.vertices = new_vertices.T
        return

    def scale(self, v):
        new_vertices = np.dot(self.S(*v).reshape(4,4),self.vertices.T)
        self.vertices = new_vertices.T
        return

    def rotx(self, ang):
        new_vertices = np.dot(self.Rx(ang).reshape(4,4),self.vertices.T)
        self.vertices = new_vertices.T
        return

    def rotz(self, ang):
        new_vertices = np.dot(self.Rz(ang).reshape(4,4),self.vertices.T)
        self.vertices = new_vertices.T
        return

    def roty(self, ang):
        new_vertices = np.dot(self.Ry(ang).reshape(4,4),self.vertices.T)
        self.vertices = new_vertices.T
        return