from pyrsistent import v
from propylean.generic_equipment_classes import _PressureChangers, _EquipmentOneInletOutlet, _Vessels, _Exchangers
from thermo.chemical import Chemical
from fluids import control_valve as cv_calculations
import fluids.compressible as compressible_fluid 
from math import pi
from propylean import streams
import propylean.properties as prop

#Get equipment index function
def get_equipment_index(tag, equipment_type=None):
    """ 
    DESCRIPTION:
        Function to get equipment index based on equipment object created.
    
    PARAMETERS:
        tag:
            Required: Yes
            Type: str
            Acceptable values: Any string user has used for tag.
            Description: Reperesents the tag of equipment user want to know the index of. 
                         User need to make sure to provide exact tag. Fuzzy search will be provided
                         later.
        equipment_type:
            Required: No
            Type: str or equipment class type
            Acceptable values: string or type of equipment object.
            Default value: None
            Description: Reperesents the type of equipment user want to know the index of. 
                         User need to make sure to provide exact tag. Fuzzy search will be provided
                         later.
    
    RETURN VALUE:
        Type: int or list of tuple
        Description: When user knows and has provided equipment_type, returned value is int and search is faster.
                     If not provided, then list of tuple of the form [(1,'Centrifugal Pump'), (3,'Positive Displacement Pump')]
                     is returned with all possible outcomes. (1,'Centrifugal Pump') represents index and type of equipment.
    
    ERROR RAISED:
        Type: General
        Description: Error for invalid equipment type is raised.
    
    SAMPLE USE CASES:
        >>> get_equipment_index('1','centrifugal pump')
        1
        >>> get_equipment_index('1','pump')
        [(1,'Centrifugal Pump'), (3,'Positive Displacement Pump')]
    """
    
    #If equipment_type is known to the user
    if equipment_type in ['Centrifugal Pump', 'centrifugal pump', 'centrifugal pumps', 'Centrifugal Pumps', CentrifugalPump]:
        return _get_equipment_index_from_equipment_list(tag, CentrifugalPump.list_objects())
    elif equipment_type in ['Positive Displacement Pump', 'PD pumps', 'resiprocating pumps', 'positive displacement pump', PositiveDisplacementPump]:
        return _get_equipment_index_from_equipment_list(tag, PositiveDisplacementPump.list_objects())
    elif equipment_type in ['Centrifugal Compressor', 'centrifugal compressor', 'centrifugal compressors','Centrifugal COmpressors']:
        return _get_equipment_index_from_equipment_list(tag, CentrifugalCompressor.list_objects())
    elif equipment_type in ['Expander', 'expander','expanders','Expanders']:
        return _get_equipment_index_from_equipment_list(tag, Expander.list_objects())
    elif equipment_type in ['Pipe Segment', 'pipe segment', 'piping', 'pipe','Pipe','pipes','Pipes', PipeSegment]:
        return _get_equipment_index_from_equipment_list(tag, PipeSegment.list_objects())
    elif equipment_type in ['Control Value', 'cv', 'control valve', 'CV', 'control valves', 'Control Valves', ControlValve]:
        return _get_equipment_index_from_equipment_list(tag, ControlValve.list_objects())
    elif equipment_type in ['Pressure Safety Valve', 'PSV', 'psv', 'safety valves', 'PSVs', PressureSafetyValve]:
        return _get_equipment_index_from_equipment_list(tag, PressureSafetyValve.list_objects())
    elif equipment_type in ['Flow Meter', 'flow meter', 'Flow Meters', 'flow meters', FlowMeter]:
        return _get_equipment_index_from_equipment_list(tag, FlowMeter.list_objects())
    elif equipment_type in ['Vertical Separator', VerticalSeparator]:
        return _get_equipment_index_from_equipment_list(tag, VerticalSeparator.list_objects())
    elif equipment_type in ['Horizontal Separator', HorizontalSeparator]:
        return _get_equipment_index_from_equipment_list(tag, HorizontalSeparator.list_objects())
    elif equipment_type in ['Column', 'column', 'columns', 'Columns', Column]:
        return _get_equipment_index_from_equipment_list(tag, Column.list_objects())
    elif equipment_type in ['Tank', 'tank', 'Tanks', 'tanks', Tank]:
        return _get_equipment_index_from_equipment_list(tag, Tank.list_objects())
    elif equipment_type in ['Shell and Tube Heat exchanger', 'S&T HE', 'S&T Heat Exchanger', ShellnTubeExchanger] :
        return _get_equipment_index_from_equipment_list(tag, ShellnTubeExchanger.list_objects())
    elif equipment_type in ['Air Cooler', 'Air Coolers', 'air coolers', AirCooler]:
        return _get_equipment_index_from_equipment_list(tag, AirCooler.list_objects())
    
    #If user knows the general type of the equipment
    elif equipment_type in ['Pump', 'pump', 'Pumps', 'pumps']:
        return [(_get_equipment_index_from_equipment_list(tag, CentrifugalPump.list_objects()),'Centrifugal Pump'),
                (_get_equipment_index_from_equipment_list(tag, PositiveDisplacementPump.list_objects()),'Positive Displacement Pump')]

    elif equipment_type in ['vessel', 'vessels', 'Vessels', 'Vessel']:
        return [(_get_equipment_index_from_equipment_list(tag, VerticalSeparator.list_objects()),'Verticle Vessel'),
                (_get_equipment_index_from_equipment_list(tag, HorizontalSeparator.list_objects()),'Horizontal Separator'),
                (_get_equipment_index_from_equipment_list(tag, Column.list_objects()),'Column'),
                (_get_equipment_index_from_equipment_list(tag, Tank.list_objects()),'Tank')
                ]
    
    elif equipment_type in ['valve', 'Valve', 'instrument', 'Instrument']:
        return [(_get_equipment_index_from_equipment_list(tag, ControlValve.list_objects()),'Control Valve'),
                (_get_equipment_index_from_equipment_list(tag, PressureSafetyValve.list_objects()),'Pressure Safety Valve'),
                (_get_equipment_index_from_equipment_list(tag, FlowMeter.list_objects()),'Flow Meter')
                ]
    
    elif equipment_type in ['exchangers', 'Exchanger', 'heat exchanger', 'Heat Exchanger',
                            'Heat Exchangers', 'heat exchangers']:
        return  [(_get_equipment_index_from_equipment_list(tag, ShellnTubeExchanger.list_objects()),'Shell and Tube Exchanger'),
                (_get_equipment_index_from_equipment_list(tag, AirCooler.list_objects()),'Air Cooler')]
    
    # If the user does not know the type of equipment at all
    elif equipment_type == None:
        return (get_equipment_index(tag,'Pump') + 
                get_equipment_index(tag, 'vessel') +
                get_equipment_index(tag, 'valve') +
                get_equipment_index(tag, 'exchangers'))
    else:
        raise Exception('Invalid Equipment type!! Got'+ str(equipment_type)+ 
                           '''Valid equipment types are:
                            * Centrifugal Pump
                            * Positive Displacement Pump
                            * Pump if you don't remember the exact type
                            * Centrifugal Compressor
                            * Expander
                            * Pipe Segment
                            * Control Value or CV
                            * Pressure Safety Valve or PSV
                            * Flow Meter
                            * Instruments or Valves if you don't remember the exact type
                            * Vertical Separator
                            * Horizontal Separator
                            * Column
                            * Tank
                            * Vessels if you don't remember the exact type
                            * S&T Heat Exchanger
                            * Air Cooler
                            * Exchanger if you don't remember the exact type''')
    
def _get_equipment_index_from_equipment_list(tag, equipment_list):
    """ 
    DESCRIPTION:
        Internal function to get equipment index from equipment_list we know to search from.
    
    PARAMETERS:
        tag:
            Required: Yes
            Type: str
            Acceptable values: Any string user has used for tag.
            Description: Reperesents the tag of equipment user want to know the index of. 
                         User need to make sure to provide exact tag. Fuzzy search will be provided
                         later.
    
    RETURN VALUE:
        Type: int or list of int
        Description: Returned value is integer if tag is known and correct.
                     TODO: Remove none_tag searches 
    
    ERROR RAISED:
        Type: None
        Description:
    
    SAMPLE USE CASES:
        
    """
    list_of_none_tag_equipments =[]
    for index, equipment in enumerate(equipment_list):
        if equipment.tag == None and tag==None:
            list_of_none_tag_equipments.append(index)           
        elif equipment.tag == tag:
            return index

    return list_of_none_tag_equipments

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
        # delattr(self, self._outlet_energy_stream_tag)
        # delattr(self, self.energy_out)
        # delattr(self, self._energy_out)
        
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
        # TODO: Update
        density = 1000
        return self.inlet_pressure/(9.8 * density)

    @property
    def head(self):
        fluid_density = 1000 # TODO THIS NEEDS TO BE UPDATED WITH STREAM PROPERTY
        value = self.differential_pressure.value / (9.8 * fluid_density)
        return prop.Length(value, "m")
    @property
    def hydraulic_power(self):
        fluid_density = 1000 # TODO THIS NEEDS TO BE UPDATED WITH STREAM PROPERTY
        value = self.inlet_mass_flowrate.value * fluid_density * 9.81 * self.head.value / (3.6e6)
        return prop.Power(value, 'W')
    @property
    def power(self):
        value = self.hydraulic_power / self.efficiency
        return prop.Power(value, "W")
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

            polytropic_efficiency:
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
        # TODO Replace methane wih stream properties
        self.methane = Chemical('methane',
                         T = self._inlet_temperature.value,
                         P = self._inlet_pressure.value)
        if 'adiabatic_efficiency' not in inputs and 'polytropic_efficiency' in inputs:
            self.polytropic_efficiency = inputs['polytropic_efficiency']
        else:
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
        value, unit = self._tuple_property_value_unit_returner(value, prop.VolumetricFlowRate)
        if value ==  None:
            value = 0.7
        self._adiabatic_efficiency = value
        self._update_equipment_object(self)
    
    @property
    def polytropic_efficiency(self):
        self = self._get_equipment_object(self)
        return compressible_fluid.isentropic_efficiency(P1 = self._inlet_pressure.value,
                                                        P2 = self._outlet_pressure.value,
                                                        k = self.methane.isentropic_exponent,
                                                        eta_s = self.adiabatic_efficiency)
    @polytropic_efficiency.setter
    def polytropic_efficiency(self, value):
        self = self._get_equipment_object(self)
        self.adiabatic_efficiency = compressible_fluid.isentropic_efficiency(P1 = self._inlet_pressure.value,
                                                                             P2 = self._outlet_pressure.value,
                                                                             k = self.methane.isentropic_exponent,
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

# Start of final classes of Piping and Instruments
class PipeSegment(_EquipmentOneInletOutlet):
    items = []
    def __init__(self, **inputs) -> None:
        """ 
        DESCRIPTION:
            Final class for creating objects to represent a Pipe Segmenet.
        
        PARAMETERS:
            Read _EquipmentOneInletOutlet class for more arguments for this class
            ID:
                Required: Yes
                Type: int or float or property.Lenght(recommended)
                Acceptable values: Non-negative values
                Default value: None
                Description: Internal Diameter of the pipe segment.

            OD:
                Required: Yes
                Type: int or float or property.Lenght(recommended)
                Acceptable values: Non-negative values
                Default value: None
                Description: Outer Diameter of the pipe segment.
            
            Length:
                Required: Yes
                Type: int or float or property.Lenght(recommended)
                Acceptable values: Non-negative values
                Default value: None
                Description: Outer Diameter of the pipe segment.

            segment_type:
                Required: No
                Type: int
                Acceptable values: 1 to 13.
                Default value: 1
                Description: Segment type/fitting type of the pipe segment.
            
            material:
                Required: No
                Type: int
                Acceptable values: 1 to 5.
                Default value: 1
                Description: Material type of the pipe segment.
        
        RETURN VALUE:
            Type: PipeSegment
            Description: Returns an object of type PipeSegment with all properties of
                         a pipe segments and fittings used in process industry piping.
        
        ERROR RAISED:
            Type:
            Description:
        
        SAMPLE USE CASES:
            >>> PS_1 = PipeSegment(tag="P1")
            >>> print(PS_1)
            Pipe Segment with tag: P1
        """
        self._index = len(PipeSegment.items)
        super().__init__( **inputs)
        self._pressure_drop = prop.Pressure(0)
        self._ID = prop.Length()
        self._OD = prop.Length()
        self._length = prop.Length()
        self._segment_type = 1
        self._material = 1

        self.segment_type = 1 if 'segment_type' not in inputs else inputs['segment_type']
        
        if self.segment_type == 1:
            if 'length' in inputs:
                self.length = inputs['length']                
            else:
                raise Exception('Straight Tube segment requires length value')  
        
        if 'material' in inputs:
            self.material = inputs['material']
        
        if ('ID' in inputs):
            self.ID = inputs['ID']
        elif ('OD' in inputs and 'thickness' in inputs):
            self.OD = inputs['OD']
            self.thickness = inputs['thickness']
        else:
            raise Exception('Define atleast ID or OD with thickness to define a pipe segment object') 
        PipeSegment.items.append(self)
    
    def __repr__(self):
        return "Pipe Segment with tag: " + self.tag   #ADD SEGMENT TYPE!!
    def __hash__(self):
        return hash(self.__repr__())
    
    @property
    def length(self):
        self = self._get_equipment_object(self)
        return self._length
    @length.setter
    def length(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Length)
        if unit is None:
            unit = self._length.unit
        self._length = prop.Length(value, unit)
        self._update_equipment_object(self)

    @property
    def ID(self):
        self = self._get_equipment_object(self)
        return self._ID
    @ID.setter
    def ID(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Length)
        if unit is None:
            unit = self._ID.unit
        self._ID = prop.Length(value, unit)
        self._update_equipment_object(self)
    
    @property
    def OD(self):
        self = self._get_equipment_object(self)
        return self._OD
    @OD.setter
    def OD(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Length)
        if unit is None:
            unit = self._OD.unit
        self._OD =prop.Length(value, unit)
        self._update_equipment_object(self)
    
    @property
    def thickness(self):
        self = self._get_equipment_object(self)
        return self._OD - self._ID
    @thickness.setter
    def thickness(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value)
        if unit is None:
            unit = self.thickness
        self._OD = self._ID + prop.Length(value, unit)
        self._update_equipment_object(self)

    @property
    def segment_type(self):
        self = self._get_equipment_object(self)
        return self._segment_type
    @segment_type.setter
    def segment_type(self, value):
        self = self._get_equipment_object(self)
        segments = '''\nSegments can be of following types and in range of numbers below:
                    1. Straight Tube
                    2. Elbow
                    3. Tee
                    4. Angle valve
                    5. Butterfly valve
                    6. Ball valve
                    7. Gate valve
                    8. Globe valve
                    9. Swing check valve
                    10. Ball check valve
                    11. Lift check valve
                    12. Reducer
                    13. Expander'''
        if value not in range(1,14):
            raise Exception(segments)
        self._segment_type = value
        self._update_equipment_object(self)
    
    @property
    def material(self):
        self = self._get_equipment_object(self)
        return self._material
    @material.setter
    def material(self, value):
        self = self._get_equipment_object(self)
        materials = '''\nSegment material can be of following types and in range of numbers below:
                    1. Raw Steel
                    2. Carbon Steel
                    3. Cast Iron
                    4. Stainless Steel
                    5. PVC''' 
        if value not in range(1, 6):
            raise Exception(materials)
        self._material = value
        self._update_equipment_object(self)

    @property
    def pressure_drop(self):
        self = self._get_equipment_object(self)
        from fluids.friction import friction_factor
        from fluids.core import Reynolds, K_from_f, dP_from_K
        if self.inlet_mass_flowrate.value == 0:
            return prop.Pressure(0, self._inlet_pressure.unit)
        roughness = (4.57e-5, 4.5e-5, 0.000259, 1.5e-5, 1.5e-6) #in meters
        # TODO
        T = prop.Temperature(self.inlet_temperature.value,
                             self.inlet_temperature.unit)
        T.unit = 'K'
        P = prop.Pressure(self.inlet_pressure.value,
                          self.inlet_pressure.unit)
        P.unit = 'Pa'
        water = Chemical('water',
                         T = T.value,
                         P = P.value)
        ID = self.ID
        ID.unit = 'm'
        length = self.length
        length.unit = 'm'
        V=(self.inlet_mass_flowrate.value/water.rhol)/(pi* ID.value**2)/4
        Re = Reynolds(V=V,
                      D=ID.value, 
                      rho=water.rhol, 
                      mu=water.mul)
        fd = friction_factor(Re, eD=roughness[self.material-1]/ID.value)
        K = K_from_f(fd=fd, L=length.value, D=ID.value)        
        drop = round(dP_from_K(K, rho=1000, V=V),3)
        drop = prop.Pressure(drop, 'Pa')
        drop.unit = self._inlet_pressure.unit
        return drop
    @pressure_drop.setter
    def pressure_drop(self, value):
        raise Exception('''Cannot manually set pressure drop for PipeSegment!\n
                         Pressure drop depends on physical properties PipeSegment and Material flowing.''')
    
    @classmethod
    def list_objects(cls):
        return cls.items

class ControlValve(_EquipmentOneInletOutlet):
    items = []
    def __init__(self, **inputs) -> None:
        """ 
        DESCRIPTION:
            Final class for creating objects to represent a Control Valve.
        
        PARAMETERS:
            Read _EquipmentOneInletOutlet class for more arguments for this class
        
        RETURN VALUE:
            Type: ControlValve
            Description: Returns an object of type ControlValve with all properties of
                         a control valve used in process industry.
        
        ERROR RAISED:
            Type:
            Description:
        
        SAMPLE USE CASES:
            >>> CV_1 = ControlValve(tag="CV1")
            >>> print(CV_1)
            Contrl Valve with tag: CV1
        """
        self._index = len(ControlValve.items)
        super().__init__( **inputs)
        ControlValve.items.append(self)
    
    def __repr__(self):
        return "Control Valve with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @property
    def Kv(self):
        self = self._get_equipment_object(self)
        # TODO UPDATE BELOW BASED ON STREAMS
        water = Chemical('water',
                         T = self.inlet_temperature.value,
                         P = self._inlet_pressure.value)
        if water.phase == 'l':
            return cv_calculations.size_control_valve_l(water.rhol, water.Psat, water.Pc, water.mul,
                                                        self._inlet_pressure.value, self._outlet_pressure.value, 
                                                        self.inlet_mass_flowrate.value/water.rhol)
        elif water.phase == 'g':
            return cv_calculations.size_control_valve_g(T = self.inlet_temperature.value, 
                                                        MW = water.MW,
                                                        mu= 1.48712E-05, # water.mug,
                                                        gamma = water.isentropic_exponent, 
                                                        Z = water.Zg,
                                                        P1 = self._inlet_pressure.value, 
                                                        P2 = self._outlet_pressure.value, 
                                                        Q = self.inlet_mass_flowrate.value/water.rhog)
        else:
            raise Exception('Possibility of fluid solification inside the control valve')

    @classmethod
    def list_objects(cls):
        return cls.items
        
class PressureSafetyValve(_EquipmentOneInletOutlet):
    items = []
    def __init__(self, **inputs) -> None:  
        self._index = len(PressureSafetyValve.items)     
        super().__init__( **inputs)
        PressureSafetyValve.items.append(self)
    
    def __repr__(self):
        return "Pressure Safety Valve with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @classmethod
    def list_objects(cls):
        return cls.items

class FlowMeter(_EquipmentOneInletOutlet):
    items = []
    def __init__(self, **inputs) -> None:
        self._index = len(FlowMeter.items)
        super().__init__( **inputs)
        FlowMeter.items.append(self)

    def __repr__(self):
        return "Flow Meter with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @classmethod
    def list_objects(cls):
        return cls.items
# End of final classes of Piping and instruments

# Start of final classes of vessels
class VerticalSeparator(_Vessels):
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

class HorizontalSeparator(_Vessels):
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

class Column(_Vessels):
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

class Tank(_Vessels):
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
# End of final classes of vessels

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
        AirCooler.items.append(self)
    
    def __repr__(self):
        return "Air Cooler with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())
    
    @classmethod
    def list_objects(cls):
        return cls.items
# End of final classes of heat exchangers      