import pandas as pd
import propylean.streams as strm
from thermo.chemical import Chemical
from fluids import control_valve as cv_calculations
import fluids.compressible as compressible_fluid 
from pipe_pressure_loss_calculator import PressureLoss as PL 

#Defining generic base class for all equipments with one inlet and outlet
class _equipment_one_inlet_outlet:
    
    def __init__(self, **inputs):
        self.tag = None if 'tag' not in inputs else inputs['tag']
        self.dynamic_state = False if 'dynamic_state' not in inputs else inputs['dynamic_state']

        #Flow properties
        self._inlet_mass_flowrate = 0 if 'inlet_mass_flowrate' not in inputs else inputs['inlet_mass_flowrate']
        self._outlet_mass_flowrate = 0 if 'outlet_mass_flowrate' not in inputs else inputs['outlet_mass_flowrate']
        self.design_flowrate = 0 if 'design_flowrate' not in inputs else inputs['design_flowrate']

        #Pressure properties
        self._inlet_pressure = None if 'inlet_pressure' not in inputs else inputs['inlet_pressure']
        self._outlet_pressure = None if 'outlet_pressure' not in inputs else inputs['outlet_pressure']
        if 'pressure_drop' in inputs:
            self.pressure_drop = inputs['pressure_drop']
        self.design_pressure = None if 'design_pressure' not in inputs else inputs['design_pressure']
        
        #Temperature properties
        self.inlet_temperature = None if 'inlet_temperature' not in inputs else inputs['inlet_temperature']
        self.outlet_temperature = None if 'outlet_temperature' not in inputs else inputs['outlet_temperature']
        self.design_temperature = None if 'design_temperature' not in inputs else inputs['design_temperature']

        
    @property
    def inlet_pressure(self):
        return self._inlet_pressure
    @inlet_pressure.setter
    def inlet_pressure(self,value):
        self._inlet_pressure = value
        self._outlet_pressure = self._inlet_pressure - self.pressure_drop
    @property
    def outlet_pressure(self):
        return self._outlet_pressure
    @outlet_pressure.setter
    def outlet_pressure(self,value):
        self._outlet_pressure = value
        self._inlet_pressure = self._outlet_pressure + self.pressure_drop
    @property
    def pressure_drop(self):
        if (self.inlet_pressure == None or
            self.outlet_pressure == None or
            self.inlet_mass_flowrate == 0):
            return 0            
        return self.inlet_pressure - self.outlet_pressure
    @pressure_drop.setter
    def pressure_drop(self,value):
        if self.inlet_pressure != None:
            self._outlet_pressure = self.inlet_pressure - value
        elif self.outlet_pressure != None:
            self._inlet_pressure = self.outlet_pressure + value
        else:
            raise Exception("Error! Assign inlet value or outlet outlet before assigning differential")
    
    @property
    def inlet_mass_flowrate(self):
        return self._inlet_mass_flowrate
    @inlet_mass_flowrate.setter
    def inlet_mass_flowrate(self,value):
        self._inlet_mass_flowrate = value
        self._outlet_mass_flowrate = self._inlet_mass_flowrate + self.inventory_change_rate
    @property
    def outlet_mass_flowrate(self):
        return self._outlet_mass_flowrate
    @outlet_mass_flowrate.setter
    def outlet_mass_flowrate(self,value):
        self._outlet_mass_flowrate = value
        self._inlet_mass_flowrate = self._outlet_mass_flowrate - self.inventory_change_rate   
    @property
    def inventory_change_rate(self):
        if not self.dynamic_state:
            return 0
        if (self._inlet_mass_flowrate == None or
            self._outlet_mass_flowrate == None):
            return None            
        return self._inlet_mass_flowrate - self._outlet_mass_flowrate
    @inventory_change_rate.setter
    def inventory_change_rate(self,value):
        if self._inlet_mass_flowrate != None:
            self._outlet_mass_flowrate = self._inlet_mass_flowrate - value
        elif self._outlet_mass_flowrate != None:
            self._inlet_mass_flowrate = self._outlet_mass_flowrate + value
        else:
            raise Exception("Error! Assign inlet value or outlet outlet before assigning differential")

#Defining generic base class for all equipments with multiple inlet and outlet. TO BE UPDATED!!!!!!       
class _equipment_multiple_inlet_outlet:
    def __init__(self):
        self.inlet_pressure = list()

#Defining generic class for all types of pressure changers like Pumps, Compressors and Expanders
class _pressure_changers(_equipment_one_inlet_outlet):
    def __init__(self,**inputs):
        self._differential_pressure = None
        if 'pressure_drop' in inputs:
            inputs['differential_pressure'] = -1 * inputs['pressure_drop']
            del inputs['pressure_drop']
        if 'inlet_pressure' in inputs:
            inputs['suction_pressure'] = inputs['inlet_pressure']
            del inputs['inlet_pressure']
        if 'outlet_pressure' in inputs:
            inputs['discharge_pressure'] = inputs['outlet_pressure']
            del inputs['outlet_pressure']
        
        super().__init__(**inputs)
        if 'suction_pressure' in inputs:
            self.inlet_pressure = inputs['suction_pressure']
            if ('differential_pressure' in inputs and 'performance_curve' in inputs or
                'differential_pressure' in inputs and 'discharge_pressure' in inputs or
                'performance_curve' in inputs and 'discharge_pressure' in inputs):
                raise Exception('Please input only one of discharge_pressure, differential_pressure or performance_curve \
                                 with suction pressure')
        if 'discharge_pressure' in inputs:
            if (self.suction_pressure != None and 
                'differential_pressure' in inputs):
                raise Exception("Please enter ethier one of discharge_pressure or differential_pressure")
            self.outlet_pressure = inputs['discharge_pressure']
        
        if 'differential_pressure' in inputs:
            if ((self.suction_pressure != None or self.discharge_pressure != None) and
                 'performance_curve' in inputs):
                 raise Exception('Please input only one of differential pressure or performance_curve')
            self.differential_pressure = inputs['differential_pressure'] 
                 
        self._performance_curve = pd.DataFrame()
        if 'performance_curve' in inputs:
            self.performace_curve = inputs['performance_curve']
        
        self._efficiency = None if 'efficiency' not in inputs else inputs['efficiency']
        
    @_equipment_one_inlet_outlet.inlet_pressure.getter
    def inlet_pressure(self):
        print('child getter')
        return self._inlet_pressure
    @_equipment_one_inlet_outlet.inlet_pressure.setter
    def inlet_pressure(self,value):
        self._inlet_pressure = value
        if self._differential_pressure!=None:
            self._outlet_pressure = self._inlet_pressure + self._differential_pressure
    @property
    def suction_pressure(self):
        return self.inlet_pressure
    @suction_pressure.setter
    def suction_pressure(self, value):
        self.inlet_pressure = value

    @_equipment_one_inlet_outlet.outlet_pressure.getter
    def outlet_pressure(self):
        print('child getter')
        return self._outlet_pressure
    @_equipment_one_inlet_outlet.outlet_pressure.setter
    def outlet_pressure(self,value):
        self._outlet_pressure = value
        if self._differential_pressure!=None:
            self._inlet_pressure = self._outlet_pressure - self._differential_pressure
    @property
    def discharge_pressure(self):
        return self.outlet_pressure
    @discharge_pressure.setter
    def discharge_pressure(self, value):
        self.outlet_pressure = value
    
    @_equipment_one_inlet_outlet.pressure_drop.getter
    def pressure_drop(self):
        print('child getter')
        return -1 * self.differential_pressure
    @_equipment_one_inlet_outlet.pressure_drop.setter
    def pressure_drop(self,value):
        self.differential_pressure = -1 * value      
    @property
    def differential_pressure(self):
        return self._differential_pressure
    @differential_pressure.setter
    def differential_pressure(self, value):
        self._differential_pressure = value
        if self.inlet_pressure != None:
            self._outlet_pressure = self._inlet_pressure + value
        elif self.outlet_pressure != None:
            self._inlet_pressure = self._outlet_pressure - value

    @property
    def performance_curve(self):
        return self._perfomace_curve
    @performance_curve.setter
    def pump_curve(self,value):
        if isinstance(value,pd.DataFrame) and value.shape[1] == 2:
                self._performance_curve = value
        else:
            raise Exception("Please enter performance_curve as pandas dataframe of 2 columns")
    
    @property
    def efficiency(self):
        return self._efficiency
    @efficiency.setter
    def efficiency(self, value):
        if value < 0:
            raise Exception("Please enter a positive value for efficiency")
        elif value <= 1:
            self._efficiency = value
        else:
            self._efficiency = value/100

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
    items = []    
    def __init__(self, **inputs):
        super().__init__( **inputs)
        self.min_flow = None if 'min_flow' not in inputs else inputs['min_flow']
        self.NPSHr = None if 'NPSHr' not in inputs else inputs['NPSHr']
        self.NPSHa = None if 'NPSHa' not in inputs else inputs['NPSHa']
        self.inlet_energy_tag = None if 'inlet_energy_tag' not in inputs else inputs['inlet_energy_tag']
        centrifugal_pump.items.append(self)
                
    @property
    def head(self):
        fluid_density = 1000 # THIS NEEDS TO BE UPDATED WITH STREAM PROPERTY
        return self.differential_pressure / (9.8 * fluid_density)
    @property
    def hydraulic_power(self):
        fluid_density = 1000 # THIS NEEDS TO BE UPDATED WITH STREAM PROPERTY
        return self.inlet_mass_flowrate * fluid_density * 9.81 * self.head / (3.6e6)
    @property
    def brake_horse_power(self):
        return self.hydraulic_power / self.efficiency
    @classmethod
    def list_objects(cls):
        return cls.items
    
class positive_displacement_pump(_pressure_changers):
    items = []
    def __init__(self, **inputs):
        super().__init__(**inputs)
        positive_displacement_pump.items.append(self)
    @classmethod
    def list_objects(cls):
        return cls.items
# End of final classes of pumps

# Start of final classes of Compressors and Expanders
class centrifugal_compressors(_pressure_changers):
    items = []
    def __init__(self, **inputs):
        super().__init__(**inputs)
        self.methane = Chemical('methane',
                         T = self.inlet_temperature,
                         P = self.inlet_pressure)
        if 'adiabatic_efficiency' not in inputs and 'polytropic_efficiency' in inputs:
            self.polytropic_efficiency = inputs['polytropic_efficiency']
        else:
            self.adiabatic_efficiency = 0.7 if 'adiabatic_efficiency' not in inputs else inputs['adiabatic_efficiency']
        self.inlet_energy_tag = None if 'inlet_energy_tag' not in inputs else inputs['inlet_energy_tag']
        centrifugal_compressors.items.append(self)
    @property
    def adiabatic_efficiency(self):
        return self._adiabatic_efficiency
    @adiabatic_efficiency.setter
    def adiabatic_efficiency(self, value):
        if value ==  None:
            value = 0.7
        self._adiabatic_efficiency = value
    
    @property
    def polytropic_efficiency(self):
        return compressible_fluid.isentropic_efficiency(P1 = self.inlet_pressure,
                                                        P2 = self.outlet_pressure,
                                                        k = self.methane.isentropic_exponent,
                                                        eta_s = self.adiabatic_efficiency)
    @polytropic_efficiency.setter
    def polytropic_efficiency(self, value):
        self.adiabatic_efficiency = compressible_fluid.isentropic_efficiency(P1 = self.inlet_pressure,
                                                                                 P2 = self.outlet_pressure,
                                                                                 k = self.methane.isentropic_exponent,
                                                                                 eta_p = value)
    @property
    def power(self):
        work = compressible_fluid.isentropic_work_compression(T1 = self.inlet_temperature,
                                                              k = self.methane.isentropic_exponent,
                                                              Z = self.methane.Z,
                                                              P1 = self.suction_pressure,
                                                              P2 = self.discharge_pressure,
                                                              eta = self.adiabatic_efficiency)
        return work * self.inlet_mass_flowrate / self.methane.MW
    @classmethod
    def list_objects(cls):
        return cls.items

class expander(_pressure_changers):
    items = []
    def __init__(self, **inputs):
        self.outlet_energy_tag = None if 'outlet_energy_tag' not in inputs else inputs['outlet_energy_tag']
        super().__init__(**inputs)
        expander.items.append(self)
    @classmethod
    def list_objects(cls):
        return cls.items

# End of final classes of compressors

# Start of final classes of Piping and Instruments
class pipe_segment(_equipment_one_inlet_outlet):
    items = []
    def __init__(self, **inputs):
        self.outlet_energy_tag = None if 'outlet_energy_tag' not in inputs else inputs['outlet_energy_tag']
        super().__init__(**inputs)
        self.segment_type = 1 if 'segment_type' not in inputs else inputs['segment_type']
        segments = '''\nSegments can be of following types and in range of numbers below:
                    1. Straight Tube
                    2. Elbow
                    3. Tee
                    4. Angle valve
                    5. Butterfly valve
                    6. Ball valve
                    7. Gate valve
                    8. Globe valve
                    9. Swing check valve
                    10. Ball check valve
                    11. Lift check valve
                    12. Reducer
                    13. Expander'''
        if self.segment_type == 1:
            if 'length' in inputs:
                self.length = inputs['length']                
            else:
                raise Exception('Straight Tube segment requires length value')
        elif self.segment_type not in range(1,14):
            raise Exception(segments)

        materials = '''\nSegment material can be of following types and in range of numbers below:
                    1. Raw Steel
                    2. Carbon Steel
                    3. Cast Iron
                    4. Stainless Steel
                    5. PVC'''   
        self.material = 1
        
        if 'material' in inputs:
            if inputs['material'] in range(1,6):
                self.material = inputs['material']
            else:
                raise Exception(materials)
        
        self.OD = None
        if ('ID' in inputs):
            self.ID = inputs['ID']
        elif ('OD' in inputs and 'thickness' in inputs):
            self.OD = inputs['OD']
            self.ID = self.OD - inputs['thickness']
        else:
            raise Exception('Define atleast ID or OD with thickness to define a pipe segment object') 
        pipe_segment.items.append(self)
    @property
    def pressure_drop(self):
        if (self.inlet_pressure == None or
            self.outlet_pressure == None or
            self.inlet_mass_flowrate == 0):
            return 0
        roughness = (4.57e-5, 4.5e-5, 0.000259, 1.5e-5, 1.5e-6) #in meters
        
        drop = round(PL.PressureLoss_DW(self.length, self.ID, self.inlet_mass_flowrate,
                                  self.inlet_temperature, 1000*roughness[self.material-1]),3)
        return drop
        
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
    
    @classmethod
    def list_objects(cls):
        return cls.items

class control_valve(_equipment_one_inlet_outlet):
    items = []
    def __init__(self, **inputs):
        super().__init__(**inputs)
        control_valve.items.append(self)
    @property
    def Kv(self):
        # UPDATE BELOW BASED ON STREAMS
        water = Chemical('water',
                         T = self.inlet_temperature,
                         P = self.inlet_pressure)
        if water.phase == 'l':
            return cv_calculations.size_control_valve_l(water.rhol, water.Psat,water.Pc, water.mul,
                                                        self.inlet_pressure, self.outlet_pressure, 
                                                        self.inlet_mass_flowrate/water.rhol)
        elif water.phase == 'g':
            return cv_calculations.size_control_valve_g(T = self.inlet_temperature, 
                                                        MW = water.MW,
                                                        mu= 1.48712E-05,#water.mug,
                                                        gamma = water.isentropic_exponent, 
                                                        Z = water.Zg,
                                                        P1 = self.inlet_pressure, 
                                                        P2 = self.outlet_pressure, 
                                                        Q = self.inlet_mass_flowrate/Chemical('water',T=273.15,P=101325).rhog)
        else:
            raise Exception('Possibility of fluid solification at control valve')

    @classmethod
    def list_objects(cls):
        return cls.items
class pressure_safety_valve(_equipment_one_inlet_outlet):
    items = []
    def __init__(self, **inputs):
        
        pressure_safety_valve.items.append(self)
        super().__init__(**inputs)
    @classmethod
    def list_objects(cls):
        return cls.items

class flow_meter(_equipment_one_inlet_outlet):
    items = []
    def __init__(self, **inputs):
        super().__init__(**inputs)
        flow_meter.items.append(self)
    @classmethod
    def list_objects(cls):
        return cls.items
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