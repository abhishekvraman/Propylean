from propylean.equipments.generic_equipment_classes import _VerticalVessels, _HorizontalVessels
from propylean.settings import Settings
from propylean.constants import Constants
from propylean import properties as prop

class VerticalSeparator(_VerticalVessels):
    items = []
    def __init__(self, **inputs) -> None:
        self._index = len(VerticalSeparator.items)
        super().__init__( **inputs)
        VerticalSeparator.items.append(self)
    
    def __repr__(self):
        return "Vertical Separator with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @classmethod
    def list_objects(cls):
        return cls.items

class HorizontalSeparator(_HorizontalVessels):
    items = []
    def __init__(self, **inputs) -> None:
        self._index = len(HorizontalSeparator.items)
        super().__init__( **inputs)
        HorizontalSeparator.items.append(self)
    
    def __repr__(self):
        return "Horizontal Separator with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @classmethod
    def list_objects(cls):
        return cls.items

class Column(_VerticalVessels):
    items = []
    def __init__(self, **inputs) -> None:
        self._index = len(Column.items)
        super().__init__( **inputs)
        Column.items.append(self)
    
    def __repr__(self):
        return "Column with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())
    
    @classmethod
    def list_objects(cls):
        return cls.items
