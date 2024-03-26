from src.objects.object import Object
from src.objects.figure import Figure


class Floor(Object):

    def __init__(self, **kwargs):

        data_schema = {"figures": list}
        super().__init__(data_schema, **kwargs)

    def from_json(self, data):

        floor = super().from_json(data)
        floor.figures = [Figure.from_json(Figure, figure) for figure in floor.figures]
        return floor