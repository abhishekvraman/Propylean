from thermo.chemical import Chemical
import propylean.properties as prop  
class EnergyStream (prop.Power):
    items = [] 
    def __init__(self, value= 0, unit= 'W', tag= None, 
                 to_equipment_tag= None, from_equipment_tag= None):
                 super().__init__(value= value, unit=unit)
                 self.tag = tag
                 self.to_equipment_tag = to_equipment_tag
                 self.from_equipment_tag = from_equipment_tag

                 EnergyStream.items.append(self)
    
    def __repr__(self) -> str:
        return 'Energy Stream Tag: ' + self.tag  

    @classmethod
    def list_objects(cls):
        return cls.items       
      
class MaterialStream:
    items = [] 
    def __init__(self, mass_flow_rate = 0,
                 pressure = 101325,
                 temperature = 298,
                 tag = None,
                 to_equipment_tag= None, from_equipment_tag= None):
                 
                 self.tag = tag
                 self.mass_flow_rate = prop.MassFlowRate(mass_flow_rate)
                 self.pressure = prop.Pressure(pressure)
                 self.temperature = prop.Temperature(temperature)
                 self.molar_flow_rate = prop.MolarFlowRate()
                 self.to_equipment_tag = to_equipment_tag
                 self.to_equipment_index = None
                 self.from_equipment_tag = from_equipment_tag 

                 MaterialStream.items.append(self)

    @classmethod
    def list_objects(cls):
        return cls.items

    def __repr__(self) -> str:
        return 'Material Stream Tag: ' + self.tag