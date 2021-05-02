# -*- coding: utf-8 -*-
import sys, os
from functools import partial

from qt import *


class QHomePane(QWidget):
    def __init__(self):
        import os
        from PyQt5 import QtWidgets, uic

        QWidget.__init__(self)
        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UI', 'Home.ui')
        uiClass, qtBaseClass = uic.loadUiType(ui_path)
        self.ui = uiClass()
        self.ui.setupUi(self)


class QHomeViewPane(QWidget):
    def __init__(self):
        import os
        from PyQt5 import QtWidgets, uic

        QWidget.__init__(self)
        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UI', 'Home_View.ui')
        uiClass, qtBaseClass = uic.loadUiType(ui_path)
        self.ui = uiClass()
        self.ui.setupUi(self)


class QHelpPane(QWidget):
    def __init__(self):
        import os
        from PyQt5 import QtWidgets, uic

        QWidget.__init__(self)
        config_ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UI', 'Help.ui')
        uiClass, qtBaseClass = uic.loadUiType(config_ui_path)
        self.ui = uiClass()
        self.ui.setupUi(self)


class QConfigPane(QWidget):
    def __init__(self):
        import os
        from PyQt5 import QtWidgets, uic
        from App import App

        QWidget.__init__(self)
        config_ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UI', 'Config.ui')
        uiClass, qtBaseClass = uic.loadUiType(config_ui_path)
        self.ui = uiClass()
        self.ui.setupUi(self)

        # load stylesheet file list
        stylesheet_name = App.instance().stylesheet_name
        files = [os.path.splitext(file)[0] for file in
                 os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stylesheets'))
                 if os.path.splitext(file)[1] == '.qss']
        self.ui.comboBoxTheme.addItems(files)
        self.ui.comboBoxTheme.currentIndexChanged.connect(self.on_theme_changed)
        # up to here

        # load language files
        language_name = App.instance().language_name
        files = ['en_us']  # english is default language
        files.extend([os.path.splitext(file)[0] for file in
                      os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'translates')) if
                      os.path.splitext(file)[1] == '.qm'])
        self.ui.comboBoxLanguage.addItems(files)
        self.ui.comboBoxLanguage.currentIndexChanged.connect(self.on_language_changed)
        # up to here

    def on_theme_changed(self, index: int):
        from App import App

        if index != -1:
            theme = self.ui.comboBoxTheme.currentText()
            App.mainWnd().load_style_sheet(theme)

    def on_language_changed(self, index: int):
        from App import App

        if index != -1:
            language = self.ui.comboBoxLanguage.currentText()
            App.mainWnd().load_language(language)