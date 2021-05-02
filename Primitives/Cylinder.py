# coding: utf-8

__author__ = "humkyung <humkyung.atools.co.kr>"

import vtk
from .SceneObject import SceneObject


class Cylinder(SceneObject):
    """A template for drawing a cylinder."""

    def __init__(self, renderer, pt1=(0, 0, 0), pt2=(0, 0, 10), radius: float = 0.5):
        """Initialize the cylinder."""
        # Call the parent constructor
        super(Cylinder, self).__init__(renderer)

        """
        points = vtk.vtkPoints()
        lines = vtk.vtkCellArray()
        lines.InsertNextCell(2)
        # point 0
        points.InsertNextPoint(pt1[0], pt1[1], pt1[2])
        lines.InsertCellPoint(0)
        # point 1
        points.InsertNextPoint(pt2[0], pt2[1], pt2[2])
        lines.InsertCellPoint(1)

        cData = vtk.vtkPolyData()
        cData.SetPoints(points)
        cData.SetLines(lines)

        c = vtk.vtkTubeFilter()
        c.SetNumberOfSides(8)
        c.SetInputData(cData)
        c.SetRadius(1000)

        cMapper = vtk.vtkPolyDataMapper()
        cMapper.SetInputConnection(c.GetOutputPort())

        #cActor = vtk.vtkActor()
        self.vtkActor.SetMapper(cMapper)
        #cActor.GetProperty().SetColor(rgb[0], rgb[1], rgb[2])
        #cActor.GetProperty().SetOpacity(opacity)
        """

        # Create a line
        line_source = vtk.vtkLineSource()
        line_source.SetPoint1(pt1[0], pt1[1], pt1[2])
        line_source.SetPoint2(pt2[0], pt2[1], pt2[2])

        # Create a tube(cylinder) around the line
        tube_filter = vtk.vtkTubeFilter()
        tube_filter.SetInputConnection(line_source.GetOutputPort())
        tube_filter.SetRadius(radius)  # default is .5
        tube_filter.SetNumberOfSides(50)
        tube_filter.Update()

        # Create a mapper and actor
        tube_mapper = vtk.vtkPolyDataMapper()
        tube_mapper.SetInputConnection(tube_filter.GetOutputPort())
        self.vtkActor.SetMapper(tube_mapper)
