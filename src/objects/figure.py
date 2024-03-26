from src.objects.object import Object
from src.objects.point import Point


class Figure(Object):

    def __init__(self, **kwargs):

        data_schema = {"points": list,
                       "mode": str}

        super().__init__(data_schema, **kwargs)


    def from_json(self, data):

        print(data)
        figure = super().from_json(data)
        figure.points = [Point.from_json(point) for point in figure.points]
        return figure