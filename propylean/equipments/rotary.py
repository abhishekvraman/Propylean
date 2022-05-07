from propylean.generic_equipment_classes import _PressureChangers
from propylean import streams
import propylean.properties as prop
import fluids.compressible as compressible_fluid 

# Start of final classes of pumps.
class CentrifugalPump(_PressureChangers):
    items = []    
    def __init__(self, **inputs) -> None:
        """ 
        DESCRIPTION:
            Final class for creating objects to represent Centrifugal Pump.
        
        PARAMETERS:
            Read _PressureChangers class for more arguments for this class
            min_flow:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Non-negative values
                Default value: None
                Description: Minimum flow requirement of the pump

            NPSHr:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Non-negative values
                Default value: None
                Description: NPSHr of the pump
        
        RETURN VALUE:
            Type: CentrifugalPump
            Description: Returns an object of type CentrifugalPump with all properties of
                         a centrifugal pump used in process industries.
        
        ERROR RAISED:
            Type:
            Description:
        
        SAMPLE USE CASES:
            >>> pump_1 = CentrifugalPump(tag="P1")
            >>> print(pump_1)
            Centrifugal Pump with tag: P1
        """
        self._index = len(CentrifugalPump.items)
        super().__init__( **inputs)
        self._NPSHr = prop.Length()
        self._NPSHa = prop.Length()
        self._min_flow = prop.VolumetricFlowRate()
        del self.energy_out
        
        if 'min_flow' in inputs:
            self.min_flow = inputs['min_flow']
        if "NPSHr" in inputs:
            self.NPSHr = inputs['NPSHr']
    
        CentrifugalPump.items.append(self)
    
    def __repr__(self):
        return "Centrifugal Pump with tag: " + self.tag
    def __hash__(self):
        return hash(self.__repr__())

    @property
    def min_flow(self):
        self = self._get_equipment_object(self)
        return self._min_flow
    @min_flow.setter
    def min_flow(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.VolumetricFlowRate)
        if unit is None:
            unit = self._min_flow.unit
        self._min_flow = prop.VolumetricFlowRate(value, unit)
        self._update_equipment_object(self)

    @property
    def NPSHr(self):
        self = self._get_equipment_object(self)
        return self._NPSHr
    @NPSHr.setter
    def NPSHr(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Pressure)
        if unit is None:
            unit = self._NPSHr.unit
        self._NPSHr = prop.Length(value, unit)
        self._update_equipment_object(self)
    
    @property
    def NPSHa(self):
        self = self._get_equipment_object(self)
        if self._inlet_material_stream_tag is None:
            raise Exception("Pump should be connected with MaterialStream at the inlet")
        stream_index = streams.get_stream_index(self._inlet_material_stream_tag, "material")
        density = self._stream_object_property_getter(stream_index, "material", "density")
        density.unit = "kg/m^3"
        old_p_unit = self.inlet_pressure.unit
        self.inlet_pressure.unit = 'Pa'
        value = self.inlet_pressure.value/(9.8 * density.value)
        self.inlet_pressure.unit = old_p_unit
        return prop.Length(value, "m")

    @property
    def head(self):
        self = self._get_equipment_object(self)
        if (self._outlet_material_stream_tag is None and
            self._inlet_material_stream_tag is None):
            raise Exception("Pump should be connected with MaterialStream either at inlet or outlet")
        stream_tag = self._inlet_material_stream_tag if self._outlet_material_stream_tag is None else self._outlet_material_stream_tag
        stream_index = streams.get_stream_index(stream_tag, "material")
        density = self._stream_object_property_getter(stream_index, "material", "density")
        density.unit = "kg/m^3"
        dp = self.differential_pressure
        dp.unit = "Pa"
        value = dp.value / (9.8 * density.value)
        return prop.Length(value, "m")
    @property
    def hydraulic_power(self):
        self = self._get_equipment_object(self)
        if (self._outlet_material_stream_tag is None and
            self._inlet_material_stream_tag is None):
            raise Exception("Centrifugal Pump should be connected with MaterialStream either at inlet or outlet")
        stream_tag = self._inlet_material_stream_tag if self._outlet_material_stream_tag is None else self._outlet_material_stream_tag
        stream_index = streams.get_stream_index(stream_tag, "material")
        vol_flowrate = self._stream_object_property_getter(stream_index, "material", "vol_flowrate")
        vol_flowrate.unit = "m^3/h"
        dp = self.differential_pressure
        dp.unit = "Pa"
        value = vol_flowrate.value * dp.value / (3.6e3)
        return prop.Power(value, 'W')
    @property
    def power(self):
        self = self._get_equipment_object(self)
        self.hydraulic_power.unit = "W"
        value = self.hydraulic_power.value / self.efficiency
        return prop.Power(value, "W")
    @power.setter
    def power(self, value):
        #TODO Proived setting feature for power
        raise Exception("Pump power value setting is not yet supported. Modify differential pressure to get required power.")
    @property
    def energy_in(self):
        return self.power
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

class PositiveDisplacementPump(_PressureChangers):
    items = []
    def __init__(self, **inputs) -> None:
        """ 
        DESCRIPTION:
            Final class for creating objects to represent a Positive Displacement Pump.
        
        PARAMETERS:
            Read _PressureChangers class for more arguments for this class
            XYZ: TODO
                Required: No
                Type: int or float (recommended)
                Acceptable values: Non-negative values
                Default value: None
                Description: XYZ
        
        RETURN VALUE:
            Type: PositiveDisplacementPump
            Description: Returns an object of type PositiveDisplacementPump with all properties of
                         a positive displacement pump used in process industries.
        
        ERROR RAISED:
            Type:
            Description:
        
        SAMPLE USE CASES:
            >>> pump_1 = PositiveDisplacementlPump(tag="P1")
            >>> print(pump_1)
            Positive Displacement Pump with tag: P1
        """
        self._index = len(PositiveDisplacementPump.items)
        super().__init__( **inputs)
        PositiveDisplacementPump.items.append(self)
    
    def __repr__(self):
        return "Positive Displacement Pump with tag: " + self.tag
    def __hash__(self):
        return hash(self.__repr__())
    
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
# End of final classes of pumps

# Start of final classes of Compressors and Expanders.
class CentrifugalCompressor(_PressureChangers):
    items = []
    def __init__(self, **inputs) -> None:
        """ 
        DESCRIPTION:
            Final class for creating objects to represent a Centrifugal Compressors.
        
        PARAMETERS:
            Read _PressureChangers class for more arguments for this class
            adiabatic_efficiency:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Non-negative values
                Default value: None
                Description: Adiabatic Efficiency of the compressor
        
        RETURN VALUE:
            Type: CentrifugalCompressor
            Description: Returns an object of type CentrifugalCompressor with all properties of
                         a Centrifugal Compressor used in process industries.
        
        ERROR RAISED:
            Type:
            Description:
        
        SAMPLE USE CASES:
            >>> CC_1 = CentrifugalCompressor(tag="P1")
            >>> print(CC_1)
            Centrifugal Compressor with tag: P1
        """
        self._index = len(CentrifugalCompressor.items)
        super().__init__( **inputs)
        self.adiabatic_efficiency = 0.7 if 'adiabatic_efficiency' not in inputs else inputs['adiabatic_efficiency']
        CentrifugalCompressor.items.append(self)
    
    def __repr__(self):
        return "Centrifugal Compressor with tag: " + self.tag
    def __hash__(self):
        return hash(self.__repr__())

    @property
    def adiabatic_efficiency(self):
        self = self._get_equipment_object(self)
        return self._adiabatic_efficiency
    @adiabatic_efficiency.setter
    def adiabatic_efficiency(self, value):
        self = self._get_equipment_object(self)
        if value ==  None:
            value = 0.7
        self._adiabatic_efficiency = value
        self._update_equipment_object(self)
    
    @property
    def polytropic_efficiency(self):
        self = self._get_equipment_object(self)
        stream_tag = self._inlet_material_stream_tag if self._outlet_material_stream_tag is None else self._outlet_material_stream_tag
        stream_index = streams.get_stream_index(stream_tag, "material")
        isentropic_exponent = self._stream_object_property_getter(stream_index, "material", "isentropic_exponent")
        return compressible_fluid.isentropic_efficiency(P1 = self._inlet_pressure.value,
                                                        P2 = self._outlet_pressure.value,
                                                        k = isentropic_exponent,
                                                        eta_s = self.adiabatic_efficiency)
    @polytropic_efficiency.setter
    def polytropic_efficiency(self, value):
        self = self._get_equipment_object(self)
        stream_tag = self._inlet_material_stream_tag if self._outlet_material_stream_tag is None else self._outlet_material_stream_tag
        stream_index = streams.get_stream_index(stream_tag, "material")
        isentropic_exponent = self._stream_object_property_getter(stream_index, "material", "isentropic_exponent")
        self.adiabatic_efficiency = compressible_fluid.isentropic_efficiency(P1 = self._inlet_pressure.value,
                                                                             P2 = self._outlet_pressure.value,
                                                                             k = isentropic_exponent,
                                                                             eta_p = value)
        self._update_equipment_object(self)

    @property
    def power(self):
        self = self._get_equipment_object(self)
        work = compressible_fluid.isentropic_work_compression(T1 = self.inlet_temperature.value,
                                                              k = self.methane.isentropic_exponent,
                                                              Z = self.methane.Z,
                                                              P1 = self._inlet_pressure.value,
                                                              P2 = self._outlet_pressure.value,
                                                              eta = self.adiabatic_efficiency)
        return work * self.inlet_mass_flowrate.value / self.methane.MW
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

class Expander(_PressureChangers):
    items = []
    def __init__(self, **inputs) -> None:
        self._index = len(Expander.items)
        super().__init__( **inputs)
        Expander.items.append(self)
    
    def __repr__(self):
        return "Expander with tag: " + self.tag
    def __hash__(self):
        return hash(self.__repr__())
    
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
            direction = 'out'
        return super().connect_stream(direction=direction, 
                                      stream_object=stream_object, 
                                      stream_tag=stream_tag, 
                                      stream_type=stream_type,
                                      stream_governed=stream_governed)
    
    def disconnect_stream(self, stream_object=None, direction=None, stream_tag=None, stream_type=None):
        if ((stream_object is not None and 
            isinstance(stream_object, streams.EnergyStream)) or
            stream_type in ['energy', 'power', 'e', 'p']):
            direction = 'out'
        return super().disconnect_stream(stream_object, direction, stream_tag, stream_type)

# End of final classes of compressors