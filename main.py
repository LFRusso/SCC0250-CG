import numpy as np
import math
import pyrr

from setup import Graphics
from ObjLoader import ObjLoader
from item import Item

vertex_src = """
        # version 330

        layout(location = 0) in vec3 a_position;
        layout(location = 1) in vec2 a_texture;
        layout(location = 2) in vec3 a_normal;
        uniform mat4 model;
        uniform mat4 projection;
        uniform mat4 view;
        out vec2 v_texture;
        void main()
        {
            gl_Position = projection * view * model * vec4(a_position, 1.0);
            v_texture = a_texture;
        }
        """
fragment_src = """
        # version 330
        
        in vec2 v_texture;
        out vec4 out_color;
        uniform sampler2D s_texture;
        void main()
        {
            out_color = texture(s_texture, v_texture);
        }
        """

#floor = Item(pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0])))
floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
floor_indices, floor_buffer = ObjLoader.load_model("meshes/floor.obj")

G = Graphics(700, 700, "Game", vertex_src, fragment_src, 2)
G.addItemBuffer(floor_buffer, "meshes/floor.jpg", 0)
G.mainLoop(floor_pos, floor_indices)