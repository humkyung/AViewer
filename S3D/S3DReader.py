# coding: utf-8
__author__ = "humkyung <humkyung@atools.co.kr>"

# Imports
import sys
import pandas
import vtk


class S3DExportReader:
    KEY = vtk.vtkInformationStringVectorKey.MakeKey('Shape', 'vtkActor')

    def __init__(self):
        self._file_path = None

    def SetFileName(self, file_path: str) -> None:
        """set S3D file path"""
        self._file_path = file_path

    def GetOutput(self, renderer) -> list:
        """return actors"""
        import sqlite3
        from itertools import islice

        def chunk(it, size):
            it = iter(it)
            return iter(lambda: tuple(islice(it, size)), ())

        res = []
        try:
            with sqlite3.connect(self._file_path) as conn:
                cursor = conn.cursor()

                sql = "SELECT VertexList, IndexList, ObjectType, ShapeType from VTEX where ObjectType != 'Pipe_S3D'"
                for row in cursor.execute(sql):
                    tokens = row[0].split(' ')
                    points_ = list(chunk(map(float, [x for x in row[0].split(' ') if x]), 3))
                    indexes = list(chunk(map(int, [x for x in row[1].split(' ') if x]), 3))
                    shape_type = row[3]

                    # Define a set of points - these are the ordered polygon vertices
                    points = vtk.vtkPoints()
                    points.Allocate(len(points_))
                    points.SetNumberOfPoints(len(points_))

                    for idx in range(len(points_)):
                        x, y, z = points_[idx][0], points_[idx][1], points_[idx][2]
                        points.InsertPoint(idx, x, y, z)

                    faces = vtk.vtkCellArray()
                    faces.Allocate(len(indexes))
                    faces.SetNumberOfCells(len(indexes))
                    for idx in range(len(indexes)):
                        # Make a cell with these points
                        triangle = [indexes[idx][0], indexes[idx][1], indexes[idx][2]]
                        faces.InsertNextCell(3, triangle)

                    # Next you create a vtkPolyData to store your face and vertex information that
                    # represents your polyhedron.
                    output = vtk.vtkPolyData()
                    output.SetPoints(points)
                    output.SetPolys(faces)

                    mapper = vtk.vtkPolyDataMapper()
                    mapper.SetInputData(output)

                    actor = vtk.vtkActor()
                    actor.SetMapper(mapper)
                    actor.GetProperty().SetInterpolationToFlat()
                    if shape_type:
                        info = actor.GetProperty().GetInformation()
                        info.Append(S3DExportReader.KEY, f"shape={shape_type}")
                    renderer.AddActor(actor)

                    del points
                    del faces
        except Exception as ex:
            from App import App
            from AppDocData import MessageType

            message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                      f"{sys.exc_info()[-1].tb_lineno}"
            print(message)

        return res