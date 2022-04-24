import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders
from OpenGL.GLU import *
import pyrr

class Item:
    def __init__(self, position):
        self.position = position

    
    def translate(self, G, v):
        loc = glGetUniformLocation(G.program, "mat_transformation")
        #new_vertices = np.dot(self.T(*v).reshape(4,4),self.vertices.T)
        #self.vertices = new_vertices.T
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

class Cube(Item):
    def __init__(self):
        self.d = 0

        self.vertices = [
            # Face 1 do Cu'bo (vértices do quadrado)
            (-0.2, -0.2, +0.2),
            (+0.2, -0.2, +0.2),
            (-0.2, +0.2, +0.2),
            (+0.2, +0.2, +0.2),

            # Face 2 do Cubo
            (+0.2, -0.2, +0.2),
            (+0.2, -0.2, -0.2),         
            (+0.2, +0.2, +0.2),
            (+0.2, +0.2, -0.2),
            
            # Face 3 do Cubo
            (+0.2, -0.2, -0.2),
            (-0.2, -0.2, -0.2),            
            (+0.2, +0.2, -0.2),
            (-0.2, +0.2, -0.2),

            # Face 4 do Cubo
            (-0.2, -0.2, -0.2),
            (-0.2, -0.2, +0.2),         
            (-0.2, +0.2, -0.2),
            (-0.2, +0.2, +0.2),

            # Face 5 do Cubo
            (-0.2, -0.2, -0.2),
            (+0.2, -0.2, -0.2),         
            (-0.2, -0.2, +0.2),
            (+0.2, -0.2, +0.2),
            
            # Face 6 do Cubo
            (-0.2, +0.2, +0.2),
            (+0.2, +0.2, +0.2),           
            (-0.2, +0.2, -0.2),
            (+0.2, +0.2, -0.2)]

    def action(self, G, *args):
        loc_color = glGetUniformLocation(G.program, "a_texture")

        self.d -= 0.01
        mat_transform = G.matMul(G.Rz(self.d), G.Ry(self.d))
        mat_transform = G.matMul(G.Rx(self.d), mat_transform)

        loc = glGetUniformLocation(G.program, "projection")
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

 
        glUniform4f(loc_color, 1, 0, 0, 1.0) ### vermelho
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        
        glUniform4f(loc_color, 0, 0, 1, 1.0) ### azul
        glDrawArrays(GL_TRIANGLE_STRIP, 4, 4)
        
        glUniform4f(loc_color, 0, 1, 0, 1.0) ### verde
        glDrawArrays(GL_TRIANGLE_STRIP, 8, 4)
        
        glUniform4f(loc_color, 1, 1, 0, 1.0) ### amarela
        glDrawArrays(GL_TRIANGLE_STRIP, 12, 4)
        
        glUniform4f(loc_color, 0.5, 0.5, 0.5, 1.0) ### cinza
        glDrawArrays(GL_TRIANGLE_STRIP, 16, 4)
        
        glUniform4f(loc_color, 0.5, 0, 0, 1.0) ### marrom
        glDrawArrays(GL_TRIANGLE_STRIP, 20, 4)
        return