class _Property:
    def __init__(self, value = None, unit= None):
        self._value = value
        self._unit = unit
    
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
            raise Exception('Selected unit is not supported or a correct unit of Length.')

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
            raise Exception('Selected unit is not supported or a correct unit of Time.')
    
class Pressure(_Property):
    def __init__(self, value = 1, unit= 'Pa'):
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
                                'mm water': 9.81,
                                'Pa': 1
                                }
            self._value =  conversion_factors[self._unit] * self._value / conversion_factors[unit]
            self._unit = unit
        except:
            raise Exception('Selected unit is not supported or a correct unit of Pressure.')

class Temperature(_Property):
    def __init__(self, value = 1, unit= 'K'):
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
        else:
            raise Exception('Selected unit is not supported or a correct unit of Temperature.')

class MassFlowRate(_Property):
    def __init__(self, value = 1, unit= 'kg/s'):
        super().__init__(value,unit)
        self.unit = unit
    
    @_Property.unit.setter
    def unit(self, unit):
        try:
            conversion_factors = {'g/s': 1000,
                                'kg/min': 1/60,
                                'kg/d': 1/(24*60*60),
                                'kg/h': 1/(60*60),
                                'lb/s': 1/2.204,
                                'lb/min': 1/(2.204*60),
                                'lb/h': 1/(2.204*60*60),
                                'lb/d': 1/(2.204*60*60*24),
                                'ton/h': 1000/(60*24),
                                'ton/d': 1000/(60*60*24),
                                'kg/s': 1
                                }
            self._value =  conversion_factors[self._unit] * self._value / conversion_factors[unit]
            self._unit = unit
        except:
            raise Exception('Selected unit is not supported or a correct unit of Mass Flow Rate.')

class VolumetricFlowRate(_Property):
    def __init__(self, value = 1, unit= 'm^3/s'):
        super().__init__(value,unit)
        self.unit = unit
    @_Property.unit.setter
    def unit(self, unit):
        try:
            conversion_factors = {'g/s': 1000,
                                'kg/min': 1/60,
                                'kg/d': 1/(24*60*60),
                                'kg/h': 1/(60*60),
                                'lb/s': 1/2.204,
                                'lb/min': 1/(2.204*60),
                                'lb/h': 1/(2.204*60*60),
                                'lb/d': 1/(2.204*60*60*24),
                                'ton/h': 1000/(60*24),
                                'ton/d': 1000/(60*60*24),
                                'kg/s': 1
                                }
            self._value =  conversion_factors[self._unit] * self._value / conversion_factors[unit]
            self._unit = unit
        except:
            raise Exception('Selected unit is not supported or a correct unit of Volume Flow Rate.')

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
            self._unit = 'W'
            raise Exception('Selected unit is not supported or a correct unit of Power. Using W instead.')
