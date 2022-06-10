from propylean.equipments.generic_equipment_classes import _VerticalVessels, _HorizontalVessels
from propylean.settings import Settings
from propylean.constants import Constants
from propylean import properties as prop

class VerticalStorage(_VerticalVessels):
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        VerticalStorage.items.append(self)
    
    def __repr__(self):
        return "Vertical Storage with tag: " + self.tag

class StorageBullet(_HorizontalVessels):
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        StorageBullet.items.append(self)
    
    def __repr__(self):
        return "Horizontal Storage with tag: " + self.tag

class Tank(_VerticalVessels):
    items = []
    def __init__(self, **inputs) -> None:
        self._index = len(Tank.items)
        super().__init__( **inputs)
        Tank.items.append(self)
    
    def __repr__(self):
        return "Tank with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())
    
    @classmethod
    def list_objects(cls):
        return cls.items

# Specialized storage.
class AirReciever(_VerticalVessels):
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        self._main_fluid = "gas"
        AirReciever.items.append(self)
    
    def __repr__(self):
        return "AirReciever with tag: " + self.tag

    @property
    def main_fluid(self):
        self = self._get_equipment_object(self)
        return self._main_fluid
    @main_fluid.setter
    def main_fluid(self, value):
        raise Exception("Setting property 'main_fluid' is disabled for AirReciever.")
