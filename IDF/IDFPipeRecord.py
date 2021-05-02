# coding: utf-8
__author__ = "humkyung <humkyung@atools.co.kr>"

# Imports
import sys
import pandas
import vtk


class IDFPipeRecord:
    FILE_POS = [7, 20, 33]

    def __init__(self):
        self._record_index = 0
        self._start = [0, 0, 0]
        self._end = [0, 0, 0]
        self._bore = None

    def parse(self, line: str) -> bool:
        """parse given line"""
        if line and len(line) > 33:
            token = line[0: 4]
            self._record_index = int(token.strip())

            tokens = [token.strip() for token in line[4:].split()]
            if len(tokens) > 6:
                self._start = [float(tokens[0]), float(tokens[1]), float(tokens[2])]
                self._end = [float(tokens[3]), float(tokens[4]), float(tokens[5])]
                self._bore = float(tokens[6])

            return True

        return False

    @property
    def record_index(self) -> int:
        """return record index"""
        return self._record_index

    @property
    def start(self) -> list:
        return self._start

    @property
    def end(self) -> list:
        return self._end

    @property
    def bore(self) -> float:
        return self._bore
