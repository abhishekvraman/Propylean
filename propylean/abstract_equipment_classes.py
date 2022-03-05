import propylean.properties as prop
from propylean import streams

_material_stream_equipment_map = dict()
_energy_stream_equipment_map = dict()

#Defining generic base class for all equipments with one inlet and outlet
class _EquipmentOneInletOutlet:
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
                Description: Equipment tag the user wants to provide. If not provided, then tag is automatically generated
            
            dynamic_state:
                Required: No
                Type: bool
                Acceptable values: True or False
                Default value: False
                Description: If equipment is in dynamic state and inventory is changing.
                             TODO: Provide dynamic simulation capabilities.
            
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
        if 'tag' not in inputs:
            self.tag = self._create_equipment_tag()  
        else:
            self.tag = inputs['tag']
        self.dynamic_state = False if 'dynamic_state' not in inputs else inputs['dynamic_state']
        # TODO: Design pressure calcs

        #Flow properties
        self._inlet_mass_flowrate = prop.MassFlowRate() 
        self._outlet_mass_flowrate = prop.MassFlowRate()
        self.design_flowrate = prop.MassFlowRate()

        #Pressure properties
        self._pressure_drop = prop.Pressure(0)
        self._inlet_pressure = prop.Pressure()
        self._outlet_pressure = prop.Pressure()
        self.design_pressure = prop.Pressure()
        
        #Temperature properties
        self._inlet_temperature = prop.Temperature()
        self._outlet_temperature = prop.Temperature()
        self.design_temperature = prop.Temperature()

        #Inlet and outlet material and energy streams
        self._inlet_material_stream_tag = None
        self._outlet_material_stream_tag = None
        self._inlet_energy_stream_tag = None
        self._outlet_energy_stream_tag = None
        
        #Energy properties
        self.energy_in = prop.Power()
        self.energy_out = prop.Power()

        #Other Porperties
        self._is_disconnection = False

        if 'pressure_drop' in inputs:
            self.pressure_drop = prop.Pressure(inputs['pressure_drop'])
    

    @property
    def index(self):
      return self._index

    @property
    def tag(self):
        return self._tag
    @tag.setter
    def tag(self, value):
        if self._check_tag_assigned(value):
            msg = "Tag '{}' already assigned!".format(value)
            raise Exception(msg)
        else:
            self._tag = value
    @property
    def inlet_pressure(self):
        self = self._get_equipment_object(self.index)
        return self._inlet_pressure
    @inlet_pressure.setter
    def inlet_pressure(self, value):
        self = self._get_equipment_object(self.index)
        unit = self._inlet_pressure.unit
        if isinstance(value, tuple):
            unit = value[1]
            value = value[0]
        elif isinstance(value, prop.Pressure):
            unit = value.unit
            value = value.value
        self._inlet_pressure = prop.Pressure(value, unit)
        self._outlet_pressure = self._inlet_pressure - self.pressure_drop
        self._update_equipment_object(self.index, self)
    
    @property
    def outlet_pressure(self):
        self = self._get_equipment_object(self.index)
        return self._outlet_pressure
    @outlet_pressure.setter
    def outlet_pressure(self, value):
        self = self._get_equipment_object(self.index)
        unit = self._outlet_pressure.unit
        if isinstance(value, tuple):
            unit = value[1]
            value = value[0]
        elif isinstance(value, prop.Pressure):
            unit = value.unit
            value = value.value
        self._outlet_pressure = prop.Pressure(value, unit)
        self._inlet_pressure = self._outlet_pressure + self.pressure_drop
        self._update_equipment_object(self.index, self)
    
    @property
    def pressure_drop(self):
        self = self._get_equipment_object(self.index)
        return self._pressure_drop
    @pressure_drop.setter
    def pressure_drop(self, value):
        self = self._get_equipment_object(self.index)
        unit = self._pressure_drop.unit
        if isinstance(value, tuple):
            unit = value[1]
            value = value[0]
        elif isinstance(value, prop.Pressure):
            unit = value.unit
            value = value.value
        self._pressure_drop = prop.Pressure(value, unit)
        self._outlet_pressure =  self._inlet_pressure - self._pressure_drop
        self._update_equipment_object(self.index, self)
        
    @property
    def inlet_temperature(self):
        self = self._get_equipment_object(self.index)
        return self._inlet_temperature
    @inlet_temperature.setter
    def inlet_temperature(self, value):
        self = self._get_equipment_object(self.index)
        unit = self._inlet_temperature.unit
        if isinstance(value, tuple):
            unit = value[1]
            value = value[0]
        elif isinstance(value, prop.Temperature):
            unit = value.unit
            value = value.value
        self._inlet_temperature = prop.Temperature(value, unit)
        self._outlet_temperature = self._inlet_temperature + self.temperature_change
        self._update_equipment_object(self.index, self)
    @property
    def outlet_temperature(self):
        self = self._get_equipment_object(self.index)
        return self._outlet_temperature
    @outlet_temperature.setter
    def outlet_temperature(self,value):
        self = self._get_equipment_object(self.index)
        unit = self._outlet_temperature.unit
        if isinstance(value, tuple):
            unit = value[1]
            value = value[0]
        elif isinstance(value, prop.Temperature):
            unit = value.unit
            value = value.value
        self._outlet_temperature = prop.Temperature(value, unit)
        self._inlet_temperature = self._outlet_temperature - self.temperature_change
        self._update_equipment_object(self.index, self)
    @property
    def temperature_change(self):
        self = self._get_equipment_object(self.index)
        value = prop.Temperature(0, self._outlet_temperature.unit) # Change as per inlet outlet power
        return value

    @property
    def inlet_mass_flowrate(self):
        self = self._get_equipment_object(self.index)
        return self._inlet_mass_flowrate
    @inlet_mass_flowrate.setter
    def inlet_mass_flowrate(self, value):
        self = self._get_equipment_object(self.index)
        unit = self._inlet_mass_flowrate.unit
        if isinstance(value, tuple):
            unit = value[1]
            value = value[0]
        if isinstance(value, prop.MassFlowRate):
            unit = value.unit
            value = value.value
        self._inlet_mass_flowrate = prop.MassFlowRate(value, unit)
        self._outlet_mass_flowrate = self._inlet_mass_flowrate + self.inventory_change_rate
        self._update_equipment_object(self.index, self)
    
    @property
    def outlet_mass_flowrate(self):
        self = self._get_equipment_object(self.index)
        return self._outlet_mass_flowrate
    @outlet_mass_flowrate.setter
    def outlet_mass_flowrate(self, value):
        self = self._get_equipment_object(self.index)
        unit = self._outlet_mass_flowrate.unit
        if isinstance(value, tuple):
            unit = value[1]
            value = value[0]
        if isinstance(value, prop.MassFlowRate):
            unit = value.unit
            value = value.value
        self._outlet_mass_flowrate = prop.MassFlowRate(value, unit)
        self._inlet_mass_flowrate = self._outlet_mass_flowrate - self.inventory_change_rate
        self._update_equipment_object(self.index, self)
    
    @property
    def inventory_change_rate(self):
        self = self._get_equipment_object(self.index)
        if not self.dynamic_state:
            return prop.MassFlowRate(0, self.inlet_mass_flowrate.unit)            
        return self._inlet_mass_flowrate - self._outlet_mass_flowrate                             
    @inventory_change_rate.setter
    def inventory_change_rate(self, value):
        self = self._get_equipment_object(self.index)
        if self._inlet_mass_flowrate.value != None:
            self._outlet_mass_flowrate.value = self._inlet_mass_flowrate.value - value
        elif self._outlet_mass_flowrate != None:
            self._inlet_mass_flowrate.value = self._outlet_mass_flowrate.value + value
        else:
            raise Exception("Error! Assign inlet value or outlet outlet before assigning differential")
        self._update_equipment_object(self.index, self)
    
    def _get_equipment_index(cls, tag):
        for index, equipment in enumerate(cls.items):
            if equipment.tag == tag:
                return index
        return None
    
    def _get_equipment_object(cls, index):
        return cls.items[index]
    
    def _update_equipment_object(cls, index, obj):
        cls.items[index] = obj
    
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.tag == other.tag
        else:
            return False


    def get_stream_tag(self, stream_type, direction):
        """ 
        DESCRIPTION:
            Class method to get stream tag using steam type and the direction.
        
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
            Class method to connect a stream object with equiment.
        
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
            if not (isinstance(stream_object, streams.EnergyStream) or
                    isinstance(stream_object, streams.MaterialStream)):
                    raise Exception("Stream object should be of type EnergyStream or Material Stream not "+
                                    +type(stream_object))
            stream_tag = stream_object.tag
            if isinstance(stream_object, streams.MaterialStream):
                stream_type = 'material'
            elif isinstance(stream_object, streams.EnergyStream):
                stream_type = 'energy'
        elif not self._is_disconnection and stream_tag is None:
            raise Exception("Either of Stream Object or Stream Tag is required for connection!")
        
        if stream_type.lower() not in ['material', 'mass', 'm', 'energy', 'power', 'e', 'p']:
            raise Exception('Incorrect stream_type specified! Provided \"'+stream_type+'\". Can only be "material/mass/m" or "energy/e/power/p"]')
        if direction.lower() not in ['in', 'inlet', 'out', 'outlet']:
            raise Exception('Incorrect direction specified! Provided \"'+direction+'\". Can only be ["in", "out", "inlet", "outlet"]')
        
        stream_index = streams.get_stream_index(stream_tag, stream_type)
        is_inlet = True if direction.lower() in ['in', 'inlet'] else False

        mapping_result = self._stream_equipment_mapper(stream_index, stream_type, is_inlet)
        if self._is_disconnection:
            stream_tag = None
            self._is_disconnection = False
        elif mapping_result:
            self._stream_equipment_properties_matcher(stream_index, 
                                                      stream_type,
                                                      is_inlet,
                                                      stream_governed)
        if stream_type.lower() in ['material', 'mass', 'm']:
            if direction.lower() in ['in', 'inlet']:
                self._inlet_material_stream_tag = stream_tag
            else:
                self._outlet_material_stream_tag = stream_tag
        else:
            if direction.lower() in ['in', 'inlet']:
                self._inlet_energy_stream_tag = stream_tag
            else:
                self._outlet_energy_stream_tag = stream_tag
        
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
                Required: Yes is stream_object or stream_tag not provided
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
            Description: True is returned if connection is successful else False
        
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
            if tag == self._inlet_material_stream_tag:
                stream_type = "material"
                direction = "in"
            elif tag == self._outlet_material_stream_tag:
                stream_type = "material"
                direction = "out"
            elif tag == self._inlet_energy_stream_tag:
                stream_type = "energy"
                direction = "in"
            elif tag == self._outlet_energy_stream_tag:
                stream_type = "energy"
                direction = "out"
            return stream_type, direction

        if stream_object is not None:
            stream_type, direction = define_index_direction(stream_object.tag)
        elif stream_tag is not None:
            stream_type, direction = define_index_direction(stream_tag)
        elif (direction is not None and 
              stream_type is not None):
              stream_tag = self.get_stream_tag(stream_type, direction)
              stream_type, direction = define_index_direction(stream_tag)
        else:
            raise Exception("To disconnect stream from equipment, provide either just connected stream object or \
                             just stream tag or just direction & stream type") 
              
        self._is_disconnection = True
        return self.connect_stream(stream_object,
                                   direction, 
                                   stream_tag,
                                   stream_type)
      
    def _stream_equipment_mapper(self, stream_index, stream_type, is_inlet):
        """ 
            DESCRIPTION:
                Internal function to map stream with equipment object.
                _material_stream_equipment_map and __energy_stream_equipment_map 
                are dictionary of list which store index of coming from and going 
                to equipment and type of equipment. Structured like 
                {12: [10, CentrifugalPump, 21, PipeSegment], 
                 23: [21, PipeSegment, 36, FlowMeter]]} 
                were 12th index stream will have data in key no. 12 
                stream is coming from equipment index is 10 of type CentrifugalPump and  
                going into equipment index is 21 of type PipeSegment.
            
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
            if (old_equipment_index is not None
                and old_equipment_type is not None):
                old_equipment_obj = old_equipment_type.list_objects()[old_equipment_index]
                old_equipment_obj.disconnect_stream(stream_type, 'in' if is_inlet else 'out')
                raise Warning("Equipment type " + old_equipment_type +
                              " with tag " + old_equipment_obj.tag + 
                              " was disconnected from stream type " + stream_type +
                              " with tag " + self.get_stream_tag(stream_type,
                                                                'in' if is_inlet else 'out'))
        try:
            set_type_index()   
        except:
            try:
                stream_equipment_map[stream_index] = [None, None, None, None]
                set_type_index()
            except Exception as e:
                raise Exception("Error occured in equipment-stream mapping:", e)

        if stream_type == 'material':
            _material_stream_equipment_map = stream_equipment_map
        else:
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
                streams.MaterialStream._update_stream_object(stream_index, stream_object)
            else:
                self._update_equipment_object(self.index, self)
        else:
            stream_object = streams.EnergyStream.list_objects()[stream_index]
            if is_inlet:
                stream_object, \
                self.energy_in = property_matcher(stream_object,
                                                  self.energy_in,
                                                  stream_governed)
                
            else:
                stream_object, \
                self.energy_out = property_matcher(stream_object,
                                                    self.energy_out,
                                                    stream_governed)
            if not stream_governed:
                streams.EnergyStream.update_object(stream_index, stream_object)

    def _create_equipment_tag(cls):
        i =0
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
        
#Defining generic base class for all equipments with multiple inlet and outlet. TODO !!!!!!       
class _EquipmentMultipleInletOutlet:
    def __init__(self) -> None:
        self._inlet_pressure.value = list()
