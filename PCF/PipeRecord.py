# coding: utf-8
__author__ = "humkyung <humkyung@atools.co.kr>"

# Imports
import sys
import pandas
import vtk


class PipeRecord:
    TOKENS = ['COMPONENT-IDENTIFIER', 'END-POINT', 'FABRICATION-ITEM', 'INSULATION-SPEC', 'INSULATION',
              'PAINTING-SPEC', 'TRACING-SPEC', 'PIPING-SPEC', 'WEIGHT', 'UCI', 'MATERIAL-LIST', 'ITEM-CODE',
              'ITEM-DESCRIPTION', 'CONTINUATION']

    def __init__(self):
        self._points = []

    def parse(self, lines: list) -> bool:
        """parse given line"""

        for idx, line in enumerate(lines):
            if idx == 0:
                continue

            tokens = line.split()
            if tokens and tokens[0] in PipeRecord.TOKENS:
                if tokens[0] == 'END-POINT':
                    self._points.append((float(tokens[1]), float(tokens[2]), float(tokens[3]), float(tokens[4])))

    @property
    def start(self) -> list:
        return self._points[0][:3]

    @property
    def end(self) -> list:
        return self._points[1][:3]

    @property
    def bore1(self) -> float:
        return self._points[0][3]

    @property
    def bore2(self) -> float:
        return self._points[1][3]