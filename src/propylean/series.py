from pandas import Series as PdSeries

class Series(PdSeries):
    def __init__(self, type="calculated") -> None:
        self._type = type
        if type.lower() == "observed":
            super().__init__()