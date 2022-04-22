import numpy as np

from setup import Graphics
from item import Item

vertex_src = """
        attribute vec3 position;
        uniform mat4 mat_transformation;

        void main(){
            gl_Position = mat_transformation * vec4(position,1.0);
        }
        """
fragment_src = """
        uniform vec4 color;
        
        void main(){
            gl_FragColor = color;
        }
        """

def cubeAction():
    print("teste")

cube_v = [
    # Face 1 do Cubo (vértices do quadrado)
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
cube_action = lambda: cubeAction()
cube = Item(cube_v, action=cube_action)


G = Graphics(700, 700, "Game")
G.addShaders(vertex_src, fragment_src)
G.addBufferData(cube.vertices, "position")
G.mainLoop([cube])