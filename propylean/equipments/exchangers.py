from propylean.generic_equipment_classes import _Exchangers
from propylean import streams
from propylean import properties as prop

# Start of final classes of heat exchangers
class ShellnTubeExchanger(_Exchangers):
    items = []
    def __init__(self, **inputs) -> None:
        self._index = len(ShellnTubeExchanger.items)
        super().__init__( **inputs)
        ShellnTubeExchanger.items.append(self)
    
    def __repr__(self):
        return "Shell & Tube Exchanger with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())
    
    @classmethod
    def list_objects(cls):
        return cls.items

class AirCooler(_Exchangers):
    items = []
    def __init__(self, **inputs) -> None:
        self._index = len(AirCooler.items)
        super().__init__( **inputs)
        self.fan_power = prop.Power() if "fan_power" not in inputs else inputs["fan_power"]
        del self.energy_out
        AirCooler.items.append(self)
    
    def __repr__(self):
        return "Air Cooler with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())
    
    @property
    def fan_power(self):
        self = self._get_equipment_object(self)
        return self._fan_power
    @fan_power.setter
    def fan_power(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Power)
        if unit is None:
            unit = self._fan_power.unit         
        self._fan_power = prop.Power(value, unit)
        self._update_equipment_object(self) 

    @property
    def energy_in(self):
        return self.fan_power
    @energy_in.setter
    def energy_in(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Power)
        if unit is None:
            unit = self.energy_in.unit
        self._energy_in = prop.Power(value, unit)
        self._update_equipment_object(self)

    @classmethod
    def list_objects(cls):
        return cls.items
    
    def connect_stream(self, 
                       stream_object=None, 
                       direction=None, 
                       stream_tag=None, 
                       stream_type=None,
                       stream_governed=True):
        if ((stream_object is not None and 
            isinstance(stream_object, streams.EnergyStream)) or
            stream_type in ['energy', 'power', 'e', 'p']):
            direction = 'in'
            stream_governed = False
        return super().connect_stream(direction=direction, 
                                      stream_object=stream_object, 
                                      stream_tag=stream_tag, 
                                      stream_type=stream_type,
                                      stream_governed=stream_governed)
    
    def disconnect_stream(self, stream_object=None, direction=None, stream_tag=None, stream_type=None):
        if ((stream_object is not None and 
            isinstance(stream_object, streams.EnergyStream)) or
            stream_type in ['energy', 'power', 'e', 'p']):
            direction = 'in'
        return super().disconnect_stream(stream_object, direction, stream_tag, stream_type)


class ElectricHeater(_Exchangers):
    items = []
    def __init__(self, **inputs) -> None:
        self._index = len(ElectricHeater.items)
        super().__init__( **inputs)
        ElectricHeater.items.append(self)
    
    def __repr__(self):
        return "Electric Heater with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())
    
    @classmethod
    def list_objects(cls):
        return cls.items
# End of final classes of heat exchangers      