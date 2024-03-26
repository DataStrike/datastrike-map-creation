import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from get_coordonate import GetCoordonate
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt5.QtWidgets import QSizePolicy
from PyQt5 import QtWidgets, uic
from matplotlib.figure import Figure
from src.objects.map import Map
from src.objects.point import Point
from src.objects.figure import Figure as FigureObject
import numpy as np
import json


class MainWindow(QMainWindow):
    def __init__(self, name, map=None):
        super().__init__()

        self.setWindowTitle("Matplotlib in PyQt5")
        uic.loadUi('main.ui', self)

        if map is None:
            self.map = Map(name=name, figures=[])
            self.map.init()

        else:
            self.map = Map.from_json(map)
            self.map.init()

        self.name = name
        self.file_reader = None

        self.mode = "fusion"

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.figure.patch.set_facecolor('black')

        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(800, 500)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.gridLayout_2.addWidget(self.canvas, 1, 0, 1, 2)
        self.addToolBar(NavigationToolbar(self.canvas, self))
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('black')  # Couleur de fond des axes

        # Pour une meilleure lisibilité, vous pouvez vouloir changer la couleur des axes et des labels
        self.ax.tick_params(axis='x', colors='white')  # Couleur des ticks de l'axe X
        self.ax.tick_params(axis='y', colors='white')  # Couleur des ticks de l'axe Y
        self.ax.spines['bottom'].set_color('white')  # Couleur du bas du cadre
        self.ax.spines['top'].set_color('white')  # Couleur du haut du cadre
        self.ax.spines['right'].set_color('white')  # Couleur de droite du cadre
        self.ax.spines['left'].set_color('white')  # Couleur de gauche du cadre
        self.ax.xaxis.label.set_color('white')  # Couleur du label de l'axe X
        self.ax.yaxis.label.set_color('white')  # Couleur du label de l'axe Y
        self.ax.title.set_color('white')  # Couleur du titre
        self.update_plot()
        self.canvas.mpl_connect('button_press_event', self.on_click)

        self.SaveMapButton.clicked.connect(self.save_map)
        self.LoadMapButton.clicked.connect(self.load_map)

        self.SelectFileButton.clicked.connect(self.load_file)

        self.CloseModeButton.clicked.connect(lambda: self.change_mode("close"))
        self.DeleteModeButton.clicked.connect(lambda: self.change_mode("delete"))
        self.SelectFigureButton.clicked.connect(lambda: self.change_mode("select"))
        self.SelectPointButton.clicked.connect(lambda: self.change_mode("select_point"))

        self.floorLessButton.clicked.connect(lambda: self.change_floor(-1))
        self.floorMoreButton.clicked.connect(lambda: self.change_floor(1))
        self.floorNewButton.clicked.connect(lambda: self.add_floor())

        self.figureNewButton.clicked.connect(lambda: self.add_figure())

        self.floorLabel.setText("Floor : {}".format(self.map.actual_floors))

        self.NameTextEdit.textChanged.connect(self.change_name_map)
        self.checkBoxFile.stateChanged.connect(self.change_state)
        self.ModeComboBox.currentIndexChanged.connect(self.change_mode_actual_figure)

        self.index_figure = 0

    def add_figure(self):
        self.map.floors[self.map.actual_floors].figures.append(FigureObject(points=[], mode="line"))
        self.index_figure = len(self.map.floors[self.map.actual_floors].figures) - 1
        self.map.index_figure = self.index_figure

    def change_floor(self, index):

        index = self.map.actual_floors + index

        try:
            t = self.map.floors[index]
            self.map.actual_floors = index
            self.update_plot()
            self.floorLabel.setText("Floor : {}".format(self.map.actual_floors))
        except IndexError:
            print("Floor doesn't exist")

    def add_floor(self):
        self.map.add_floor()
        self.update_plot()
        self.floorLabel.setText("Floor : {}".format(self.map.actual_floors))

    def change_mode_actual_figure(self, index):
        selected_item = self.ModeComboBox.itemText(index)
        self.map.floors[self.map.actual_floors].figures[self.index_figure].mode = selected_item
        self.update_plot()

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
            elif self.mode == "select":
                self.index_figure = self.find_nearest_point_index((event.xdata, event.ydata))[0]
                self.map.index_figure = self.index_figure
                self.FiguresLabel.setText("Figure : {}".format(self.index_figure))
            elif self.mode == "select_point":
                self.reference_point = self.find_nearest_point_index((event.xdata, event.ydata))

    def delete_point(self, x, y):
        # Recherche de l'indice du point le plus proche des coordonnées données
        index_figure, index = self.find_nearest_point_index((x, y))
        # Suppression du point
        del self.map.floors[self.map.actual_floors].figures[index_figure].points[index]
        self.update_plot()

    def merge_points(self, point1, point2):
        # Recherche des indices des points dans la liste de points
        index_figure1, index1 = self.find_nearest_point_index(point1)
        index_figure2, index2 = self.find_nearest_point_index(point2)

        # Ajout du nouveau point au premier ensemble de points
        self.map.floors[self.map.actual_floors].figures[index_figure1].points.append(Point(x=self.map.floors[self.map.actual_floors].figures[index_figure1].points[index1].x, y=self.map.floors[self.map.actual_floors].figures[index_figure1].points[index1].y))


        # Rafraîchissement du graphique
        self.update_plot()

    def add_obstacle_point(self, x, y):

        x = float(x)
        y = float(y)

        self.map.add_points_in_obstacles(x, y)
        self.update_plot()

    def add_point(self, x, y):

        if self.mode == "select_point":
            x = float(x)
            y = float(y)

            self.map.add_point_to_specific_point(x, y, self.reference_point[0], self.reference_point[1])
            self.reference_point[1] += 1
            self.update_plot()


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

        for f_index, figure in enumerate(self.map.floors[self.map.actual_floors].figures):
            for p_index, p in enumerate(figure.points):
                distance = np.sqrt((point[0] - p.x) ** 2 + (point[1] - p.y) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_index = p_index
                    nearest_figure_index = f_index

        return nearest_figure_index, nearest_index

    def update_plot(self):
        self.ax.clear()

        # Affichage des points
        for i, figure in enumerate(self.map.floors[self.map.actual_floors].figures):
            x = [point.x for point in figure.points]
            y = [point.y for point in figure.points]

            if figure.mode == "line":
                self.ax.plot(x, y, 'bo-')
            if figure.mode == "obstacle":
                self.ax.plot(x, y, 'w-')
            if figure.mode == "fond":
                self.ax.fill(x, y, 'o')
                self.ax.plot(x, y, 'w-')

        self.canvas.draw()

    def change_mode(self, mode):
        self.mode = mode
        self.ModeLabel.setText("Mode : {}".format(mode))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("test")
    window.show()
    sys.exit(app.exec_())