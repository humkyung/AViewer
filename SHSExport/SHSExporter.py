# coding: utf-8
__author__ = "humkyung <humkyung@atools.co.kr>"

# Imports
import os
import sys
import pandas
import vtk


class SHSExporter:
    class Mesh:
        SHAPE_CODE = {'Cylinder': 1, 'Torus': 2, 'Plane': 3}

        def __init__(self):
            self._vertices = []
            self._normals = []
            self._triangles = []
            self._shape_type = None
            self._color = None

        @property
        def vertices(self):
            return self._vertices

        @property
        def triangles(self):
            return self._triangles

        @property
        def shape_type(self):
            return self._shape_type

        @shape_type.setter
        def shape_type(self, value):
            self._shape_type = value

        @property
        def shape_type_code(self) -> int:
            if self._shape_type in SHSExporter.Mesh.SHAPE_CODE:
                return SHSExporter.Mesh.SHAPE_CODE[self._shape_type]
            else:
                return 0

        @property
        def color(self):
            return self._color

        @color.setter
        def color(self, value):
            self._color = value

        def write(self, file, idx: int) -> None:
            import struct

            try:
                file.write(struct.pack('I', idx))  # mesh id

                data = struct.pack('ffff', self.color[0], self.color[1], self.color[2], 1)
                file.write(data)
                data = struct.pack('I', len(self.vertices))
                file.write(data)
                data = struct.pack('I', len(self.triangles))
                file.write(data)
                for idx in range(len(self.vertices)):
                    data = struct.pack('fff', self.vertices[idx][0], self.vertices[idx][1], self.vertices[idx][2])
                    file.write(data)

                for id in self.triangles:
                    data = struct.pack('H', id)
                    file.write(data)

                data = struct.pack('I', self.shape_type_code)
                file.write(data)
            except Exception as ex:
                message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                          f"{sys.exc_info()[-1].tb_lineno}"
                print(message)

    def __init__(self):
        self._render = None
        self._file_path = None
        self._mesh_tables = []

    def SetRenderWindow(self, render) -> None:
        """set render window"""

        self._render = render

    def SetFileName(self, file_path: str) -> None:
        """return vtkPolyData"""
        self._file_path = file_path

    def Write(self):
        """
        @brief: write all objects to given file
        """

        import struct
        from S3D.S3DReader import S3DExportReader

        try:
            with open(self._file_path, 'wb') as f:
                version = 1
                data = struct.pack('I', version)
                f.write(data)

                renderers = self._render.GetRenderers()
                renderers.InitTraversal()
                count = renderers.GetNumberOfItems()
                for _ in range(count):
                    render = renderers.GetNextItem()
                    actors = render.GetActors()
                    numActors = actors.GetNumberOfItems()
                    if not numActors:
                        continue

                    # Structure Table
                    # structure count
                    data = struct.pack('I', numActors)
                    f.write(data)

                    actors.InitTraversal()
                    for i in range(0, numActors):
                        f.write(struct.pack('II', i, 2))  # node id, node type
                        f.write(struct.pack('I', 0))  # name length

                        actor = actors.GetNextItem()
                        bounds = actor.GetBounds()
                        f.write(struct.pack('ffffff', bounds[0], bounds[1], bounds[2], bounds[3], bounds[4], bounds[5]))  # bounding box
                        f.write(struct.pack('ffffffffffffffff',
                                            1, 0, 0, 0,
                                            0, 1, 0, 0,
                                            0, 0, 1, 0,
                                            0, 0, 0, 1))  # transform matrix
                        f.write(struct.pack('I', 0))  # property count
                        f.write(struct.pack('I', 1))  # mesh count
                        f.write(struct.pack('I', i))  # mesh id
                        f.write(struct.pack('I', 0))  # child node id list count

                        prop = actor.GetProperty()
                        info = prop.GetInformation()
                        mesh = SHSExporter.Mesh()
                        mesh.color = prop.GetColor()
                        if info.Has(S3DExportReader.KEY):
                            props = actor.GetProperty().GetInformation().Length(S3DExportReader.KEY)
                            for prop_idx in range(props):
                                value = actor.GetProperty().GetInformation().Get(S3DExportReader.KEY, prop_idx)
                                tokens = value.split('=')
                                mesh.shape_type = tokens[1] if len(tokens) == 2 and 'shape' == tokens[0] else None

                        mapper = actor.GetMapper()

                        data = mapper.GetInput()
                        normals = data.GetPointData().GetNormals()

                        points = data.GetPoints()
                        num = points.GetNumberOfPoints()
                        for idx in range(num):
                            pt = points.GetPoint(idx)
                            mesh.vertices.append(pt)

                        polys = data.GetPolys()
                        cells = polys.GetNumberOfCells()
                        for idx in range(cells):
                            id_list = vtk.vtkIdList()
                            polys.GetNextCell(id_list)
                            ids = id_list.GetNumberOfIds()
                            for idx_ in range(ids):
                                id = id_list.GetId(idx_)
                                mesh.triangles.append(id)

                        self._mesh_tables.append(mesh)

                # PropTable
                # property count
                data = struct.pack('I', 0)
                f.write(data)

                # Mesh Table
                # mesh count
                data = struct.pack('I', len(self._mesh_tables))
                f.write(data)
                for idx, mesh in enumerate(self._mesh_tables):
                    mesh.write(f, idx)
        except Exception as ex:
            message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                      f"{sys.exc_info()[-1].tb_lineno}"
            print(message)


if __name__ == '__main__':
    import struct

    file_path = 'd:\\Projects\\ATOOLS\\AViewer\\Projects\\2020.12.22.shs'
    with open(file_path, mode='rb') as file:  # b is important -> binary
        data = file.read()
        version = struct.unpack('I', data[:4])

        pos = 4
        # structure
        structure_cnt, pos = struct.unpack('I', data[pos:pos + 4]), pos + 4
        for idx in range(structure_cnt[0]):
            index, pos = struct.unpack('I', data[pos:pos + 4]), pos + 4
            type_, pos = struct.unpack('I', data[pos:pos + 4]), pos + 4
            name_len, pos = struct.unpack('I', data[pos:pos + 4]), pos + 4
            bbox, pos = struct.unpack('ffffff', data[pos:pos + 4*6]), pos + 4*6
            transform, pos = struct.unpack('ffffffffffffffff', data[pos:pos + 4 * 16]), pos + 4 * 16
            prop_cnt, pos = struct.unpack('I', data[pos:pos + 4]), pos + 4
            mesh_cnt, pos = struct.unpack('I', data[pos:pos + 4]), pos + 4
            mesh_id, pos = struct.unpack('I', data[pos:pos + 4]), pos + 4
            child_node_cnt, pos = struct.unpack('I', data[pos:pos + 4]), pos + 4
        # up to here

        # property
        property_cnt, pos = struct.unpack('I', data[pos:pos + 4]), pos + 4
        # up to here

        # mesh
        mesh_count, pos = struct.unpack('I', data[pos:pos + 4]), pos + 4
        for mesh in range(mesh_count[0]):
            mesh_id, pos = struct.unpack('I', data[pos:pos + 4]), pos + 4
            (r, g, b, a), pos = struct.unpack('ffff', data[pos:pos + 16]), pos + 4*4
            vertex_cnt, pos = struct.unpack('I', data[pos:pos + 4]), pos + 4
            triangle_cnt, pos = struct.unpack('I', data[pos:pos + 4]), pos + 4

            for vertex in range(vertex_cnt[0]):
                (x, y, z), pos = struct.unpack('fff', data[pos:pos + 4*3]), pos + 4*3

            for triangle in range(triangle_cnt[0]):
                index, pos = struct.unpack('H', data[pos:pos + 2]), pos + 2

            shape_type, pos = struct.unpack('I', data[pos: pos + 4]), pos + 4
        # up to here
