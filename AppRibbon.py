# -*- coding: utf-8 -*-
import sys
import os
from functools import partial

from qt import *
# PyQtRibbon: import, and error msg if not installed
try:
    from PyQtRibbon.FileMenu import QFileMenu, QFileMenuPanel
    from PyQtRibbon.RecentFilesManager import QRecentFilesManager
    from PyQtRibbon.Ribbon import QRibbon, QRibbonTab, QRibbonSection
except (ImportError, NameError):
    errormsg = 'You haven\'t installed PyQtRibbon, or your installation of it is broken. Please download or fix it.'
    raise Exception(errormsg)


class MyMenu(QMenu):
    def event(self, event):
        if event.type() == QEvent.Show:
            self.move(self.parent().mapToGlobal(QPoint(0, 0)) + QPoint(0, self.height()))
        return super(MyMenu, self).event(event)


class AppRibbon(QRibbon):
    """ Class that represents App ribbon """

    def __init__(self):
        """ Creates and initializes the App Ribbon """
        QRibbon.__init__(self)

        # Set up the file menu
        self.fileMenu = AppRibbonFileMenu()
        self.setFileMenu(self.fileMenu)

        # Add tabs
        self.btns = {}
        self.add_home_tab()
        self.add_help_tab()

    def add_home_tab(self):
        """ Adds the Home Tab """
        from App import App
        from RibbonPanes import QHomePane, QHomeViewPane

        try:
            tab = self.addTab(self.tr('Home'))
            main_wnd = App.mainWnd()

            # Home Section
            cSection = tab.addSection(self.tr('Home'))
            pane = QHomePane()
            pane.ui.toolButtonOpen.clicked.connect(App.mainWnd().open_file)
            m = MyMenu('Menu', pane.ui.toolButtonOpen)
            action1 = m.addAction('3D Model', main_wnd.open_file)
            action2 = m.addAction('AFexport', main_wnd.open_afexport)
            pane.ui.toolButtonOpen.setMenu(m)
            pane.ui.toolButtonSave.clicked.connect(App.mainWnd().save_output)
            pane.ui.toolButtonNetworkx.clicked.connect(App.mainWnd().on_click_networkx)
            cSection.addCustomWidget(pane)

            # Home View Section
            cSection = tab.addSection(self.tr('View'))
            pane = QHomeViewPane()
            pane.ui.horizontalSliderOpacity.valueChanged.connect(main_wnd.on_opacity_changed)
            pane.ui.toolButtonLeftView.clicked.connect(main_wnd.on_left_view)
            pane.ui.toolButtonRightView.clicked.connect(main_wnd.on_right_view)
            pane.ui.toolButtonFrontView.clicked.connect(main_wnd.on_front_view)
            pane.ui.toolButtonBackView.clicked.connect(main_wnd.on_back_view)
            pane.ui.toolButtonTopView.clicked.connect(main_wnd.on_top_view)
            pane.ui.toolButtonBottomView.clicked.connect(main_wnd.on_bottom_view)
            pane.ui.toolButtonIsoView.clicked.connect(main_wnd.on_iso_view)
            cSection.addCustomWidget(pane)
        except Exception as ex:
            message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                      f"{sys.exc_info()[-1].tb_lineno}"
            pass

        return  # Everything after this is old

    def add_help_tab(self):
        """ Adds the Help Tab """
        from App import App
        from RibbonPanes import QHelpPane

        try:
            tab = self.addTab('Help')  # "Help"

            # Action Section
            cSection = tab.addSection('Help')
            pane = QHelpPane()
            pane.ui.toolButtonHelp.clicked.connect(App.mainWnd().on_help)
            cSection.addCustomWidget(pane)
        except Exception as ex:
            message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                      f"{sys.exc_info()[-1].tb_lineno}"
            pass

        return  # Everything after this is old


class AppRibbonFileMenu(QFileMenu):
    """ Widget that represents the file menu for the ribbon """

    def __init__(self):
        """ Creates and initializes the menu """
        from App import App
        from RibbonPanes import QConfigPane

        QFileMenu.__init__(self)
        main_wnd = App.mainWnd()
        """
        self.setRecentFilesText(self.tr('Recent levels'))

        # Add a recent files manager
        self.recentFilesMgr = QRecentFilesManager()
        self.setRecentFilesManager(self.recentFilesMgr)
        self.recentFileClicked.connect(self.handleRecentFileClicked)
        """

        pane = QConfigPane()
        self._addBtn(pane)
        self.addSeparator()
        self.addButton(icon=':/images/Exit.svg', title=self.tr('Exit'), handler=main_wnd.close)

    def handleRecentFileClicked(self, path):
        """ Handles recent files being clicked """
        pass

