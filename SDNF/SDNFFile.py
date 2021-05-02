# coding: utf-8
""" This is SDNFFile module """

import sys
import os
from SDNFComment import SDNFComment
from SDNFElementFactory import SDNFElementFactory

import enum


class SDNFFile:
    """This is SNDFFile class"""

    class Ver(enum.Enum):
        VER_2 = 1
        VER_3 = 2

    VER = Ver.VER_2

    def __init__(self):
        self._elements = []

    @property
    def elements(self):
        """return all elements of file"""
        return self._elements

    def is_comment(self, line):
        """check if given line is comment"""
        return line and '#' == line[0]

    def read(self, file_path):
        """read given sdnf file"""

        if os.path.isfile(file_path):
            factory = SDNFElementFactory.instance()

            with open(file_path, 'r') as file:
                while True:
                    line = file.readline().strip()
                    if not line:
                        break

                    if self.is_comment(line):
                        self._elements.append(SDNFComment(line))
                    else:
                        element = factory.create_of(line)
                        if element:
                            element.parse(file, line)
                            self._elements.append(element)


if __name__ == '__main__':
    sdnf = SDNFFile()
    sdnf.read('d:\\Projects\\DKTPlates\\Docs\\20s_pr11b.dat')
    print(f"length = {len(sdnf._elements)}")
