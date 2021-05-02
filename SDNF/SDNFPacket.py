# coding: utf-8
""" This is SDNFPacket module """

from SDNFElement import SDNFElement


class SDNFPacket(SDNFElement):
    """This is SDNFPacket class"""

    def __init__(self):
        self._elements = []

    def parse(self, file, start):
        pass

    @property
    def element_count(self):
        """return element count"""
        return len(self._elements)

    def element_at(self, at):
        """return a element located at given position"""

        if at < len(self._elements):
            return self._elements[at]

        return None