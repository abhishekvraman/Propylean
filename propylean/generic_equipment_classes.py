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
                pressure_drop or differential_pressure:
                    Required: No
                    Type: int/float or Pressure(recommended)
                    Acceptable values: Non-negative integer
                    Default value: based on unit    
                    Description: Pressure drop or differential pressure of the equipment.
                
                efficiency:
                    Required: No
                    Type: int or float (recommended)
                    Acceptable values: Non-negative integer
                    Default value: based on unit    
                    Description: Efficiency of the equipment.

                performance_curve:
                    Required: No
                    Type: pandas DataFrame
                    Acceptable values: Non-negative integer in dataframe with flow and head values.
                    Default value: pandas.DataFrame()    
                    Description: Performance curve of the pump. 
                                 E.g. pd.DataFrame([{'flow':[2, 10, 30, 67], 'head':[45, 20, 10, 2]}]) 

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
        
        super().__init__(**inputs)
        
        if 'differential_pressure' in inputs:
            if ((self._inlet_pressure != None or self._outlet_pressure != None) and
                 'performance_curve' in inputs):
                 raise Exception('Please input only one of differential pressure or performance_curve')
            diff_presure = inputs['differential_pressure'] 
            if isinstance(diff_presure, prop.Pressure):
                self._pressure_drop = prop.Pressure(-1 * diff_presure.value,
                                                    diff_presure.unit)
            elif isinstance(diff_presure, tuple):
                self._pressure_drop = prop.Pressure(-1 * diff_presure[0],
                                                     diff_presure[1])
                 
        self._performance_curve = pd.DataFrame()
        if 'performance_curve' in inputs:
            self.performace_curve = inputs['performance_curve']
        
        self._efficiency = 100 if 'efficiency' not in inputs else inputs['efficiency']
        
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
        super(_PressureChangers,self.__class__).outlet_pressure.fset(self, value)
    
    @property
    def differential_pressure(self):
        return prop.Pressure(-1 * self.pressure_drop.value,
                             self.pressure_drop.unit)
    @differential_pressure.setter
    def differential_pressure(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Pressure)
        if unit is None:
            unit = self.pressure_drop.unit         
        self.pressure_drop = prop.Pressure(-1 * value,
                                           unit)   
        self._update_equipment_object(self)   
    
    @property
    def performance_curve(self):
        self = self._get_equipment_object(self)
        return self._perfomace_curve
    @performance_curve.setter
    def performance_curve(self,value):
        self = self._get_equipment_object(self)
        if isinstance(value, pd.DataFrame) and value.shape[1] == 2:
                self._performance_curve = value
        else:
            raise Exception("Please enter performance_curve as pandas dataframe of 2 columns.\nOne for Flow and other for head.")
        self._update_equipment_object(self)
    
    @property
    def efficiency(self):
        self = self._get_equipment_object(self)
        return self._efficiency
    @efficiency.setter
    def efficiency(self, value):
        self = self._get_equipment_object(self)
        if value < 0:
            raise Exception("Please enter a positive value for efficiency")
        elif value <= 1:
            self._efficiency = value
        else:
            self._efficiency = value/100
        self._update_equipment_object(self)
    
    @property
    def power(self):
        self = self._get_equipment_object(self)
        return self._power
    @power.setter
    def power(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Power)
        if unit is None:
            unit = self._power.unit         
        self._power = prop.Power(value, unit)
        self._update_equipment_object(self)  
    
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
class _Exchangers(_EquipmentOneInletOutlet):
    def __init__(self, **inputs) -> None:
        """ 
        DESCRIPTION:
            Parent class for all equipment which has primary task to be an 
            Temperature changer of a stream. For e.g. Heater and Cooler.
        
        PARAMETERS:
            temperature_change:
                Required: No
                    Type: int/float or Temperature(recommended)
                    Acceptable values: Non-negative integer
                    Default value: based on unit    
                    Description: Temperature change of stream in the equipment.
                                 That is difference between inlet stream and outlet stream.
                
            efficiency:
                Required: No
                Type: int or float (recommended)
                Acceptable values: Non-negative integer
                Default value: based on unit    
                Description: Efficiency of the equipment.

        RETURN VALUE:
            Type: _Exchangers
            Description: object with all _EquipmentOneInletOutlet and other exchanger related properties.
        
        ERROR RAISED:
            Type:
            Description: 
        
        SAMPLE USE CASES:
            >>>  class AwesomeNewExchanger(_Exchangers):
            >>>     def __init__(**kwargs):
            >>>         some_property = 20 
        """
        super().__init__(**inputs)
        self.temperature_change = prop.Temperature(0, 'K') if "temperature_change" not in inputs\
                                                               else inputs["temperature_change"] 
        if "energy_in" in inputs:
            self.energy_in = inputs["energy_in"]
        if "energy_out" in inputs:
            self.energy_out = inputs["energy_out"]
        self._efficiency = 100 if 'efficiency' not in inputs else inputs['efficiency']
    
    @property
    def temperature_change(self):
        self = self._get_equipment_object(self)
        return self._temperature_change
    @temperature_change.setter
    def temperature_change(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Temperature)
        if unit is None:
            unit = self._temperature_change.unit
        
        self._temperature_change = prop.Temperature(value, unit)
        
        self._update_equipment_object(self)
    
    @property
    def efficiency(self):
        self = self._get_equipment_object(self)
        return self._efficiency
    @efficiency.setter
    def efficiency(self, value):
        self = self._get_equipment_object(self)
        if value < 0:
            raise Exception("Please enter a positive value for efficiency")
        elif value <= 1:
            self._efficiency = value
        else:
            self._efficiency = value/100
        self._update_equipment_object(self)