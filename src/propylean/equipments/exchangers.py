from propylean.equipments.generic_equipment_classes import _Exchangers
from propylean import streams
from propylean import properties as prop
from propylean.validators import _Validators

# Start of final classes of heat exchangers
class ShellnTubeExchanger(_Exchangers):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__( **inputs)
        self._index = len(ShellnTubeExchanger.items)
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
        super().__init__( **inputs)
        self.fan_power = prop.Power() if "fan_power" not in inputs else inputs["fan_power"]
        del self.energy_out
        self._index = len(AirCooler.items)
        AirCooler.items.append(self)
    
    def __repr__(self):
        self = self._get_equipment_object(self)
        return "Air Cooler with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())
    
    @property
    def temperature_change(self):
        self = self._get_equipment_object(self)
        value = -1 * self._temperature_change.value
        return prop.Temperature(value, self._temperature_change.unit)
    @temperature_change.setter
    def temperature_change(self, value):
        _Validators.validate_arg_prop_value_type("temperature_change", value, (prop.Temperature, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Temperature)
        if unit is None:
            unit = self._temperature_change.unit
        self._temperature_change = prop.Temperature(-1 * value, unit)
        self._outlet_temperature =  self._inlet_temperature + self._temperature_change
        self._update_equipment_object(self)

    @property
    def fan_power(self):
        self = self._get_equipment_object(self)
        return self._fan_power
    @fan_power.setter
    def fan_power(self, value):
        _Validators.validate_arg_prop_value_type("fan_power", value, (prop.Power, int, float, tuple))
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
        _Validators.validate_arg_prop_value_type("energy_in", value, (prop.Power, int, float, tuple))
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
            stream_type in ['energy', 'e']):
            if direction is not None and 'out' in direction:
                raise Exception('AirCooler only supports fan energy inlet.')
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
            stream_type in ['energy', 'e']):
            if direction is not None and 'out' in direction:
                raise Exception('AirCooler only supports fan energy inlet.')
            direction = 'in'
        return super().disconnect_stream(stream_object, direction, stream_tag, stream_type)

class ElectricHeater(_Exchangers):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__( **inputs)
        self.power = prop.Power() if "power" not in inputs else inputs["power"]
        del self.energy_out
        self._index = len(ElectricHeater.items)
        ElectricHeater.items.append(self)
    
    def __repr__(self):
        self = self._get_equipment_object(self)
        return "Electric Heater with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())
    
    def connect_stream(self, 
                       stream_object=None, 
                       direction=None, 
                       stream_tag=None, 
                       stream_type=None,
                       stream_governed=True):
        if ((stream_object is not None and 
            isinstance(stream_object, streams.EnergyStream)) or
            stream_type in ['energy', 'e']):
            if direction is not None and 'out' in direction:
                raise Exception('ElectricHeater only supports energy inlet.')
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
            stream_type in ['energy', 'e']):
            if direction is not None and 'out' in direction:
                raise Exception('ElectricHeater only supports energy inlet.')
            direction = 'in'
        return super().disconnect_stream(stream_object, direction, stream_tag, stream_type)

    @property
    def power(self):
        self = self._get_equipment_object(self)
        return self._power
    @power.setter
    def power(self, value):
        _Validators.validate_arg_prop_value_type("energy_in", value, (prop.Power, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Power)
        if unit is None:
            unit = self._power.unit         
        self._power = prop.Power(value, unit)
        self._update_equipment_object(self) 

    @property
    def energy_in(self):
        return self.power
    @energy_in.setter
    def energy_in(self, value):
        _Validators.validate_arg_prop_value_type("energy_in", value, (prop.Power, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Power)
        if unit is None:
            unit = self.energy_in.unit
        self._energy_in = prop.Power(value, unit)
        self._update_equipment_object(self)

    @classmethod
    def list_objects(cls):
        return cls.items
# End of final classes of heat exchangers      