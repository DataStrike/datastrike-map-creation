from src.objects.object import Object
from src.objects.point import Point
from src.objects.figure import Figure


class Map(Object):

    def __init__(self, **kwargs):
        data_schema = {
                        "name": str,
                        "figures": list
                      }

        self.actual_obstacle = 1
        super().__init__(data_schema, **kwargs)

        if len(self.figures) == 0:
            self.figures.append(Figure(points=[], mode="full"))

    def add_point(self, x, y):
        self.figures[0].points.append(Point(x=x, y=y))
        # self.points.append(Point(x=x, y=y))

    def add_points_in_obstacles(self, x, y):
        if len(self.figures) <= self.actual_obstacle:
            self.figures.append(Figure(points=[], mode="line"))
            print("add obstacle")
        self.figures[self.actual_obstacle].points.append(Point(x=x, y=y))

    def from_json(self, data):
        map = super().from_json(data)
        for figure in map.figures:
            print(figure)
        map.figures = [Figure.from_json(Figure, figure) for figure in map.figures]
        return map