#Defining generic base class for all equipments with one inlet and outlet
class _equipment_one_inlet_outlet:
    def __init__(self, **inputs):
        self.tag = None if 'tag' not in inputs else inputs['tag']
        self.dynamic_state = False if 'dynamic_state' not in inputs else inputs['dynamic_state']

        #Pressure properties
        self.inlet_pressure = None if 'inlet_pressure' not in inputs else inputs['inlet_pressure']
        self.outlet_pressure = None if 'outlet_pressure' not in inputs else inputs['outlet_pressure']
        if 'pressure_drop' in inputs:
            self.pressure_drop = inputs['pressure_drop']
        self.design_pressure = None if 'design_pressure' not in inputs else inputs['design_pressure']
        
        #Temperature properties
        self.inlet_temperature = None if 'inlet_temperature' not in inputs else inputs['inlet_temperature']
        self.outlet_temperature = None if 'outlet_temperature' not in inputs else inputs['outlet_temperature']
        self.design_temperature = None if 'design_temperature' not in inputs else inputs['design_temperature']

        #Flow properties
        self.inlet_flowrate = None if 'inlet_flowrate' not in inputs else inputs['inlet_flowrate']
        self.outlet_flowrate = None if 'outlet_flowrate' not in inputs else inputs['outlet_flowrate']
        self.design_flowrate = None if 'design_flowrate' not in inputs else inputs['design_flowrate']
        
    @property
    def pressure_drop(self):
        if (self.inlet_pressure == None or
            self.outlet_pressure == None):
            return None            
        return self.inlet_pressure - self.outlet_pressure
    @pressure_drop.setter
    def pressure_drop(self,value):
        if self.inlet_pressure != None:
            self.outlet_pressure = self.inlet_pressure - value
        elif self.outlet_pressure != None:
            self.inlet_pressure = self.outlet_pressure + value
        else:
            raise Exception("Error! Assign inlet value or outlet outlet before assigning differential")

    @property
    def inventory_change_rate(self):
        if (self.inlet_flowrate == None or
            self.outlet_flowrate == None):
            return None            
        return self.inlet_flowrate - self.outlet_flowrate
    @inventory_change_rate.setter
    def inventory_change_rate(self,value):
        if self.inlet_flowrate != None:
            self.outlet_flowrate = self.inlet_flowrate - value
        elif self.outlet_flowrate != None:
            self.inlet_flowrate = self.outlet_flowrate + value
        else:
            raise Exception("Error! Assign inlet value or outlet outlet before assigning differential")

#Defining generic base class for all equipments with multiple inlet and outlet        
class _equipment_multiple_inlet_outlet:
    def __init__(self):
        self.inlet_pressure = list()
#Defining generic class for all types of pressure enhancers like Pumps and Compressors
class _pressure_changers(_equipment_one_inlet_outlet):
    def __init__(self,**inputs):
        super().__init__(**inputs)
        if 'suction_pressure' in inputs:
            self.inlet_pressure = inputs['suction_pressure']
        if 'discharge_pressure' in inputs:
            self.outlet_pressure = inputs['discharge_pressure']
        if 'differential_pressure' in inputs:
            self.pressure_drop = -1 * inputs['differential_pressure']

    @property
    def suction_pressure(self):
        return self.inlet_pressure
    @suction_pressure.setter
    def suction_pressure(self, value):
        self.inlet_pressure = value

    @property
    def discharge_pressure(self):
        return self.outlet_pressure
    @discharge_pressure.setter
    def discharge_pressure(self, value):
        self.outlet_pressure = value
    
    @property
    def differential_pressure(self):
        return -1*self.pressure_drop
    @discharge_pressure.setter
    def discharge_pressure(self, value):
        self.pressure_drop = -1*value

#Defining generic class for all types of vessels.  NEEDS SUPER CLASS WITH MULTI INPUT AND OUTPUT 
class _vessel():
    def __init__(self, **inputs):
        super().__init__(**inputs)
        self.ID = None if 'ID' not in inputs else inputs['ID']
        self.length = None if 'length' not in inputs else inputs['length']
        
        self.LLLL = None if 'LLLL' not in inputs else inputs['LLLL']
        self.LLL = None if 'LLL' not in inputs else inputs['LLL']
        self.NLL = None if 'NLL' not in inputs else inputs['NLL']
        self.HLL = None if 'HLL' not in inputs else inputs['HLL']
        self.HHLL = None if 'HHLL' not in inputs else inputs['HHLL']

#Defining generic class for all types of heat exchangers NEEDS SUPER CLASS WITH MULTI INPUT AND OUTPUT
class _exchanger():
    def __init__(self, **inputs):
        #Hot side
        self.hot_side_operating_pressure = None if 'hot_side_operating_pressure' not in inputs else inputs['hot_side_operating_pressure']
        self.hot_side_flowrate = None if 'hot_side_flowrate' not in inputs else inputs['hot_side_flowrate']
        self.hot_side_inlet_temp = None if 'hot_side_inlet_temp' not in inputs else inputs['hot_side_inlet_temp']
        self.hot_side_outlet_temp = None if 'hot_side_outlet_temp' not in inputs else inputs['hot_side_outlet_temp']
        self.hot_side_pressure_drop = None if 'hot_side_pressure_drop' not in inputs else inputs['hot_side_pressure_drop']
        #Cold Side
        self.cold_side_operating_pressure = None if 'cold_side_operating_pressure' not in inputs else inputs['cold_side_operating_pressure']
        self.cold_stream_flowrate = None if 'cold_stream_flowrate' not in inputs else inputs['cold_stream_flowrate']
        self.cold_side_inlet_temp = None if 'cold_side_inlet_temp' not in inputs else inputs['cold_side_inlet_temp']
        self.cold_side_outlet_temp = None if 'cold_side_outlet_temp' not in inputs else inputs['cold_side_outlet_temp']
        self.cold_side_pressure_drop = None if 'cold_side_pressure_drop' not in inputs else inputs['cold_side_pressure_drop']
        
#----------------------Generic Classes End here. Final classes below---------------------------------------------------------

# Start of final classes pumps
class centrifugal_pump(_pressure_changers):
    def __init__(self, **inputs):
        super().__init__( **inputs)
        self.min_flow = None if "min_flow" not in inputs else inputs['min_flow']
        self.NPSHr = None if 'NPSHr' not in inputs else inputs['NPSHr']
        self.NPSHa = None if 'NPSHa' not in inputs else inputs['NPSHa']

class positive_displacement_pump(_pressure_changers):
    def __init__(self, **inputs):
        super().__init__(**inputs)
# End of final classes of pumps

# Start of final classes of Compressors and Expanders
class centrifugal_compressors(_pressure_changers):
    def __init__(self, **inputs):
        super().__init__(**inputs)
class expander(_pressure_changers):
    def __init__(self, **inputs):
        super().__init__(**inputs)
# End of final classes of compressors

# Start of final classes of Piping and Instruments
class pipe(_equipment_one_inlet_outlet):
    def __init__(self, **inputs):
        super().__init__(**inputs)
        self.ID = None if 'ID' not in inputs else inputs['ID']
        self.OD = None if 'OD' not in inputs else inputs['OD']
        if 'thickness' in inputs:
            self.thickness = inputs['thickness']

    @property
    def thickness(self):
        if self.ID == None or self.OD == None:
            return None
        return self.OD - self.ID
    @thickness.setter
    def thickness(self, value):
        if self.ID != None:
            self.OD = self.ID + value
        elif self.OD !=None:
            self.ID = self.OD - value
        else:
            raise Exception("Atleast define ID or OD of pipe before defining thickness")
    
class control_valve(_equipment_one_inlet_outlet):
    def __init__(self, **inputs):
        super().__init__(**inputs)

class pressure_safety_valve(_equipment_one_inlet_outlet):
    def __init__(self, **inputs):
        super().__init__(**inputs)

class flow_meter(_equipment_one_inlet_outlet):
    def __init__(self, **inputs):
        super().__init__(**inputs)

# End of final classes of Piping and instruments


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

# Start of final classes of heat exchangers
class shell_and_tube_HE(_exchanger):
    def __init__(self, **inputs):
        super().__init__(**inputs)

class air_coolers(_exchanger):
    def __init__(self, **inputs):
        super().__init__(**inputs)
# End of final classes of heat exchangers      