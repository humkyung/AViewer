# coding: utf-8
""" This is application module """
import sys
import os

if hasattr(sys, 'frozen'):
  os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from qt import *

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from AppDocData import AppDocData


class App(QApplication):
    NAME = 'AViewer'

    """ This is App class inherits from QApplication """
    def __init__(self, args):
        import locale

        super(App, self).__init__(args)
        app_doc_data = AppDocData.instance()
        app_style = app_doc_data.loadAppStyle()
        self.setStyle(app_style)

        configs = app_doc_data.getAppConfigs('app', 'stylesheets')
        if configs and len(configs) == 1:
            self.load_style_sheet(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stylesheets',
                                             f"{configs[0].value}"))
            self.stylesheet_name = configs[0].value
        else:
            self.load_style_sheet(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stylesheets', 'coffee'))
            self.stylesheet_name = 'coffee'

        # load language file
        self._translator = None
        configs = app_doc_data.getAppConfigs('app', 'language')
        if configs and len(configs) == 1:
            qm_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'translates', f"{configs[0].value}.qm")
        else:
            locale = locale.getdefaultlocale()
            qm_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'translates', f"{locale[0]}.qm")

        self.load_language(qm_file)
        # up to here

        self._mainWnd = None

        self.qApp = self

    def load_style_sheet(self, sheetName: str):
        """load application style sheet"""
        try:
            file = QFile('%s.qss' % sheetName.lower())
            file.open(QFile.ReadOnly)

            styleSheet = file.readAll()
            styleSheet = str(styleSheet, encoding='utf8')

            self.setStyleSheet(styleSheet)
        finally:
            file.close()

    def load_language(self, language_file: str):
        """ load translator with given language file """
        try:
            if self._translator is not None:
                self.removeTranslator(self._translator)

            self.language_name = 'en_us'
            if os.path.isfile(language_file):
                self._translator = QTranslator()  # I18N 관련
                self._translator.load(language_file)
                self.installTranslator(self._translator)
                self.language_name = os.path.splitext(os.path.basename(language_file))[0]
        finally:
            pass

    @staticmethod
    def mainWnd():
        """return the main window"""
        app = QApplication.instance()
        for widget in app.topLevelWidgets():
            if isinstance(widget, QMainWindow):
                return widget

        return None


if __name__ == '__main__':
    from MainWindow import MainWindow
    from ExceptionHandler import QExceptionHandler

    app = App(sys.argv)
    app.setStyle('fusion')

    """ log for unhandled exception """
    exceptionHandler = QExceptionHandler()
    sys._excepthook = sys.excepthook
    sys.excepthook = exceptionHandler.handler

    AppDocData.instance().ex = exceptionHandler
    app._mainWnd = MainWindow.instance()
    app._mainWnd.show()
    sys.exit(app.exec_())