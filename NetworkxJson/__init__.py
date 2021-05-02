# coding: utf-8

# Imports
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
Qt = QtCore.Qt


# Basic library things
def version():
    """Returns the Json version number"""
    ver = '0.0.1'
    return ver

def documentation():
    """Returns the Json help documentation"""
    doclist = ''

    doclist += f"Json {version()}"
    doclist += 'Help Documentation'
    doclist += '------------------'
    doclist += 'Docs will go here eventually.'
    doclist += ''
    doclist += ''
    doclist += ''
    doclist += ''

    docs = '\n'.join(doclist)
    return docs
