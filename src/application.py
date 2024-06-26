import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from get_coordonate import GetCoordonate
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt5.QtWidgets import QSizePolicy
from PyQt5 import QtWidgets, uic
from matplotlib.figure import Figure
from src.objects.map import Map
from src.objects.point import Point
import numpy as np
import json


class MainWindow(QMainWindow):
    def __init__(self, name, map=None):
        super().__init__()

        self.setWindowTitle("Matplotlib in PyQt5")
        uic.loadUi('main.ui', self)

        if map is None:
            self.map = Map(name=name, figures=[])
        else:
            self.map = Map.from_json(map)

        self.name = name
        self.file_reader = None

        self.mode = "fusion"

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(800, 500)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.gridLayout_2.addWidget(self.canvas)

        self.ax = self.figure.add_subplot(111)
        self.update_plot()
        self.canvas.mpl_connect('button_press_event', self.on_click)

        self.SaveMapButton.clicked.connect(self.save_map)
        self.LoadMapButton.clicked.connect(self.load_map)

        self.SelectFileButton.clicked.connect(self.load_file)

        self.CloseModeButton.clicked.connect(lambda: self.change_mode("close"))
        self.DeleteModeButton.clicked.connect(lambda: self.change_mode("delete"))
        self.GetModeButton.clicked.connect(lambda: self.change_mode("get"))

        self.NameTextEdit.textChanged.connect(self.change_name_map)
        self.checkBoxFile.stateChanged.connect(self.change_state)

    def change_name_map(self):
        self.name = self.NameTextEdit.toPlainText()
        self.map.name = self.name

    def change_state(self):
        if self.file_reader is not None:
            if self.checkBoxFile.isChecked():
                self.file_reader.running = True
            else:
                self.file_reader.running = False

    def save_map(self):
        map_json = self.map.export_json()
        map_json = json.dumps(map_json, indent=4, sort_keys=True, default=str)
        with open("{}.json".format(self.name), 'w') as f:
            f.write(map_json)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select TXT File", "", "TXT Files (*.txt)")

        if file_path:
            if self.file_reader is not None:
                self.file_reader.running = False

            self.file_reader = GetCoordonate(file_path, self)
            self.file_reader.start()

            if self.checkBoxFile.isChecked():
                self.file_reader.running = True
            else:
                self.file_reader.running = False

            file_path_name = file_path.split("/")[-1]
            name = file_path_name.split(".")[0]
            self.FileLabel.setText(name)

    def load_map(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select JSON File", "", "JSON Files (*.json)")

        if file_path:
            with open(file_path, 'r') as file:
                map_json = json.load(file)

            self.map = Map.from_json(self.map, map_json)
            self.update_plot()

            file_path_name = file_path.split("/")[-1]
            name = file_path_name.split(".")[0]
            self.NameTextEdit.setText(name)

    def on_click(self, event):
        if event.inaxes == self.ax:
            if self.mode == "close":
                if not hasattr(self, 'first_click'):
                    self.first_click = (event.xdata, event.ydata)
                else:
                    second_click = (event.xdata, event.ydata)
                    self.merge_points(self.first_click, second_click)
                    delattr(self, 'first_click')
                    self.update_plot()
            elif self.mode == "delete":
                self.delete_point(event.xdata, event.ydata)

    def delete_point(self, x, y):
        # Recherche de l'indice du point le plus proche des coordonnées données
        index, index_figure = self.find_nearest_point_index((x, y))
        # Suppression du point
        del self.map.figures[index][index_figure]
        self.update_plot()

    def merge_points(self, point1, point2):
        # Recherche des indices des points dans la liste de points
        index_figure1, index1 = self.find_nearest_point_index(point1)
        index_figure2, index2 = self.find_nearest_point_index(point2)

        # Ajout du nouveau point au premier ensemble de points
        self.map.figures[index_figure1].append(Point(x=self.map.figures[index_figure1][index1].x, y=self.map.figures[index_figure1][index1].y))


        # Rafraîchissement du graphique
        self.update_plot()

    def add_obstacle_point(self, x, y):

        x = float(x)
        y = float(y)

        self.map.add_points_in_obstacles(x, y)
        self.update_plot()

    def add_point(self, x, y):

        try:
            x = float(x)
            y = float(y)

            self.map.add_point(x, y)
            self.update_plot()


        except ValueError:
            print("Erreur de conversion de coordonnées")
    def find_nearest_point_index(self, point):
        min_distance = float('inf')
        nearest_index = None
        nearest_figure_index = None

        for f_index, figure in enumerate(self.map.figures):
            for p_index, p in enumerate(figure):
                distance = np.sqrt((point[0] - p.x) ** 2 + (point[1] - p.y) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_index = p_index
                    nearest_figure_index = f_index

        return nearest_figure_index, nearest_index

    def update_plot(self):
        self.ax.clear()

        # Affichage des points
        for i, figure in enumerate(self.map.figures):
            x = [point.x for point in figure]
            y = [point.y for point in figure]
            if i == 0:
                self.ax.plot(x, y, 'bo-')
            else:
                self.ax.plot(x, y, 'ro-')

        self.canvas.draw()

    def change_mode(self, mode):
        self.mode = mode
        self.ModeLabel.setText("Mode : {}".format(mode))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("test")
    window.show()
    sys.exit(app.exec_())