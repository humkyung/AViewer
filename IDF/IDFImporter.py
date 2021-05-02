# coding: utf-8
__author__ = "humkyung <humkyung@atools.co.kr>"

# Imports
import os
from enum import IntEnum
from .IDFRecord import IDFRecord
from .IDFPipeRecord import IDFPipeRecord


class IDFImporter:
    class Marker(IntEnum):
        PIPE = 100
        OFFSET_METRIC = 300
        OFFSET_IMPERIAL = 301
        END_OF_FILE = 999

    def __init__(self):
        self._file_path = None
        self._offset = [0, 0, 0]
        self._records = []

    @property
    def records(self) -> list:
        return self._records

    @property
    def offset(self) -> list:
        return self._offset

    def SetFileName(self, file_path: str) -> None:
        self._file_path = file_path

    def Read(self) -> None:
        """read given file"""

        if os.path.isfile(self._file_path):
            self._records.clear()

            for filelineno, line in enumerate(open(self._file_path, encoding="utf-8")):
                if not line:
                    break

                token = line[0: 4].strip()
                item_code = int(token) if token else 0

                if item_code == IDFImporter.Marker.END_OF_FILE:
                    break
                elif item_code == IDFImporter.Marker.OFFSET_METRIC:
                    record = IDFRecord()
                    record.parse(line)
                    self._offset = [record.start[0]*100000, record.start[1]*1000000, record.start[2]*100000]
                elif item_code == IDFImporter.Marker.PIPE:
                    record = IDFPipeRecord()
                    record.parse(line)
                    self._records.append(record)
                elif item_code in [35, 36]:  # elbow
                    record = IDFRecord()
                    record.parse(line)
                    self._records.append(record)
                elif item_code in [45, 46, 47]:  # TERF
                    record = IDFRecord()
                    record.parse(line)
                    self._records.append(record)
                elif item_code in [105]:  # FLWN
                    record = IDFRecord()
                    record.parse(line)
                    self._records.append(record)
                elif item_code in [107]:  # FLBL
                    record = IDFRecord()
                    record.parse(line)
                    self._records.append(record)

    def GetOutput(self, renderer):
        """add actors to renderer"""
        from Primitives.Cylinder import Cylinder

        for record in self._records:
            if record.record_index == IDFImporter.Marker.PIPE:
                cylinder = Cylinder(renderer, record.start, record.end, record.bore)
                renderer.AddActor(cylinder.vtkActor)


if __name__ == '__main__':
    importer = IDFImporter()
    importer.read('79qcd01br01401.idf')
