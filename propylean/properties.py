class Pressure:
    def __init__(self, value = 1, unit= 'Pa'):
        self.value = value
        self.unit = unit
    
    def __repr__(self) -> str:
        return str(self.value) + ' ' + self.unit

class Temperature:
    def __init__(self, value = 1, unit= 'K'):
        self.value = value
        self.unit = unit
    
    def __repr__(self) -> str:
        return str(self.value) + ' ' + self.unit

class MassFlowRate:
    def __init__(self, value = 1, unit= 'Kg/s'):
        self.value = value
        self.unit = unit
    
    def __repr__(self) -> str:
        return str(self.value) + ' ' + self.unit

class Power:
    def __init__(self, value = 1, unit= 'W'):
        self.value = value
        self.unit = unit
    
    def __repr__(self) -> str:
        return str(self.value) + ' ' + self.unit