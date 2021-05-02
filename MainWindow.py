# coding: utf-8
""" This is MainWindow module """

import sys
import os
import subprocess
import asyncio
from multiprocessing import Process, Queue
from functools import partial

from qt import *
from waitingspinnerwidget import QtWaitingSpinner

import vtk
from VTKViewer import QVTKViewer
from Scene import Scene

from UI.MainWindow_UI import Ui_MainWindow
from SingletonInstance import SingletonInstane
from AppDocData import *
from AppRibbon import AppRibbon


class QSpinnerPane(QWidget):
    def __init__(self):
        import os
        from PyQt5 import QtWidgets, uic

        QWidget.__init__(self)
        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UI', 'Spinner.ui')
        uiClass, qtBaseClass = uic.loadUiType(ui_path)
        self.ui = uiClass()
        self.ui.setupUi(self)


class MainWindow(QMainWindow, Ui_MainWindow, SingletonInstane):
    """ This is MainWindow class """
    addMessage = Signal(Enum, str)

    def __init__(self):
        """ initialize """
        from App import App
        from Primitives.Axes import Axes

        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.addMessage.connect(self.add_message)

        try:
            self.waiting_spinner = QtWaitingSpinner(self.statusbar)

            self.actionSave.triggered.connect(self.save_output)

            self.ribbon = AppRibbon()
            self.setMenuWidget(self.ribbon)

            app_doc_data = AppDocData.instance()
            _translate = QCoreApplication.translate
            version = QCoreApplication.applicationVersion()
            self.setWindowTitle(f"{App.NAME}({version})")

            self.ren = Scene()

            self.vtk_viewer = QVTKViewer(self, self.ren)
            self.verticalLayout.addWidget(self.vtk_viewer)

            self.ren.SetBackground2(1, 1, 1)
            self.ren.SetGradientBackground(1)

            self.axes = Axes(self.ren)

            self.vtk_viewer.start()
        except Exception as ex:
            from AppDocData import MessageType

            message = f"error occurred({str(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                      f"{sys.exc_info()[-1].tb_lineno}"

            self.addMessage.emit(MessageType.Error, message)

    def load_style_sheet(self, file: str):
        """load stylesheets"""
        from App import App

        App.instance().load_style_sheet(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stylesheets', file))

        app_doc_data = AppDocData.instance()
        configs = [Config('app', 'stylesheets', file)]
        app_doc_data.save_app_configs(configs)

    def load_language(self, file: str):
        """ load language file and then apply selected language """
        from App import App

        try:
            qm_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'translates', f"{file}.qm")
            App.instance().load_language(qm_file)

            app_doc_data = AppDocData.instance()
            configs = [Config('app', 'language', file)]
            app_doc_data.save_app_configs(configs)
        finally:
            self.retranslateUi(self)

    def open_file(self):
        """pop up open file dialog"""
        supporting_files = ['*.stl', '*.dxf', '*.s3d', '*.vrml', '*.idf', '*.pcf', '*.json']

        try:
            file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', "",
                                                       f"3D Files ({';'.join(supporting_files)});;")
            if file_path:
                self.build_scene(file_path)
        except Exception as ex:
            from App import App
            message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                      f"{sys.exc_info()[-1].tb_lineno}"
            self.addMessage.emit(MessageType.Error, message)

    def open_afexport(self):
        """pop up open afexport dialog"""
        from OpenAutoFormDialog import QOpenAutoFormDialog
        from AFexport.AFexportReader import AFexportReader

        try:
            dlg = QOpenAutoFormDialog(self)
            if QDialog.Accepted == dlg.exec_():
                self.build_scene(dlg.node_file_path, dlg.element_file_path)
        except Exception as ex:
            from App import App
            message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                      f"{sys.exc_info()[-1].tb_lineno}"
            self.addMessage.emit(MessageType.Error, message)

    def on_opacity_changed(self, value: int):
        """opacity is changed"""

        actors = self.ren.GetActors()
        actors.InitTraversal()
        for idx in range(actors.GetNumberOfItems()):
            actor = actors.GetNextActor()
            actor.GetProperty().SetOpacity(float(value/100.))

        self.vtk_viewer.render_window.Render()

    def on_left_view(self):
        """left view"""
        from ViewActions import ViewActions

        self.ren.view.update_camera(ViewActions.ViewDir.LeftView)

    def on_right_view(self):
        """right view"""
        from ViewActions import ViewActions

        self.ren.view.update_camera(ViewActions.ViewDir.RightView)

    def on_front_view(self):
        """front view"""
        from ViewActions import ViewActions

        self.ren.view.update_camera(ViewActions.ViewDir.FrontView)

    def on_back_view(self):
        """back view"""
        from ViewActions import ViewActions

        self.ren.view.update_camera(ViewActions.ViewDir.BackView)

    def on_top_view(self):
        """top view"""
        from ViewActions import ViewActions

        self.ren.view.update_camera(ViewActions.ViewDir.TopView)

    def on_bottom_view(self):
        """bottom view"""
        from ViewActions import ViewActions

        self.ren.view.update_camera(ViewActions.ViewDir.BottomView)

    def on_iso_view(self):
        """iso view"""
        from ViewActions import ViewActions

        self.ren.view.update_camera(ViewActions.ViewDir.IsoView)

    def open_nodes(self):
        """ load nodes from csv file """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog.getOpenFileName(self, "Open nodes file", os.getcwd(), "csv files(*.csv)",
                                               options=options)
        if file_name[0]:
            import pandas as pandas

            self.lineEditNodes.setText(file_name[0])

            self.nodes_data = pandas.read_csv(file_name[0])
            # self.table.dataFrameChanged.connect(self.datatable_updated)
            self.table_nodes_widget.setDataFrame(self.nodes_data)

    def open_elements(self):
        """ load elements from csv file """

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog.getOpenFileName(self, "Open elements file", os.getcwd(), "csv files(*.csv)",
                                                options=options)
        if file_name[0]:
            import pandas as pandas

            self.lineEditElements.setText(file_name[0])

            self.elements_data = pandas.read_csv(file_name[0])
            # self.table.dataFrameChanged.connect(self.datatable_updated)
            self.table_elements_widget.setDataFrame(self.elements_data)

    def add_message(self, messageType, message):
        """add message to listwidget"""
        from AppDocData import MessageType

        try:
            current = QDateTime.currentDateTime()

            item = QListWidgetItem('{}: {}'.format(current.toString('hh:mm:ss'), message))
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            if messageType == MessageType.Error:
                item.setBackground(Qt.red)

            self.listWidgetLog.insertItem(0, item)
        except Exception as ex:
            print('error occurred({}) in {}:{}'.format(repr(ex), sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                       sys.exc_info()[-1].tb_lineno))

    def test_code(self) -> dict:
        import sqlite3
        from itertools import islice

        def chunk(it, size):
            it = iter(it)
            return iter(lambda: tuple(islice(it, size)), ())

        data = {'actor': []}
        try:
            with sqlite3.connect("S3D Test.db") as conn:
                cursor = conn.cursor()

                sql = 'SELECT VertexList, IndexList from VTEX'
                cursor.execute(sql)
                rows = cursor.fetchall()
                for row in rows:
                    tokens = row[0].split(' ')
                    points_ = list(chunk(map(float, [x for x in row[0].split(' ') if x]), 3))
                    indexes = list(chunk(map(int, [x for x in row[1].split(' ') if x]), 3))

                    # Define a set of points - these are the ordered polygon vertices
                    points = vtk.vtkPoints()
                    points.SetNumberOfPoints(len(points_))

                    for idx in range(len(points_)):
                        x, y, z = points_[idx][0], points_[idx][1], points_[idx][2]
                        points.InsertPoint(idx, x, y, z)

                    faces = vtk.vtkCellArray()
                    for idx in range(len(indexes)):
                        # Make a cell with these points
                        triangle = vtk.vtkTriangle()
                        node0, node1, node2 = indexes[idx][0], indexes[idx][1], indexes[idx][2]
                        triangle.GetPointIds().SetId(0, node0)
                        triangle.GetPointIds().SetId(1, node1)
                        triangle.GetPointIds().SetId(2, node2)
                        faces.InsertNextCell(triangle)

                    # Next you create a vtkPolyData to store your face and vertex information that
                    # represents your polyhedron.
                    output = vtk.vtkPolyData()
                    output.SetPoints(points)
                    output.SetPolys(faces)

                    mapper = vtk.vtkPolyDataMapper()
                    mapper.SetInputData(output)

                    actor = vtk.vtkActor()
                    actor.SetMapper(mapper)
                    data['actor'].append(actor)
        except Exception as ex:
            from App import App
            message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                      f"{sys.exc_info()[-1].tb_lineno}"
            self.addMessage.emit(MessageType.Error, message)

        return data

    class Worker(QThread):
        finished = pyqtSignal(dict)

        def __init__(self, file_path: str, element_file_path: str, renderer):
            super().__init__()

            self._file_path = file_path
            self._element_file_path = element_file_path
            self._renderer = renderer

        def run(self):
            from ReaderFactory import ReaderFactory
            from AFexport.AFexportReader import AFexportReader
            from S3D.S3DReader import S3DExportReader
            from IDF.IDFImporter import IDFImporter
            from PCF.PCFImporter import PCFImporter
            from NetworkxJson.NetworkxJsonImporter import NetworksJsonImporter

            data = {}
            reader = ReaderFactory.get(self._file_path, self._element_file_path)
            if reader:
                mapper = vtk.vtkPolyDataMapper()
                if type(reader) is vtk.vtkVRMLImporter:
                    actors = reader.GetRenderer().GetActors()
                    data['actor'] = actors
                    self.finished.emit(data)
                    return
                elif type(reader) is S3DExportReader:
                    actors = reader.GetOutput(self._renderer)
                    """
                    data['actor'] = actors
                    """
                    self.finished.emit({'actor': None})
                    return
                elif type(reader) is IDFImporter:
                    reader.GetOutput(self._renderer)
                    self.finished.emit({'actor': None})
                    return
                elif type(reader) is PCFImporter:
                    reader.GetOutput(self._renderer)
                    self.finished.emit({'actor': None})
                    return
                elif type(reader) is NetworksJsonImporter:
                    reader.GetOutput(self._renderer)
                    self.finished.emit({'actor': None})
                    return
                elif type(reader) is not AFexportReader:
                    if vtk.VTK_MAJOR_VERSION <= 5:
                        mapper.SetInput(reader.GetOutput())
                    else:
                        mapper.SetInputConnection(reader.GetOutputPort())
                else:
                    mapper.SetInputData(reader.GetOutput())

                actor = vtk.vtkActor()
                actor.SetMapper(mapper)
                data['actor'] = [actor,]

                self.finished.emit(data)

    def build_scene(self, file_path: str, element_file_path: str = None):
        """
        @brief: build scene
        """
        from ReaderFactory import ReaderFactory
        from AFexport.AFexportReader import AFexportReader

        try:
            app_doc_data = AppDocData.instance()

            self.ren.RemoveAllViewProps()

            self.worker = MainWindow.Worker(file_path, element_file_path, self.ren)
            self.worker.finished.connect(self.on_finished)
            self.waiting_spinner.start()
            self.worker.start()
        except Exception as ex:
            from App import App
            message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                      f"{sys.exc_info()[-1].tb_lineno}"
            self.addMessage.emit(MessageType.Error, message)

    def on_finished(self, data):
        from Primitives import Sphere, Cylinder

        if data and data['actor']:
            actors = data['actor']
            for actor in actors:
                actor.GetProperty().SetInterpolationToFlat()
                self.ren.AddActor(actor)

            #self.ren.reset_camera_tight(margin_factor=1.0)

        self.vtk_viewer.render_window.Render()

        self.waiting_spinner.stop()

    def convert_pc_file(self):
        """convert pc file"""
        import decimal

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        name, _ = QFileDialog.getOpenFileName(self, "Open pc,m01 file", os.getcwd(), "pc files(*.pc);;m01 files(*.m01)",
                                              options=options)
        if name:
            import pandas as pandas

            try:
                headers = ['$ PAM-GENERIS FORMATTED FILE PRODUCED BY AFK\n',
                           'FREE\n',
                           'SOLVER STAMP\n',
                           'DATACHECK NO\n',
                           '$ NODES\n',
                           'MAT   /     1  100    7.8E-6         0\n',
                           'BraceSill\n',
                           '       210                 0.3       0.7\n',
                           '\n',
                           '\n',
                           '\n',
                           '\n'
                           ]
                nodes = []
                shells = []
                with open(name) as file:
                    line_no = 1
                    for line in file:
                        _type = line[:5].strip()
                        if _type == 'NODE':
                            index = line[8:16].strip()
                            x = line[16:32].strip()
                            y = line[32:48].strip()
                            z = line[48:64].strip()
                            nodes.append((index, x, y, z))
                        elif _type == 'SHELL':
                            index = line[8:16].strip()
                            padding = line[16:24].strip()
                            node_idx1 = line[24:32].strip()
                            node_idx2 = line[32:40].strip()
                            node_idx3 = line[40:48].strip()
                            shells.append((index, padding, node_idx1, node_idx2, node_idx3))
                        elif line and not nodes and not shells:  # node와 shell보다 먼저 나오는 부분을 header로 처리한다
                            """header"""
                            pass

                        line_no += 1

                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                name, _ = QFileDialog.getSaveFileName(self, "Save pc file", os.path.splitext(name)[0] + '.pc',
                                                      filter="pc files(*.pc)", options=options)
                if name:
                    with open(name, 'w') as file:
                        file.writelines(headers)
                        for node in nodes:
                            file.write(
                                'NODE  / ' + format(f"{node[0]}", ">8s") + format(f"{decimal.Decimal(node[1]):.6f}",
                                                                                  ">16s") +
                                format(f"{decimal.Decimal(node[2]):.6f}", ">16s") + format(
                                    f"{decimal.Decimal(node[3]):.6f}", ">16s") +
                                format("0", ">8s") + '\n')
                        for shell in shells:
                            file.write('SHELL / ' + format(f"{shell[0]}", ">8s") + format(f"{shell[1]}", ">8s") +
                                       format(f"{shell[2]}", ">8s") + format(f"{shell[3]}", ">8s") + format(
                                f"{shell[4]}",
                                ">8s") +
                                       format("3", ">16") + '\n')

                    self.show_message(self.tr('Information'), self.tr('Converting is done'))
            except Exception as ex:
                from App import App
                message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                          f"{sys.exc_info()[-1].tb_lineno}"
                self.addMessage.emit(MessageType.Error, message)

    def generate_output(self):
        """ generate output """

        self.build_scene()

        self.show_message(f"AutoForm", f"Rendering node and element is complete")

    def save_output(self):
        """ save generated output """
        from SHSExport.SHSExporter import SHSExporter

        try:
            supporting_files = ['VRML Files(*.vrml)', '3D Files(*.shs)']

            file_path, _ = QFileDialog.getSaveFileName(self, 'Save', '', f"{';;'.join(supporting_files)};;",
                                                       options=QFileDialog.DontUseNativeDialog)
            if file_path:
                ext = os.path.splitext(file_path)[1]
                if ext.lower() == '.vrml':
                    exporter = vtk.vtkVRMLExporter()
                    exporter.SetRenderWindow(self.ren.GetRenderWindow())
                    exporter.SetFileName(file_path)
                    exporter.Write()
                    exporter.Update()
                elif ext.lower() == '.shs':
                    exporter = SHSExporter()
                    exporter.SetRenderWindow(self.ren.GetRenderWindow())
                    exporter.SetFileName(file_path)
                    exporter.Write()
        except Exception as ex:
            message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                      f"{sys.exc_info()[-1].tb_lineno}"
            self.addMessage.emit(MessageType.Error, message)

    def on_click_networkx(self):
        """
        @brief pop-up a dialog related to networkx
        """
        import json
        import networkx as nx
        from NetworkxJson.NetworkxJsonImporter import NetworksJsonImporter
        from AppDocData import AppDocData
        from NetworkxDialog import QNetworkxDialog

        try:
            app_doc_data = AppDocData.instance()

            actors = self.ren.GetActors()
            num_actors = actors.GetNumberOfItems()
            if num_actors:
                dlg = QNetworkxDialog(self.ren, self)
                dlg.show()
                pass
        except Exception as ex:
            message = f'error occurred({ex}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:' \
                      f'{sys.exc_info()[-1].tb_lineno}'
            print(message)

    def on_help(self):
        """show help document"""
        pass

    def show_message(self, title, text):
        """pop-up message box"""

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)

        msg.setWindowTitle(title)
        msg.setText(text)

        return msg.exec_()


if __name__ == '__main__':
    import locale
    from App import App

    app = App(sys.argv)
    try:
        app._mainWnd = MainWindow.instance()
        app._mainWnd.show()
        sys.exit(app.exec_())
    except Exception as ex:
        print('error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                  sys.exc_info()[-1].tb_lineno))
    finally:
        pass
