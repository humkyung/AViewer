# coding: utf-8
""" This is Scene module """

from warnings import warn
from qt import *
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from MouseInteractorHighLightActor import MouseInteractorHighLightActor


class QVTKViewer(QFrame):
    def __init__(self, parent, renderer):
        super(QVTKViewer, self).__init__(parent)

        self.interactor = QVTKRenderWindowInteractor(self)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.interactor)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.interactor.GetRenderWindow().AddRenderer(renderer)

        self.style = MouseInteractorHighLightActor()
        self.style.SetDefaultRenderer(renderer)
        self.interactor.SetInteractorStyle(self.style)

    @property
    def render_window(self):
        return self.interactor.GetRenderWindow()

    def process_pick(self, object, event):
        point_id = object.GetPointId()
        if point_id >= 0:
            vector_magnitude = self.glyphs.GetOutput().GetPointData().GetScalars().GetTuple(point_id)
            self.arrow_picked.emit(vector_magnitude[0])

    def start(self):
        self.interactor.Initialize()
        self.interactor.Start()
