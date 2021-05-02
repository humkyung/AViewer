# coding: utf-8
"""This is SDNFVBrace module"""

from SDNFLinearMember import SDNFLinearMember


class SDNFVBrace(SDNFLinearMember):
    """This is SDNFVBrace class"""

    def __init__(self):
        SDNFLinearMember.__init__(self)
        self._member_type = SDNFLinearMember.ElmType.VBRACE