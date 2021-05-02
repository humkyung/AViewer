# coding: utf-8

__author__ = "humkyung <humkyung.atools.co.kr>"
import vtk
from .SceneObject import SceneObject


class Axes(SceneObject):
    """This is a axes class"""
    terrainPoints = None

    def __init__(self, renderer):
        """Initialize the terrain. This is derived from the expCos.py example on the vtk.org website, link is above."""
        # Call the parent constructor
        super(Axes, self).__init__(renderer)

        def make_annotated_cube_actor(colors):
            """make annotated cube actor"""

            # Annotated Cube setup
            annotated_cube = vtk.vtkAnnotatedCubeActor()
            annotated_cube.SetFaceTextScale(0.366667)

            # Anatomic labeling
            annotated_cube.SetXPlusFaceText('X+')
            annotated_cube.SetXMinusFaceText('X-')
            annotated_cube.SetYPlusFaceText('Y+')
            annotated_cube.SetYMinusFaceText('Y-')
            annotated_cube.SetZPlusFaceText('Z+')
            annotated_cube.SetZMinusFaceText('Z-')

            # Change the vector text colors
            annotated_cube.GetTextEdgesProperty().SetColor(colors.GetColor3d('Black'))
            annotated_cube.GetTextEdgesProperty().SetLineWidth(1)

            annotated_cube.GetXPlusFaceProperty().SetColor(colors.GetColor3d('Turquoise'))
            annotated_cube.GetXMinusFaceProperty().SetColor(colors.GetColor3d('Turquoise'))
            annotated_cube.GetYPlusFaceProperty().SetColor(colors.GetColor3d('Mint'))
            annotated_cube.GetYMinusFaceProperty().SetColor(colors.GetColor3d('Mint'))
            annotated_cube.GetZPlusFaceProperty().SetColor(colors.GetColor3d('Tomato'))
            annotated_cube.GetZMinusFaceProperty().SetColor(colors.GetColor3d('Tomato'))
            annotated_cube.SetXFaceTextRotation(90)
            annotated_cube.SetYFaceTextRotation(180)
            annotated_cube.SetZFaceTextRotation(-90)
            # Make the annotated cube transparent
            annotated_cube.GetCubeProperty().SetOpacity(0)

            # Colored faces cube setup
            cube_source = vtk.vtkCubeSource()
            cube_source.Update()

            face_colors = vtk.vtkUnsignedCharArray()
            face_colors.SetNumberOfComponents(3)
            face_x_plus = colors.GetColor3ub('Red')
            face_x_minus = colors.GetColor3ub('Green')
            face_y_plus = colors.GetColor3ub('Blue')
            face_y_minus = colors.GetColor3ub('Yellow')
            face_z_plus = colors.GetColor3ub('Cyan')
            face_z_minus = colors.GetColor3ub('Magenta')
            face_colors.InsertNextTypedTuple(face_x_minus)
            face_colors.InsertNextTypedTuple(face_x_plus)
            face_colors.InsertNextTypedTuple(face_y_minus)
            face_colors.InsertNextTypedTuple(face_y_plus)
            face_colors.InsertNextTypedTuple(face_z_minus)
            face_colors.InsertNextTypedTuple(face_z_plus)

            cube_source.GetOutput().GetCellData().SetScalars(face_colors)
            cube_source.Update()

            cube_mapper = vtk.vtkPolyDataMapper()
            cube_mapper.SetInputData(cube_source.GetOutput())
            cube_mapper.Update()

            cube_actor = vtk.vtkActor()
            cube_actor.SetMapper(cube_mapper)

            # Assemble the colored cube and annotated cube texts into a composite prop.
            prop_assembly = vtk.vtkPropAssembly()
            prop_assembly.AddPart(annotated_cube)
            prop_assembly.AddPart(cube_actor)
            return prop_assembly

        colors = vtk.vtkNamedColors()
        axesActor = make_annotated_cube_actor(colors)

        self.__axes = vtk.vtkOrientationMarkerWidget()
        self.__axes.SetOrientationMarker(axesActor)
        self.__axes.SetInteractor(renderer.GetRenderWindow().GetInteractor())
        self.__axes.SetDefaultRenderer(renderer)
        self.__axes.SetEnabled(1)
        self.__axes.On()
        self.__axes.InteractiveOff()