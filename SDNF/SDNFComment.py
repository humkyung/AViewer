# coding: utf-8
""" This is SDNFComment module """

from SDNFElement import SDNFElement


class SDNFComment(SDNFElement):
    """This is SDNFComment class"""

    def __init__(self, comment):
        self._comment = comment

    @property
    def comment(self):
        """return comment string"""
        return self._comment
