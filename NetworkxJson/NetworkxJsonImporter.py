# coding: utf-8
__author__ = "humkyung <humkyung@atools.co.kr>"

# Imports
import os, sys
import vtk
from enum import IntEnum


class NetworksJsonImporter:
    KEY = vtk.vtkInformationStringVectorKey.MakeKey('Attribute', 'vtkActor')

    def __init__(self):
        self._file_path = None
        self._nodes = {}
        self._edges = []

    def SetFileName(self, file_path: str) -> None:
        self._file_path = file_path

    def Read(self) -> None:
        """
        @brief: read given file
        """
        import json

        if os.path.isfile(self._file_path):
            _dict = None
            with open(self._file_path, encoding="utf-8") as f:
                all = f.read()
                _dict = json.loads(all)

            if _dict:
                self.Parse(_dict)

    def Parse(self, _dict: dict):
        """
        @brief: parse given lines
        """

        for node in _dict['nodes']:
            self._nodes[node['name']] = [float(x) for x in node['pos'].split(',')]

        for edge in _dict['edges']:
            self._edges.append([edge['start'], edge['end'], float(edge['length'])])

    def GetOutput(self, renderer):
        """
        @brief: add actors to renderer
        """

        from Primitives.Sphere import Sphere
        from Primitives.Cylinder import Cylinder

        try:
            for name, pos in self._nodes.items():
                actor = Sphere(renderer, pos).actor
                info = actor.GetProperty().GetInformation()
                info.Append(NetworksJsonImporter.KEY, f'{{\"name\":\"{name}\"}}')

            # Generate the polyline for the spline.
            points = vtk.vtkPoints()
            edge_data = vtk.vtkPolyData()

            # Edges
            for edge in self._edges:
                u, v = edge[0], edge[1]
                (sx, sy, sz) = self._nodes[u]
                (ex, ey, ez) = self._nodes[v]
                actor = Cylinder(renderer, pt1=(sx, sy, sz), pt2=(ex, ey, ez), radius=0.1).actor
                info = actor.GetProperty().GetInformation()
                info_str = f'{{\"start\":\"{u}\",\"end\":\"{v}\",\"length\":\"{edge[2]}\"}}'
                info.Append(NetworksJsonImporter.KEY, info_str)
        except Exception as ex:
            message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                      f"{sys.exc_info()[-1].tb_lineno}"
            print(message)


if __name__ == '__main__':
    importer = NetworksJsonImporter()
    importer.SetFileName('sample.json')
    importer.Read()
