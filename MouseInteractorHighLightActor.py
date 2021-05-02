# coding: utf-8
""" This is MouseInteractorHighLightActor module """

from warnings import warn
import sys
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import numpy as np


class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)

        self.LastPickedActor = None
        self.LastPickedProperty = vtk.vtkProperty()

    def leftButtonPressEvent(self, obj, event) -> None:
        try:
            clickPos = self.GetInteractor().GetEventPosition()

            picker = vtk.vtkPropPicker()
            picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())

            # get the new
            self.NewPickedActor = picker.GetActor()

            # If something was selected
            if self.NewPickedActor:
                # If we picked something before, reset its property
                if self.LastPickedActor:
                    self.LastPickedActor.GetProperty().DeepCopy(self.LastPickedProperty)

                # Save the property of the picked actor so that we can
                # restore it next time
                self.LastPickedProperty.DeepCopy(self.NewPickedActor.GetProperty())
                # Highlight the picked actor by changing its properties
                self.NewPickedActor.GetProperty().SetColor(1.0, 0.0, 0.0)
                self.NewPickedActor.GetProperty().SetDiffuse(1.0)
                self.NewPickedActor.GetProperty().SetSpecular(0.0)

                # save the last picked actor
                self.LastPickedActor = self.NewPickedActor

            self.OnLeftButtonDown()
        except Exception as ex:
            from App import App
            from AppDocData import MessageType

            message = f"error occurred({str(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                      f"{sys.exc_info()[-1].tb_lineno}"

            App.mainWnd().addMessage.emit(MessageType.Error, message)