from thermo.chemical import Chemical
import propylean.properties as prop

class EnergyStream (prop.Power):
    items = [] 
    def __init__(self, value=0, unit='W', tag=None, 
                 to_equipment_tag=None, to_equipment_type=None,
                 from_equipment_tag=None, from_equipment_type=None):
                 
                 super().__init__(value=value, unit=unit)
                 self.tag = tag
                 self.assign_equipment('to', to_equipment_tag, to_equipment_type)
                 self.assign_equipment('from', from_equipment_tag, from_equipment_type)
                 EnergyStream.items.append(self)
    
    def assign_equipment(self, to_or_from, equipment_tag, equipment_type, equipment_index=None):
        inlet_outlet = None
        if to_or_from in ['to','To','TO']:
            inlet_outlet = 'inlet'
            self.to_equipment_tag = equipment_tag
            self.to_equipment_type = equipment_type
            self.to_equipment_index = equipment_index if equipment_index != None else None
        elif to_or_from in ['from','From','FROM']:
            inlet_outlet = 'outlet'
            self.from_equipment_tag = equipment_tag
            self.from_equipment_type = equipment_type
            self.from_equipment_index = equipment_index if equipment_index != None else None

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
                 to_equipment_tag=None, to_equipment_type=None,
                 from_equipment_tag= None, from_equipment_type=None):
                 
                 self.tag = tag
                 self.mass_flow_rate = prop.MassFlowRate(mass_flow_rate)
                 self.pressure = prop.Pressure(pressure)
                 self.temperature = prop.Temperature(temperature)
                 self.molar_flow_rate = prop.MolarFlowRate()
                 self.to_equipment_tag = to_equipment_tag
                 self.to_equipment_type = to_equipment_type
                 self.to_equipment_index = None
                 self.from_equipment_tag = from_equipment_tag
                 self.from_equipment_type = from_equipment_type 

                 MaterialStream.items.append(self)

    @classmethod
    def list_objects(cls):
        return cls.items

    def __repr__(self) -> str:
        return 'Material Stream Tag: ' + self.tag

#Get stream index function
def get_stream_index(tag, stream_type=None):
    if stream_type in ['energy', 'Energy', 'Power','e','E']:
        stream_list = EnergyStream.list_objects()
    elif stream_type in ['material', 'Material', 'mass', 'Mass','m','M']:
        stream_list = MaterialStream.list_objects()
    elif stream_type==None:
        return [(get_stream_index(tag, 'energy'),'Energy Stream'),(get_stream_index(tag, 'material'),'Material Stream')]
    else:
        raise Exception('Stream type does not exist! Please ensure stream type is either Energy or Material')
    list_of_none_tag_streams =[]

    for index, stream in enumerate(stream_list):
        if stream.tag == None and tag==None:
            list_of_none_tag_streams.append(index)           
        elif stream.tag == tag:
            return index
        
    if tag != None:
        raise Exception("Stream tag not found!!")

    return list_of_none_tag_streams

