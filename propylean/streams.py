from thermo import Mixture
import propylean.properties as prop

class Stream(object):
   
    def __init__(self, tag=None, **inputs) -> None:
        self._tag = None
        self._to_equipment_tag = None
        self._from_equipment_tag = None
        self.tag = tag

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
        tag = class_name + "_" + str(i)
        while cls._check_tag_assigned(tag):
            tag = class_name+ "_" + str(i)
            i += 1
        return tag
    
    def _check_tag_assigned(cls, tag):
        for stream in cls.items:
            if tag == stream.tag:
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

                 self._vol_flowrate = prop.VolumetricFlowRate()
                 self._mol_flowrate = prop.MolarFlowRate()
                 self._molecular_weight = prop.MolecularWeigth()
                 self._Z_g = 1
                 self._Z_l = 0
                 self._isentropic_exponent = 1.3
                 self._phase = None
                 self._Psat = None
                 self._Pc = None

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
        old_mf_unit = self.mass_flowrate.unit
        density = self.density
        self.mass_flowrate.unit = 'kg/s'
        density.unit = 'kg/m^3'
        unit = self._vol_flowrate.unit
        self._vol_flowrate = prop.VolumetricFlowRate(self.mass_flowrate.value/density.value)
        self._vol_flowrate.unit = unit
        self.mass_flowrate.unit = old_mf_unit
        return self._vol_flowrate
    
    @property
    def molecular_weight(self):
        self = self._get_stream_object(self)
        return self._molecular_weight
    @molecular_weight.setter
    def molecular_weight(self, value):
        if MaterialStream.property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.MolecularWeigth)
        if unit is None:
            unit = self._molecular_weight.unit
        self._molecular_weight = prop.MolecularWeigth(value, unit)
        self._update_stream_object(self)

    @property
    def mol_flowrate(self):
        self = self._get_stream_object(self)
        old_mf_unit = self.mass_flowrate.unit
        old_mw_unit = self.molecular_weight.unit
        self.mass_flowrate.unit = 'kg/s'
        self.molecular_weight.unit = 'kg/mol'
        unit = self._mol_flowrate.unit
        self._mol_flowrate = prop.MolarFlowRate(self.mass_flowrate.value/self.molecular_weight.value)
        self._mol_flowrate.unit = unit
        self.mass_flowrate.unit = old_mf_unit
        self.molecular_weight.unit = old_mw_unit
        return self._mol_flowrate

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
        if MaterialStream.property_package:
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
        if MaterialStream.property_package:
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
        if MaterialStream.property_package:
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
        if MaterialStream.property_package:
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
        if MaterialStream.property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.DViscosity)
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
        if MaterialStream.property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.DViscosity)
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
        if MaterialStream.property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.DViscosity)
        if unit is None:
            unit = self._d_viscosity_g.unit
        self._d_viscosity_g = prop.DViscosity(value, unit)
        self._update_stream_object(self)
    
    @property
    def isentropic_exponent(self):
        self = self._get_stream_object(self)
        return self._isentropic_exponent
    @isentropic_exponent.setter
    def isentropic_exponent(self, value):
        if MaterialStream.property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        self._isentropic_exponent = value
        self._update_stream_object(self)

    @property
    def phase(self):
        self = self._get_stream_object(self)
        return self._phase
    @phase.setter
    def phase(self, value):
        if MaterialStream.property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        self._phase = value
        self._update_stream_object(self)
    
    @property
    def Psat(self):
        self = self._get_stream_object(self)
        return self._Psat
    @Psat.setter
    def Psat(self, value):
        if MaterialStream.property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        self._Psat = value
        self._update_stream_object(self)

    @property
    def Pc(self):
        self = self._get_stream_object(self)
        return self._Pc
    @Pc.setter
    def Pc(self, value):
        if MaterialStream.property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        self._Pc = value
        self._update_stream_object(self)
    
    @property
    def Z_g(self):
        self = self._get_stream_object(self)
        return self._Z_g
    @Z_g.setter
    def Z_g(self, value):
        if MaterialStream.property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        self._Z_g = value
        self._update_stream_object(self)
    
    @property
    def Z_l(self):
        self = self._get_stream_object(self)
        return self._Z_g
    @Z_l.setter
    def Z_l(self, value):
        if MaterialStream.property_package:
            raise Exception("Property cannot be changed when using a Property Package.")
        self = self._get_stream_object(self)
        self._Z_l = value
        self._update_stream_object(self)
    
    def _update_properties(self):
        if self.components.fractions is None:
            return
        arg_map = {'mass': 'ws',
                   'mol': 'zs',
                   'vol_l': 'Vfls',
                   'vol_g': 'Vfgs'}
        old_p_unit = self.pressure.unit 
        old_t_unit = self.temperature.unit
        self.pressure.unit = 'Pa'
        self.temperature.unit = 'K'
        kwarg = {arg_map[self.components.type]: self.components.fractions,
                 'T': self.temperature.value,
                 'P': self.pressure.value}  
        mx = Mixture(**kwarg)
        self.pressure.unit = old_p_unit
        self.temperature.unit = old_t_unit
        
        # Assigning Phase
        phase = mx.phase
        if phase is not None:
            self.phase = phase

        # Assigning Densities
        rho = mx.rho
        if rho is not None:
            self.density = prop.Density(rho, 'kg/m^3')
        
        rhol = mx.rhol
        if rhol is not None:
            self.density_l = prop.Density(rhol, 'kg/m^3')
    
        rhog = mx.rhog
        if rhog is not None:
            self.density_g = prop.Density(rhog, 'kg/m^3')

        # Assigning Viscosities
        mu = mx.mu
        if mu is not None:
            self.d_viscosity = prop.DViscosity(mu, 'Pa-s')
        
        mul = mx.mul
        if mul is not None:
            self.d_viscosity_l = prop.DViscosity(mul, 'Pa-s')
            
        mug = mx.mug       
        if mug is not None:
            self.d_viscosity_g = prop.DViscosity(mug, 'Pa-s')
        
        # Assigning Molecular Weight
        MW = mx.MW
        if MW is not None:
            self.molecular_weight = prop.MolecularWeigth(MW, 'g/mol')
        
        #Assiging Compressibility Factor Z
        Z = mx.Z
        if Z is not None:
            self.Z = Z
        
        Z_l = mx.Zl
        if Z_l is not None:
            self.Z_l = Z_l
        
        Z_g = mx.Zg
        if Z_g is not None:
            self.Z_g = Z_g
        
        # Assigning Isnetropic Exponent
        isentropic_exponent = mx.isentropic_exponent
        if isentropic_exponent is not None:
            self.isentropic_exponent = isentropic_exponent
        
        # Assiging Psat and Pc
        Psat_indiv = mx.Psats
        Psat = None
        if len(Psat_indiv)==1:
            Psat = Psat_indiv[0]
        else:
            import statistics
            Psat = statistics.fmean(Psat_indiv)
        if Psat is not None:
            self.Psat = Psat
        Pc = mx.Pc
        if Pc is not None:
            self.Pc = Pc

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

    for index, stream in enumerate(stream_list):        
        if stream.tag == tag:
            return index
    
    raise Exception("Stream tag not found!!")