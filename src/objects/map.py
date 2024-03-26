from src.objects.object import Object
from src.objects.point import Point
from src.objects.figure import Figure
from src.objects.floor import Floor

class Map(Object):

    def __init__(self, **kwargs):
        data_schema = {
                        "name": str,
                        "floors": list,
                      }

        self.actual_floors = 0
        self.actual_obstacle = 1

        self.index_figure = 0
        super().__init__(data_schema, **kwargs)

        # if len(self.floors) == 0:
        #     self.floors.append(Floor(figures=[]))
        #
        # if len(self.floors[self.actual_floors].figures) == 0:
        #     self.floors[self.actual_floors].figures.append(Figure(points=[], mode="full"))

    def add_floor(self):
        self.floors.append(Floor(figures=[]))
        self.actual_floors += 1
        self.floors[self.actual_floors].figures.append(Figure(points=[], mode="full"))

    def init(self):

        if len(self.floors) == 0:
            self.floors.append(Floor(figures=[]))

        if len(self.floors[self.actual_floors].figures) == 0:
            self.floors[self.actual_floors].figures.append(Figure(points=[], mode="full"))

    def add_point(self, x, y):
        if len(self.floors[self.actual_floors]) <= self.index_figure:
            self.floors[self.actual_floors].append(Figure(points=[], mode="line"))

        self.floors[self.actual_floors][self.index_figure].points.append(Point(x=x, y=y))

    def add_point_to_specific_point(self, x, y, figure_index, point_index):
        new_point = Point(x=x, y=y)
        self.floors[self.actual_floors][figure_index].points.insert(point_index + 1, new_point)

    def add_points_in_obstacles(self, x, y):
        if len(self.floors[self.actual_floors]) <= self.actual_obstacle:
            self.floors[self.actual_floors].append(Figure(points=[], mode="line"))
            print("add obstacle")
        self.floors[self.actual_floors][self.actual_obstacle].points.append(Point(x=x, y=y))

    def from_json(self, data):
        map = super().from_json(data)
        map.floors = [Floor.from_json(Floor, floor) for floor in map.floors]
        return map