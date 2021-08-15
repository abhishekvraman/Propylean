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
    def __repr__(self) -> str:
        return str(self.value) + ' ' + self.unit
    @property
    def unit(self):
        return self._unit
    @unit.setter
    def unit(self, unit):
        self._unit = unit

class Pressure(_Property):
    def __init__(self, value = 1, unit= 'Pa'):
        super().__init__(value,unit) 

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
    def __init__(self, value = 1, unit= 'Kg/s'):
        super().__init__(value,unit)

class VolumetricFlowRat(_Property):
    def __init__(self, value = 1, unit= 'm^3/s'):
        super().__init__(value,unit)

class Power(_Property):
    def __init__(self, value = 1, unit= 'W'):
        super().__init__(value,unit)
