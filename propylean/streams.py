from pandas import DataFrame
from thermo import Mixture
import propylean.properties as prop
class Stream(object):
   
    def __init__(self, tag=None, **inputs) -> None:
        self._tag = None
        self._to_equipment_tag = None
        self._from_equipment_tag = None
        self.tag = tag if tag is not None else self._create_stream_tag()

    @property
    def tag(self):
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
    
    @classmethod
    def _update_stream_object(cls, obj):
        if cls.__name__ != type(obj).__name__:
            raise Exception("Object type should be {} type. Type passed is {}".format(cls.__name__, type(obj).__name__))
        try:
            cls.items[obj.index] = obj
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

    def _create_stream_tag(cls):
        i = 1
        class_name = type(cls).__name__
        tag = class_name+ "_" + str(i)
        while cls._check_tag_assigned(tag):
            tag = class_name+ "_" + str(i)
            i += 1
        return tag
    
    def _check_tag_assigned(cls, tag):
        for equipment in cls.items:
            if tag == equipment.tag:
                return True
        return False
    
    def _tuple_property_value_unit_returner(self, value, property_type):
        if isinstance(value, tuple):
            return value[0], value[1]
        elif isinstance(value, property_type):
            return value.value, value.unit
        elif any([isinstance(value, float), isinstance(value, int)]):
            return value, None
        
class EnergyStream (Stream):
    items = [] 
    def __init__(self, tag=None, amount=(0, 'W')):
        super().__init__(tag)
        self._amount = prop.Power() 
        self.amount = amount
        EnergyStream.items.append(self)

    @property
    def amount(self):
        self = self._get_stream_object(self)
        return self._amount
    @amount.setter
    def amount(self, value):
        self = self._get_stream_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Power)
        if unit is None:
            unit = self.amount.unit
        self._amount = prop.Power(value, unit)
        self._update_stream_object(self)

    def __repr__(self) -> str:
        return 'Energy Stream Tag: ' + self.tag
    
    @classmethod
    def list_objects(cls):
        return cls.items
      
class MaterialStream(Stream):
    property_package = None
    items = [] 
    def __init__(self,tag = None,
                 mass_flowrate = 0,
                 pressure = 101325,
                 temperature = 298):
                 
                 super().__init__(tag)
                 self._index = len(MaterialStream.items)
                 self._mass_flowrate = prop.MassFlowRate()
                 self._pressure = prop.Pressure()
                 self._temperature = prop.Temperature()
                 
                 self.mass_flowrate = mass_flowrate
                 self.temperature = temperature
                 self.pressure = pressure
                 self._density = prop.Density()
                 self._density_l = prop.Density()
                 self._density_g = prop.Density()
                 self._density_s = prop.Density()
                 self._d_viscosity = prop.DViscosity()
                 self._d_viscosity_l = prop.DViscosity()
                 self._d_viscosity_g = prop.DViscosity()
                 self._components = prop.Components()

                 MaterialStream.items.append(self)
        
    @property
    def pressure(self):
        self = self._get_stream_object(self)
        return self._pressure
    @pressure.setter
    def pressure(self, value):
        self = self._get_stream_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Pressure)
        if unit is None:
            unit = self._pressure.unit
        self._pressure = prop.Pressure(value, unit)
        self._update_stream_object(self)

    @property
    def temperature(self):
        self = self._get_stream_object(self)
        return self._temperature
    @temperature.setter
    def temperature(self, value):
        self = self._get_stream_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Temperature)
        if unit is None:
            unit = self._temperature.unit
        self._temperature = prop.Temperature(value, unit)
        self._update_stream_object(self)

    @property
    def mass_flowrate(self):
        self = self._get_stream_object(self)
        return self._mass_flowrate
    @mass_flowrate.setter
    def mass_flowrate(self, value):
        self = self._get_stream_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.MassFlowRate)
        if unit is None:
            unit = self._mass_flowrate.unit
        self._mass_flowrate = prop.MassFlowRate(value, unit)
        self._update_stream_object(self)
    
    @property
    def vol_flowrate(self):
        self = self._get_stream_object(self)
        mass_flowrate = self.mass_flowrate
        density = self.density
        mass_flowrate.unit = 'kg/s'
        density.unit = 'kg/m^3'
        return prop.VolumetricFlowRate(mass_flowrate.value/density.value)
    
    @property
    def mol_flowrate(self):
        self = self._get_stream_object(self)
        mass_flowrate = self.mass_flowrate
        density = self.density
        mass_flowrate.unit = 'kg/s'
        density.unit = 'kg/m^3'
        return prop.VolumetricFlowRate(mass_flowrate.value/density.value)

    @property
    def components(self):
        self = self._get_stream_object(self)
        return self._components
    @components.setter
    def components(self, value):
        # if MaterialStream().property_package is None:
        #     raise Exception("Property package must be set before setting components.")
        # if not isinstance(value, DataFrame):
        #     raise Exception("Compnents should be pandas DataFrame")
        self = self._get_stream_object(self)
        self._components = value
        self._update_properties()
        self._update_stream_object(self)

    @property
    def density(self):
        self = self._get_stream_object(self)
        return self._density
    @density.setter
    def density(self, value):
        if MaterialStream().property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Density)
        if unit is None:
            unit = self._density.unit
        self._density = prop.Density(value, unit)
        self._update_stream_object(self)
    
    @property
    def density_l(self):
        self = self._get_stream_object(self)
        return self._density_l
    @density_l.setter
    def density_l(self, value):
        if MaterialStream().property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Density)
        if unit is None:
            unit = self._density_l.unit
        self._density_l = prop.Density(value, unit)
        self._update_stream_object(self)
    
    @property
    def density_g(self):
        self = self._get_stream_object(self)
        return self._density_g
    @density_g.setter
    def density_g(self, value):
        if MaterialStream().property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Density)
        if unit is None:
            unit = self._density_g.unit
        self._density_g = prop.Density(value, unit)
        self._update_stream_object(self)
    
    @property
    def density_s(self):
        self = self._get_stream_object(self)
        return self._density_s
    @density_s.setter
    def density_s(self, value):
        if MaterialStream().property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Density)
        if unit is None:
            unit = self._density_s.unit
        self._density_s = prop.Density(value, unit)
        self._update_stream_object(self)

    @property
    def d_viscosity(self):
        self = self._get_stream_object(self)
        return self._d_viscosity
    @d_viscosity.setter
    def d_viscosity(self, value):
        if MaterialStream().property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Density)
        if unit is None:
            unit = self._d_viscosity.unit
        self._d_viscosity = prop.DViscosity(value, unit)
        self._update_stream_object(self)
    
    @property
    def d_viscosity_l(self):
        self = self._get_stream_object(self)
        return self._d_viscosity_l
    @d_viscosity_l.setter
    def d_viscosity_l(self, value):
        if MaterialStream().property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Density)
        if unit is None:
            unit = self._density_l.unit
        self._d_viscosity_l = prop.DViscosity(value, unit)
        self._update_stream_object(self)
    
    @property
    def d_viscosity_g(self):
        self = self._get_stream_object(self)
        return self._d_viscosity_g
    @d_viscosity_g.setter
    def d_viscosity_g(self, value):
        if MaterialStream().property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Density)
        if unit is None:
            unit = self._d_viscosity_g.unit
        self._d_viscosity_g = prop.DViscosity(value, unit)
        self._update_stream_object(self)
    
    def _update_properties(self):
        if self.components.fractions is None:
            return
        arg_map = {'mass': 'ws',
                   'mol': 'zs',
                   'vol_l': 'Vfls',
                   'vol_g': 'Vfgs'}
        T = self.temperature
        T.unit = 'K'
        P = self.pressure
        P.unit = 'Pa'
        kwarg = {arg_map[self.components.type]: self.components.fractions,
                 'T': T.value,
                 'P': P.value}  
        mx = Mixture(**kwarg)
        rho = mx.rho
        rhol = mx.rhol
        rhog = mx.rhog
        rhos = mx.rhos
        if rho is not None:
            self.density = prop.Density(rho, 'kg/m^3')
        if rhol is not None:
            self.density_l = prop.Density(mx.rhol, 'kg/m^3')
        if rhog is not None:
            self.density_g = prop.Density(mx.rhog, 'kg/m^3')
        if rhos is not None:
            self.density_s = mx.rhoss

    @classmethod
    def list_objects(cls):
        return cls.items
    
    def __repr__(self) -> str:
        return 'Material Stream Tag: ' + self.tag

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

