# coding: utf-8
""" This is exception handler module """

import sys
import os

from qt import *

import logging
from datetime import datetime
from App import App


class QExceptionHandler(QObject):
    """ This is exception handler class """

    errorSignal = Signal()

    def __init__(self):
        super(QExceptionHandler, self).__init__()

        log_folder = os.path.join(os.getenv('ALLUSERSPROFILE'), f"{App.NAME}")
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)

        self.log_path = os.path.join(log_folder, f"{App.NAME}.log")
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename=self.log_path, filemode='a', level=logging.CRITICAL)
        self.logger.critical(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def handler(self, exctype, value, traceback):
        """ log exception, file name and line number """
        from App import App
        from AppDocData import MessageType

        message = 'error occurred({}) in {}:{}'.format(value, traceback.tb_frame.f_code.co_filename, traceback.tb_lineno)
        message = 'Unhandled exception: {}'.format(message)
        self.errorSignal.emit()
        self.logger.critical(message)
        message = 'CRITICAL : Unhandled exception: {}'.format(message)

        try:
            App.mainWnd().addMessage.emit(MessageType.Error, message)  
        except Exception as ex:
            pass