# coding: utf-8
"""This is SDNFBeam module"""

from SDNFLinearMember import SDNFLinearMember


class SDNFBeam(SDNFLinearMember):
    """This is SDNFBeam class"""

    def __init__(self):
        SDNFLinearMember.__init__(self)
        self._member_type = SDNFLinearMember.ElmType.BEAM
