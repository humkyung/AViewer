# coding: utf-8
""" This is Data Transfer dialog module """

import os
import sys

from qt import *

from AppDocData import AppDocData, MessageType

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '\\UI')
import SaveOutput_UI

__author__ = "humkyung <zbaekhk@gmail.com>"

class Thread(QThread):
    """
    단순히 0부터 100까지 카운트만 하는 쓰레드
    값이 변경되면 그 값을 change_value 시그널에 값을 emit 한다.
    """
    # 사용자 정의 시그널 선언
    change_value = Signal(int)

    def __init__(self):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.cnt = 0
        self._status = True

        self.normal_contact_file_header = []
        self.normal_contact_file = None

        self.tangent_contact_file_header = []
        self.tangent_contact_file = None

    def __del__(self):
        self.wait()

    def run(self):
        from AppDocData import AppDocData

        self.mutex.lock()

        app_doc_data = AppDocData.instance()
        count = 0
        with open(self.normal_contact_file, 'w') as f:
            f.writelines(self.normal_contact_file_header)
            for node, normal in sorted(app_doc_data.normals.items()):
                f.write(format(f"{node}", ">8s") + f" {normal[0]} {normal[1]}  {normal[2]}\n")

                count += 1
                self.change_value.emit(count)

            f.write(format("0", ">8s") + "\n")

        with open(self.tangent_contact_file, 'w') as f:
            f.writelines(self.tangent_contact_file_header)
            for node, tangent in sorted(app_doc_data.tangents.items()):
                f.write(format(f"{node}", ">8s") + f" {tangent[0]} {tangent[1]}  {tangent[2]}\n")

                count += 1
                self.change_value.emit(count)

            f.write(format("0", ">8s") + "\n")

        self.mutex.unlock()

    def toggle_status(self):
        self._status = not self._status
        if self._status:
            self.cond.wakeAll()

    @property
    def status(self):
        return self._status


class QSaveOutputDialog(QDialog):
    """ This is save output dialog class """

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.th = Thread()

        self.ui = SaveOutput_UI.Ui_SaveOutputDialog()
        self.ui.setupUi(self)
        self.ui.pushButtonNormalFilePath.clicked.connect(self.select_normal_file)
        self.ui.pushButtonTangentFilePath.clicked.connect(self.select_tangent_file)
        self.load_data()
        self.th.change_value.connect(self.ui.progressBar.setValue)
        self.th.finished.connect(self.exit)

    def load_data(self):
        app_doc_data = AppDocData.instance()

        self.ui.labelNumOfNormal.setText(str(len(app_doc_data.normals)))
        self.ui.labelNumOfTangent.setText(str(len(app_doc_data.tangents)))

    def select_normal_file(self):
        """select a file to save normal contact pressure"""

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        name, _ = QFileDialog.getSaveFileName(self, "Save normal contact file", os.getcwd(), "asc files(*.asc)",
                                                options=options)
        if name:
            self.ui.lineEditNormalFilePath.setText(name + '.asc' if os.path.splitext(name)[1].upper() != '.ASC'
                                                   else name)

    def select_tangent_file(self):
        """select a file to save tangent contact pressure"""

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        name, _ = QFileDialog.getSaveFileName(self, "Save tangent contact file", os.getcwd(), "asc files(*.asc)",
                                              options=options)
        if name:
            self.ui.lineEditTangentFilePath.setText(name + '.asc' if os.path.splitext(name)[1].upper() != '.ASC'
                                                    else name)

    def exit(self):
        """exit dialog"""

        self.ui.progressBar.setMaximum(self.ui.progressBar.maximum())
        self.ui.buttonBox.setEnabled(True)

    def accept(self):
        """save normal/tangent contact pressure values to file"""
        from AppDocData import AppDocData

        try:
            app_doc_data = AppDocData.instance()

            self.ui.buttonBox.setEnabled(False)
            self.ui.progressBar.setMaximum(len(app_doc_data.normals) + len(app_doc_data.tangents))

            self.th.normal_contact_file = self.ui.lineEditNormalFilePath.text()
            self.th.tangent_contact_file = self.ui.lineEditTangentFilePath.text()

            self.th.normal_contact_file_header = [
                f"    {len(app_doc_data.normals)}{self.ui.lineEditNormalContact.text()}\n",
                f"{self.ui.lineEditName.text()}\n",
                f"Contour       {self.ui.lineEditContour.text()}\n",
                f" Unit         {self.ui.lineEditUnit.text()}\n",
                f" Dimension    {self.ui.spinBoxDimension.value()}\n",
                f" Type         {self.ui.lineEditType.text()}\n",
                f" Entity       {self.ui.lineEditEntity.text()}\n",
                f"State         {self.ui.lineEditState.text()}\n",
                f" Number       {self.ui.lineEditNumber.text()}\n"
            ]

            self.th.tangent_contact_file_header = [
                f"    {len(app_doc_data.tangents)}{self.ui.lineEditTangentContact.text()}\n",
                f"{self.ui.lineEditTangentName.text()}\n",
                f"Contour       {self.ui.lineEditTangentContour.text()}\n",
                f" Unit         {self.ui.lineEditTangentUnit.text()}\n",
                f" Dimension    {self.ui.spinBoxTangentDimension.value()}\n",
                f" Type         {self.ui.lineEditTangentType.text()}\n",
                f" Entity       {self.ui.lineEditTangentEntity.text()}\n",
                f"State         {self.ui.lineEditTangentState.text()}\n",
                f" Number       {self.ui.lineEditTangentNumber.text()}\n"
            ]

            self.th.start()
        except Exception as ex:
            from App import App
            message = 'error occurred({}) in {}:{}'.format(repr(ex), sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            App.mainWnd().addMessage.emit(MessageType.Error, message)
