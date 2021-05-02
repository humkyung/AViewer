# coding: utf-8
""" This is SDNFElementFactory module """

from SingletonInstance import SingletonInstane
from SDNFTitlePacket import SDNFTitlePacket


class SDNFElementFactory(SingletonInstane):
    """This is SDNFElementFactory class"""

    LINEAR_MEMBER_PACKET = 'Packet 10'
    COLUMN_TYPE_STR = '"COLUMN"'
    BEAM_TYPE_STR = '"BEAM"'
    HBRACE_TYPE_STR = '"HBRACE"'
    VBRACE_TYPE_STR	= '"VBRACE"'

    def __init__(self):
        pass

    def create_of(self, type_str):
        """create a element corresponding to type_str"""
        from SDNFLinearMemberPacket import SDNFLinearMemberPacket
        from SDNFColumn import SDNFColumn
        from SDNFBeam import SDNFBeam
        from SDNFHBrace import SDNFHBrace
        from SDNFVBrace import SDNFVBrace

        res = None
        if type_str == SDNFTitlePacket.TITLE_PACKET:
            res = SDNFTitlePacket()
        elif type_str == SDNFElementFactory.LINEAR_MEMBER_PACKET:
            res = SDNFLinearMemberPacket()
        elif type_str.upper() == SDNFElementFactory.COLUMN_TYPE_STR:
            res = SDNFColumn()
        elif type_str.upper() == SDNFElementFactory.BEAM_TYPE_STR:
            res = SDNFBeam()
        elif type_str.upper() == SDNFElementFactory.HBRACE_TYPE_STR:
            res = SDNFHBrace()
        elif type_str.upper() == SDNFElementFactory.VBRACE_TYPE_STR:
            res = SDNFVBrace()

        return res
