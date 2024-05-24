from propylean.validators import _Validators
from propylean.constants import ConversionFactors
from warnings import warn

class _Property(object):
    def __init__(self, value=None, unit=None, min_val=None, max_val=None):
        _Validators.validate_arg_prop_value_type("value", value, (int, float))
        _Validators.validate_arg_prop_value_type("unit", unit, str)
        self._value = value
        self._min_val = min_val
        self._max_val = max_val
        self._unit = unit
    
    def __eq__(self, other):
        if (isinstance(other, _Property) and
            self.value == other.value and
            self.unit == other.unit):
                return True
        return False
    
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, value):
        _Validators.validate_arg_prop_value_type("value", value, (int, float))
        self._value = value
    
    @property
    def max_val(self):
        return self._max_val if self._max_val is not None else self._value
    @max_val.setter
    def max_val(self, value):
        _Validators.validate_arg_prop_value_type("max_val", value, (int, float))
        self._max_val = value
    
    @property
    def min_val(self):
        return self._min_val if self._min_val is not None else self._value
    @min_val.setter
    def min_val(self, value):
        _Validators.validate_arg_prop_value_type("min_val", value, (int, float))
        self._min_val = value
    
    @property
    def unit(self):
        return self._unit
    @unit.setter
    def unit(self, unit):
        _Validators.validate_arg_prop_value_type("unit", unit, (str))
        self._unit = unit

    def __repr__(self) -> str:
        return str(self.value) + ' ' + self.unit
    
    def __add__(self, other):
        if self.unit != other.unit:
            other.unit = self.unit
        return type(self)(value=self.value + other.value, 
                          unit=self.unit,
                          min_val=self.max_val + other.min_val,
                          max_val=self.max_val + other.max_val)
    
    def __sub__(self, other):
        if self.unit != other.unit:
            other.unit = self.unit
        return type(self)(value=self.value - other.value,
                          unit=self.unit,
                          min_val=self.min_val - other.min_val, 
                          max_val=self.max_val - other.min_val)
    
    def __truediv__(self, other):
        if self.unit != other.unit:
            other.unit = self.unit
        return self.value / other.value

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.unit != other.unit:
                other.unit = self.unit
            return self.value == other.value
        else:
            return False
    
    def _convert_values_for_unit_change(self, unit, invert_factor=False):
        """
        Internal function to convert all values (min, norm and max values) for any unit change.
        """
        conversion_factor = getattr(ConversionFactors, self.__class__.__name__.upper())
        conversion_factor = conversion_factor[unit] / conversion_factor[self._unit]
        if invert_factor:
            conversion_factor = 1 / conversion_factor
        if self._value is not None:
            self._value *= conversion_factor
        if self._max_val is not None:
            self._max_val *= conversion_factor
        if self._min_val is not None:
            self._min_val *= conversion_factor 
        self._unit = unit

class Length(_Property):
    def __init__(self, value=0, unit='m', min_val=None, max_val=None):
        super().__init__(value, unit, max_val=max_val, min_val=min_val)
        self.unit = unit

    @_Property.unit.setter
    def unit(self, unit):
        _Validators.validate_arg_prop_value_type("unit", unit, (str))
        try:
            self._convert_values_for_unit_change(unit, True)
        except KeyError:
            raise Exception('''Selected unit is not supported or a correct unit of Length.
                               Supported units are:
                               1. m for meters
                               2. mm for millimeters
                               3. km for Kilometers
                               4. cm for centimeters
                               5. inch
                               6. mile
                               7. yard
                               8. foot
                               You selected '{}'.
                               '''.format(unit))
        except:
            raise

class Time(_Property):
    def __init__(self, value=0, unit='sec', min_val=None, max_val=None):
        super().__init__(value, unit, max_val=max_val, min_val=min_val)
        self.unit = unit

    @_Property.unit.setter
    def unit(self, unit):
        _Validators.validate_arg_prop_value_type("unit", unit, (str))
        try:
            self._convert_values_for_unit_change(unit, True)
        except KeyError:
            raise Exception('''Selected unit is not supported or a correct unit of Time.
                               Supported units are:
                               1. s for seconds
                               2. min for minutes
                               3. hour
                               4. day
                               5. week
                               6. month
                               7. year
                               You selected '{}'.
                               '''.format(unit))
        except:
            raise
    
class Pressure(_Property):
    def __init__(self, value=101325, unit='Pa', min_val=None, max_val=None):
        super().__init__(value, unit, max_val=max_val, min_val=min_val)
        self.unit = unit

    @_Property.unit.setter
    def unit(self, unit):
        _Validators.validate_arg_prop_value_type("unit", unit, (str))
        try:
            self._convert_values_for_unit_change(unit, True)
        except KeyError:
            raise Exception('''Selected unit is not supported or a correct unit of Length.
                               Supported units are:
                               1. Pa for Pascals
                               2. m water for meters of water column
                               3. in water for inches of water column
                               4. mm Hg for millimeters of Mercury
                               5. Torr
                               6. ata
                               7. kg/cm^2 for kilogram per square centimeter 
                               8. MPa for Mega Pascal
                               9. kPa for Kilo Pascal
                               10. psi for Pound per square inch
                               11. bar
                               12. atm for Atmospheres
                               You selected '{}'.
                               '''.format(unit))
        except:
            raise

class Temperature(_Property):
    def __init__(self, value=298, unit='K', min_val=None, max_val=None):
        super().__init__(value, unit, max_val=max_val, min_val=min_val)
        self.unit = unit
    
    @_Property.unit.setter
    def unit(self, unit):
        _Validators.validate_arg_prop_value_type("unit", unit, (str))
        if unit in ['K', 'C', 'F', 'R']:
            while unit != self._unit:
                if self._unit == 'K':
                    self._value -= 273.15
                    self._unit = 'C'
                    if unit == self._unit:
                        break
                if self._unit == 'C':
                    self._value = self._value * 9/5 + 32
                    self._unit = 'F'
                    if unit == self._unit:
                        break
                if self._unit == 'F':
                    self._value = self._value  + 459.67
                    self._unit = 'R'
                    if unit == self._unit:
                        break
                if self._unit == 'R':
                    self._value = self._value  * 5 / 9
                    self._unit = 'K'
                    if unit == self._unit:
                        break
            self._value = round(self.value,5)
        else:
            raise Exception('''Selected unit is not supported or a correct unit of Temperature.
                               Supported units are:
                               1. K for Kelvin
                               2. C for Degrees Celsius
                               3. F for Degree Fahrenheit
                               4. R for Degree Rankine
                               You selected '{}'.
                               '''.format(unit))

    def __add__(self, other):
        old_unit = self.unit
        self.unit = other.unit
        addition = self.value + other.value
        addition = Temperature(addition, other.unit)
        self.unit = old_unit
        addition.unit = old_unit
        return addition
    
    def __sub__(self, other):
        old_unit = self.unit
        self.unit = other.unit
        subtraction = self.value - other.value
        subtraction = Temperature(subtraction, other.unit)
        self.unit = old_unit
        subtraction.unit = old_unit
        return subtraction
        
class MassFlowRate(_Property):
    def __init__(self, value=0, unit='kg/s', min_val=None, max_val=None):
        super().__init__(value, unit, max_val=max_val, min_val=min_val)
        self.unit = unit
    
    @_Property.unit.setter
    def unit(self, unit):
        _Validators.validate_arg_prop_value_type("unit", unit, (str))
        try:
            self._convert_values_for_unit_change(unit)
        except KeyError:
            raise Exception('''Selected unit is not supported or a correct unit of Mass Flow Rate.
                               Supported units are:
                               1. kg/s for kilogram per seconds
                               2. kg/min for kilogram per minutes
                               3. kg/h for kilogram per hour
                               4. kg/d for kilogram per day
                               5. g/s for gram per second
                               6. lb/s for pound per second
                               7. lb/min for pound per minutes
                               8. lb/h for pound per hour
                               9. lb/d for pound per day
                               10. ton/d for metric ton per day
                               11. ton/h for metric ton per hour
                               You selected '{}'.
                               '''.format(unit))
        except:
            raise
    
    def __add__(self, other):
        return super().__add__(other)

class Mass(_Property):
    def __init__(self, value=0, unit='kg', min_val=None, max_val=None):
        super().__init__(value, unit, max_val=max_val, min_val=min_val)
        self.unit = unit
    
    @_Property.unit.setter
    def unit(self, unit):
        _Validators.validate_arg_prop_value_type("unit", unit, (str))
        try:
            self._convert_values_for_unit_change(unit)
        except KeyError:
            raise Exception('''Selected unit is not supported or a correct unit of Mass Flow Rate.
                               Supported units are:
                               1. kg for kilogram 
                               2. g for gram
                               3. lb for pound
                               4. ton for metric ton
                               You selected '{}'.
                               '''.format(unit))
        except:
            raise
    
    def __add__(self, other):
        return super().__add__(other)

class MolecularWeigth(_Property):
    def __init__(self, value=0, unit='g/mol', min_val=None, max_val=None):
        super().__init__(value, unit, max_val=max_val, min_val=min_val)
        self.unit = unit
    @_Property.unit.setter
    def unit(self, unit):
        _Validators.validate_arg_prop_value_type("unit", unit, (str))
        try:
            self._convert_values_for_unit_change(unit)
        except KeyError:
            raise Exception('''Selected unit is not supported or a correct unit of Molecular Weight.
                               Following are the supported units:
                               1. g/mol for gram per mol
                               2. kg/mol for kilogram per mol
                               You selected '{}'.
                               '''.format(unit))
        except:
            raise

class MolarFlowRate(_Property):
    def __init__(self, value=1, unit='mol/s', min_val=None, max_val=None):
        super().__init__(value, unit, max_val=max_val, min_val=min_val)
        self.unit = unit
    
    @_Property.unit.setter
    def unit(self, unit):
        _Validators.validate_arg_prop_value_type("unit", unit, (str))
        try:
            self._convert_values_for_unit_change(unit)
        except KeyError:
            raise Exception('''Selected unit is not supported or a correct unit of Molar Flow Rate.
                               Supported units are:
                               1. mol/s for moles per seconds
                               2. mol/min for moles per minutes
                               3. mol/h for moles per hour
                               4. mol/d for moles per day
                               5. lbmol/s for poundmole per second
                               6. lbmol/min for poundmole per minute
                               7. lbmol/d for poundmole per day
                               8. kmol/h for kilomole per hour
                               9. kmol/d for kilomole per day
                               You selected '{}'.
                               '''.format(unit))
        except:
            raise

class VolumetricFlowRate(_Property):
    def __init__(self, value = 1, unit='m^3/s', min_val=None, max_val=None):
        super().__init__(value, unit, max_val=max_val, min_val=min_val)
        self.unit = unit
    @_Property.unit.setter
    def unit(self, unit):
        _Validators.validate_arg_prop_value_type("unit", unit, (str))
        try:
            self._convert_values_for_unit_change(unit)
        except KeyError:
            raise Exception('''Selected unit is not supported or a correct unit of Volumetric Flow Rate.
                               Following are the supported units:
                               1. m^3/s for cubic meter per second
                               2. ft^3/s for cubic feet per second
                               3. cm^3/s for cubic centimeter per second
                               4. m^3/min for cubic meter per minute
                               5. m^3/h for cubic meter per hour
                               6. m^3/d for cubic meter per day,
                               7. ft^3/min for cubic feet per minute,
                               8. ft^3/h for cubic feet per hour
                               9. ft^3/d for cubic feet per day
                               10. gal/s for US Gallons per second
                               11. gal/min for US Gallon per minute
                               12. gal/h for US Gallon per hour
                               13. gal/d for US Gallin per day
                               14. lit/s for Liters per second
                               15. lit/min for Liters per minute
                               16. lit/h for Liters per hour
                               17. lit/d  for Liters per day
                               You selected '{}'.
                               '''.format(unit))
        except:
            raise

class Volume(_Property):
    def __init__(self, value = 0, unit= 'm^3', min_val=None, max_val=None):
        super().__init__(value, unit, max_val=max_val, min_val=min_val)
        self.unit = unit
    @_Property.unit.setter
    def unit(self, unit):
        _Validators.validate_arg_prop_value_type("unit", unit, (str))
        try:
            self._convert_values_for_unit_change(unit)
        except KeyError:
            raise Exception('''Selected unit is not supported or a correct unit of Volumetric Flow Rate.
                               Following are the supported units:
                               1. m^3 for cubic meter
                               2. ft^3 for cubic feet
                               3. cm^3 for cubic centimeter
                               4. gal for US Gallons
                               5. lit for Liters
                               You selected '{}'.
                               '''.format(unit))
        except:
            raise

class Density(_Property):
    def __init__(self, value = 0, unit= 'kg/m^3', min_val=None, max_val=None):
        super().__init__(value, unit, max_val=max_val, min_val=min_val)
        self.unit = unit
    @_Property.unit.setter
    def unit(self, unit):
        _Validators.validate_arg_prop_value_type("unit", unit, (str))
        try:
            self._convert_values_for_unit_change(unit)
        except KeyError:
            raise Exception('''Selected unit is not supported or a correct unit of Density.
                               Following are the supported units:
                               1. kg/m^3 for kilograms per cubic meter
                               2. g/cm^3 for grams per per cubic centimeter
                               3. lbm/ft^3 for pound mass per cubic feet
                               You selected '{}'.
                               '''.format(unit))
        except:
            raise

class DViscosity(_Property):
    def __init__(self, value = 0, unit= 'Pa-s', min_val=None, max_val=None):
        super().__init__(value, unit, max_val=max_val, min_val=min_val)
        self.unit = unit
    @_Property.unit.setter
    def unit(self, unit):
        _Validators.validate_arg_prop_value_type("unit", unit, (str))
        try:
            self._convert_values_for_unit_change(unit)
        except KeyError:
            raise Exception('''Selected unit is not supported or a correct unit of Dynamic Viscosity.
                               Following are the supported units:
                               1. Pa-s for Pascal second
                               2. cP for centipoise
                               3. lb/(ft-s) for pound mass per cubic feet
                               You selected '{}'.
                               '''.format(unit))
        except:
            raise

class Power(_Property):
    def __init__(self, value = 0, unit= 'W', min_val=None, max_val=None):
        super().__init__(value, unit, max_val=max_val, min_val=min_val)
        self.unit = unit

    @_Property.unit.setter
    def unit(self, unit):
        _Validators.validate_arg_prop_value_type("unit", unit, (str))
        try:
            self._convert_values_for_unit_change(unit, True)
        except KeyError:
            raise Exception('''Selected unit is not supported or a correct unit of Power. 
                               Following units are supported:
                               1. W for Watts
                               2. BTU/h for British Termal Units per hour
                               3. BTU/min for Brititsh Termal Units per minutes
                               4. BTU/s for British Termal Units per second
                               5. cal/h for calories per hour
                               6. cal/s for calories per second
                               7. erg/h for ergs per hour
                               8. erg/min for ergs per minutes
                               9. erg/s for ergs per second
                               10. hp for Horse Power
                               11. MMBTU/h for Million Metric BTU/h
                               12. MMBTU/min
                               13. MMBTU/s
                               14. kW for kilo watts
                               15. MW for mega watts
                               16. GW for giga watts
                               17. TW for tera watts
                               18. kWh/d for kilo watt hours per day
                               19. MWh/d for Mega watt hours per day
                               20. GWh/d for Giga watt hour per day
                               21. TWh/d for Tera watt hour per day
                               You selected '{}'.
                               '''.format(unit))
        except:
            raise

class Frequency(_Property):
    def __init__(self, value=0, unit='Hz', min_val=None, max_val=None):
        super().__init__(value, unit, max_val=max_val, min_val=min_val)
        self.unit = unit
    @_Property.unit.setter
    def unit(self, unit):
        _Validators.validate_arg_prop_value_type("unit", unit, (str))
        try:
            self._convert_values_for_unit_change(unit)
        except KeyError:
            raise Exception('''Selected unit is not supported or a correct unit of Dynamic Viscosity.
                               Following are the supported units:
                               1. Hz for Hertz(cycle per second)
                               2. /min for cylce per minute
                               3. /hour for cycle per hour
                               You selected '{}'.
                               '''.format(unit))
        except:
            raise

class Components(object):
    def __init__(self, fractions=None, type="mass"):
        if fractions is not None:
            _Validators.validate_arg_prop_value_type("fractions", fractions, (dict))
        _Validators.validate_arg_prop_value_type("type", type, (str))        
        self.fractions = fractions
        self.type = type
    def __eq__(self, other):
        if self.type==other.type and self.fractions==other.fractions:
            return True
        return False

class Dimensionless(_Property):
    def __init__(self, value=None, name=None, min_val=None, max_val=None):
        super().__init__(value=value, unit=None, max_val=max_val, min_val=min_val)
        self._name = name
    
    @property
    def name(self):
        return self._name if self._name is not None else str(self.__class__.__name__)
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def unit(self):
        return None
    @unit.setter
    def unit(self, unit):
        raise Exception("{} does not have unit.".format(self.name))
    
    def __repr__(self) -> str:
        return "{} with value {}".format(self.name, self.value)

class Efficiency(Dimensionless):
    def __init__(self, value=1, min_val=0, max_val=1):
        super().__init__(value=value, name="Efficiency", max_val=max_val, min_val=min_val)
        if value < 0 or min_val < 0 or max_val < 0:
            raise Exception("Provide a non-negative value for efficiency.")
        else:
            if value > 1:
                self.value =  value/100
                warn("Efficiency value set to {} considering value provided in percent.".format(value/100))
            if max_val > 1:
                self.max_val = max_val/100
                warn("Efficiency max_val set to {} considering value provided in percent.".format(max_val/100))
            if min_val > 1:
                self.min_val = min_val/100
                warn("Efficiency min_val set to {} considering value provided in percent.".format(min_val/100))