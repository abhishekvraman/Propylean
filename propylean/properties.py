class _Property(object):
    def __init__(self, value = None, unit= None):
        self._value = value
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
        self._value = value
    
    @property
    def unit(self):
        return self._unit
    @unit.setter
    def unit(self, unit):
        self._unit = unit

    def __repr__(self) -> str:
        return str(self.value) + ' ' + self.unit
    
    def __add__(self, other):
        if self.unit != other.unit:
            other.unit = self.unit
        return type(self)(self.value + other.value, self.unit) 
    
    def __sub__(self, other):
        if self.unit!=other.unit:
            other.unit = self.unit
        return type(self)(self.value - other.value, self.unit)
    
    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.unit != other.unit:
                other.unit = self.unit
            return self.value == other.value
        else:
            return False

class Length(_Property):
    def __init__(self, value = 0, unit= 'm'):
        super().__init__(value,unit)
        self.unit = unit

    @_Property.unit.setter
    def unit(self, unit):
        try:
            conversion_factors = {
                                'foot': 1/3.28083,
                                'yard': 1/1.09361,
                                'mile': 1/0.000621371,
                                'cm': 1/100,
                                'inch': 1/39.3701,
                                'km':10^3,
                                'mm': 1/1000,
                                'm': 1
                                }
            self._value =  conversion_factors[self._unit] * self._value / conversion_factors[unit]
            self._unit = unit
        except:
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

class Time(_Property):
    def __init__(self, value = 0, unit= 'sec'):
        super().__init__(value,unit)
        self.unit = unit

    @_Property.unit.setter
    def unit(self, unit):
        try:
            conversion_factors = {
                                'year': (3600*24*30*12),
                                'month': (3600*24*30),
                                'week': (3600*24*7),
                                'day': (3600*24),
                                'hour':3600,
                                'min': 60,
                                'sec': 1
                                }
            self._value =  conversion_factors[self._unit] * self._value / conversion_factors[unit]
            self._unit = unit
        except:
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
    
class Pressure(_Property):
    def __init__(self, value = 101325, unit= 'Pa'):
        super().__init__(value,unit)
        self.unit = unit

    @_Property.unit.setter
    def unit(self, unit):
        try:
            conversion_factors = {'atm': 101320,
                                'bar': 100000,
                                'psi': 6893,
                                'kPa': 1000,
                                'MPa': 1000000,
                                'kg/cm^2': 98070,
                                'ata': 98070,
                                'Torr': 133.3,
                                'mm Hg': 133.3,
                                'in water':2490,
                                'm water': 0.00981,
                                'Pa': 1
                                }
            self._value =  conversion_factors[self._unit] * self._value / conversion_factors[unit]
            self._unit = unit
        except:
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

class Temperature(_Property):
    def __init__(self, value = 298, unit= 'K'):
        super().__init__(value,unit)
        self.unit = unit
    
    @_Property.unit.setter
    def unit(self, unit):
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
        kelvin_self = Temperature(self.value, self.unit)
        kelvin_self.unit = other.unit = 'K'
        sum = Temperature(kelvin_self.value + other.value, 'K')
        sum.unit = self.unit # Converting back to original unit of first.
        return sum 
    
    def __sub__(self, other):
        kelvin_self = Temperature(self.value, self.unit)
        kelvin_self.unit = other.unit = 'K'
        subtraction = Temperature(kelvin_self.value - other.value, 'K')
        subtraction.unit = self.unit # Converting back to original unit of first.
        return subtraction 
        
class MassFlowRate(_Property):
    def __init__(self, value = 0, unit= 'kg/s'):
        super().__init__(value, unit)
        self.unit = unit
    
    @_Property.unit.setter
    def unit(self, unit):
        try:
            conversion_factors = {'g/s': 1000,
                                'kg/min': 1/(1/60),
                                'kg/d': 1*(24*60*60),
                                'kg/h': 1*(60*60),
                                'lb/s': 2.204,
                                'lb/min': 2.204*60,
                                'lb/h': 2.204*(60*60),
                                'lb/d': 2.204*(60*60*24),
                                'ton/h': 0.001*(60*60),
                                'ton/d': 0.001*(60*60*24),
                                'kg/s': 1
                                }
            self._value =  conversion_factors[unit] * self._value / conversion_factors[self._unit]
            self._unit = unit
        except:
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
    
    def __add__(self, other):
        return super().__add__(other)

class MolecularWeigth(_Property):
    def __init__(self, value = 0, unit= 'g/mol'):
        super().__init__(value, unit)
        self.unit = unit
    @_Property.unit.setter
    def unit(self, unit):
        try:
            conversion_factors = {
                                  'kg/mol': 0.001,
                                  'g/mol': 1
                                }
            self._value =  conversion_factors[unit] * self._value / conversion_factors[self._unit]
            self._unit = unit
        except:
            raise Exception('''Selected unit is not supported or a correct unit of Molecular Weight.
                               Following are the supported units:
                               1. g/mol for gram per mol
                               2. kg/mol for kilogram per mol
                               3. TODO...
                               You selected '{}'.
                               '''.format(unit))

class MolarFlowRate(_Property):
    def __init__(self, value = 1, unit= 'mol/s'):
        super().__init__(value,unit)
        self.unit = unit
    
    @_Property.unit.setter
    def unit(self, unit):
        try:
            conversion_factors = {'lbmol/h': 7.93664,
                                'mol/min': 1*60,
                                'mol/d': 1*(24*60*60),
                                'mol/h': 1*(60*60),
                                'lbmol/s': 7.93664*3600,
                                'lbmol/min': 7.93664*60,
                                'lbmol/d': 7.93664*24,
                                'kmol/h': 1/1000*(60*24),
                                'kmol/d': 1000*(60*60*24),
                                'mol/s': 1
                                }
            self._value =  conversion_factors[unit] * self._value / conversion_factors[self._unit]
            self._unit = unit
        except:
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

class VolumetricFlowRate(_Property):
    def __init__(self, value = 1, unit= 'm^3/s'):
        super().__init__(value,unit)
        self.unit = unit
    @_Property.unit.setter
    def unit(self, unit):
        try:
            conversion_factors = {'ft^3/s': 35.3146,
                                'cm^3/s': 1000000,
                                'm^3/min': 60,
                                'm^3/h': 3600,
                                'm^3/d': 3600*24,
                                'ft^3/min': 35.3146*60,
                                'ft^3/h': 35.3146*60*60,
                                'ft^3/d': 35.3146*60*60*24,
                                'gal/s': 264.172,
                                'gal/min': 264.172*60,
                                'gal/h': 264.172*60*60,
                                'gal/d': 264.172*60*60*24,
                                'lit/s': 1000,
                                'lit/min': 60000,
                                'lit/h': 3600000,
                                'lit/d': 3600000*24,
                                'm^3/s': 1
                                }
            self._value =  conversion_factors[unit] * self._value / conversion_factors[self._unit]
            self._unit = unit
        except:
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

class Density(_Property):
    def __init__(self, value = 0, unit= 'kg/m^3'):
        super().__init__(value, unit)
        self.unit = unit
    @_Property.unit.setter
    def unit(self, unit):
        try:
            conversion_factors = {'g/cm^3': 0.001,
                                'lbm/ft^3': 0.062479,
                                'kg/m^3': 1
                                }
            self._value =  conversion_factors[unit] * self._value / conversion_factors[self._unit]
            self._unit = unit
        except:
            raise Exception('''Selected unit is not supported or a correct unit of Density.
                               Following are the supported units:
                               1. kg/m^3 for kilograms per cubic meter
                               2. g/cm^3 for grams per per cubic centimeter
                               3. lbm/ft^3 for pound mass per cubic feet
                               You selected '{}'.
                               '''.format(unit))

class DViscosity(_Property):
    def __init__(self, value = 0, unit= 'Pa-s'):
        super().__init__(value, unit)
        self.unit = unit
    @_Property.unit.setter
    def unit(self, unit):
        try:
            conversion_factors = {'lb/(ft-s)': 1.4881,
                                'cP': 1000,
                                'Pa-s': 1
                                }
            self._value =  conversion_factors[unit] * self._value / conversion_factors[self._unit]
            self._unit = unit
        except:
            raise Exception('''Selected unit is not supported or a correct unit of Dynamic Viscosity.
                               Following are the supported units:
                               1. Pa-s for Pascal second
                               2. cP for centipoise
                               3. lb/(ft-s) for pound mass per cubic feet
                               You selected '{}'.
                               '''.format(unit))

class Power(_Property):
    def __init__(self, value = 0, unit= 'W'):
        super().__init__(value,unit)
        self.unit = unit

    @_Property.unit.setter
    def unit(self, unit):
        try:
            conversion_factors = {'BTU/h': 0.293071070172222,
                                'BTU/min': 17.5842642103333,
                                'BTU/s': 1055.05585262,
                                'cal/h': 0.001163,
                                'cal/s': 4.1868,
                                'erg/h': 2.777778E-11,
                                'erg/min': 1.666667E-9,
                                'erg/s': 1E-7,
                                'hp': 735.49875,
                                'MMBTU/h': 293071.070172222,
                                'MMBTU/min': 17584264.2103333,
                                'MMBTU/s': 1055055852.62,
                                'kW': 1000,
                                'MW': 1000000,
                                'GW': 1000000000,
                                'TW': 1000000000000,
                                'kWh/d': 41.667,
                                'MWh/d': 41666.67,
                                'GWh/d': 41666666.67,
                                'TWh/d': 41666666666.67,
                                'W': 1
                                }
            self._value = conversion_factors[self._unit] * self._value / conversion_factors[unit]
            self._unit = unit
        except:
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

class Components(object):
    def __init__(self, fractions=None, type="mass"):
        self.fractions = fractions
        self.type = type