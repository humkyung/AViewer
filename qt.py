import sys

"""
if 'PyQt5' in sys.modules:
"""
# PyQt6
"""
if True:
    from PyQt6.QtGui import *
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import Qt
    from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
    from PyQt6.QtSvg import *
    from PyQt6.QtXml import *
"""
# PyQt5
if True:
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
    from PyQt5.QtSvg import *
    from PyQt5.QtXml import *
"""
else:
    # PySide2
    from PySide2 import QtGui, QtWidgets, QtCore
    from PySide2.QtCore import Signal, Slot
    import pkg_resources.py2_warn
"""