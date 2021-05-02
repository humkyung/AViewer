# coding: utf-8
""" This is Data Transfer dialog module """

import os
import sys

from qt import *

from AppDocData import AppDocData, MessageType

from UI.OpenAutoForm_UI import Ui_OpenAutoFormDialog

__author__ = "humkyung <humkyung@atools.co.kr>"


class QOpenAutoFormDialog(QDialog):
    """ This is save output dialog class """

    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.ui = Ui_OpenAutoFormDialog()
        self.ui.setupUi(self)
        self.ui.toolButtonNodefile.clicked.connect(self.open_nodes)
        self.ui.toolButtonElementfile.clicked.connect(self.open_elements)

    @property
    def node_file_path(self):
        return self.ui.lineEditNodes.text()

    @property
    def element_file_path(self):
        return self.ui.lineEditElements.text()

    def open_nodes(self):
        """ load nodes from csv file """

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog.getOpenFileName(self, "Open nodes file", os.getcwd(), "csv files(*.csv)",
                                               options=options)
        if file_name[0]:
            self.ui.lineEditNodes.setText(file_name[0])

    def open_elements(self):
        """ load elements from csv file """

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog.getOpenFileName(self, "Open elements file", os.getcwd(), "csv files(*.csv)",
                                                options=options)
        if file_name[0]:
            self.ui.lineEditElements.setText(file_name[0])

    def accept(self):
        if self.ui.lineEditNodes.text() and self.ui.lineEditElements.text():
            QDialog.accept(self)
        else:
            QMessageBox.information(self, self.tr("Information"), self.tr('Please select node and element file'))

    def reject(self):
        QDialog.reject(self)
