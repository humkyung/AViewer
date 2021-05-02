# coding: utf-8
"""This is SDNFLinearMemberPacket module"""

from SDNFElement import SDNFElement
from SDNFPacket import SDNFPacket


class SDNFLinearMemberPacket(SDNFPacket):
    """This is SDNFLinearMemberPacket"""

    def __init__(self):
        self._num_of_members = None
        self._elements = []

    @property
    def num_of_members(self):
        """return number of members"""
        return self._num_of_members

    @property
    def elements(self):
        """return all elements in linear member packet"""
        return self._elements

    def parse(self, file, start):
        """parse linear member"""

        from SDNFElementFactory import SDNFElementFactory
        from SDNFLinearMember import SDNFLinearMember

        line = file.readline().strip()  # unit and num of members
        tokens = line.split()
        if len(tokens) == 2:
            unit = tokens[0]
            if -1 != unit.find('meters'):
                self.unit = SDNFElement.UNIT.METER
            else:
                self.unit = SDNFElement.UNIT.MILLIMETER

            self._num_of_members = int(tokens[1])

        factory = SDNFElementFactory.instance()
        for i in range(self._num_of_members):
            line = file.readline()
            if line == "":
                break
            line = line.strip()

            record1 = SDNFLinearMember.Record1()
            record1.parse(line)
            element = factory.create_of(record1.type)
            if element:
                element.unit = self.unit
                element.parse(file, line)
                self._elements.append(element)
