# coding: utf-8
__author__ = "humkyung <humkyung@atools.co.kr>"

# Imports
import os
from enum import IntEnum


class PCFImporter:
    TOKENS = ['ISOGEN-FILES', 'UNITS-BORE', 'UNITS-CO-ORDS', 'UNITS-BOLT-LENGTH', 'UNITS-BOLT-DIA', 'UNITS-WEIGHT',
              'PIPELINE-REFERENCE', 'PIPE', 'WELD', 'ELBOW', 'FLANGE', 'FLOW-ARROW', 'END-CONNECTION-PIPELINE',
              'MATERIALS', 'ITEM-CODE']

    def __init__(self):
        self._file_path = None
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

            lines = []
            for filelineno, line in enumerate(open(self._file_path, encoding="utf-8")):
                if not line:
                    break

                tokens = line.split()
                if tokens and not line[0].isspace():
                    if lines:
                        self.Parse(lines)

                    lines.clear()
                    lines.append(line)
                elif tokens:
                    lines.append(line)

            if lines:
                self.Parse(lines)

    def Parse(self, lines: list):
        """parse given lines"""
        from .PipeRecord import PipeRecord
        from .ElbowRecord import ElbowRecord
        from .TeeRecord import TeeRecord

        if lines:
            tokens = lines[0].split()
            if tokens[0].upper() == 'PIPE':
                record = PipeRecord()
                record.parse(lines)
                self._records.append(record)
            elif tokens[0].upper() == 'ELBOW':
                record = ElbowRecord()
                record.parse(lines)
                self._records.append(record)
            elif tokens[0].upper() == 'TEE':
                record = TeeRecord()
                record.parse(lines)
                self._records.append(record)

    def GetOutput(self, renderer):
        """add actors to renderer"""
        from .PipeRecord import PipeRecord
        from .ElbowRecord import ElbowRecord
        from .TeeRecord import TeeRecord
        from Primitives.Cylinder import Cylinder
        from Primitives.CTorus import CTorus

        count = 0
        for record in self._records:
            if type(record) is PipeRecord:
                cylinder = Cylinder(renderer, record.start, record.end, record.bore1*25.4*0.5)
                renderer.AddActor(cylinder.vtkActor)
            elif type(record) is ElbowRecord:
                ctorus = CTorus(renderer, record.start, record.end, record.center, record.angle, record.bore1*25.4*0.5)
                renderer.AddActor(ctorus.vtkActor)
            elif type(record) is TeeRecord:
                cylinder = Cylinder(renderer, record.start, record.end, record.bore1 * 25.4 * 0.5)
                cylinder = Cylinder(renderer, record.center, record.branch_point, record.branch_bore * 25.4 * 0.5)


if __name__ == '__main__':
    importer = PCFImporter()
    importer.SetFileName('d:\\Projects\\ATOOLS\\AViewer\\Docs\\02. LATEST PCF\\SC2851__100__P1001__MEG-100-PI-ISO-P1001-001__00.pcf')
    importer.Read()
