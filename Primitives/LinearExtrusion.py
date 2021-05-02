# coding: utf-8

__author__ = "humkyung <humkyung.atools.co.kr>"

import vtk
from .SceneObject import SceneObject


class LinearExtrusion(SceneObject):
    """A template for drawing a linear extrusion."""

    def __init__(self, renderer, pts: list, dir: list, scale: float):
        """Initialize the linear extrusion."""
        # Call the parent constructor
        super(LinearExtrusion, self).__init__(renderer)

        # Create a section shape
        points = vtk.vtkPoints()
        for idx, pt in enumerate(pts):
            points.InsertPoint(idx, pt[0], pt[1], pt[2])
            
        faces = vtk.vtkCellArray()
        # Make a cell with these points
        facet = range(len(pts))
        faces.InsertNextCell(len(pts), facet)
            
        profile = vtk.vtkPolyData()
        profile.SetPoints(points)
        profile.SetPolys(faces)

        # Extrude the profile to make the bottle.
        extrude = vtk.vtkLinearExtrusionFilter()
        extrude.SetInputData(profile)
        extrude.SetVector(dir[0], dir[1], dir[0])
        extrude.CappingOn()
        extrude.SetScaleFactor(scale)
        extrude.SetExtrusionTypeToNormalExtrusion()
        
        triangle_filter = vtk.vtkTriangleFilter()
        triangle_filter.SetInputConnection(extrude.GetOutputPort())

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(triangle_filter.GetOutputPort())
        self.vtkActor.SetMapper(mapper)