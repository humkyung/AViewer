# coding: utf-8
__author__ = "humkyung <humkyung@atools.co.kr>"

# Imports
import sys
import pandas
import vtk


class AFexportReader:
    def __init__(self):
        self._nodes_data = None
        self._elements_data = None
        self._normals = {}
        self._tangents = {}

    def SetFileName(self, node_file_path: str, element_file_path: str) -> None:
        """read node and element csv file"""
        self._nodes_data = pandas.read_csv(node_file_path)
        self._elements_data = pandas.read_csv(element_file_path)

    def GetOutput(self) -> vtk.vtkPolyData:
        """return vtkPolyData"""
        res = None

        try:
            node_data = self._nodes_data.loc[:, self._nodes_data.columns[:4]]
            elem_data = self._elements_data.loc[:, self._elements_data.columns[:10]]

            # Define a set of points - these are the ordered polygon vertices
            points = vtk.vtkPoints()
            points.SetNumberOfPoints(len(node_data))

            progress = 0
            for i in range(len(node_data)):
                idx = node_data.at[i, self._nodes_data.columns[0]]
                x = node_data.at[i, self._nodes_data.columns[1]]
                y = node_data.at[i, self._nodes_data.columns[2]]
                z = node_data.at[i, self._nodes_data.columns[3]]
                points.InsertPoint(idx, x, y, z)

                progress += 1

            faces = vtk.vtkCellArray()
            faces.SetNumberOfCells(len(elem_data))
            for i in range(len(elem_data)):
                # Make a cell with these points
                node0 = elem_data.at[i, self._elements_data.columns[1]]
                node1 = elem_data.at[i, self._elements_data.columns[2]]
                node2 = elem_data.at[i, self._elements_data.columns[3]]
                triangle = [node0, node1, node2]
                faces.InsertNextCell(3, triangle)

                p0 = points.GetPoint(node0)
                p1 = points.GetPoint(node1)
                p2 = points.GetPoint(node2)
                norm = [0.0, 0.0, 0.0]
                vtk.vtkTriangle.ComputeNormal(p0, p1, p2, norm)
                norm = pandas.Series(norm)
                norm *= (elem_data.at[i, self._elements_data.columns[5]] / triangle.GetNumberOfPoints())

                if node0 not in self._normals:
                    self._normals[node0] = norm
                else:
                    self._normals[node0] += norm

                if node1 not in self._normals:
                    self._normals[node1] = norm
                else:
                    self._normals[node1] += norm

                if node2 not in self._normals:
                    self._normals[node2] = norm
                else:
                    self._normals[node2] += norm

                tangent = [elem_data.at[i, self._elements_data.columns[7]],
                           elem_data.at[i, self._elements_data.columns[8]],
                           elem_data.at[i, self._elements_data.columns[9]]]
                tangent = pandas.Series(tangent)
                tangent *= (elem_data.at[i, self._elements_data.columns[6]] / triangle.GetNumberOfPoints())

                if node0 not in self._tangents:
                    self._tangents[node0] = tangent
                else:
                    self._tangents[node0] += tangent

                if node1 not in self._tangents:
                    self._tangents[node1] = tangent
                else:
                    self._tangents[node1] += tangent

                if node2 not in self._tangents:
                    self._tangents[node2] = tangent
                else:
                    self._tangents[node2] += tangent

            # Next you create a vtkPolyData to store your face and vertex information that
            # represents your polyhedron.
            res = vtk.vtkPolyData()
            res.SetPoints(points)
            res.SetPolys(faces)
        except Exception as ex:
            from App import App
            from AppDocData import MessageType

            message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                      f"{sys.exc_info()[-1].tb_lineno}"
            App.mainWnd().addMessage.emit(MessageType.Error, message)

        return res