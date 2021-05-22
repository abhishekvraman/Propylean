class _pressure_reducing_valve:
    def __init__(self, **inputs):
        self.tag = None if 'tag' not in inputs else inputs['tag']
        if 'outlet_pressure' in inputs and 'inlet_pressure' in inputs:
            self.outlet_pressure = inputs['outlet_pressure']
            self.inlet_pressure = inputs['inlet_pressure']
            self.pressure_drop = self.inlet_pressure - self.outlet_pressure
        elif 'pressure_drop' in inputs and 'inlet_pressure' in inputs:
            self.pressure_drop = inputs['pressure_drop']
            self.inlet_pressure = inputs['inlet_pressure']
            self.outlet_pressure = self.inlet_pressure - self.pressure_drop
        elif 'outlet_pressure' in inputs and 'pressure_drop' in inputs:
            self.pressure_drop = inputs['pressure_drop']
            self.outlet_pressure = inputs['outlet_pressure']
            self.inlet_pressure = self.outlet_pressure + self.pressure_drop
        else:
            self.inlet_pressure = None if 'inlet_pressue' not in inputs else inputs['inlet_pressue']
            self.outlet_pressure = None if 'outlet_pressue' not in inputs else inputs['outlet_pressue']
            self.pressure_drop = None if 'pressure_drop' not in inputs else inputs['pressue_drop']


class control_valve(_pressure_reducing_valve):
    def __init__(self, **inputs):
        super().__init__(**inputs)

class pressure_safety_valve(_pressure_reducing_valve):
    def __init__(self, **inputs):
        super().__init__(**inputs)