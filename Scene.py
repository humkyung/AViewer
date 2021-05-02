# coding: utf-8
""" This is Scene module """

from warnings import warn
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import numpy as np


class Scene(vtk.vtkRenderer):
    """Your scene class.

    This is an important object that is responsible for preparing objects
    e.g. actors and volumes for rendering. This is a more pythonic version
    of ``vtkRenderer`` proving simple methods for adding and removing actors
    but also it provides access to all the functionality
    available in ``vtkRenderer`` if necessary.
    """

    def __init__(self):
        from ViewActions import ViewActions

        self.view = ViewActions(self)
        self.projection()

    def background(self, color):
        """Set a background color."""
        self.SetBackground(color)

    def add(self, *actors):
        """Add an actor to the scene."""
        for actor in actors:
            if isinstance(actor, vtk.vtkVolume):
                self.AddVolume(actor)
            elif isinstance(actor, vtk.vtkActor2D):
                self.AddActor2D(actor)
            elif hasattr(actor, 'add_to_scene'):
                actor.add_to_scene(self)
            else:
                self.AddActor(actor)

    def rm(self, actor):
        """Remove a specific actor."""
        self.RemoveActor(actor)

    def clear(self):
        """Remove all actors from the scene."""
        self.RemoveAllViewProps()

    def rm_all(self):
        """Remove all actors from the scene."""
        self.RemoveAllViewProps()

    def projection(self, proj_type='parallel'):
        """Deside between parallel or perspective projection.

        Parameters
        ----------
        proj_type : str
            Can be 'parallel' or 'perspective' (default).

        """
        if proj_type == 'parallel':
            self.GetActiveCamera().ParallelProjectionOn()
        else:
            self.GetActiveCamera().ParallelProjectionOff()

    def reset_camera(self):
        """Reset the camera to an automatic position given by the engine."""
        self.ResetCamera()

    def reset_camera_tight(self, margin_factor=1.02):
        """ Resets camera so the content fit tightly within the window.

        Parameters
        ----------
        margin_factor : float (optional)
            Margin added around the content. Default: 1.02.

        """
        self.ComputeAspect()
        cam = self.GetActiveCamera()
        aspect = self.GetAspect()

        X1, X2, Y1, Y2, Z1, Z2 = self.ComputeVisiblePropBounds()
        width, height = X2 - X1, Y2 - Y1
        center = np.array((X1 + width / 2., Y1 + height / 2., 0))

        angle = np.pi * cam.GetViewAngle() / 180.
        dist = max(width / aspect[0], height) / np.sin(angle / 2.) / 2.
        position = center + np.array((0, 0, dist * margin_factor))

        cam.SetViewUp(0, 1, 0)
        cam.SetPosition(*position)
        cam.SetFocalPoint(*center)
        self.ResetCameraClippingRange(X1, X2, Y1, Y2, Z1, Z2)

        parallelScale = max(width / aspect[0], height) / 2.
        cam.SetParallelScale(parallelScale * margin_factor)

    def reset_clipping_range(self):
        """Reset the camera to an automatic position given by the engine."""
        self.ResetCameraClippingRange()

    def camera(self):
        """Return the camera object."""
        return self.GetActiveCamera()

    def get_camera(self):
        """Return Camera information: Position, Focal Point, View Up."""
        cam = self.GetActiveCamera()
        return cam.GetPosition(), cam.GetFocalPoint(), cam.GetViewUp()

    def camera_info(self):
        """Return Camera information."""
        cam = self.camera()
        print('# Active Camera')
        print('   Position (%.2f, %.2f, %.2f)' % cam.GetPosition())
        print('   Focal Point (%.2f, %.2f, %.2f)' % cam.GetFocalPoint())
        print('   View Up (%.2f, %.2f, %.2f)' % cam.GetViewUp())

    def set_camera(self, position=None, focal_point=None, view_up=None):
        """Set up camera position / Focal Point / View Up."""
        if position is not None:
            self.GetActiveCamera().SetPosition(*position)
        if focal_point is not None:
            self.GetActiveCamera().SetFocalPoint(*focal_point)
        if view_up is not None:
            self.GetActiveCamera().SetViewUp(*view_up)
        self.ResetCameraClippingRange()

    def size(self):
        """Scene size."""
        return self.GetSize()

    def zoom(self, value):
        """Rescale scene's camera.

        In perspective mode, decrease the view angle by the specified
        factor. In parallel mode, decrease the parallel scale by the specified
        factor. A value greater than 1 is a zoom-in, a value less than 1 is a
        zoom-out.

        """
        self.GetActiveCamera().Zoom(value)

    def azimuth(self, angle):
        """Rotate scene's camera.

        Rotate the camera about the view up vector centered at the focal
        point. Note that the view up vector is whatever was set via SetViewUp,
        and is not necessarily perpendicular to the direction of projection.
        The result is a horizontal rotation of the camera.

        """
        self.GetActiveCamera().Azimuth(angle)

    def yaw(self, angle):
        """Yaw scene's camera.

        Rotate the focal point about the view up vector, using the camera's
        position as the center of rotation. Note that the view up vector is
        whatever was set via SetViewUp, and is not necessarily perpendicular
        to the direction of projection. The result is a horizontal rotation of
        the scene.

        """
        self.GetActiveCamera().Yaw(angle)

    def elevation(self, angle):
        """Elevate scene's camera.

        Rotate the camera about the cross product of the negative of the
        direction of projection and the view up vector, using the focal point
        as the center of rotation. The result is a vertical rotation of the
        scene.
        """
        self.GetActiveCamera().Elevation(angle)

    def pitch(self, angle):
        """Pitch scene's camera.

        Rotate the focal point about the cross product of the view up
        vector and the direction of projection, using the camera's position as
        the center of rotation. The result is a vertical rotation of the
        camera.
        """
        self.GetActiveCamera().Pitch(angle)

    def roll(self, angle):
        """Roll scene's camera.

        Rotate the camera about the direction of projection. This will
        spin the camera about its axis.
        """
        self.GetActiveCamera().Roll(angle)

    def dolly(self, value):
        """Dolly In/Out scene's camera.

        Divide the camera's distance from the focal point by the given
        dolly value. Use a value greater than one to dolly-in toward the focal
        point, and use a value less than one to dolly-out away from the focal
        point.
        """
        self.GetActiveCamera().Dolly(value)

    def camera_direction(self):
        """Get camera direction.

        Get the vector in the direction from the camera position to the
        focal point. This is usually the opposite of the ViewPlaneNormal, the
        vector perpendicular to the screen, unless the view is oblique.
        """
        return self.GetActiveCamera().GetDirectionOfProjection()

    @property
    def frame_rate(self):
        rtis = self.GetLastRenderTimeInSeconds()
        fps = 1.0 / rtis
        return fps

    def fxaa_on(self):
        self.SetUseFXAA(True)

    def fxaa_off(self):
        self.SetUseFXAA(False)


class Renderer(Scene):
    """Your scene class.

    This is an important object that is responsible for preparing objects
    e.g. actors and volumes for rendering. This is a more pythonic version
    of ``vtkRenderer`` proving simple methods for adding and removing actors
    but also it provides access to all the functionality
    available in ``vtkRenderer`` if necessary.

    .. deprecated:: 0.2.0
          `Renderer()` will be removed in Fury 0.3.0, it is replaced by the
          class `Scene()`
    """

    def __init__(self, _parent=None):
        """Init old class with a warning."""
        warn("Class 'fury.window.Renderer' is deprecated, instead"
             " use class 'fury.window.Scene'.", PendingDeprecationWarning)

    @staticmethod
    def renderer(background=None):
        """Create a Scene.

        .. deprecated:: 0.2.0
              `renderer` will be removed in Fury 0.3.0, it is replaced by the
              class `Scene()`

        Parameters
        ----------
        background : tuple
            Initial background color of scene

        Returns
        -------
        v : Scene instance
            scene object

        Examples
        --------
        >>> from fury import window, actor
                >>> import numpy as np
        >>> r = window.renderer()
        >>> lines=[np.random.rand(10,3)]
        >>> c=actor.line(lines, window.colors.red)
        >>> r.add(c)
        >>> #window.show(r)

        """
        deprecation_msg = ("Method 'fury.window.renderer' is deprecated, instead"
                           " use class 'fury.window.Scene'.")
        warn(PendingDeprecationWarning(deprecation_msg))

        scene = Scene()
        if background is not None:
            scene.SetBackground(background)

        return scene

    @staticmethod
    def ren(background=None):
        """Create a Scene.

        .. deprecated:: 0.2.0
              `ren` will be removed in Fury 0.3.0, it is replaced by
              `Scene()`
        """
        return renderer(background=background)

    @staticmethod
    def add(scene, a):
        """Add a specific actor to the scene.

        .. deprecated:: 0.2.0
              `ren` will be removed in Fury 0.3.0, it is replaced by
              `Scene().add`
        """
        warn("Class 'fury.window.add' is deprecated, instead"
             " use class 'fury.window.Scene.add'.", PendingDeprecationWarning)
        scene.add(a)

    @staticmethod
    def rm(scene, a):
        """Remove a specific actor from the scene.

        .. deprecated:: 0.2.0
              `ren` will be removed in Fury 0.3.0, it is replaced by
              `Scene().rm`
        """
        warn("Class 'fury.window.rm' is deprecated, instead"
             " use class 'fury.window.Scene.rm'.", PendingDeprecationWarning)
        scene.rm(a)

    @staticmethod
    def clear(scene):
        """Remove all actors from the scene.

        .. deprecated:: 0.2.0
              `ren` will be removed in Fury 0.3.0, it is replaced by
              `Scene().clear`
        """
        warn("Class 'fury.window.clear' is deprecated, instead"
             " use class 'fury.window.Scene.clear'.", PendingDeprecationWarning)
        scene.clear()

    @staticmethod
    def rm_all(scene):
        """Remove all actors from the scene.

        .. deprecated:: 0.2.0
              `ren` will be removed in Fury 0.3.0, it is replaced by
              `Scene().rm_all`
        """
        warn("Class 'fury.window.rm_all' is deprecated, instead"
             " use class 'fury.window.Scene.rm_all'.", PendingDeprecationWarning)
        scene.rm_all()
