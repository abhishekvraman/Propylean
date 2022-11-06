from propylean.equipments.generic_equipment_classes import _VerticalVessels, _HorizontalVessels
from propylean.settings import Settings
from propylean.constants import Constants
from propylean import properties as prop

class VerticalSeparator(_VerticalVessels):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__( **inputs)
        self._index = len(VerticalSeparator.items)
        VerticalSeparator.items.append(self)
    
    def __repr__(self):
        self = self._get_equipment_object(self)
        return "Vertical Separator with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @classmethod
    def list_objects(cls):
        return cls.items

class HorizontalSeparator(_HorizontalVessels):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__( **inputs)
        self._index = len(HorizontalSeparator.items)
        HorizontalSeparator.items.append(self)
    
    def __repr__(self):
        self = self._get_equipment_object(self)
        return "Horizontal Separator with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @classmethod
    def list_objects(cls):
        return cls.items

class Column(_VerticalVessels):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__( **inputs)
        self._index = len(Column.items)
        Column.items.append(self)
    
    def __repr__(self):
        self = self._get_equipment_object(self)
        return "Column with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())
    
    @classmethod
    def list_objects(cls):
        return cls.items

class FlareKOD(_HorizontalVessels):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        self._index = len(FlareKOD.items)
        FlareKOD.items.append(self)