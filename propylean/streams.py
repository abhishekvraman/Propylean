from ast import expr_context
from thermo.chemical import Chemical
import propylean.properties as prop

class EnergyStream (prop.Power):
    items = [] 
    def __init__(self, value=0, unit='W', tag=None, 
                 to_equipment_tag=None, to_equipment_type=None,
                 from_equipment_tag=None, from_equipment_type=None):
                 
                 super().__init__(value=value, unit=unit)
                 self.tag = tag
                 self.assign_equipment('to', to_equipment_tag, to_equipment_type)
                 self.assign_equipment('from', from_equipment_tag, from_equipment_type)
                 EnergyStream.items.append(self)
    
    def assign_equipment(self, to_or_from, equipment_tag, equipment_type, equipment_index=None):
        inlet_outlet = None
        if to_or_from in ['to','To','TO']:
            inlet_outlet = 'inlet'
            self.to_equipment_tag = equipment_tag
            self.to_equipment_type = equipment_type
            self.to_equipment_index = equipment_index if equipment_index != None else None
        elif to_or_from in ['from','From','FROM']:
            inlet_outlet = 'outlet'
            self.from_equipment_tag = equipment_tag
            self.from_equipment_type = equipment_type
            self.from_equipment_index = equipment_index if equipment_index != None else None

    def __repr__(self) -> str:
        return 'Energy Stream Tag: ' + self.tag

    @classmethod
    def list_objects(cls):
        return cls.items

    @classmethod
    def _update_stream_object(cls, index, object):
        if not isinstance(object, EnergyStream):
            raise Exception("Object type should be EnergyStream type. Type passed is ", type(object))
        cls.items[index] = object
      
class MaterialStream:
    items = [] 
    def __init__(self,tag = None,
                 mass_flowrate = 0,
                 pressure = 101325,
                 temperature = 298):
                 
                 self._tag = None
                 self._index = len(MaterialStream.items)
                 self._mass_flowrate = prop.MassFlowRate()
                 self._pressure = prop.Pressure()
                 self._temperature = prop.Temperature()
                 self.to_equipment = None
                 self.from_equipment = None
                 
                 self.tag = tag
                 self.mass_flowrate = mass_flowrate
                 self.temperature = temperature
                 self.pressure = pressure

                 MaterialStream.items.append(self)

    @property
    def tag(self):
        try:
            self = self._get_stream_object(self)
        except:
            pass
        return self._tag
    @tag.setter
    def tag(self, value):
        self = self._get_stream_object(self)
        if value is None:
            value = self._create_stream_tag()
        if self._check_tag_assigned(value):
            raise Exception("Tag already assinged!")
        self._tag = value
        self._update_stream_object(self)
    
    @property
    def index(self):
        return self._index
        
    @property
    def pressure(self):
        self = self._get_stream_object(self)
        return self._pressure
    @pressure.setter
    def pressure(self, value):
        self = self._get_stream_object(self)
        unit = self._pressure.unit
        if isinstance(value, tuple):
            unit = value[1]
            value = value[0]
        elif isinstance(value, prop.Pressure):
            unit = value.unit
            value = value.value
        self._pressure = prop.Pressure(value, unit)
        self._update_stream_object(self)

    @property
    def temperature(self):
        self = self._get_stream_object(self)
        return self._temperature
    @temperature.setter
    def temperature(self, value):
        self = self._get_stream_object(self)
        unit = self._temperature.unit
        if isinstance(value, tuple):
            unit = value[1]
            value = value[0]
        elif isinstance(value, prop.Temperature):
            unit = value.unit
            value = value.value
        self._temperature = prop.Temperature(value, unit)
        self._update_stream_object(self)

    @property
    def mass_flowrate(self):
        self = self._get_stream_object(self)
        return self._mass_flowrate
    @mass_flowrate.setter
    def mass_flowrate(self, value):
        self = self._get_stream_object(self)
        unit = self._mass_flowrate.unit
        if isinstance(value, tuple):
            unit = value[1]
            value = value[0]
        elif isinstance(value, prop.MassFlowRate):
            unit = value.unit
            value = value.value
        self._mass_flowrate = prop.MassFlowRate(value, unit)
        self._update_stream_object(self)

    @classmethod
    def list_objects(cls):
        return cls.items
    
    @classmethod
    def _update_stream_object(cls, object):
        if not isinstance(object, MaterialStream):
            raise Exception("Object type should be MaterialStream type. Type passed is ", type(object))
        try:
            cls.items[object.index] = object
        except:
            pass
    
    def _get_stream_index(cls, tag):
        for index, stream in enumerate(cls.items):
            if stream.tag == tag:
                return index
        return None
    def _get_stream_object(cls, obj):
        try:
            return cls.items[obj.index]
        except:
            return obj

    def __repr__(self) -> str:
        return 'Material Stream Tag: ' + self.tag
    
    def _create_stream_tag(cls):
        i = 1
        class_name = type(cls).__name__
        tag = class_name+ "_" + str(i)
        while cls._check_tag_assigned(tag):
            tag = class_name+ "_" + str(i)
            i += 1
        return tag
    @classmethod
    def _check_tag_assigned(cls, tag):
        for equipment in cls.items:
            if tag == equipment.tag:
                return True
        return False

#Get stream index function
def get_stream_index(tag, stream_type=None):
    if stream_type in ['energy', 'Energy', 'Power','e','E']:
        stream_list = EnergyStream.list_objects()
    elif stream_type in ['material', 'Material', 'mass', 'Mass','m','M']:
        stream_list = MaterialStream.list_objects()
    elif stream_type==None:
        return [(get_stream_index(tag, 'energy'),'Energy Stream'),(get_stream_index(tag, 'material'),'Material Stream')]
    else:
        raise Exception('Stream type does not exist! Please ensure stream type is either Energy or Material')
    list_of_none_tag_streams =[]

    for index, stream in enumerate(stream_list):
        if stream.tag == None and tag==None:
            list_of_none_tag_streams.append(index)           
        elif stream.tag == tag:
            return index
        
    if tag != None:
        raise Exception("Stream tag not found!!")

    return list_of_none_tag_streams

