# coding: utf-8

__author__ = "humkyung <humkyung.atools.co.kr>"

import vtk
from .SceneObject import SceneObject


class Sphere(SceneObject):
    """A template for drawing a sphere."""

    def __init__(self, renderer, center, radius: float = 1):
        """Initialize the sphere."""
        # Call the parent constructor
        super(Sphere, self).__init__(renderer)
        
        sphereSource = vtk.vtkSphereSource()
        sphereSource.SetCenter(center[0], center[1], center[2])
        sphereSource.SetRadius(radius)
        # Make it a little more defined
        sphereSource.SetThetaResolution(24)
        sphereSource.SetPhiResolution(24)
         
        sphereMapper = vtk.vtkPolyDataMapper()
        sphereMapper.SetInputConnection(sphereSource.GetOutputPort())
         
        self.vtkActor.SetMapper(sphereMapper)
