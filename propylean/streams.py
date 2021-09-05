from thermo.chemical import Chemical
import propylean.properties as prop  
class EnergyStream (prop.Power):
    def __init__(self, value= 0, unit= 'W', tag= None, 
                 to_equipment_tag= None, from_equipment_tag= None):
                 super().__init__(value= value, unit=unit)
                 self.tag = tag
                 self.to_equipment_tag = to_equipment_tag
                 self.from_equipment_tag = from_equipment_tag
            
      
class MaterialStream:
    def __init__(self, mass_flow_rate = 0,
                 Pressure = 1,
                 Temperature = 25,
                 tag = None):
                 self.tag = tag
                 self.mass_flow_rate = mass_flow_rate
                 self.Pressure = Pressure
                 self.Temperature = Temperature