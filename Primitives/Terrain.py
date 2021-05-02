# coding: utf-8

__author__ = "humkyung <humkyung.atools.co.kr>"
import vtk
from .SceneObject import SceneObject


class Terrain(SceneObject):
    """A simple template for a terrain.
    Derived from http://vtk.org/gitweb?p=VTK.git;a=blob;f=Examples/Modelling/Python/expCos.py
    """
    terrainPoints = None

    def __init__(self, renderer, surfaceSize):
        """Initialize the terrain. This is derived from the expCos.py example on the vtk.org website, link is above."""
        # Call the parent constructor
        super(Terrain, self).__init__(renderer)
                
        # We create a 'surfaceSize' by 'surfaceSize' point plane to sample
        plane = vtk.vtkPlaneSource()
        plane.SetXResolution(surfaceSize)
        plane.SetYResolution(surfaceSize)
        
        # We transform the plane by a factor of 'surfaceSize' on X and Y
        transform = vtk.vtkTransform()
        transform.Scale(surfaceSize, surfaceSize, 1)
        transF = vtk.vtkTransformPolyDataFilter()
        transF.SetInputConnection(plane.GetOutputPort())
        transF.SetTransform(transform)
        
        # Compute the function that we use for the height generation. 
        # [Original comment] Note the unusual GetPolyDataInput() & GetOutputPort() methods.
        surfaceF = vtk.vtkProgrammableFilter()
        surfaceF.SetInputConnection(transF.GetOutputPort())
        
        # [Original comment] The SetExecuteMethod takes a Python function as an argument
        # In here is where all the processing is done.
        def bessel():
            import math

            input = surfaceF.GetPolyDataInput()
            numPts = input.GetNumberOfPoints()
            newPts = vtk.vtkPoints()
            derivs = vtk.vtkFloatArray()
        
            for i in range(0, numPts):
                x = input.GetPoint(i) 
                x, z = x[:2] # Get the XY plane point, which we'll make an XZ plane point so that's it a ground surface - this is a convenient point to remap it...
        
                # Now do your surface construction here, which we'll just make an arbitrary wavy surface for now.
                y = math.sin(x / float(surfaceSize) * 6.282) * math.cos(z / float(surfaceSize) * 6.282)
        
                newPts.InsertPoint(i, x, y, z)
                derivs.InsertValue(i, y)
        
            surfaceF.GetPolyDataOutput().CopyStructure(input)
            surfaceF.GetPolyDataOutput().SetPoints(newPts)
            surfaceF.GetPolyDataOutput().GetPointData().SetScalars(derivs)
        
        surfaceF.SetExecuteMethod(bessel)
        
        # We warp the plane based on the scalar values calculated above
        warp = vtk.vtkWarpScalar()
        warp.SetInputConnection(surfaceF.GetOutputPort())
        warp.XYPlaneOn()

        # Set the range of the colour mapper to the function min/max we used to generate the terrain.
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(warp.GetOutputPort())
        mapper.SetScalarRange(-1, 1)

        # Make our terrain wireframe so that it doesn't occlude the whole scene
        self.vtkActor.GetProperty().SetRepresentationToWireframe()
        
        # Finally assign this to the parent class actor so that it draws.
        self.vtkActor.SetMapper(mapper)