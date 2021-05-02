# coding: utf-8
__author__ = "humkyung <humkyung@atools.co.kr>"

# Imports
import os
from enum import IntEnum
from .SDNFFile import SDNFFile


class SDNFImporter:
    def __init__(self):
        self._file_path = None

    def SetFileName(self, file_path: str) -> None:
        self._file_path = file_path

    def Read(self) -> None:
        """read given file"""
        pass

    def GetOutput(self, renderer):
        """add actors to renderer"""

        if os.path.isfile(self._file_path):
            file = SDNFFile()
            file.read(self._file_path)
            for element in file.elements:
                pass


if __name__ == '__main__':
    importer = SDNFImporter()
    importer.Read('79qcd01br01401.idf')
