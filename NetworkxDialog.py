# coding: utf-8
""" This is Networkx dialog module """

import os
import sys

from qt import *

__author__ = "humkyung <humkyung@atools.co.kr>"


class QNetworkxDialog(QDialog):
    """ This is Networkx dialog class """

    def __init__(self, renderer, parent):
        from PyQt5 import uic
        import json
        from AppDocData import AppDocData
        from NetworkxJson.NetworkxJsonImporter import NetworksJsonImporter

        QDialog.__init__(self, parent)

        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UI', 'Networkx.ui')
        uiClass, qtBaseClass = uic.loadUiType(ui_path)
        self.ui = uiClass()
        self.ui.setupUi(self)

        self.ui.pushButtonFind.clicked.connect(self.on_clicked_find)
        self.ui.pushButtonAddNode.clicked.connect(self.on_clicked_add_node)
        self.ui.pushButtonAddEdge.clicked.connect(self.on_clicked_add_edge)
        self.ui.pushButtonAutoCalc.clicked.connect(self.on_clicked_calc_edge_weight)
        self.ui.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.on_clicked_save)

        self._renderer = renderer
        self._nodes = {}
        self._edges = {}

        self.build_graph()

    def build_graph(self):
        """
        build graph
        """
        import json
        from AppDocData import AppDocData
        from NetworkxJson.NetworkxJsonImporter import NetworksJsonImporter

        app_doc_data = AppDocData.instance()

        actors = self._renderer.GetActors()
        num_actors = actors.GetNumberOfItems()
        if num_actors:
            app_doc_data.g.clear()

            node_names = []
            actors.InitTraversal()
            for i in range(0, num_actors):
                actor = actors.GetNextItem()
                props = actor.GetProperty().GetInformation().Length(NetworksJsonImporter.KEY)
                for prop_idx in range(props):
                    value = actor.GetProperty().GetInformation().Get(NetworksJsonImporter.KEY, prop_idx)
                    _dict = json.loads(value)
                    if 'name' in _dict:  # node
                        self._nodes[_dict['name']] = actor
                        node_names.append(_dict['name'])
                    elif 'start' in _dict and 'end' in _dict and 'length' in _dict:  # edge
                        self._edges[actor] = [_dict['start'], _dict['end']]
                        app_doc_data.g.add_edge(_dict['start'], _dict['end'], length=float(_dict['length']))

            self.ui.comboBoxStart.clear()
            self.ui.comboBoxEnd.clear()
            self.ui.comboBoxEdgeStart.clear()
            self.ui.comboBoxEdgeEnd.clear()

            self.ui.comboBoxStart.addItems(node_names)
            self.ui.comboBoxEnd.addItems(node_names)
            self.ui.comboBoxEdgeStart.addItems(node_names)
            self.ui.comboBoxEdgeEnd.addItems(node_names)

    def find_node(self, name: str):
        """
        find a actor with name and return it if found otherwise return None
        """
        import json
        from NetworkxJson.NetworkxJsonImporter import NetworksJsonImporter

        actors = self._renderer.GetActors()
        num_actors = actors.GetNumberOfItems()
        if num_actors:
            actors.InitTraversal()
            for i in range(0, num_actors):
                actor = actors.GetNextItem()
                props = actor.GetProperty().GetInformation().Length(NetworksJsonImporter.KEY)
                for prop_idx in range(props):
                    value = actor.GetProperty().GetInformation().Get(NetworksJsonImporter.KEY, prop_idx)
                    _dict = json.loads(value)
                    if 'name' in _dict and _dict['name'] == name:  # node
                        return actor

        return None

    def on_clicked_find(self):
        """
        find shortest path with given start and end node
        """
        import vtk
        import networkx as nx
        from AppDocData import AppDocData

        try:
            colors = vtk.vtkNamedColors()

            """clear color"""
            for node, actor in self._nodes.items():
                actor.GetProperty().SetColor(colors.GetColor3d("White"))
            for actor, _ in self._edges.items():
                actor.GetProperty().SetColor(colors.GetColor3d("White"))

            app_doc_data = AppDocData.instance()
            start, end = None, None

            start_node_name, end_node_name = self.ui.comboBoxStart.currentText(), self.ui.comboBoxEnd.currentText()
            if start_node_name and end_node_name and start_node_name != end_node_name:
                path = nx.dijkstra_path(app_doc_data.g, start_node_name, end_node_name, 'length')
                for node in path:
                    self._nodes[node].GetProperty().SetColor(colors.GetColor3d("Banana"))
                    if not start:
                        start = node
                    else:
                        end = node
                        matches = [actor for actor, edge in self._edges.items() if start in edge and end in edge]
                        for match in matches:
                            match.GetProperty().SetColor(colors.GetColor3d("Banana"))
                        start, end = end, None

                self._renderer.GetRenderWindow().Render()
            else:
                QMessageBox.warning(self, self.tr('Warning'), self.tr('Please check input values'))
        except Exception as ex:
            message = f'error occurred({ex}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:' \
                      f'{sys.exc_info()[-1].tb_lineno}'
            print(message)

    def on_clicked_add_node(self):
        """
        add a new node
        """
        from Primitives.Sphere import Sphere
        from NetworkxJson.NetworkxJsonImporter import NetworksJsonImporter

        try:
            if self.ui.lineEditNodeName.text() and self.ui.lineEditNodeX.text() and self.ui.lineEditNodeY.text() and \
                    self.ui.lineEditNodeZ.text():
                name = self.ui.lineEditNodeName.text()
                if name not in self._nodes:
                    pos = [float(self.ui.lineEditNodeX.text()), float(self.ui.lineEditNodeY.text()),
                           float(self.ui.lineEditNodeZ.text())]
                    actor = Sphere(self._renderer, pos).actor
                    info = actor.GetProperty().GetInformation()
                    info.Append(NetworksJsonImporter.KEY, f'{{\"name\":\"{name}\"}}')

                    self._renderer.GetRenderWindow().Render()

                    self.build_graph()
                else:
                    QMessageBox.warning(self, self.tr('Warning'), self.tr('There is node which has same name'))
            else:
                QMessageBox.warning(self, self.tr('Warning'), self.tr('Name or Coordinates is empty'))
        except Exception as ex:
            message = f'error occurred({ex}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:' \
                      f'{sys.exc_info()[-1].tb_lineno}'
            QMessageBox.warning(self, self.tr('Warning'), self.tr(message))

    def on_clicked_calc_edge_weight(self):
        """
        calculate edge weight which is distance between two nodes
        """
        import math
        import vtk

        if self.ui.comboBoxEdgeStart.currentText() and self.ui.comboBoxEdgeEnd.currentText():
            u, v = self.ui.comboBoxEdgeStart.currentText(), self.ui.comboBoxEdgeEnd.currentText()
            start, end = self.find_node(u), self.find_node(v)
            sphere = start.GetMapper().GetInputConnection(0, 0).GetProducer()
            start_pos = sphere.GetCenter()

            sphere = end.GetMapper().GetInputConnection(0, 0).GetProducer()
            end_pos = sphere.GetCenter()

            distance = vtk.vtkMath.Distance2BetweenPoints(start_pos, end_pos)
            distance = math.sqrt(distance)
            self.ui.lineEditEdgeWeight.setText(str(distance))

    def on_clicked_add_edge(self):
        """
        add a new edge
        """
        from AppDocData import AppDocData
        from Primitives.Cylinder import Cylinder
        from NetworkxJson.NetworkxJsonImporter import NetworksJsonImporter

        try:
            if self.ui.comboBoxEdgeStart.currentText() and self.ui.comboBoxEdgeEnd.currentText() and \
                    self.ui.lineEditEdgeWeight.text():
                u, v = self.ui.comboBoxEdgeStart.currentText(), self.ui.comboBoxEdgeEnd.currentText()
                start, end = self.find_node(u), self.find_node(v)

                sphere = start.GetMapper().GetInputConnection(0, 0).GetProducer()
                start_pos = sphere.GetCenter()

                sphere = end.GetMapper().GetInputConnection(0, 0).GetProducer()
                end_pos = sphere.GetCenter()

                weight = float(self.ui.lineEditEdgeWeight.text())

                actor = Cylinder(self._renderer, pt1=start_pos, pt2=end_pos, radius=0.1).actor
                info = actor.GetProperty().GetInformation()
                info_str = f'{{\"start\":\"{u}\",\"end\":\"{v}\",\"length\":\"{weight}\"}}'
                info.Append(NetworksJsonImporter.KEY, info_str)
                self._edges[actor] = [u, v]

                app_doc_data = AppDocData.instance()
                app_doc_data.g.add_edge(u, v, length=float(weight))
            else:
                QMessageBox.Warning(self, self.tr('Warning'), self.tr('Name or Coordinates is empty'))
        except Exception as ex:
            message = f'error occurred({ex}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:' \
                      f'{sys.exc_info()[-1].tb_lineno}'
            QMessageBox.warning(self, self.tr('Warning'), self.tr(message))

    def on_clicked_save(self):
        """
        save nodes and edges to json file
        """
        import json
        from AppDocData import AppDocData
        from NetworkxJson.NetworkxJsonImporter import NetworksJsonImporter

        supporting_files = ['Json Files(*.json)']

        file_path, _ = QFileDialog.getSaveFileName(self, 'Save', '', f"{';;'.join(supporting_files)};;",
                                                   options=QFileDialog.DontUseNativeDialog)
        if file_path:
            app_doc_data = AppDocData.instance()

            json_data = {'nodes':[], 'edges':[]}

            actors = self._renderer.GetActors()
            num_actors = actors.GetNumberOfItems()
            if num_actors:
                actors.InitTraversal()
                for i in range(0, num_actors):
                    actor = actors.GetNextItem()
                    props = actor.GetProperty().GetInformation().Length(NetworksJsonImporter.KEY)
                    for prop_idx in range(props):
                        value = actor.GetProperty().GetInformation().Get(NetworksJsonImporter.KEY, prop_idx)
                        _dict = json.loads(value)
                        if 'name' in _dict:  # node
                            sphere = actor.GetMapper().GetInputConnection(0, 0).GetProducer()
                            position = sphere.GetCenter()
                            json_data['nodes'].append({'name': _dict['name'],
                                                       'pos': f'{position[0]},{position[1]},{position[2]}'})
                        elif 'start' in _dict and 'end' in _dict and 'length' in _dict:  # edge
                            self._edges[actor] = [_dict['start'], _dict['end']]
                            json_data['edges'].append({'start': _dict['start'], 'end': _dict['end'],
                                                       'length': _dict['length']})

            with open(file_path, "w", encoding='utf-8') as file:
                json.dump(json_data, file, indent=4)
