# coding: utf-8

__author__ = "humkyung <humkyung.atools.co.kr>"


class Point:
    """This is a point class"""

    def __init__(self, x: float = 1, y: float = 0, z: float = 0):
        """Initialize the point with (1, 0, 0)"""
        self._x, self._y, self._z = x, y, z

    @property
    def pt(self):
        return self._x, self._y, self._z