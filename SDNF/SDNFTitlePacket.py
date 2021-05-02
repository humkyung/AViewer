# coding: utf-8
""" This is SDNFTitlePacket module """

from SDNFPacket import SDNFPacket


class SDNFTitlePacket(SDNFPacket):
    """This is SDNFTitlePacket class"""

    TITLE_PACKET = 'Packet 00'

    def __init__(self):
        self._ver_string = None
        self.engineering_firm_id = None
        self.client_id = None
        self.structure_id = None
        self.project_id = None

    def parse_version(self, file):
        """parse version"""
        from SDNFFile import SDNFFile

        pos, count = file.tell(), 0

        while True:
            line = file.readline().strip()
            count += 1
            if '"' != line[0]:
                break

        file.seek(pos)

        if count == 6:
            self._ver_string = '"SDNF Version 2.0"'
            SDNFFile.VER = SDNFFile.Ver.VER_2
        else:
            line = file.readline().strip()
            self._ver_string = line
            SDNFFile.VER = SDNFFile.Ver.VER_3

    def parse(self, file, start):
        """parse data for title packet"""

        self.parse_version(file)

        line = file.readline().strip()
        self.engineering_firm_id = line[:80]
        line = file.readline().strip()
        self.client_id = line[:80]
        line = file.readline().strip()
        self.structure_id = line[:80]
        line = file.readline().strip()
        self.project_id = line[:80]
