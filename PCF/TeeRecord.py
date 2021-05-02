# coding: utf-8
__author__ = "humkyung <humkyung@atools.co.kr>"

# Imports
import sys
import pandas
import vtk


class TeeRecord:
    TOKENS = ['COMPONENT-IDENTIFIER', 'END-POINT', 'CENTRE-POINT', 'BRANCH1-POINT', 'SKEY', 'ITEM-CODE',
              'ITEM-DESCRIPTION', 'UCI', 'INSULATION-SPEC', 'INSULATION', 'PAINTING-SPEC', 'TRACING-SPEC', 'PIPING-SPEC',
              'FABRICATION-ITEM', 'WEIGHT']

    def __init__(self):
        self._points = []
        self._center = None
        self._branch_point = None

    def parse(self, lines: list) -> bool:
        """parse given line"""

        for idx, line in enumerate(lines):
            if idx == 0:
                continue

            tokens = line.split()
            if tokens and tokens[0] in TeeRecord.TOKENS:
                if tokens[0] == 'END-POINT':
                    self._points.append((float(tokens[1]), float(tokens[2]), float(tokens[3]), float(tokens[4])))
                elif tokens[0] == 'CENTRE-POINT':
                    self._center = (float(tokens[1]), float(tokens[2]), float(tokens[3]))
                elif tokens[0] == 'BRANCH1-POINT':
                    self._branch_point = (float(tokens[1]), float(tokens[2]), float(tokens[3]), float(tokens[4]))

    @property
    def start(self) -> list:
        return self._points[0][:3]

    @property
    def end(self) -> list:
        return self._points[1][:3]

    @property
    def center(self) -> list:
        return self._center

    @property
    def bore1(self) -> float:
        return self._points[0][3]

    @property
    def bore2(self) -> float:
        return self._points[1][3]

    @property
    def branch_point(self):
        return self._branch_point[:3]

    @property
    def branch_bore(self):
        return self._branch_point[3]