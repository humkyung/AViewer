# coding: utf-8
"""This is SDNFHBrace module"""

from SDNFLinearMember import SDNFLinearMember


class SDNFHBrace(SDNFLinearMember):
    """This is SDNFHBrace class"""

    def __init__(self):
        SDNFLinearMember.__init__(self)
        self._member_type = SDNFLinearMember.ElmType.HBRACE