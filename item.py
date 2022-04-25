import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
from OpenGL.GLU import *
import glfw
import pyrr

class Item:
    def __init__(self, position, indices, buffer, texture_file=None):
        self.position = position
        self.indices = indices
        self.buffer = buffer
        self.texture_file = texture_file


        self.Rz = lambda x: np.array([  [np.cos(x), -np.sin(x), 0.0, 0.0], 
                                        [np.sin(x),  np.cos(x), 0.0, 0.0], 
                                        [0.0,      0.0, 1.0, 0.0], 
                                        [0.0,      0.0, 0.0, 1.0]], np.float32)
        
        self.Rx = lambda x: np.array([  [1.0,   0.0,    0.0, 0.0], 
                                        [0.0, np.cos(x), -np.sin(x), 0.0], 
                                        [0.0, np.sin(x),  np.cos(x), 0.0], 
                                        [0.0,   0.0,    0.0, 1.0]], np.float32)
        
        self.Ry = lambda x: np.array([   [np.cos(x),     0.0,  np.sin(x),    0.0], 
                                               [0.0,     1.0,        0.0,    0.0], 
                                        [-np.sin(x),     0.0,  np.cos(x),    0.0], 
                                               [0.0,     0.0,        0.0,    1.0]], np.float32)

        self.T = lambda x,y,z: np.array([   [1.0,   0.0,    0.0,     x], 
                                            [0.0,   1.0,    0.0,     y], 
                                            [0.0,   0.0,    1.0,     z], 
                                            [0.0,   0.0,    0.0,     1.0]], np.float32)
        
        self.S = lambda x,y,z: np.array([     [x,    0.0,    0.0, 0.0], 
                                            [0.0,      y,    0.0, 0.0], 
                                            [0.0,    0.0,      z, 0.0], 
                                            [0.0,    0.0,    0.0, 1.0]], np.float32)
        return

    def processInput(self, G, key):
        return

    def playAction(self, G, *args):
        return

    def onSpawn(self, G, *args):
        return
    
    def translate(self, v):
        v.append(0)
        self.position[-1] = self.position[-1] + np.array(v)
        return

    def scale(self, v):
        self.position = np.dot(self.S(*v), self.position)
        return

    def rotx(self, ang):
        self.position = np.dot(self.Rx(ang), self.position)
        return

    def rotz(self, ang):
        self.position = np.dot(self.Rz(ang), self.position)
        return

    def roty(self, ang):
        self.position = np.dot(self.Ry(ang), self.position)
        return

class Cube(Item):
    def playAction(self, G):
        self.roty(0.01)
        return

    def onSpawn(self, G, *args):
        self.scale([0.02,0.02,0.02])
        return

class Table(Item):
    def onSpawn(self, G, *args):
        self.scale([0.004,0.004,0.004])
        return

    def processInput(self, G, key):
        if key == glfw.KEY_MINUS:
            self.scale([0.9,0.9,0.9])
        if key == glfw.KEY_EQUAL:
            self.scale([1.1,1.1,1.1])
        return

class House(Item):
    def onSpawn(self, G, *args):
        self.scale([7,7,7])
        return

class Teapot(Item):
    def onSpawn(self, G, *args):
        self.scale([.5,.5,.5])
        self.rotz(.5)
        self.roty(.6)
        return

    def processInput(self, G, key):
        if key == glfw.KEY_1:
            self.rotz(.1)
        if key == glfw.KEY_2:
            self.roty(.1)
        return

class Tree(Item):
    def onSpawn(self, G, *args):
        self.scale([10,10,10])
        self.rotx(1.5)
        return

class Mug(Item):
    def onSpawn(self, G, *args):
        self.moving = True
        self.scale([10,10,10])
        return
    
    def processInput(self, G, key):
        if key == glfw.KEY_RIGHT:
            self.translate([.3, 0, 0])
        if key == glfw.KEY_LEFT:
            self.translate([-.3, 0, 0])
        if key == glfw.KEY_UP:
            self.translate([0, 0, -.3])
        if key == glfw.KEY_DOWN:
            self.translate([0, 0, .3])
        return

    def playAction(self, G):
        self.roty(0.01)
        return