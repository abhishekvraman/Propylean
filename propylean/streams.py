from thermo.chemical import Chemical
        
class EnergyStream:
    def __init__(self, value= 0, unit= 'kW', tag= None, 
                 to_equipment_tag= None, from_equipment_tag= None):
        self._value = value
        self._unit = unit
        self.tag = tag
        self.to_equipment_tag = to_equipment_tag
        self.from_equipment_tag = from_equipment_tag
        a = self.get_value_in('W') #To test if the energy unit is supported  

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
        if self._value != 0:
            self.value = self.get_value_in(unit)
        self._unit = unit  
    
    def get_value_in(self, unit):
        if unit == self._unit:
            return self.value
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
            return conversion_factors[self._unit] * self._value / conversion_factors[unit]
        except:
            self._unit = 'kW'
            raise Exception('Selected unit is not supported or a correct unit of Power. Using kW instead.')

class MaterialStream:
    def __init__(self, mass_flow_rate = 0,
                 Pressure = 1,
                 Temperature = 25,
                 tag = None):
                 self.tag = tag
                 self.mass_flow_rate = mass_flow_rate
                 self.Pressure = Pressure
                 self.Temperature = Temperature