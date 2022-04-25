import numpy as np
import math
import pyrr

from setup import Graphics
from ObjLoader import ObjLoader
from item import Item, Cube, Table, House, Teapot, Tree, Mug

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

teapot_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-3, 1.6, -12]))
teapot_indices, teapot_buffer = ObjLoader.load_model("meshes/teapot.obj")
teapot = Teapot(teapot_pos, teapot_indices, teapot_buffer, "textures/crate.jpg")

table_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-4, 0, -10]))
table_indices, table_buffer = ObjLoader.load_model("meshes/table.obj")
table = Table(table_pos, table_indices, table_buffer, "textures/table.jpg")

house_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([15, 0, -11]))
house_indices, house_buffer = ObjLoader.load_model("meshes/house.obj")
house = House(house_pos, house_indices, house_buffer, "textures/brick.jpg")

floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, -10]))
floor_indices, floor_buffer = ObjLoader.load_model("meshes/floor.obj")
floor = Item(floor_pos, floor_indices, floor_buffer, "textures/grass.jpg")

tree_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-10, 0, -20]))
tree_indices, tree_buffer = ObjLoader.load_model("meshes/trees.obj")
tree = Tree(tree_pos, tree_indices, tree_buffer, "textures/trees.png")

mug_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([15, 1.5, -5]))
mug_indices, mug_buffer = ObjLoader.load_model("meshes/mug.obj")
mug = Mug(mug_pos, mug_indices, mug_buffer, "textures/crate.jpg")

G = Graphics(700, 700, "Game", vertex_src, fragment_src, [tree, floor, table, house, teapot, mug])
G.mainLoop()