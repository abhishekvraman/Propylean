#Defining generic base class for all equipments 
class _equipment:
    def __init__(self, **inputs):
        self.tag = None if 'tag' not in inputs else inputs['tag']
        self.operating_pressure = None if 'operating_pressure' not in inputs else inputs['operating_pressure']
        self.design_pressure = None if 'design_pressure' not in inputs else inputs['design_pressure']
        self.operating_temperature = None if 'operating_temperature' not in inputs else inputs['operating_temperature']
        self.design_temperature = None if 'design_temperature' not in inputs else inputs['design_temperature']

#Defining generic class for all types of pumps
class _pump(_equipment):
    def __init__(self,**inputs):
        super().__init__(**inputs)
        self.suction_pressure = None if 'suction_pressure' not in inputs else inputs['suction_pressure']
        self.discharge_pressure = None if 'discharge_pressure' not in inputs else inputs['discharge_pressure']
        self.operating_pressure = self.discharge_pressure
        self.flow_rate = None if 'flow_rates' not in inputs else inputs['flow_rates']
        self.hydraulic_efficiency = None if 'hydraulic_efficiency' not in inputs else inputs['hydraulic_efficiency']

#Defining generic class for all types of vessels
class _vessel(_equipment):
    def __init__(self, **inputs):
        super().__init__(**inputs)
        self.ID = None if 'ID' not in inputs else inputs['ID']
        self.length = None if 'length' not in inputs else inputs['length']
        
        self.LLLL = None if 'LLLL' not in inputs else inputs['LLLL']
        self.LLL = None if 'LLL' not in inputs else inputs['LLL']
        self.NLL = None if 'NLL' not in inputs else inputs['NLL']
        self.HLL = None if 'HLL' not in inputs else inputs['HLL']
        self.HHLL = None if 'HHLL' not in inputs else inputs['HHLL']

#Defining generic class for all types of heat exchangers
class _exchanger(_equipment):
    def __init__(self, **inputs):
        super().__init__(**inputs)
        self.hot_stream_temp = None if 'hot_stream_temp' not in inputs else inputs['hot_stream_temp']
        self.hot_stream_flow = None if 'hot_stream_flow' not in inputs else inputs['hot_stream_flow']
        self.cold_stream_temp = None if 'cold_stream_temp' not in inputs else inputs['cold_stream_temp']
        self.cold_stream_flow = None if 'cold_stream_flow' not in inputs else inputs['cold_stream_flow']






# Start of final classes pumps
class centrifugal_pump(_pump):
    def __init__(self, **inputs):
        super().__init__( **inputs)
        self.min_recirculation = None if "min_recirculation" not in inputs else inputs['min_recirculation']
        self.NPSHr = None if 'NPSHr' not in inputs else inputs['NPSHr']
        self.NPSHa = None if 'NPSHa' not in inputs else inputs['NPSHa']

class positive_displacement_pump(_pump):
    def __init__(self, **inputs):
        super().__init__(**inputs)
# End of final classes of pumps

# Start of final classes of vessels
class vertical_separator(_vessel):
    def __init__(self, **inputs):
        super().__init__(**inputs)

class horizontal_separator(_vessel):
    def __init__(self, **inputs):
        super().__init__(**inputs)

class column(_vessel):
    def __init__(self, **inputs):
        super().__init__(**inputs)

class tank(_vessel):
    def __init__(self, **inputs):
        super().__init__(**inputs)
# End of final classes of vessels

# Start of final classes of Compressors
class compressor(_equipment):
    def __init__(self, **inputs):
        super().__init__(**inputs)
        self.suction_pressure = None if 'suction_pressure' not in inputs else inputs['suction_pressure']
        self.discharge_pressure = None if 'discharge_pressure' not in inputs else inputs['discharge_pressure']
        self.operating_pressure = self.discharge_pressure
        self.flow_rate = None if 'flow_rates' not in inputs else inputs['flow_rates']

# End of final classes of compressors

# Start of final classes of heat exchangers

class shell_and_tube_HE(_exchanger):
    def __init__(self, **inputs):
        super().__init__(**inputs)
        