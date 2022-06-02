from propylean.abstract_equipment_classes import _EquipmentOneInletOutlet, _EquipmentMultipleInletOutlet
import propylean.properties as prop
import pandas as pd
from math import pi
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
                    Default value: 100%    
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
class _Vessels(_EquipmentMultipleInletOutlet, _EquipmentOneInletOutlet):
    def __init__(self, **inputs) -> None:
        """ 
        DESCRIPTION:
            Parent class for all equipment which has primary task to be a vessel
            of a stream. For e.g. Tanks and reactors.
        
        PARAMETERS:
            ID:
                Required: No
                Type: int or float or Length(recommended)
                Acceptable values: Non-negative integer
                Default value: based on unit    
                Description: Internal diameter of the vessel.
            
            OD:
                Required: No
                Type: int or float or Length(recommended)
                Acceptable values: Non-negative integer
                Default value: based on unit    
                Description: Outer diameter of the vessel.

            thickness:
                Required: No
                Type: int or float or Length(recommended)
                Acceptable values: Non-negative integer
                Default value: based on unit    
                Description: thickness of the vessel.
            
            length:
                Required: No
                Type: int or float or Length(recommended)
                Acceptable values: Non-negative integer
                Default value: based on unit    
                Description: tan-line length of the vessel.
            
            LLL, LLLL, HLL, NLL and HHLL:
                Required: No
                Type: int or float or Length(recommended)
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
        self.operating_pressure = prop.Pressure()
        self.operating_temperature = prop.Temperature()
        if ('ID' in inputs and inputs['ID'] is not None):
                self.ID = inputs['ID']
                if 'OD' in inputs and inputs['OD'] is not None:
                    self.OD = inputs['OD']
                elif 'thickness' in inputs and inputs['thickness'] is not None:
                    self.thickness = inputs['thickness']
        elif ('OD' in inputs and 'thickness' in inputs):
            self.OD = inputs['OD']
            self.ID = inputs['thickness']
            self.ID = self.OD - self.ID
        else:
            raise Exception('Define atleast ID or OD with thickness to define a pipe segment object') 
            
        self.length = prop.Length() if 'length' not in inputs else prop.Length(inputs['length'])
        
        self.LLLL = prop.Length() if 'LLLL' not in inputs else prop.Length(inputs['LLLL'])
        self.LLL = prop.Length() if 'LLL' not in inputs else prop.Length(inputs['LLL'])
        self.NLL = prop.Length() if 'NLL' not in inputs else prop.Length(inputs['NLL'])
        self.HLL = prop.Length() if 'HLL' not in inputs else prop.Length(inputs['HLL'])
        self.HHLL = prop.Length() if 'HHLL' not in inputs else prop.Length(inputs['HHLL'])

        self.head_type = "ellipsoidal" if "head_type" not in inputs else inputs["ellipsoidal"]

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
        # if self._OD - self._ID <= prop.Length(0):
        #     raise Exception("ID is not less than OD! Change ID or OD or thickness.")
        return self._OD - self._ID
    @thickness.setter
    def thickness(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Length)
        if unit is None:
            unit = self.thickness
        self._OD = self._ID + prop.Length(value, unit)
        self._update_equipment_object(self)

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
    def LLLL(self):
        self = self._get_equipment_object(self)
        return self._LLLL
    @LLLL.setter
    def LLLL(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Length)
        if unit is None:
            unit = self._LLLL.unit
        self._LLLL = prop.Length(value, unit)
        self._update_equipment_object(self)
    
    @property
    def LLL(self):
        self = self._get_equipment_object(self)
        return self._LLL
    @LLL.setter
    def LLL(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Length)
        if unit is None:
            unit = self._LLL.unit
        self._LLL = prop.Length(value, unit)
        self._update_equipment_object(self)
    
    @property
    def NLL(self):
        self = self._get_equipment_object(self)
        return self._NLL
    @NLL.setter
    def NLL(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Length)
        if unit is None:
            unit = self._NLL.unit
        self._NLL = prop.Length(value, unit)
        self._update_equipment_object(self)
    
    @property
    def HLL(self):
        self = self._get_equipment_object(self)
        return self._HLL
    @HLL.setter
    def HLL(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Length)
        if unit is None:
            unit = self._HLL.unit
        self._HLL = prop.Length(value, unit)
        self._update_equipment_object(self)
    
    @property
    def HHLL(self):
        self = self._get_equipment_object(self)
        return self._HHLL
    @HHLL.setter
    def HHLL(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Length)
        if unit is None:
            unit = self._HHLL.unit
        self._HHLL = prop.Length(value, unit)
        self._update_equipment_object(self)
    
    @property
    def head_type(self):
        self = self._get_equipment_object(self)
        return self._head_type
    @head_type.setter
    def head_type(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Length)
        if unit is None:
            unit = self._head_type.unit
        self._head_type = prop.Length(value, unit)
        self._update_equipment_object(self)
    
    @property
    def operating_pressure(self):
        return self.outlet_pressure
    @operating_pressure.setter
    def operating_pressure(self, value):
        self.outlet_pressure = value
    
    @property
    def operating_temperature(self):
        return self.operating_temperature
    @operating_temperature.setter
    def operating_temperature(self, value):
        self.outlet_temperature = value

class _VerticalVessels(_Vessels):
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
    
    @property
    def volume(self):


class _HorizontalVessels(_Vessels):
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
  
#Defining generic class for all types of heat exchangers NEEDS SUPER CLASS WITH MULTI INPUT AND OUTPUT
class _Exchangers(_EquipmentOneInletOutlet):
    def __init__(self, **inputs) -> None:
        """ 
        DESCRIPTION:
            Parent class for all equipment which has primary task to be an 
            Temperature changer of a stream. For e.g. Heater and Cooler.
        
        PARAMETERS:
            temperature_decrease:
                Required: No
                    Type: int/float or Temperature(recommended)
                    Acceptable values: Non-negative integer
                    Default value: based on unit    
                    Description: Temperature decrease of stream in the equipment.
                                 That is decrease from inlet stream to outlet stream.
            
            temperature_increase:
                Required: No
                    Type: int/float or Temperature(recommended)
                    Acceptable values: Non-negative integer
                    Default value: based on unit    
                    Description: Temperature increase of stream in the equipment.
                                 That is increase from inlet stream to outlet stream.
                
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
        if ("temperature_increase" not in inputs and
            "temperature_decrease" not in inputs):
            self.temperature_increase = prop.Temperature(0, 'K')
        elif "temperature_increase" in inputs:
            self.temperature_increase = inputs["temperature_increase"]
        else:
            self.temperature_decrease = inputs["temperature_decrease"] 
        if "energy_in" in inputs:
            self.energy_in = inputs["energy_in"]
        if "energy_out" in inputs:
            self.energy_out = inputs["energy_out"]
        self._efficiency = 100 if 'efficiency' not in inputs else inputs['efficiency']
        
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