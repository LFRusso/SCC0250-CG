import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import pyrr

from camera import Camera
from TextureLoader import load_texture

class Graphics:
    def __init__(self, width, height, title, vertex_src, fragment_src, buffers):
        self.width = width
        self.height = height
        self.lastX = width/2
        self.lastY = height/2
        self.projection = pyrr.matrix44.create_perspective_projection_matrix(45, width/height, 0.1, 100)
        self.first_mouse = True
        self.left, self.right, self.forward, self.backward = False, False, False, False
        self.camera = Camera()

        glfw.init()
        #glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        self.window = glfw.create_window(width, height, title, None, None)
        
        # Callbacks
        glfw.set_cursor_pos_callback(self.window, self._mouse_look_clb)
        glfw.set_cursor_enter_callback(self.window, self._mouse_enter_clb)
        glfw.set_window_size_callback(self.window, self._window_resize_clb)
        glfw.set_key_callback(self.window, self._keyboard_clb)

        # capture the mouse cursor
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        # make the context current
        glfw.make_context_current(self.window)
        glfw.show_window(self.window)

        self._add_shaders(vertex_src, fragment_src, buffers)


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
        return

    def _window_resize_clb(self, window, width, height):
        glViewport(0, 0, width, height)
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, projection)
        return
        
    def _keyboard_clb(self, window, key, scancode, action, mode):
        global left, right, forward, backward
        if (key == glfw.KEY_ESCAPE or key == glfw.KEY_Q) and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        if key == glfw.KEY_W and action == glfw.PRESS:
            self.forward = True
        elif key == glfw.KEY_W and action == glfw.RELEASE:
            self.forward = False
        if key == glfw.KEY_S and action == glfw.PRESS:
            self.backward = True
        elif key == glfw.KEY_S and action == glfw.RELEASE:
            self.backward = False
        if key == glfw.KEY_A and action == glfw.PRESS:
            self.left = True
        elif key == glfw.KEY_A and action == glfw.RELEASE:
            self.left = False
        if key == glfw.KEY_D and action == glfw.PRESS:
            self.right = True
        elif key == glfw.KEY_D and action == glfw.RELEASE:
            self.right = False
        return

    def _mouse_look_clb(self, window, xpos, ypos):
        if self.first_mouse:
            self.lastX = xpos
            self.lastY = ypos

        xoffset = xpos - self.lastX
        yoffset = ypos - self.lastY

        self.lastX = xpos
        self.lastY = ypos
 
        self.camera.process_mouse_movement(xoffset, yoffset)
        return

    def _mouse_enter_clb(self, window, entered):
        if entered:
            self.first_mouse = False
        else:
            self.first_mouse = True
        return

    def matMul(self, a, b):
        m_a = a.reshape(4,4)
        m_b = b.reshape(4,4)
        m_c = np.dot(m_a,m_b)
        c = m_c.reshape(1,16)
        return c
    
    def _add_shaders(self, vertex_src, fragment_src, buffers):
            
        self.shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

        # Make the default program
        glUseProgram(self.shader)
        glClearColor(0, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Request a buffer slot from GPU
        self.VAO = glGenVertexArrays(buffers)
        self.VBO = glGenBuffers(buffers)
        self.textures = glGenTextures(buffers)
        
        self.model_loc = glGetUniformLocation(self.shader, "model")
        self.proj_loc = glGetUniformLocation(self.shader, "projection")
        self.view_loc = glGetUniformLocation(self.shader, "view")

        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, self.projection)
        return

    def addItemBuffer(self, buffer, texture_file, index):
        glBindVertexArray(self.VAO[index])
        # Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[index])
        glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)

        # vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(0))
        # textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(12))
        # normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        load_texture(texture_file, self.textures[index])
        return

    def move(self):
        if self.left:
            self.camera.process_keyboard("LEFT", 0.05)
        if self.right:
            self.camera.process_keyboard("RIGHT", 0.05)
        if self.forward:
            self.camera.process_keyboard("FORWARD", 0.05)
        if self.backward:
            self.camera.process_keyboard("BACKWARD", 0.05)
        return

    def mainLoop(self, floor_pos, floor_indices):
        view_loc = glGetUniformLocation(self.shader, "view")

        while not glfw.window_should_close(self.window):
            glfw.poll_events() 
            self.move()

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            view = self.camera.get_view_matrix()
            glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
            # draw the floor
            glBindVertexArray(self.VAO[0])
            glBindTexture(GL_TEXTURE_2D, self.textures[0])
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, floor_pos)
            glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))

            #view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 2, 16]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))
            #glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
            #for item in self.items:
            #    item.action(self)
            

            glfw.swap_buffers(self.window)
        glfw.terminate()
