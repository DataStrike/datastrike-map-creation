from src.objects.object import Object


class Point(Object):

    def __init__(self, **kwargs):

        data_schema = {"x": float,
                       "y": float
                       }

        super().__init__(data_schema, **kwargs)
