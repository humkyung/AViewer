# coding: utf-8
""" This is SDNFElement module """

import enum


class SDNFElement:
    """This is SDNFElement class"""

    class UNIT(enum.Enum):
        NONE = 0x00
        MILLIMETER = 0x01
        CENTIMETER = 0x02
        METER = 0x02

    class Axis(enum.Enum):
        NORMAL_AXIS = 0
        ROT_ABOUT_X_AXIS = 1

    def __init__(self):
        self._unit = SDNFElement.UNIT.NONE
        self._axis = SDNFElement.Axis.NORMAL_AXIS
        self.web_frange_start = -1
        self.web_frange_end = -1

    @property
    def axis(self):
        """return axis"""
        return self._axis

    @property
    def unit(self):
        """return unit"""
        return self._unit

    @unit.setter
    def unit(self, value):
        """set unit with given value"""
        self._unit = value

    def parse(self, file, start):
        """parse element section"""

        # 1'st line
        line = file.readline()

        # 2'nd line
        line = file.readline()

        line = file.readline()
        line = file.readline()
        line = file.readline()
        line = file.readline()
        line = file.readline()
        line = file.readline()

        line = file.readline()
        tokens = line.split()
        self.web_frange_start = int(tokens[1])
        self.web_frange_end = int(tokens[2])
