class equipment:
    def __init__(self, 
                 name=None, 
                 operating_pressure=None,
                 operating_temperature=None):
        self.name = name
        self.operating_pressure = operating_pressure
        self.operating_temperature = operating_temperature

class pump:
    def __init__(self, suction_pressure=None,
                 name=None, 
                 operating_pressure=None,
                 operating_temperature=None):
        self.suction_pressure = suction_pressure
        super().__init__(name, operating_pressure, operating_temperature)
