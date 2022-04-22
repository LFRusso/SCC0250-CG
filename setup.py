import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
from OpenGL.GLU import *
import numpy as np

class Graphics:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height

        glfw.init()
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
        self.window = glfw.create_window(width, height, title, None, None)
        glfw.make_context_current(self.window)
        glfw.show_window(self.window)


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
    
    def addShaders(self, vertex_src, fragment_src):
        # Set shaders source
        self.program  = glCreateProgram()
        self.vertex   = glCreateShader(GL_VERTEX_SHADER)
        self.fragment = glCreateShader(GL_FRAGMENT_SHADER)

        # Set shaders source
        glShaderSource(self.vertex, vertex_src)
        glShaderSource(self.fragment, fragment_src)

        # Compile shaders
        glCompileShader(self.vertex)
        if not glGetShaderiv(self.vertex, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(self.vertex).decode()
            print(error)
            raise RuntimeError("Erro de compilacao do Vertex Shader")

        glCompileShader(self.fragment)
        if not glGetShaderiv(self.fragment, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(self.fragment).decode()
            print(error)
            raise RuntimeError("Erro de compilacao do Fragment Shader")

        # Attach shader objects to the program
        glAttachShader(self.program, self.vertex)
        glAttachShader(self.program, self.fragment)
        
        # Build program
        glLinkProgram(self.program)
        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            print(glGetProgramInfoLog(self.program))
            raise RuntimeError('Linking error')
            
        # Make program the default program
        glUseProgram(self.program)

        # Request a buffer slot from GPU
        self.buffer = glGenBuffers(1)
        # Make this buffer the default one
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
        
        
    def addBufferData(self, data, location):
        data = np.array(data, dtype=np.float32)

        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)

        pos = glGetAttribLocation(self.program, location)
        glEnableVertexAttribArray(pos)
        glVertexAttribPointer(pos, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        return

    def getUniformLocation(self, identifier):
        return glGetUniformLocation(program, identifier)

    def mainLoop(self, items):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0,0.1,0.1,1)
        while not glfw.window_should_close(self.window):
            glfw.poll_events() 
            
            for item in items:
                item.action()
            glRotatef(1, 3, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            glfw.swap_buffers(self.window)
        glfw.terminate()
