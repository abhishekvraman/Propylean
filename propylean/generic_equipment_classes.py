from propylean.abstract_equipment_classes import _EquipmentOneInletOutlet, _EquipmentMultipleInletOutlet
import propylean.properties as prop
import pandas as pd
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
        
    @property
    def suction_pressure(self):
        return super(_PressureChangers, self).inlet_pressure
    @suction_pressure.setter
    def suction_pressure(self, value):
        super(_PressureChangers, self.__class__).inlet_pressure.fset(self, value)

    @property
    def discharge_pressure(self):
        return super(_PressureChangers, self).outlet_pressure
    @discharge_pressure.setter
    def discharge_pressure(self, value):
        super(_PressureChangers,self. __class__).outlet_pressure.fset(self, value)
    
    @property
    def differential_pressure(self):
        return prop.Pressure(-1 * self.pressure_drop.value,
                             self.pressure_drop.unit)
    @differential_pressure.setter
    def differential_pressure(self, value):
        self = self._get_equipment_object(self.index)
        unit = self.pressure_drop.unit
        if isinstance(value, tuple):
            unit = value[1]
            value = value[0]
        elif isinstance(value, prop.Pressure):
            unit = value.unit
            value = value.value         
        self.pressure_drop = prop.Pressure(-1 * value,
                                           unit)   
        self._update_equipment_object(self.index, self)   
    

    @property
    def performance_curve(self):
        self = self._get_equipment_object(self.index)
        return self._perfomace_curve
    @performance_curve.setter
    def pump_curve(self,value):
        self = self._get_equipment_object(self.index)
        if isinstance(value,pd.DataFrame) and value.shape[1] == 2:
                self._performance_curve = value
        else:
            raise Exception("Please enter performance_curve as pandas dataframe of 2 columns")
        self._update_equipment_object(self.index, self)
    
    @property
    def efficiency(self):
        self = self._get_equipment_object(self.index)
        return self._efficiency
    @efficiency.setter
    def efficiency(self, value):
        self = self._get_equipment_object(self.index)
        if value < 0:
            raise Exception("Please enter a positive value for efficiency")
        elif value <= 1:
            self._efficiency = value
        else:
            self._efficiency = value/100
        self._update_equipment_object(self.index, self)

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
 