# coding: utf-8
"""This is SDNFColumn module"""

from SDNFLinearMember import SDNFLinearMember


class SDNFColumn(SDNFLinearMember):
    """This is SDNFColumn class"""

    def __init__(self):
        SDNFLinearMember.__init__(self)
        self._member_type = SDNFLinearMember.ElmType.COLUMN