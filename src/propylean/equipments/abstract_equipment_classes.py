import propylean.properties as prop
from propylean import streams
from propylean.validators import _Validators
import warnings

global _material_stream_equipment_map
_material_stream_equipment_map = dict()
global _energy_stream_equipment_map
_energy_stream_equipment_map = dict()

# Defining generic base class for all equipments with one inlet and outlet.
class _EquipmentOneInletOutlet(object):
    items = []
    def __init__(self, **inputs) -> None:
        """ 
        DESCRIPTION:
            Internal base class to define an equipment with one inlet and outlet.
            All final classes inherits from this base class.
            Read individual final classed for further description.
    
        PARAMETERS:
            tag:
                Required: No
                Type: str
                Acceptable values: Any string type
                Default value: None
                Description: Equipment tag the user wants to provide. If not provided, then tag is automatically generated.

            pressure_drop:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Any
                Default value: None
                Description: Represents pressure drop the equipment. Negative value implies pressure increase.
            

        RETURN VALUE:
            Type: _EquipmentOneInletOutlet
            Description: Object of type _EquipmentOneInletOutlet
        
        ERROR RAISED:
            Type: Various
            Description: 
        
        SAMPLE USE CASES:
            >>> class NewEquipment(_EquipmentOneInletOutlet):
                ......
        """
        self.tag = inputs.pop('tag', self._create_equipment_tag())

        #Flow properties
        self._inlet_mass_flowrate = prop.MassFlowRate() 
        self._outlet_mass_flowrate = prop.MassFlowRate()
        self._inventory_change_rate = prop.MassFlowRate()
        self.design_flowrate = prop.MassFlowRate()

        #Pressure properties
        self._pressure_drop = prop.Pressure(0)
        self._inlet_pressure = prop.Pressure()
        self._outlet_pressure = prop.Pressure()
        self._design_pressure = prop.Pressure()
        
        #Temperature properties
        self._temperature_increase = prop.Temperature(0, 'K')
        self._inlet_temperature = prop.Temperature()
        self._outlet_temperature = prop.Temperature()
        self._design_temperature = prop.Temperature()

        #Inlet and outlet material and energy streams
        self._inlet_material_stream_tag = None
        self._outlet_material_stream_tag = None
        self._inlet_energy_stream_tag = None
        self._outlet_energy_stream_tag = None
        self._inlet_material_stream_index = None
        self._outlet_material_stream_index = None
        self._inlet_energy_stream_index = None
        self._outlet_energy_stream_index = None
        
        #Energy properties
        self._energy_in = prop.Power()
        self._energy_out = prop.Power()

        #Other Porperties
        self.main_fluid = "liquid" if "main_fluid" not in inputs else inputs["main_fluid"]
        self._is_disconnection = False

        if 'pressure_drop' in inputs:
            self.pressure_drop = inputs['pressure_drop']
    
    @property
    def index(self):
      return self._index

    @property
    def tag(self):
        return self._tag
    @tag.setter
    def tag(self, value):
        _Validators.validate_arg_prop_value_type("tag", value, (str))
        if self._check_tag_assigned(value):
            msg = "Tag '{}' already assigned!".format(value)
            raise Exception(msg)
        else:
            self._tag = value

    @property
    def inlet_pressure(self):
        self = self._get_equipment_object(self)
        return self._inlet_pressure
    @inlet_pressure.setter
    def inlet_pressure(self, value):
        _Validators.validate_arg_prop_value_type("inlet_pressure", value, (prop.Pressure, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Pressure)
        if unit is None:
            unit = self._inlet_pressure.unit
        self._inlet_pressure = prop.Pressure(value, unit)
        self._outlet_pressure = self._inlet_pressure - self.pressure_drop
        self._update_equipment_object(self)
    
    @property
    def outlet_pressure(self):
        self = self._get_equipment_object(self)
        return self._outlet_pressure
    @outlet_pressure.setter
    def outlet_pressure(self, value):
        _Validators.validate_arg_prop_value_type("outlet_pressure", value, (prop.Pressure, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Pressure)
        if unit is None:
            unit = self._outlet_pressure.unit
        self._outlet_pressure = prop.Pressure(value, unit)
        self._inlet_pressure = self._outlet_pressure + self.pressure_drop
        self._update_equipment_object(self)
    
    @property
    def pressure_drop(self):
        self = self._get_equipment_object(self)
        return self._pressure_drop
    @pressure_drop.setter
    def pressure_drop(self, value):
        _Validators.validate_arg_prop_value_type("pressure_drop", value, (prop.Pressure, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Pressure)
        if unit is None:
            unit = self._pressure_drop.unit
        self._pressure_drop = prop.Pressure(value, unit)
        self._outlet_pressure =  self._inlet_pressure - self._pressure_drop
        self._update_equipment_object(self)
    
    @property
    def design_pressure(self):
        self = self._get_equipment_object(self)
        return self._design_pressure
    @design_pressure.setter
    def design_pressure(self, value):
        _Validators.validate_arg_prop_value_type("design_pressure", value, (prop.Pressure, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Pressure)
        if unit is None:
            unit = self._design_pressure.unit
        self._design_pressure = prop.Pressure(value, unit)
        self._update_equipment_object(self)

    @property
    def inlet_temperature(self):
        self = self._get_equipment_object(self)
        return self._inlet_temperature
    @inlet_temperature.setter
    def inlet_temperature(self, value):
        _Validators.validate_arg_prop_value_type("inlet_temperature", value, (prop.Temperature, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Temperature)
        if unit is None:
            unit = self._inlet_temperature.unit
        self._inlet_temperature = prop.Temperature(value, unit)
        self._outlet_temperature = self._inlet_temperature + self.temperature_increase
        self._update_equipment_object(self)

    @property
    def outlet_temperature(self):
        self = self._get_equipment_object(self)
        return self._outlet_temperature
    @outlet_temperature.setter
    def outlet_temperature(self,value):
        _Validators.validate_arg_prop_value_type("outlet_temperature", value, (prop.Temperature, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Temperature)
        if unit is None:
            unit = self._outlet_temperature.unit
        self._outlet_temperature = prop.Temperature(value, unit)
        self._inlet_temperature = self._outlet_temperature - self.temperature_increase
        self._update_equipment_object(self)

    @property
    def temperature_increase(self):
        self = self._get_equipment_object(self)
        return self._temperature_increase
    @temperature_increase.setter
    def temperature_increase(self, value):
        _Validators.validate_arg_prop_value_type("temperature_increase", value, (prop.Temperature, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Temperature)
        if unit is None:
            unit = self._temperature_increase.unit
        self._temperature_increase = prop.Temperature(value, unit)
        self._outlet_temperature =  self._inlet_temperature + self._temperature_increase
        self._update_equipment_object(self)
    @property
    def temperature_decrease(self):
        self = self._get_equipment_object(self)
        decrease = -1 * self._temperature_increase.value
        return prop.Temperature(decrease, self._temperature_increase.unit)
    @temperature_decrease.setter
    def temperature_decrease(self, value):
        _Validators.validate_arg_prop_value_type("temperature_decrease", value, (prop.Temperature, int, float, tuple))
        if isinstance(value, prop.Temperature):
            value = prop.Temperature(-1 * value.value, value.unit)
        elif isinstance(value, tuple):
            value = prop.Temperature(-1 * value[0], value[1])
        elif isinstance(value, (int, float)):
            value = prop.Temperature(-1 * value, self._temperature_increase.unit)
        self.temperature_increase = value
    
    @property
    def design_temperature(self):
        self = self._get_equipment_object(self)
        return self._design_pressure
    @design_temperature.setter
    def design_temperature(self, value):
        _Validators.validate_arg_prop_value_type("design_temperature", value, (prop.Temperature, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Temperature)
        if unit is None:
            unit = self._design_temperature.unit
        self._design_temperature = prop.Temperature(value, unit)
        self._update_equipment_object(self)

    @property
    def inlet_mass_flowrate(self):
        self = self._get_equipment_object(self)
        return self._inlet_mass_flowrate
    @inlet_mass_flowrate.setter
    def inlet_mass_flowrate(self, value):
        _Validators.validate_arg_prop_value_type("inlet_mass_flowrate", value, (prop.MassFlowRate, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.MassFlowRate)
        if unit is None:
            unit = self._inlet_mass_flowrate.unit
        self._inlet_mass_flowrate = prop.MassFlowRate(value, unit)
        self._outlet_mass_flowrate = self._inlet_mass_flowrate + self.inventory_change_rate
        self._update_equipment_object(self)
    
    @property
    def outlet_mass_flowrate(self):
        self = self._get_equipment_object(self)
        return self._outlet_mass_flowrate
    @outlet_mass_flowrate.setter
    def outlet_mass_flowrate(self, value):
        _Validators.validate_arg_prop_value_type("outlet_mass_flowrate", value, (prop.MassFlowRate, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.MassFlowRate)
        if unit is None:
            unit = self._outlet_mass_flowrate.unit
        self._outlet_mass_flowrate = prop.MassFlowRate(value, unit)
        self._inlet_mass_flowrate = self._outlet_mass_flowrate - self.inventory_change_rate
        self._update_equipment_object(self)
    
    @property
    def inventory_change_rate(self):
        self = self._get_equipment_object(self)
        return self._inventory_change_rate
    @inventory_change_rate.setter
    def inventory_change_rate(self, value):
        _Validators.validate_arg_prop_value_type("inventory_change_rate", value, (int, float, prop.MassFlowRate))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.MassFlowRate)
        if unit is None:
            unit = self.inventory_change_rate.unit
        self._update_equipment_object(self)
    
    @property
    def energy_in(self):
        self = self._get_equipment_object(self)
        return self._energy_in
    @energy_in.setter
    def energy_in(self, value):
        _Validators.validate_arg_prop_value_type("energy_in", value, (prop.Power, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Power)
        if unit is None:
            unit = self.energy_in.unit
        self._energy_in = prop.Power(value, unit)
        self._update_equipment_object(self)
    @energy_in.deleter
    def energy_in(self):
        self = self._get_equipment_object(self)
        del self._energy_in
        self._update_equipment_object(self)

    @property
    def energy_out(self):
        self = self._get_equipment_object(self)
        return self._energy_out
    @energy_out.setter
    def energy_out(self, value):
        _Validators.validate_arg_prop_value_type("energy_out", value, (prop.Power, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Power)
        if unit is None:
            unit = self.energy_out.unit
        self._energy_in = prop.Power(value, unit)
        self._update_equipment_object(self)
    @energy_out.deleter
    def energy_out(self):
        self = self._get_equipment_object(self)
        del self._energy_out
        self._update_equipment_object(self) 
    
    def _get_equipment_index(cls, tag):
        for index, equipment in enumerate(cls.items):
            if equipment.tag == tag:
                return index
        return None
    
    @classmethod
    def _get_equipment_object(cls, obj):
        try:
            return cls.items[obj.index]
        except IndexError:
            raise Exception("Equipment does not exist!")
        except AttributeError:
            return obj
    
    @classmethod
    def _update_equipment_object(cls, obj):
        _Validators.validate_arg_prop_value_type("obj", obj, cls)
        try:
            cls.items[obj.index] = obj
        except:
            pass
    
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.tag == other.tag
        else:
            return False

    def get_stream_tag(self, stream_type, direction):
        """ 
        DESCRIPTION:
            Method to tsg ogf stream connected to the equipment using steam 
            type and the direction.
        
        PARAMETERS:
            stream_type:
                Required: Yes
                Type: str
                Acceptable values: 'm', 'mass', 'e', 'energy'
                Description: Type of stream user wants to get tag of.
            direction:
                Required: Yes
                Type: str
                Acceptable values: 'in', 'out', 'inlet' or 'outlet'
                Description: Direction of stream with respect to equipment user wants to get tag of.
       
        RETURN VALUE:
            Type: str
            Description: Tag value of stream user has assigned to the stream
        
        ERROR RAISED:
            Type: General TODO
            Description: Raises error if arguments are incorrect
        
        SAMPLE USE CASES:
            >>> eq1.get_stream_tag('m', 'out')
            >>> eq1.get_stream_tag('energy', 'in')
        """
        _Validators.validate_arg_prop_value_type("stream_type", stream_type, (str))
        _Validators.validate_arg_prop_value_list("stream_type", stream_type, ['m', 'mass', 'e', 'energy', 'material'])
        _Validators.validate_arg_prop_value_type("direction", direction, (str))
        _Validators.validate_arg_prop_value_list("direction", direction, ['in', 'out', 'inlet', 'outlet'])

        if stream_type.lower() in ['material', 'mass', 'm']:
            stream_tag = [self._inlet_material_stream_tag, self._outlet_material_stream_tag]
        elif stream_type.lower() in ['energy', 'power', 'e', 'p']:
            stream_tag = [self._inlet_energy_stream_tag, self._outlet_energy_stream_tag]
        else:
            raise Exception('Incorrect stream_type specified! Provided \"'+stream_type+'\". Can only be "material/mass/m" or "energy/e/power/p"]')
        
        if direction.lower() in ['in', 'inlet']:
                return stream_tag[0]
        elif direction.lower() in ['out', 'outlet']:
            return stream_tag[1]
        else:
            raise Exception('Incorrect direction specified! Provided \"'+direction+'\". Can only be ["in", "out", "inlet", "outlet"]')

    def connect_stream(self,
                       stream_object=None,
                       direction=None, 
                       stream_tag=None,
                       stream_type=None,
                       stream_governed=True):
        """ 
        DESCRIPTION:
            Method to connect a stream object with equiment.
        
        PARAMETERS:
            stream_object:
                Required: No if stream_tag is provided else Yes
                Type: EnergyStream or MaterialStream
                Acceptable values: object of specified stream types
                Default value: None
                Description: Stream object user wants to connect the equipment with.
            
            direction:
                Required: Yes for material stream. For energy stream not needed
                Type: str
                Acceptable values: 'in', 'out', 'inlet' or 'outlet'
                Default value: None
                Description: Direction in which stream should be with respect to equipment.
            
            stream_tag:
                Required: No if stream_object is provided else Yes
                Type: str
                Acceptable values: stream tag provided by user
                Default value: None
                Description: Stream object with known stream_tag user wants to connect the equipment with.

            stream_type:
                Required: No if stream_object provided
                Type: str
                Acceptable values: 'm', 'mass', 'e', 'energy'
                Description: Type of stream user wants to connect.

            stream_governed:
                Required: No 
                Type: bool
                Default values: True
                Description: Determines if stream will govern the property. Fluid property will be passed.    

        RETURN VALUE:
            Type: bool
            Description: True is returned if connection is successful else False
        
        ERROR RAISED:
            Type: General
            Description: Error raised if arguments are wrong
        
        SAMPLE USE CASES:
            >>> eq1.connect_stream(en1)
            >>> eq1.connect_stream(direction='out', stream_tag='Pump-outlet', stream_type='m')
        """
        if stream_object is not None:
            _Validators.validate_arg_prop_value_type("stream_object", stream_object, (streams.MaterialStream, streams.EnergyStream))
            _Validators.validate_arg_prop_value_type("direction", direction, str)
            _Validators.validate_arg_prop_value_type("stream_governed", stream_governed, bool)
            _Validators.validate_arg_prop_value_list("direction", direction, ['in', 'out', 'inlet', 'outlet'])
            if not (isinstance(stream_object, streams.EnergyStream) or
                    isinstance(stream_object, streams.MaterialStream)):
                    raise Exception("Stream object should be of type EnergyStream or Material Stream not " +
                                    type(stream_object))
            stream_tag = stream_object.tag
            if isinstance(stream_object, streams.MaterialStream):
                stream_type = 'm'
            elif isinstance(stream_object, streams.EnergyStream):
                stream_type = 'e'
        elif not self._is_disconnection and stream_tag is None:
            raise Exception("Either of Stream Object or Stream Tag is required for connection!")
        else:
            _Validators.validate_arg_prop_value_type("stream_tag", stream_tag, str)
            _Validators.validate_arg_prop_value_type("direction", direction, str)
            _Validators.validate_arg_prop_value_list("direction", direction, ['in', 'out', 'inlet', 'outlet'])
            _Validators.validate_arg_prop_value_type("stream_type", stream_type, str)
            _Validators.validate_arg_prop_value_list("stream_type", stream_type, ['m', 'mass', 'e', 'energy', 'material'])
            _Validators.validate_arg_prop_value_type("stream_governed", stream_governed, bool)
        
        stream_index = streams.get_stream_index(stream_tag, stream_type)
        is_inlet = True if direction.lower() in ['in', 'inlet'] else False

        mapping_result = self._stream_equipment_mapper(stream_index, stream_type, is_inlet)
        if self._is_disconnection:
            stream_tag = stream_index = None
            
        if stream_type.lower() in ['material', 'mass', 'm']:
            if direction.lower() in ['in', 'inlet']:
                self._inlet_material_stream_tag = stream_tag
                self._inlet_material_stream_index = stream_index
            else:
                self._outlet_material_stream_tag = stream_tag
                self._outlet_material_stream_index = stream_index
        else:
            if direction.lower() in ['in', 'inlet']:
                self._inlet_energy_stream_tag = stream_tag
                self._inlet_energy_stream_index = stream_index
            else:
                self._outlet_energy_stream_tag = stream_tag
                self._outlet_energy_stream_index = stream_index
        
        if mapping_result and not self._is_disconnection:
            self._stream_equipment_properties_matcher(stream_index, 
                                                      stream_type,
                                                      is_inlet,
                                                      stream_governed)
        return mapping_result

    def disconnect_stream(self, 
                          stream_object=None,
                          direction=None, 
                          stream_tag=None,
                          stream_type=None):
        """ 
        DESCRIPTION:
            Class method to disconnect a stream object from equiment.
        
        PARAMETERS:
            stream_object:
                Required: No if stream_tag is provided else Yes
                Type: EnergyStream or MaterialStream
                Acceptable values: object of specified stream types
                Default value: None
                Description: Stream object user wants to disconnect the equipment with.
            
            direction:
                Required: Yes if stream_object or stream_tag not provided
                Type: str
                Acceptable values: 'in', 'out', 'inlet' or 'outlet'
                Default value: None
                Description: Direction in which stream should be with respect to equipment.
            
            stream_tag:
                Required: No if stream_object is provided else Yes
                Type: str
                Acceptable values: stream tag provided by user
                Default value: None
                Description: Stream object with known stream_tag user wants to disconnect the equipment from.

            stream_type:
                Required: No if stream_object provided
                Type: str
                Acceptable values: 'm', 'mass', 'e', 'energy'
                Description: Type of stream user wants to disconnect.

        RETURN VALUE:
            Type: bool
            Description: True is returned if disconnection is successful else False
        
        ERROR RAISED:
            Type: General
            Description: Error raised if arguments are wrong
        
        SAMPLE USE CASES:
            >>> eq1.disconnect_stream(s1)
            >>> eq1.disconnect_stream(stream_tag='Pump-outlet')
            >>> eq1.disconnect_stream(direction='in', stream_type="energy")
        """
               
        def define_index_direction(tag):
            " This function is internal function. Not to be used elsewhere."
            stream_type = None
            direction = None
            if tag == self._inlet_material_stream_tag:
                stream_type = "m"
                direction = "in"
            elif tag == self._outlet_material_stream_tag:
                stream_type = "m"
                direction = "out"
            elif tag == self._inlet_energy_stream_tag:
                stream_type = "e"
                direction = "in"
            elif tag == self._outlet_energy_stream_tag:
                stream_type = "e"
                direction = "out"
            return stream_type, direction

        if stream_object is not None:
            _Validators.validate_arg_prop_value_type("stream_object", stream_object, (streams.MaterialStream, streams.EnergyStream))
            stream_type, direction = define_index_direction(stream_object.tag)
        elif stream_tag is not None:
            _Validators.validate_arg_prop_value_type("stream_tag", stream_tag, (str))
            stream_type, direction = define_index_direction(stream_tag)
        elif (direction is not None and 
              stream_type is not None):
              _Validators.validate_arg_prop_value_type("direction", direction, (str))
              _Validators.validate_arg_prop_value_type("stream_type", stream_type, (str))
              _Validators.validate_arg_prop_value_list("direction", direction, ['in', 'out', 'inlet', 'outlet'])
              _Validators.validate_arg_prop_value_list("stream_type", stream_type, ['m', 'mass', 'e', 'energy', 'material'])
              stream_tag = self.get_stream_tag(stream_type, direction)
              stream_type, direction = define_index_direction(stream_tag)
        else:
            raise Exception("To disconnect stream from equipment, provide either just connected stream object or\
                             just stream tag or just direction & stream type") 

        # Validate if connection is there.
        if stream_type is None and direction is None:
            warnings.warn("Already there is no connection.")
            return

        if stream_type.lower() in ['material', 'mass', 'm']:
            if direction.lower() in ['in', 'inlet']:
                if (self._inlet_material_stream_tag is None or 
                   self._inlet_material_stream_index is None):
                   warnings.warn("Material Inlet already has no connection.")
                   return 
            else:
                if (self._outlet_material_stream_tag is None or 
                   self._outlet_material_stream_index is None):
                   warnings.warn("Material Outlet already has no connection.")
                   return 
                  
        else:
            if direction.lower() in ['in', 'inlet']:
                if (self._inlet_energy_stream_tag is None or 
                   self._inlet_energy_stream_index is None):
                   warnings.warn("Energy Inlet already has no connection.")
                   return 
            else:
                if (self._outlet_energy_stream_tag is None or 
                   self._outlet_energy_stream_index is None):
                   warnings.warn("Energy Outlet already has no connection.")
                   return       

        self._is_disconnection = True
        return self.connect_stream(stream_object,
                                   direction, 
                                   stream_tag,
                                   stream_type)
      
    def _stream_equipment_mapper(self, stream_index, stream_type, is_inlet):
        """ 
            DESCRIPTION:
                Internal function to map stream with equipment object.
                _material_stream_equipment_map and _energy_stream_equipment_map 
                are dictionary of list which store index of coming from and going 
                to equipment and type of equipment. Structured like 
                {12: [10, CentrifugalPump, 21, PipeSegment], 
                 23: [21, PipeSegment, 36, FlowMeter]]} 
                where 12th index stream will have data in key no. 12. 
                Stream is coming from equipment with index 10 and is of type CentrifugalPump.  
                Stream is going into equipment with index 21 of type PipeSegment.
            
            PARAMETERS:
                stream_index:
                    Required: Yes
                    Type: int
                    Acceptable values: Non-negative integer
                    Default value: Not Applicable
                    Description: Index of the stream in the stream list it belongs to.
                
                stream_type:
                    Required: Yes
                    Type: string
                    Acceptable values: 'material' or 'energy'
                    Default value: Not Applicable
                    Description: Index of the stream in the stream list it belongs to.
                
                is_inlet:
                    Required: Yes
                    Type: bool
                    Acceptable values: True or False
                    Default value: Not Applicable
                    Description: True or False if stream is inlet to equipment.
            
            RETURN VALUE:
                Type: bool
                Description: If mapping was successful True is returned else False
            
            ERROR RAISED:
                Type:
                Description: 
            
            SAMPLE USE CASES:
                >>>  _stream_equipment_mapper(10, 'm', False)
                >>> stream_index = get_stream_index("Compressor1_power", "energy")
                >>>  _stream_equipment_mapper(stream_index, 'e', True)
                
        """

        if stream_index is None or isinstance(stream_index, list):
            return False
        e_type, e_index = (3, 2) if is_inlet else (1, 0)
        global _material_stream_equipment_map
        global _energy_stream_equipment_map
        if stream_type in ['m', 'material']:
            stream_equipment_map = _material_stream_equipment_map
        elif stream_type in ['e', 'energy']:
            stream_equipment_map =_energy_stream_equipment_map
        else:
            raise Exception('Incorrect stream type {}'.format(stream_type)+\
                            " Can only be 'm' or 'e' ")
        equipment_type = type(self)
        equipment_index = self._get_equipment_index(self.tag)
        def set_type_index():
            old_equipment_type = stream_equipment_map[stream_index][e_type]
            old_equipment_index = stream_equipment_map[stream_index][e_index]
            stream_equipment_map[stream_index][e_type] = equipment_type if not self._is_disconnection else None
            stream_equipment_map[stream_index][e_index] = equipment_index if not self._is_disconnection else None
            if (not self._is_disconnection and
                old_equipment_index is not None
                and old_equipment_type is not None):
                old_equipment_obj = old_equipment_type.list_objects()[old_equipment_index]
                old_equipment_obj.disconnect_stream(stream_type=stream_type, direction='in' if is_inlet else 'out')
                warnings.warn("Equipment type " + str(old_equipment_type) +
                              " with tag " + old_equipment_obj.tag + 
                              " was disconnected from stream type " + str(stream_type) +
                              " with tag " + str(self.get_stream_tag(stream_type,
                                                                'in' if is_inlet else 'out')))
        try:
            set_type_index()   
        except:
            try:
                stream_equipment_map[stream_index] = [None, None, None, None]
                set_type_index()
            except Exception as e:
                raise Exception("Error occured in equipment-stream mapping:", e)

        if stream_type in ['material', 'm']:
            _material_stream_equipment_map = stream_equipment_map
        elif stream_type in ['energy', 'e']:
            _energy_stream_equipment_map = stream_equipment_map
        return True

    def _stream_equipment_properties_matcher(self, stream_index, 
                                             stream_type, 
                                             is_inlet, 
                                             stream_governed=True):
        """ 
            DESCRIPTION:
                Internal function to match properties of stream with that of equipment object's.
            
            PARAMETERS:
                stream_index:
                    Required: Yes
                    Type: int
                    Acceptable values: Non-negative integer
                    Default value: Not Applicable
                    Description: Index of the stream in the stream list it belongs to.
                
                stream_type:
                    Required: Yes
                    Type: string
                    Acceptable values: 'material' or 'energy'
                    Default value: Not Applicable
                    Description: Index of the stream in the stream list it belongs to.
                
                is_inlet:
                    Required: Yes
                    Type: bool
                    Acceptable values: True or False
                    Default value: Not Applicable
                    Description: True or False if stream is inlet to equipment or not.
                
                stream_governed:
                    Required: False
                    Type: bool
                    Acceptable values: True or False
                    Default value: Not Applicable
                    Description: Determines if stream to govern the property or equipment.
                                 If True, stream property are assigned to equipment.
                                 If False, equipment property are assigned to stream.
            
            RETURN VALUE:
                Type: bool
                Description: If matching was successful, True is returned else False.
            
            ERROR RAISED:
                Type:
                Description: 
            
            SAMPLE USE CASES:
                >>>  _stream_equipment_properties_matcher(10, 'm', False)
                >>> stream_index = get_stream_index("Compressor1_power", "energy")
                >>>  _stream_equipment_properties_matcher(stream_index, 'e', True)
                
        """
        def property_matcher(stream_property, equipment_property, stream_governed):
            if stream_governed:
                return stream_property, stream_property
            return equipment_property, equipment_property

        if stream_type.lower() in ['m', 'material', 'mass']:
            stream_object = streams.MaterialStream.list_objects()[stream_index]
            if is_inlet:
                stream_object.mass_flowrate, \
                self.inlet_mass_flowrate = property_matcher(stream_object.mass_flowrate,
                                                            self._inlet_mass_flowrate,
                                                            stream_governed)
                stream_object.pressure, \
                self.inlet_pressure = property_matcher(stream_object.pressure,
                                                       self._inlet_pressure,
                                                       stream_governed)
                stream_object.temperature, \
                self.inlet_temperature = property_matcher(stream_object.temperature,
                                                          self._inlet_temperature,
                                                          stream_governed)
            else:
                stream_object.mass_flowrate, \
                self.outlet_mass_flowrate = property_matcher(stream_object.mass_flowrate,
                                                             self._outlet_mass_flowrate,
                                                             stream_governed)
                stream_object.pressure, \
                self.outlet_pressure = property_matcher(stream_object.pressure,
                                                        self._outlet_pressure,
                                                        stream_governed)
                stream_object.temperature, \
                self.outlet_temperature = property_matcher(stream_object.temperature,
                                                           self._outlet_temperature,
                                                           stream_governed)
            if not stream_governed:
                streams.MaterialStream._update_stream_object(stream_object)
            else:
                self._update_equipment_object(self)
        else:
            stream_object = streams.EnergyStream.list_objects()[stream_index]
            if is_inlet:
                stream_object.amount, \
                self.energy_in = property_matcher(stream_object.amount,
                                                  self.energy_in,
                                                  stream_governed)     
            else:
                stream_object.amount, \
                self.energy_out = property_matcher(stream_object.amount,
                                                    self.energy_out,
                                                    stream_governed)
            if not stream_governed:
                streams.EnergyStream._update_stream_object(stream_object)
        self._physical_chemical_reaction()

    def _connected_stream_property_getter(self, is_inlet, stream_type, property=None):
        """ 
            DESCRIPTION:
                Internal function to get object of stream.
            
            PARAMETERS:
                is_inlet:
                    Required: Yes
                    Type: bool
                    Default value: Not Applicable
                    Description: True if stream is inlet to equipment. False if stream is outlet.
                
                stream_type:
                    Required: Yes
                    Type: string
                    Acceptable values: 'material' or 'energy'
                    Default value: Not Applicable
                    Description: Index of the stream in the stream list it belongs to.
                
                property:
                    Required: Yes if stream_type is material
                    Type: String
                    Description: Type of property. See the if else ladder.

            
            RETURN VALUE:
                Type: Any supported property
            
            ERROR RAISED:
                Type:
                Description: 
            
            SAMPLE USE CASES:
                >>> Psat = self._connected_stream_property_getter(True, "material", "Psat")
                
        """
        
        if stream_type.lower() in ['m', 'material', 'mass']:
            stream_index = self._inlet_material_stream_index if is_inlet else self._outlet_material_stream_index
            if stream_index is None:
                raise Exception("Equipment not connected to MaterialStream!")
            stream_object = streams.MaterialStream.list_objects()[stream_index]  
        else:
            stream_index = self._inlet_energy_stream_index if is_inlet else self._outlet_energy_stream_index
            if stream_index is None:
                raise Exception("Equipment not connected to EnergyStream!")
            stream_object = streams.EnergyStream.list_objects()[stream_index]
            return stream_object.amount
        
        if property=="tag":
            return stream_object.tag
        elif property=="pressure":
            return stream_object.pressure
        elif property=="temperature":
            return stream_object.temperature
        elif property=="mass_flowrate":
            return stream_object.mass_flowrate
        elif property=="vol_flowrate":
            return stream_object.vol_flowrate
        elif property=="molecular_weight":
            return stream_object.molecular_weight
        elif property=="mol_flowrate":
            return stream_object.mol_flowrate
        elif property=="components":
            return stream_object.components
        elif property=="density":
            return stream_object.density
        elif property=="density_l":
            return stream_object.density_l
        elif property=="density_g":
            return stream_object.density_g
        elif property=="d_viscosity":
            return stream_object.d_viscosity
        elif property=="d_viscosity_l":
            return stream_object.d_viscosity_l
        elif property=="d_viscosity_g":
            return stream_object.d_viscosity_g
        elif property=="isentropic_exponent":
            return stream_object.isentropic_exponent
        elif property=="phase":
            return stream_object.phase
        elif property=="Z_g":
            return stream_object.Z_g
        elif property=="Psat":
            return stream_object.Psat
        elif property=="Pc":
            return stream_object.Pc
            
    def _create_equipment_tag(cls):
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
        """ 
            DESCRIPTION:
                Internal function to get value and unit from either tuple,
                property, float or int based on how user has provided.
            
            PARAMETERS:
                value:
                    Required: Yes
                    Type: tuple or property or int or float
                    Default value: Not Applicable
                    Description: Value provided by the user
                
                property_type:
                    Required: Yes
                    Type: Propylean property
                    Description: Type of property.

            
            RETURN VALUE:
                Type: Tuple
            
            ERROR RAISED:
                Type:
                Description: 
            
            SAMPLE USE CASES:
                self._tuple_property_value_unit_returner(prop.Length(10, "cm"), prop.Length)  
        """
        if isinstance(value, tuple):
            return value[0], value[1]
        elif isinstance(value, property_type):
            return value.value, value.unit
        elif any([isinstance(value, float), isinstance(value, int)]):
            return value, None

    def _physical_chemical_reaction(self):
        # If both inlet and outlet streams are not conneted to the equipment
        # no need to exchange properties between streams.
        
        if (self._outlet_material_stream_index is not None and
            self._inlet_material_stream_index is not None):
            inlet_m_stream_object = streams.MaterialStream.list_objects()[self._inlet_material_stream_index]
            outlet_m_stream_object = streams.MaterialStream.list_objects()[self._outlet_material_stream_index]

            # Inlet streams will always be governing.
            outlet_m_stream_object.molecular_weight = inlet_m_stream_object.molecular_weight
            outlet_m_stream_object.components = inlet_m_stream_object.components
            outlet_m_stream_object.density = inlet_m_stream_object.density
            outlet_m_stream_object.density_l = inlet_m_stream_object.density_l
            outlet_m_stream_object.density_g = inlet_m_stream_object.density_g
            outlet_m_stream_object.density_s = inlet_m_stream_object.density_s
            outlet_m_stream_object.d_viscosity = inlet_m_stream_object.d_viscosity
            outlet_m_stream_object.d_viscosity_l = inlet_m_stream_object.d_viscosity_l
            outlet_m_stream_object.d_viscosity_g = inlet_m_stream_object.d_viscosity_g
            outlet_m_stream_object.isentropic_exponent = inlet_m_stream_object.isentropic_exponent
            outlet_m_stream_object.phase = inlet_m_stream_object.phase
            outlet_m_stream_object.Psat = inlet_m_stream_object.Psat
            outlet_m_stream_object.Pc = inlet_m_stream_object.Pc
            outlet_m_stream_object.Z_g = inlet_m_stream_object.Z_g
            outlet_m_stream_object.Z_l = inlet_m_stream_object.Z_l

        if (self._outlet_energy_stream_index is not None and
            self._inlet_energy_stream_index is not None):
            inlet_e_stream_object = streams.EnergyStream.list_objects()[self._inlet_energy_stream_index]
            outlet_e_stream_object = streams.EnergyStream.list_objects()[self._outlet_energy_stream_index]
            outlet_e_stream_object.amount = inlet_e_stream_object.amount

    def delete(self):
        """ 
        DESCRIPTION:
            Method to delete an equipment object.
        
        PARAMETERS:
            None

        RETURN VALUE:
            Type: bool
            Description: True is returned if deletion is successful else False
        
        ERROR RAISED:
            Type: General
            Description: 
        
        SAMPLE USE CASES:
            >>> eq1 = CentrifugalPump()
            >>> eq1.delete()
        """
        result = True
        if self._inlet_material_stream_index is not None:
            result = result & self.disconnect_stream(direction='in',
                                                     stream_tag=self._inlet_material_stream_tag,
                                                     stream_type='material')
        if self._outlet_material_stream_index is not None:
            result = result & self.disconnect_stream(direction='out',
                                                     stream_tag=self._outlet_material_stream_tag,
                                                     stream_type='material')
        if self._inlet_energy_stream_index is not None:
            result = result & self.disconnect_stream(direction='in',
                                                     stream_tag=self._inlet_energy_stream_tag,
                                                     stream_type='energy')
        if self._outlet_energy_stream_index is not None:
            result = result & self.disconnect_stream(direction='out',
                                                     stream_tag=self._outlet_energy_stream_tag,
                                                     stream_type='energy')
        del self.items[self.index]
        del self
        return result

#Defining generic base class for all equipments with multiple inlet and outlet. TODO !!!!!!       
class _EquipmentMultipleInletOutlet:
    def __init__(self) -> None:
        pass
