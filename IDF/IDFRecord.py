# coding: utf-8
__author__ = "humkyung <humkyung@atools.co.kr>"

# Imports
import sys
import pandas
import vtk


class IDFRecord:
    FILE_POS = [7, 20, 33]

    def __init__(self):
        self._record_index = 0
        self._start = [0, 0, 0]

    def parse(self, line: str) -> bool:
        """parse given line"""
        if line and len(line) > 33:
            token = line[0: 4]
            self._record_index = int(token.strip())

            self._start[0] = float(line[IDFRecord.FILE_POS[0]: IDFRecord.FILE_POS[0] + 11].strip())
            self._start[1] = float(line[IDFRecord.FILE_POS[1]: IDFRecord.FILE_POS[1] + 11].strip())
            self._start[2] = float(line[IDFRecord.FILE_POS[2]: IDFRecord.FILE_POS[2] + 11].strip())

            return True

        return False

    @property
    def record_index(self) -> int:
        """return record index"""
        return self._record_index

    @property
    def start(self) -> list:
        return self._start
