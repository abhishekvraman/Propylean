from turtle import st
from attr import s
import pandas as pd
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
                Required: No TODO: Make tag as required or randomly generate a tag.
                Type: str
                Acceptable values: Any string type
                Default value: None
                Description: Equipment tag the user wants to provide
            
            dynamic_state:
                Required: No
                Type: bool
                Acceptable values: True or False
                Default value: False
                Description: If equipment is in dynamic state and inventory is changing.
                             TODO: Provide dynamic simulation capabilities.
            
            inlet_mass_flowrate:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Any
                Default value: None
                Description: Represents material inlet flowrate to the equipment.
            
            outlet_mass_flowrate:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Any
                Default value: None
                Description: Represents material outlet flowrate to the equipment.
            
            design_flowrate:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Any
                Default value: None
                Description: Represents material design flowrate of the equipment.

            inlet_pressure:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Any
                Default value: None
                Description: Represents material inlet pressure to the equipment.
            
            outlet_pressure:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Any
                Default value: None
                Description: Represents material outlet pressure to the equipment.
            
            design_pressure:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Any
                Default value: None
                Description: Represents material design pressure of the equipment.
            
            inlet_temperature:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Any
                Default value: None
                Description: Represents material inlet temperature to the equipment.
            
            outlet_temperature:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Any
                Default value: None
                Description: Represents material outlet temperature to the equipment.
            
            design_temperature:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Any
                Default value: None
                Description: Represents material design temperature of the equipment.

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
        self.tag = None if 'tag' not in inputs else inputs['tag']
        self.dynamic_state = False if 'dynamic_state' not in inputs else inputs['dynamic_state']

        #Flow properties
        self._inlet_mass_flowrate = prop.MassFlowRate() if 'inlet_mass_flowrate' not in inputs else prop.MassFlowRate(inputs['inlet_mass_flowrate'])
        self._outlet_mass_flowrate = prop.MassFlowRate() if 'outlet_mass_flowrate' not in inputs else prop.MassFlowRate(inputs['outlet_mass_flowrate'])
        # TODO: Design pressure calcs
        self.design_flowrate = prop.MassFlowRate() if 'design_flowrate' not in inputs else prop.MassFlowRate(inputs['design_flowrate'])

        #Pressure properties
        self._inlet_pressure = prop.Pressure() if 'inlet_pressure' not in inputs else prop.Pressure(inputs['inlet_pressure'])
        self._outlet_pressure = prop.Pressure() if 'outlet_pressure' not in inputs else prop.Pressure(inputs['outlet_pressure'])
        if 'pressure_drop' in inputs:
            self.pressure_drop = prop.Pressure(inputs['pressure_drop'])
        self.design_pressure = prop.Pressure() if 'design_pressure' not in inputs else prop.Pressure(inputs['design_pressure'])
        
        #Temperature properties
        self._inlet_temperature = prop.Temperature() if 'inlet_temperature' not in inputs else prop.Temperature(inputs['inlet_temperature'])
        self._outlet_temperature = prop.Temperature() if 'outlet_temperature' not in inputs else prop.Temperature(inputs['outlet_temperature'])
        self.design_temperature = prop.Temperature() if 'design_temperature' not in inputs else prop.Temperature(inputs['design_temperature'])

        #Inlet and outlet material and energy streams
        self._inlet_material_stream_tag = None
        self._outlet_material_stream_tag = None
        self._inlet_energy_stream_tag = None
        self._outlet_energy_stream_tag = None
        
        #Other Porperties
        self._is_disconnection = False
    @property
    def inlet_pressure(self):
        return self._inlet_pressure
    @inlet_pressure.setter
    def inlet_pressure(self, value):
        if isinstance(value, tuple):
            self._inlet_pressure.unit = value[1]
            value = value[0]
        elif isinstance(value, prop.Pressure):
            self._inlet_pressure.unit = value.unit
            value = value.value
        self._inlet_pressure.value = value
        self._outlet_pressure.value = self._inlet_pressure.value - self.pressure_drop.value
    @property
    def outlet_pressure(self):
        return self._outlet_pressure
    @outlet_pressure.setter
    def outlet_pressure(self,value):
        if isinstance(value, tuple):
            self._outlet_pressure.unit = value[1]
            value = value[0]
        elif isinstance(value, prop.Pressure):
            self._outlet_pressure.unit = value.unit
            value = value.value
        self._outlet_pressure.value = value
        self._inlet_pressure.value = self._outlet_pressure.value + self.pressure_drop.value
    @property
    def pressure_drop(self):
        if (self._inlet_pressure.value == None or
            self._outlet_pressure.value == None or
            self._inlet_mass_flowrate.value == 0):
            value = 0
        else:
            value = self._inlet_pressure.value - self._outlet_pressure.value
        return prop.Pressure(value=value, unit=self._inlet_pressure.unit)
    @pressure_drop.setter
    def pressure_drop(self, value):
        if isinstance(value, tuple):
            self._outlet_pressure.unit = value[1]
            value = value[0]
        elif isinstance(value, prop.Pressure):
            value = value.value
            # TODO Unit is not set
        if self._inlet_pressure.value != None:
            self._outlet_pressure.value = self._inlet_pressure.value - value
        elif self._outlet_pressure.value != None:
            self._inlet_pressure.value = self._outlet_pressure.value + value
        else:
            raise Exception("Error! Assign inlet value or outlet outlet before assigning differential")
    
    @property
    def inlet_temperature(self):
        return self._inlet_temperature
    @inlet_temperature.setter
    def inlet_temperature(self, value):
        if isinstance(value, tuple):
            self._inlet_temperature.unit = value[1]
            value = value[0]
        elif isinstance(value, prop.Temperature):
            self._inlet_temperature.unit = value.unit
            value = value.value
        self._inlet_temperature.value = value
    @property
    def outlet_temperature(self):
        return self._outlet_temperature
    @outlet_temperature.setter
    def outlet_temperature(self,value):
        if isinstance(value, tuple):
            self._outlet_temperature.unit = value[1]
            value = value[0]
        elif isinstance(value, prop.Temperature):
            self._outlet_temperature.unit = value.unit
            value = value.value
        self._outlet_temperature.value = value

    @property
    def inlet_mass_flowrate(self):
        return self._inlet_mass_flowrate
    @inlet_mass_flowrate.setter
    def inlet_mass_flowrate(self, value):
        unit = self._inlet_mass_flowrate.unit
        if isinstance(value, prop.MassFlowRate):
            unit = value.unit
            value = value.value
        self._inlet_mass_flowrate.value = value
        self._inlet_mass_flowrate.unit = unit
        self._outlet_mass_flowrate.value = self._inlet_mass_flowrate.value + self.inventory_change_rate.value
    @property
    def outlet_mass_flowrate(self):
        return self._outlet_mass_flowrate
    @outlet_mass_flowrate.setter
    def outlet_mass_flowrate(self, value):
        unit = self._outlet_mass_flowrate.unit
        if isinstance(value, prop.MassFlowRate):
            unit = value.unit
            value = value.value
        self._outlet_mass_flowrate.value = value
        self._outlet_mass_flowrate.unit = unit
        self._inlet_mass_flowrate.value = self._outlet_mass_flowrate.value - self.inventory_change_rate.value   
    @property
    def inventory_change_rate(self):
        if not self.dynamic_state:
            return prop.MassFlowRate(0, self.inlet_mass_flowrate.unit)
        if (self._inlet_mass_flowrate.value == None or
            self._outlet_mass_flowrate.value == None):
            return None            
        return prop.MassFlowRate(self._inlet_mass_flowrate.value - self._outlet_mass_flowrate.value,
                                 self.outlet_mass_flowrate.unit)
    @inventory_change_rate.setter
    def inventory_change_rate(self, value):
        if self._inlet_mass_flowrate.value != None:
            self._outlet_mass_flowrate.value = self._inlet_mass_flowrate.value - value
        elif self._outlet_mass_flowrate != None:
            self._inlet_mass_flowrate.value = self._outlet_mass_flowrate.value + value
        else:
            raise Exception("Error! Assign inlet value or outlet outlet before assigning differential")
    
    @classmethod
    def get_equipment_index(cls, tag):
        for index, equipment in enumerate(cls.items):
            if equipment.tag == tag:
                return index
        return None



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
                       stream_type=None):
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
                                                      is_inlet)
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
        equipment_index = self.get_equipment_index(self.tag)
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
        def property_matcher(stream_property, equipment_property):
            if stream_governed:
                equipment_property = stream_property
            else:
                stream_property = equipment_property
            return stream_property, equipment_property
        if stream_type.lower() in ['m', 'material', 'mass']:
            stream_object = streams.MaterialStream.list_objects()[stream_index]
            if is_inlet:
                stream_object.mass_flowrate, \
                self.inlet_mass_flowrate = property_matcher(stream_object.mass_flowrate,
                                                            self.inlet_mass_flowrate)
                stream_object.pressure, \
                self.inlet_pressure = property_matcher(stream_object.pressure,
                                                            self.inlet_pressure)
                stream_object.temperature, \
                self.inlet_temperature = property_matcher(stream_object.temperature,
                                                            self.inlet_temperature)
            else:
                stream_object.mass_flowrate, \
                self.outlet_mass_flowrate = property_matcher(stream_object.mass_flowrate,
                                                            self.outlet_mass_flowrate)
                stream_object.pressure, \
                self.outlet_pressure = property_matcher(stream_object.pressure,
                                                            self.outlet_pressure)
                stream_object.temperature, \
                self.outlet_temperature = property_matcher(stream_object.temperature,
                                                            self.outlet_temperature)
            streams.MaterialStream.list_objects()[stream_index] = stream_object # TODO change this
        else:
            stream_object = streams.EnergyStream.list_objects()[stream_index]
            # if is_inlet:
            #     stream_object, \
            #     self.energy_in = property_matcher(stream_object,
            #                                       self.energy_in)
                
            # else:
            #     stream_object, \
            #     self.energy_out = property_matcher(stream_object,
            #                                         self.energy_out)
            
            streams.EnergyStream.list_objects()[stream_index] = stream_object # TODO change this
        
        
#Defining generic base class for all equipments with multiple inlet and outlet. TODO !!!!!!       
class _EquipmentMultipleInletOutlet:
    def __init__(self) -> None:
        self._inlet_pressure.value = list()

#Defining generic class for all types of pressure changers like Pumps, Compressors and Expanders
class _PressureChangers(_EquipmentOneInletOutlet):
    def __init__(self,**inputs) -> None:
        """ 
            DESCRIPTION:
                Parent class for all equipment which has primary task to change
                pressure of a stream. For e.g. Pumps and compressors.
            
            PARAMETERS:
                inlet_pressure or suction_pressure:
                    Required: No
                    Type: int or float (recommended)
                    Acceptable values: Non-negative integer
                    Default value: based on unit    
                    Description: Inlet or suction pressure of the equipment.
                
                outlet_pressure or discharge_pressure:
                    Required: No
                    Type: int or float (recommended)
                    Acceptable values: Non-negative integer
                    Default value: based on unit    
                    Description: Outlet or discharge pressure of the equipment.
                
                pressure_drop or differential_pressure:
                    Required: No
                    Type: int or float (recommended)
                    Acceptable values: Non-negative integer
                    Default value: based on unit    
                    Description: Pressure drop or differential pressure of the equipment.

                performance_curve:
                    Required: No
                    Type: int or float (recommended)
                    Acceptable values: Non-negative integer
                    Default value: based on unit    
                    Description: Pressure drop or differential pressure of the equipment.

            RETURN VALUE:
                Type: _PressureChangers
                Description: object with all _EquipmentOneInletOutlet and other pressure changer properties.
            
            ERROR RAISED:
                Type:
                Description: 
            
            SAMPLE USE CASES:
                >>>  class AwesomeCompressor(_PressureChangers):
                >>>     def __init__(**kwargs):
                >>>         some_property = 20
                
        """
        
        if 'pressure_drop' in inputs:
            inputs['differential_pressure'] = -1 * inputs['pressure_drop']
            del inputs['pressure_drop']
        if 'inlet_pressure' in inputs:
            inputs['suction_pressure'] = inputs['inlet_pressure']
            del inputs['inlet_pressure']
        if 'outlet_pressure' in inputs:
            inputs['discharge_pressure'] = inputs['outlet_pressure']
            del inputs['outlet_pressure']
        
        super().__init__(**inputs)
        if 'suction_pressure' in inputs:
            self._inlet_pressure.value = inputs['suction_pressure']
            if ('differential_pressure' in inputs and 'performance_curve' in inputs or
                'differential_pressure' in inputs and 'discharge_pressure' in inputs or
                'performance_curve' in inputs and 'discharge_pressure' in inputs):
                raise Exception('Please input only one of discharge_pressure, differential_pressure or performance_curve \
                                 with suction pressure')
        if 'discharge_pressure' in inputs:
            if (self.suction_pressure != None and 
                'differential_pressure' in inputs):
                raise Exception("Please enter ethier one of discharge_pressure or differential_pressure")
            self._outlet_pressure = inputs['discharge_pressure']
        
        if 'differential_pressure' in inputs:
            if ((self.suction_pressure != None or self.discharge_pressure != None) and
                 'performance_curve' in inputs):
                 raise Exception('Please input only one of differential pressure or performance_curve')
            self.differential_pressure = inputs['differential_pressure'] 
                 
        self._performance_curve = pd.DataFrame()
        if 'performance_curve' in inputs:
            self.performace_curve = inputs['performance_curve']
        
        self._efficiency = None if 'efficiency' not in inputs else inputs['efficiency']
        
    @_EquipmentOneInletOutlet.inlet_pressure.getter
    def inlet_pressure(self):
        return self._inlet_pressure
    @_EquipmentOneInletOutlet.inlet_pressure.setter
    def inlet_pressure(self, value):
        if isinstance(value, tuple):
            self._inlet_pressure.unit = value[1]
            value = value[0]
        elif isinstance(value, prop.Pressure):
            self._inlet_pressure.unit = value.unit
            value = value.value
        self._inlet_pressure.value = value
        if self.differential_pressure.value != prop.Pressure().value:
            self._outlet_pressure.value = self._inlet_pressure.value + self.differential_pressure.value
    @property
    def suction_pressure(self):
        return self._inlet_pressure
    @suction_pressure.setter
    def suction_pressure(self, value):
        self.inlet_pressure = value

    @_EquipmentOneInletOutlet.outlet_pressure.getter
    def outlet_pressure(self):
        return self._outlet_pressure
    @_EquipmentOneInletOutlet.outlet_pressure.setter
    def outlet_pressure(self,value):
        if isinstance(value, tuple):
            self._outlet_pressure.unit = value[1]
            value = value[0]
        elif isinstance(value, prop.Pressure):
            self._outlet_pressure.unit = value.unit
            value = value.value
        self._outlet_pressure.value = value
        if self.differential_pressure.value != prop.Pressure().value:
            self._inlet_pressure.value = self._outlet_pressure.value - self.differential_pressure.value
    @property
    def discharge_pressure(self):
        return self._outlet_pressure
    @discharge_pressure.setter
    def discharge_pressure(self, value):
        if isinstance(value, tuple):
            self.outlet_pressure.unit = value[1]
            value = value[0]
        self.outlet_pressure.value = value
    
    @property
    def differential_pressure(self):
        return prop.Pressure(-1 * self.pressure_drop.value,
                             self.pressure_drop.unit)
    @differential_pressure.setter
    def differential_pressure(self,value):
        self.pressure_drop = -1 * value      
    

    @property
    def performance_curve(self):
        return self._perfomace_curve
    @performance_curve.setter
    def pump_curve(self,value):
        if isinstance(value,pd.DataFrame) and value.shape[1] == 2:
                self._performance_curve = value
        else:
            raise Exception("Please enter performance_curve as pandas dataframe of 2 columns")
    
    @property
    def efficiency(self):
        return self._efficiency
    @efficiency.setter
    def efficiency(self, value):
        if value < 0:
            raise Exception("Please enter a positive value for efficiency")
        elif value <= 1:
            self._efficiency = value
        else:
            self._efficiency = value/100

#Defining generic class for all types of vessels.  NEEDS SUPER CLASS WITH MULTI INPUT AND OUTPUT 
class _Vessels(_EquipmentMultipleInletOutlet):
    def __init__(self, **inputs) -> None:
        """ 
        DESCRIPTION:
            Parent class for all equipment which has primary task to be a vessel
            of a stream. For e.g. Tanks and reactors.
        
        PARAMETERS:
            ID:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Non-negative integer
                Default value: based on unit    
                Description: Internal diameter of the vessel.
            
            length:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Non-negative integer
                Default value: based on unit    
                Description: Length of the vessel.
            
            LLL, LLLL, HLL, NLL and HHLL:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Non-negative integer
                Default value: based on unit    
                Description: Low Liquid Level(LLL), Low-Low Liquid Level(LLLL), High Liquid Level(HLL),
                             Normal Liquid Level(NLL), and High-high Liquid Level.

        RETURN VALUE:
            Type: _Vessels
            Description: object with all _EquipmentOneInletOutlet and other vessel related properties.
        
        ERROR RAISED:
            Type:
            Description: 
        
        SAMPLE USE CASES:
            >>>  class AwesomeReactor(_Vessels):
            >>>     def __init__(**kwargs):
            >>>         some_property = 20
                
    """
        super().__init__(**inputs)
        self.ID = prop.Length() if 'ID' not in inputs else prop.Length(inputs['ID'])
        self.length = prop.Length() if 'length' not in inputs else prop.Length(inputs['length'])
        
        self.LLLL = prop.Length() if 'LLLL' not in inputs else prop.Length(inputs['LLLL'])
        self.LLL = prop.Length() if 'LLL' not in inputs else prop.Length(inputs['LLL'])
        self.NLL = prop.Length() if 'NLL' not in inputs else prop.Length(inputs['NLL'])
        self.HLL = prop.Length() if 'HLL' not in inputs else prop.Length(inputs['HLL'])
        self.HHLL = prop.Length() if 'HHLL' not in inputs else prop.Length(inputs['HHLL'])

#Defining generic class for all types of heat exchangers NEEDS SUPER CLASS WITH MULTI INPUT AND OUTPUT
class _Exchangers(_EquipmentMultipleInletOutlet):
    def __init__(self, **inputs) -> None:
        """ 
        DESCRIPTION:
            Parent class for all equipment which has primary task to be an exchanger
            of a stream. For e.g. Tanks and reactors.
        
        PARAMETERS:
            TODO

        RETURN VALUE:
            Type: _Exchangers
            Description: object with all _EquipmentOneInletOutlet and other exchanger related properties.
        
        ERROR RAISED:
            Type:
            Description: 
        
        SAMPLE USE CASES:
            >>>  class AwesomeReactor(_Vessels):
            >>>     def __init__(**kwargs):
            >>>         some_property = 20
                
    """
        #Hot side
        self.hot_side_operating_pressure = None if 'hot_side_operating_pressure' not in inputs else inputs['hot_side_operating_pressure']
        self.hot_side_flowrate = None if 'hot_side_flowrate' not in inputs else inputs['hot_side_flowrate']
        self.hot_side_inlet_temp = None if 'hot_side_inlet_temp' not in inputs else inputs['hot_side_inlet_temp']
        self.hot_side_outlet_temp = None if 'hot_side_outlet_temp' not in inputs else inputs['hot_side_outlet_temp']
        self.hot_side_pressure_drop = None if 'hot_side_pressure_drop' not in inputs else inputs['hot_side_pressure_drop']
        #Cold Side
        self.cold_side_operating_pressure = None if 'cold_side_operating_pressure' not in inputs else inputs['cold_side_operating_pressure']
        self.cold_stream_flowrate = None if 'cold_stream_flowrate' not in inputs else inputs['cold_stream_flowrate']
        self.cold_side_inlet_temp = None if 'cold_side_inlet_temp' not in inputs else inputs['cold_side_inlet_temp']
        self.cold_side_outlet_temp = None if 'cold_side_outlet_temp' not in inputs else inputs['cold_side_outlet_temp']
        self.cold_side_pressure_drop = None if 'cold_side_pressure_drop' not in inputs else inputs['cold_side_pressure_drop']
 