# coding: utf-8

# Imports
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
Qt = QtCore.Qt


# Basic library things
def version():
    """Returns the S3DExport version number"""
    ver = '0.0.1'
    return ver

def documentation():
    """Returns the S3DExport help documentation"""
    doclist = ''

    doclist += f"S3Dxport {version()}"
    doclist += 'Help Documentation'
    doclist += '------------------'
    doclist += 'Docs will go here eventually.'
    doclist += ''
    doclist += ''
    doclist += ''
    doclist += ''

    docs = '\n'.join(doclist)
    return docs
