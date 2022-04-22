import numpy as np
import math

from setup import Graphics
from item import Cube

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

cube = Cube()

G = Graphics(700, 700, "Game")
G.addShaders(vertex_src, fragment_src)
G.addBufferData(cube.vertices, "position")
G.mainLoop([cube])