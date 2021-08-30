from thermo.chemical import Chemical
        
class EnergyStream:
    def __init__(self, value= 0, unit= 'kW', tag= None, 
                 to_equipment_tag= None, from_equipment_tag= None):
        a=2    

        
class MaterialStream:
    def __init__(self, mass_flow_rate = 0,
                 Pressure = 1,
                 Temperature = 25,
                 tag = None):
                 self.tag = tag
                 self.mass_flow_rate = mass_flow_rate
                 self.Pressure = Pressure
                 self.Temperature = Temperature