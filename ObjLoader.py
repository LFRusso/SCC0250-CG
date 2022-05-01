import numpy as np

class ObjLoader:
    buffer = []

    @staticmethod
    def search_data(data_values, coordinates, skip, data_type):
        for d in data_values:
            if d == skip:
                continue
            if data_type == 'float':
                coordinates.append(float(d))
            elif data_type == 'int':
                coordinates.append(int(d)-1)


    @staticmethod # sorted vertex buffer for use with glDrawArrays function
    def create_sorted_vertex_buffer(indices_data, vertices, textures, normals):
        for i, ind in enumerate(indices_data):
            if i % 3 == 0: # sort the vertex coordinates
                start = ind * 3
                end = start + 3
                ObjLoader.buffer.extend(vertices[start:end])
            elif i % 3 == 1: # sort the texture coordinates
                start = ind * 2
                end = start + 2
                ObjLoader.buffer.extend(textures[start:end])
            elif i % 3 == 2: # sort the normal vectors
                start = ind * 3
                end = start + 3
                ObjLoader.buffer.extend(normals[start:end])

    @staticmethod
    def get_normals(indices_data, vertices, normals):
        num_verts = len(vertices) // 3
        num_normals = len(indices_data) // 3
        
        v = np.reshape(vertices, (num_verts, 3))
        
        for i1 in range(num_normals):
            start = i1 * 3
            end = start + 3
            v1, v2, v3 = v[indices_data[start:end]]
            edge1 = v1-v2
            edge2 = v1-v3

            normals += list(np.cross(edge1, edge2))

    @staticmethod
    def load_model(file):
        vert_coords = [] # vertex coordinates
        tex_coords = [] # texture coordinates
        norm_coords = [] # vertex normals

        all_indices = [] # vertex, texture and normal indices
        indices = [] # indices for indexed drawing


        with open(file, 'r') as f:
            line = f.readline()
            while line:
                values = line.split()
                try:
                    if values[0] == 'v':
                        ObjLoader.search_data(values, vert_coords, 'v', 'float')
                    elif values[0] == 'vt':
                        ObjLoader.search_data(values, tex_coords, 'vt', 'float')
                    elif values[0] == 'vn':
                        ObjLoader.search_data(values, norm_coords, 'vn', 'float')
                    elif values[0] == 'f':
                        for value in values[1:]:
                            if '/' not in value: # vertex and index only
                                val = value
                                ObjLoader.search_data([val, val, '1'], all_indices, 'f', 'int')
                                indices.append(int(val)-1)
                            elif '//' not in value:
                                val = value.split('/')
                                if(len(val) == 2):
                                    val = [val[0], val[1], '1']
                                    ObjLoader.search_data(val, all_indices, 'f', 'int')
                                    indices.append(int(val[0])-1)
                                else:
                                    ObjLoader.search_data(val, all_indices, 'f', 'int')
                                    indices.append(int(val[0])-1)
                            else:
                                val = value.split('//')
                                val = [val[0], val[0], val[1]]
                                ObjLoader.search_data(val, all_indices, 'f', 'int')
                                indices.append(int(val[0])-1)
                except:
                    pass
                line = f.readline()

        if len(tex_coords) == 0:
            tex_coords = [0.,0.]*len(indices)
        if len(norm_coords) == 0:
            ObjLoader.get_normals(indices, vert_coords, norm_coords)

        ObjLoader.create_sorted_vertex_buffer(all_indices, vert_coords, tex_coords, norm_coords)

        buffer = ObjLoader.buffer.copy() 
        ObjLoader.buffer = [] 

        return np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32')

