from propylean.equipments.abstract_equipment_classes import _EquipmentOneInletOutlet, _EquipmentMultipleInletOutlet
import propylean.properties as prop
from propylean.constants import Constants
import pandas as pd
from math import pi, sqrt, acos

#Defining generic class for all types of pressure changers like Pumps, Compressors and Expanders.
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
    
#Defining generic class for all types of vessels. 
class _Vessels(_EquipmentOneInletOutlet):
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
                Default value: 0 m   
                Description: Internal diameter of the vessel.
            
            OD:
                Required: No
                Type: int or float or Length(recommended)
                Acceptable values: Non-negative integer
                Default value: 0 m    
                Description: Outer diameter of the vessel.

            thickness:
                Required: No
                Type: int or float or Length(recommended)
                Acceptable values: Non-negative integer
                Default value: 0 m    
                Description: thickness of the vessel.
            
            length:
                Required: No
                Type: int or float or Length(recommended)
                Acceptable values: Non-negative integer
                Default value: 0 m   
                Description: tan-line length of the vessel.
            
            LLL, LLLL, HLL, NLL and HHLL:
                Required: No
                Type: int or float or Length(recommended)
                Acceptable values: Non-negative integer
                Default value: 0 m    
                Description: Low Liquid Level(LLL), Low-Low Liquid Level(LLLL), High Liquid Level(HLL),
                             Normal Liquid Level(NLL), and High-high Liquid Level.
            
            head_type:
                Required: No
                Type: String
                Acceptable values: {head_types}
                Default value: elliptical    
                Description: Type of head for the vessel.
            
            main_fluid:
                Required: No
                Type: String
                Acceptable values: ["liquid", "gas"]
                Default value: liquid    
                Description: Type of fluid which the vessel stores.
            
            is_blanketed:
                Required: No
                Type: Boolean
                Default value: False
                Description: Specifies if the vessel is blanketed or not.
            
        RETURN VALUE:
            Type: _Vessels
            Description: object with all _EquipmentOneInletOutlet and other vessel related properties.
        
        PROPERTIES:
            operating_pressure:
                Type: int or float or Pressure(recommended)  
                Acceptable values: Any
                Default value: 101325 Pa  
                Description: Operating pressure of the vessel. operating_pressure is
                             considered equal to outlet_pressure and can be considered as
                             alias of each other. Setting or getting one effects the other.
            
            operating_temperature:
                Type: int or float or Pressure(recommended)   
                Acceptable values: Any
                Default value: 298 K 
                Description: Operating temperature of the vessel. operating_temperature is
                             considered equal to outlet_temperature and can be considered as
                             alias of each other. Setting or getting one effects the other.

            vessel_volume:
                Type: int or float or Volume(recommended)   
                Acceptable values: Any
                Default value: 0 m^3 
                Description:Total volumetric space of the vessel including heads.
            
            liquid_level:
                Type: int or float or Length(recommended)
                Acceptable values: Non-negative integer
                Default value: 0 m   
                Description: liquid level of the vessel.
        
        ERROR RAISED:
            Type:
            Description: 
        
        SAMPLE USE CASES:
            >>>  class AwesomeReactor(_Vessels):
            >>>     def __init__(**kwargs):
            >>>         some_property = 20
                
    """.format(head_types=Constants.HEAD_TYPES)
        super().__init__(**inputs)
        self._ID = prop.Length()
        self._OD = prop.Length()
        self._length = prop.Length()
        self._LLLL = prop.Length()
        self._LLL = prop.Length()
        self._NLL = prop.Length()
        self._HLL = prop.Length()
        self._HHLL = prop.Length()
        self.blanketing = None
        self._material = 1
        self.operating_pressure = prop.Pressure()
        self.operating_temperature = prop.Temperature()
        if ('ID' in inputs and inputs['ID'] is not None):
                self.ID = inputs['ID']
                if 'OD' in inputs and inputs['OD'] is not None:
                    self.OD = inputs['OD']
                elif 'thickness' in inputs and inputs['thickness'] is not None:
                    self.thickness = inputs['thickness']
                else:
                    self.thickness = self.calculate_thickness()
                
        elif ('OD' in inputs and 'thickness' in inputs):
            self.OD = inputs['OD']
            self.ID = inputs['thickness']
            self.ID = self.OD - self.ID
        
        self.length = prop.Length() if 'length' not in inputs else inputs['length']
        
        self.LLLL = prop.Length() if 'LLLL' not in inputs else inputs['LLLL']
        self.LLL = prop.Length() if 'LLL' not in inputs else inputs['LLL']
        self.NLL = prop.Length() if 'NLL' not in inputs else inputs['NLL']
        self.liquid_level = prop.Length() if 'NLL' not in inputs else inputs['NLL']
        self.HLL = prop.Length() if 'HLL' not in inputs else inputs['HLL']
        self.HHLL = prop.Length() if 'HHLL' not in inputs else inputs['HHLL']

        self._head_type = "torispherical" if "head_type" not in inputs else inputs["head_type"]
        
        if "is_blanketed" in inputs and inputs["is_blanketed"]:
            self.blanketing = _Blanketing(tag=self.tag)
            self.blanketing.inlet_pressure = self.operating_pressure

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
    
    def calculate_thickness(self):
        #TODO: Update calculations based on design pressure.
        return prop.Length(0.01)

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
    @length.deleter
    def length(self):
        self = self._get_equipment_object(self)
        del self._length
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
    @LLLL.deleter
    def LLLL(self):
        self = self._get_equipment_object(self)
        del self._LLLL
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
    @LLL.deleter
    def LLL(self):
        self = self._get_equipment_object(self)
        del self._LLL
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
    @NLL.deleter
    def NLL(self):
        self = self._get_equipment_object(self)
        del self._NLL
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
    @HLL.deleter
    def HLL(self):
        self = self._get_equipment_object(self)
        del self._HLL
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
    @HHLL.deleter
    def HHLL(self):
        self = self._get_equipment_object(self)
        del self._HHLL
        self._update_equipment_object(self)

    @property
    def head_type(self):
        self = self._get_equipment_object(self)
        return self._head_type
    @head_type.setter
    def head_type(self, value):
        self = self._get_equipment_object(self)
        if value not in Constants.HEAD_TYPES:
            raise Exception("""Head type '{0}', not supported. Supported types are:\n
            {1}""".format(value, Constants.HEAD_TYPES))
        self._head_type = value
        self._update_equipment_object(self)
    @head_type.deleter
    def head_type(self):
        self = self._get_equipment_object(self)
        del self._head_type
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
                    ''' 
        if value not in range(1, 6):
            raise Exception(materials)
        self._material = value
        self._update_equipment_object(self)

    @property
    def main_fluid(self):
        self = self._get_equipment_object(self)
        return self._main_fluid
    @main_fluid.setter
    def main_fluid(self, value):
        self = self._get_equipment_object(self)
        self._main_fluid = value
        self._update_equipment_object(self)

    @property
    def pressure_drop(self):
        g = Constants.g
        self = self._get_equipment_object(self)
        if ((self._inlet_energy_stream_index is not None or
             self._outlet_energy_stream_index is not None) and 
             self.main_fluid == "liquid"):
            is_inlet = False if self._inlet_material_stream_index is None else True
            density = self._connected_stream_property_getter(is_inlet, "material", "density")
            density.unit = "kg/m^3"
            pd = density.vaule * g * self.liquid_level.value
            return prop.Pressure(pd)
        return self._pressure_drop
    @pressure_drop.setter
    def pressure_drop(self, value):
        if ((self._inlet_energy_stream_index is not None or
             self._outlet_energy_stream_index is not None) and 
             self.main_fluid == "liquid"):
            raise Exception("Pressure drop cannot be set for vessels with main fluid as liquid.")
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Pressure)
        if unit is None:
            unit = self._pressure_drop.unit
        self._pressure_drop = prop.Pressure(value, unit)
        self._outlet_pressure =  self._inlet_pressure - self._pressure_drop
        self._update_equipment_object(self)
               
    @property
    def operating_pressure(self):
        return self.inlet_pressure
    @operating_pressure.setter
    def operating_pressure(self, value):
        self.inlet_pressure = value
        if self.blanketing is not None:
            self.blanketing.inlet_pressure = value
    
    @property
    def operating_temperature(self):
        return self.inlet_temperature
    @operating_temperature.setter
    def operating_temperature(self, value):
        self.inlet_temperature = value
        if self.blanketing is not None:
            self.blanketing.inlet_temperature = value
    
    @property
    def vessel_volume(self):
        D = self.ID.value
        L = self.length.value
        t = self.thickness.value
        cylinder_volume = pi * D * D * L / 4
        # Volume of both heads.
        head_volume = 0
        if self.head_type == "hemispherical":
            # Spherical heads are not exact sphere but part of it.
            # Dish depth = D/2
            head_volume = pi * (D ** 3) / 6 
        elif self.head_type == "elliptical":
            # Dish depth = D/4
            head_volume = pi * (D ** 3) / 12
        elif self.head_type == "torispherical":
            Rc = D + t
            Rk = 3 * t
            z = Rc - sqrt((Rc - Rk)**2 - (self.OD.value/2 - t - Rk)**2)
            head_volume = 0.9 * 4 * pi * Rc * Rc * z / 3 
        return prop.Volume(cylinder_volume + head_volume, "m^3")

    @property
    def liquid_level(self):
        self = self._get_equipment_object(self)
        return self._liquid_level
    @liquid_level.setter
    def liquid_level(self, value):
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Length)
        if unit is None:
            unit = self._liquid_level.unit
        self._liquid_level = prop.Length(value, unit)
        self._update_equipment_object(self)

    def get_inventory(self, type="volume"):
        self = self._get_equipment_object(self)
        if self.main_fluid == "gas":
            if type == "volume":
                liquid_volume = self._get_liquid_volume()
                gas_volume = self.vessel_volume - liquid_volume
                return gas_volume 
            else:
                is_inlet = False if self._inlet_material_stream_index is None else True
                density = self._connected_stream_property_getter(is_inlet, "material", "density_g")
                return prop.Mass(self.inventory().value * density) 
        else:
            if type == "volume":
                return self._get_liquid_volume()
            else:
                is_inlet = False if self._inlet_material_stream_index is None else True
                density = self._connected_stream_property_getter(is_inlet, "material", "density_l")
                mass = self._get_liquid_volume().value * density.value
    
class _VerticalVessels(_Vessels):
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
    
    def _get_head_volume(self):
        head_volume = 0
        D = self.ID.value
        if self.head_type == "hemispherical":
            # Dish depth = D/2
            head_volume = pi * (D ** 3) / 12
        elif self.head_type == "elliptical":
            # Dish depth = D/4
            head_volume = pi * (D ** 3) / 24
        elif self.head_type == "torispherical":
            Rc = (self.ID + self.thickness).value
            Rk = 3 * self.thickness.value
            z = Rc - sqrt((Rc - Rk)**2 - (self.OD.value/2 - self.thickness.value - Rk)**2)
            head_volume = 0.9 * 4 * pi * Rc * Rc * z / 3
        return prop.Volume(head_volume) 

    def _get_cylinder_volume(self):
        volume = pi * self.ID.value**2 * self.liquid_level.value / 4
        return prop.Volume(volume)
    
    def _get_liquid_volume(self):
        head_volume = self._get_head_volume()
        cylinder_volume = self._get_cylinder_volume()
        return cylinder_volume + head_volume

class _HorizontalVessels(_Vessels):
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
    
    def _get_head_volume(self):
        self = self._get_equipment_object(self)
        C = 0
        if self.head_type == "hemispherical":
            C = 1
        elif self.head_type == "elliptical":
            C = 0.5
        elif self.head_type == "torispherical":
            Rk = 3 * self.thickness.value
            t_by_Dext = self.thickness/self.OD
            C = 0.30939 + 1.7197 * (Rk - 0.06 * self.OD.value)/self.ID.value - 0.16116 * t_by_Dext + 0.98997 * t_by_Dext**2
        head_volume = self._get_head_volume_by_type(C)
        return prop.Volume(head_volume) 
    
    def _get_head_volume_by_type(self, C):
        head_volume = (self.ID.value ** 3) * pi 
        H_by_ID = self.liquid_level / self.ID
        head_volume *= 3 * H_by_ID**2 - 2 * H_by_ID**3
        head_volume /= 12
        head_volume *= C
        return head_volume

    def _get_cylinder_volume(self):
        self = self._get_equipment_object(self)
        volume = 0
        # alpha = cos-1(1-H/R)
        R = self.ID.value / 2
        H = self.liquid_level.value
        L = self.length.value
        radians = 1 - H / R
        alpha = acos(radians)
        volume = L * ((R ** 2) * alpha - (R - H) * sqrt(2*R*H - H*H))
        return prop.Volume(volume)
    
    def _get_liquid_volume(self):
        head_volume = self._get_head_volume()
        cylinder_volume = self._get_cylinder_volume()
        return cylinder_volume + head_volume + head_volume

class _SphericalVessels(_Vessels):
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        del self.head_type
        del self.length
    
    @property
    def vessel_volume(self):
        self = self._get_equipment_object(self)
        D = self.ID.value
        volume = 2 * self._get_hemisphere_volume(D, D/2)
        return prop.Volume(volume)
    def _get_liquid_volume(self):
        self = self._get_equipment_object(self)
        H = self.liquid_level.value
        D = self.ID.value
        if H <= D/2:
            volume = self._get_hemisphere_volume(D, H)
        else:
            volume = self._get_hemisphere_volume(D, D/2)
            volume -=  self._get_hemisphere_volume(D, H)
        return prop.Volume(volume)
    
    def _get_hemisphere_volume(self, D, H):
        return pi * H**2 *(1.5 * D - H) / 3

class _Blanketing(_EquipmentOneInletOutlet):
    def __init__(self, **inputs) -> None:
        inputs["tag"] += "_blanketing" 
        super().__init__(**inputs)
        del self.energy_in
        del self.energy_out
    
    def __repr__(self):
        return "Blanketing with tag: " + self.tag
    @property
    def pressure_drop(self):
        return prop.Pressure(0)
    @pressure_drop.setter
    def pressure_drop(self, value):
        raise Exception("Pressure drop setting for blanketing is not allowed as it is an intermittent process.")
    
    @property
    def temperature_increase(self):
        return prop.Temperature(0, "K")
    @temperature_increase.setter
    def temperature_increase(self, value):
        raise Exception("Temperature increase setting for blanketing is not allowed as it is an intermittent process.")
        
    @property
    def temperature_decrease(self):
        return prop.Temperature(0, "K")
    @temperature_decrease.setter
    def temperature_decrease(self, value):
        raise Exception("Temperature decrease setting for blanketing is not allowed as it is an intermittent process.")
        

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