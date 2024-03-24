from src.objects.object import Object
from src.objects.point import Point

class Map(Object):

    def __init__(self, **kwargs):
        data_schema = {
                        "name": str,
                        "figures": list
                      }

        self.actual_obstacle = 1
        super().__init__(data_schema, **kwargs)
        self.figures.append([])

    def add_point(self, x, y):
        self.figures[0].append(Point(x=x, y=y))
        # self.points.append(Point(x=x, y=y))

    def add_points_in_obstacles(self, x, y):
        if not self.actual_obstacle in self.figures:
            self.figures.append([])
        self.figures[self.actual_obstacle].append(Point(x=x, y=y))

    def from_json(self, data):
        map = super().from_json(data)
        map.figures = [[Point.from_json(point) for point in figure] for figure in map.figures]
        return map