from propylean.equipments.generic_equipment_classes import _VerticalVessels, _HorizontalVessels,\
    _SphericalVessels, _Blanketing
from propylean.settings import Settings
from propylean.constants import Constants
from propylean import properties as prop

class VerticalStorage(_VerticalVessels):
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        if "is_blanketed" in inputs and inputs["is_blanketed"]:
            self.blanketing = _Blanketing(tag=self.tag)

        VerticalStorage.items.append(self)
    
    def __repr__(self):
        return "Vertical Storage with tag: " + self.tag

class Bullet(_HorizontalVessels):
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        if "is_blanketed" in inputs and inputs["is_blanketed"]:
            self.blanketing = _Blanketing(tag=self.tag)  
        Bullet.items.append(self)
    
    def __repr__(self):
        return "Horizontal Storage with tag: " + self.tag

class Tank(_VerticalVessels):
    items = []
    def __init__(self, **inputs) -> None:
        self._index = len(Tank.items)
        super().__init__( **inputs)
        inputs["head_type"] = "Flat"
        if "is_blanketed" in inputs and inputs["is_blanketed"]:
            self.blanketing = _Blanketing(tag=self.tag)
        Tank.items.append(self)
    
    def __repr__(self):
        return "Tank with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())
    
    @property
    def head_type(self):
        self = self._get_equipment_object(self)
        return self._head_type
    @head_type.setter
    def head_type(self, value):
        raise Exception("Setting head_type for Tank is not allowed for tanks.")
    
    @classmethod
    def list_objects(cls):
        return cls.items

class Sphere(_SphericalVessels):
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs) 
        if "is_blanketed" in inputs and inputs["is_blanketed"]:
            self.blanketing = _Blanketing(tag=self.tag)
    
    def __repr__(self):
        return "Sphere with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

# Specialized storage equipments.
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
        raise Exception("Setting property 'main_fluid' is not allowed for AirReciever.")
