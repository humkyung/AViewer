# coding: utf-8

__author__ = "humkyung <humkyung.atools.co.kr>"

import vtk
from .SceneObject import SceneObject


class CTorus(SceneObject):
    """A template for drawing a circular torus."""

    def __init__(self, renderer, pt1=(0, 0, 0), pt2=(0, 0, 10), center=(5, 0, 5), angle: float = 90, radius: float = 0.5):
        """Initialize the ctorus."""
        # Call the parent constructor
        import math

        super(CTorus, self).__init__(renderer)
        self._resolution = 12

        mid = ((pt1[0] + pt2[0]) * 0.5, (pt1[1] + pt2[1]) * 0.5, (pt1[2] + pt2[2]) * 0.5)
        length = math.sqrt(vtk.vtkMath.Distance2BetweenPoints(pt1, center))

        L = length / math.sin(math.radians(angle) * 0.5)
        dir = [mid[0] - center[0], mid[1] - center[1], mid[2] - center[2]]
        vtk.vtkMath.Normalize(dir)
        self._origin = (center[0] + dir[0] * L, center[1] + dir[1] * L, center[2] + dir[2] * L)

        # create a circle
        circle = vtk.vtkRegularPolygonSource()
        circle.SetCenter((pt1[0] - self._origin[0], pt1[1] - self._origin[1], pt1[2] - self._origin[2]))
        circle.SetNormal((pt1[0] - center[0], pt1[1] - center[1], pt1[2] - center[2]))
        circle.SetRadius(radius)
        circle.SetNumberOfSides(24)
        circle.Update()
        circle_points = circle.GetOutput().GetPoints()  # get points from circle
        del circle

        # Setup points and lines
        points = vtk.vtkPoints()
        points.Allocate((self._resolution + 1) * circle_points.GetNumberOfPoints())
        faces = vtk.vtkCellArray()
        faces.SetNumberOfCells(self._resolution * circle_points.GetNumberOfPoints())
        lines = vtk.vtkCellArray()

        num = circle_points.GetNumberOfPoints()
        for idx in range(num):
            points.InsertNextPoint(circle_points.GetPoint(idx))
            if idx < num - 1:
                line = vtk.vtkLine()
                line.GetPointIds().SetId(0, idx)
                line.GetPointIds().SetId(1, idx + 1)
                lines.InsertNextCell(line)
            else:
                line = vtk.vtkLine()
                line.GetPointIds().SetId(0, idx)
                line.GetPointIds().SetId(1, 0)
                lines.InsertNextCell(line)

        appended_polydata = vtk.vtkAppendPolyData()

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(circle_points)
        polydata.SetLines(lines)
        appended_polydata.AddInputData(polydata)

        vectors = [(center[0] - pt1[0], center[1] - pt1[1], center[2] - pt1[2]),
                   (pt2[0] - pt1[0], pt2[1] - pt1[1], pt2[2] - pt1[2])]
        normal = [0, 0, 0]
        vtk.vtkMath.Cross(vectors[0], vectors[1], normal)
        vtk.vtkMath.Normalize(normal)

        transform = vtk.vtkTransform()
        transform.Identity()
        transform.RotateWXYZ(angle/self._resolution, normal[0], normal[1], normal[2])

        for idx in range(self._resolution):
            transform_filter = vtk.vtkTransformPolyDataFilter()
            transform_filter.SetInputData(polydata)
            transform_filter.SetTransform(transform)
            transform_filter.Update()
            polydata = transform_filter.GetOutput()

            for idx in range(num):
                points.InsertNextPoint(polydata.GetPoint(idx))

            appended_polydata.AddInputData(polydata)
            appended_polydata.Update()

        clean = vtk.vtkCleanPolyData()
        clean.SetInputData(appended_polydata.GetOutput())
        clean.Update()

        for v in range(self._resolution):
            for u in range(circle_points.GetNumberOfPoints()):
                faces.InsertNextCell(4, [v*circle_points.GetNumberOfPoints() + u,
                                         v*circle_points.GetNumberOfPoints() + (u + 1) % circle_points.GetNumberOfPoints(),
                                         (v + 1)*circle_points.GetNumberOfPoints() + (u + 1) % circle_points.GetNumberOfPoints(),
                                         (v + 1)*circle_points.GetNumberOfPoints() + u])

        output = vtk.vtkPolyData()
        output.SetPoints(points)
        output.SetPolys(faces)

        transform_ = vtk.vtkTransform()
        transform_.Identity()
        transform_.Translate(self._origin)

        filter = vtk.vtkTransformPolyDataFilter()
        filter.SetTransform(transform_)
        filter.SetInputData(output)

        # Create a mapper and actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(filter.GetOutputPort())
        self.vtkActor.SetMapper(mapper)

    @property
    def origin(self):
        return self._origin

    @property
    def resolution(self) -> int:
        return self._resolution