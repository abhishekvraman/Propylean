import pandas as pd
import propylean.properties as prop
from thermo.chemical import Chemical
from fluids import control_valve as cv_calculations
import fluids.compressible as compressible_fluid 
from math import pi
from propylean import streams

#Defining generic base class for all equipments with one inlet and outlet
class _EquipmentOneInletOutlet:
    def __init__(self, **inputs) -> None:
        self.tag = None if 'tag' not in inputs else inputs['tag']
        self.dynamic_state = False if 'dynamic_state' not in inputs else inputs['dynamic_state']

        #Flow properties
        self._inlet_mass_flowrate = 0 if 'inlet_mass_flowrate' not in inputs else inputs['inlet_mass_flowrate']
        self._outlet_mass_flowrate = 0 if 'outlet_mass_flowrate' not in inputs else inputs['outlet_mass_flowrate']
        self.design_flowrate = 0 if 'design_flowrate' not in inputs else inputs['design_flowrate']

        #Pressure properties
        self._inlet_pressure = prop.Pressure(1) if 'inlet_pressure' not in inputs else prop.Pressure(inputs['inlet_pressure'])
        self._outlet_pressure = prop.Pressure(1) if 'outlet_pressure' not in inputs else prop.Pressure(inputs['outlet_pressure'])
        if 'pressure_drop' in inputs:
            self.pressure_drop = inputs['pressure_drop']
        self.design_pressure = None if 'design_pressure' not in inputs else inputs['design_pressure']
        
        #Temperature properties
        self.inlet_temperature = None if 'inlet_temperature' not in inputs else inputs['inlet_temperature']
        self.outlet_temperature = None if 'outlet_temperature' not in inputs else inputs['outlet_temperature']
        self.design_temperature = None if 'design_temperature' not in inputs else inputs['design_temperature']

        #Inlet and outlet material streams
        self._inlet_stream_index = None if 'inlet_stream_tag' not in inputs else streams.get_stream_index(inputs['inlet_stream_tag'], 'm')
        
        self._outlet_stream_index = None if 'outlet_stream_tag' not in inputs else streams.get_stream_index(inputs['outlet_stream_tag'], 'm')
        
    @property
    def inlet_pressure(self):
        return self._inlet_pressure
    @inlet_pressure.setter
    def inlet_pressure(self,value):
        self._inlet_pressure.value = value
        self._outlet_pressure.value = self._inlet_pressure.value - self.pressure_drop
    @property
    def outlet_pressure(self):
        return self._outlet_pressure
    @outlet_pressure.setter
    def outlet_pressure(self,value):
        self._outlet_pressure.value = value
        self._inlet_pressure.value = self._outlet_pressure.value + self.pressure_drop
    @property
    def pressure_drop(self):
        if (self._inlet_pressure.value == None or
            self._outlet_pressure.value == None or
            self._inlet_mass_flowrate == 0):
            return 0            
        return self._inlet_pressure.value - self._outlet_pressure.value
    @pressure_drop.setter
    def pressure_drop(self,value):
        if self._inlet_pressure.value != None:
            self._outlet_pressure.value = self._inlet_pressure.value - value
        elif self._outlet_pressure.value != None:
            self._inlet_pressure.value = self._outlet_pressure.value + value
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
class _EquipmentMultipleInletOutlet:
    def __init__(self) -> None:
        self._inlet_pressure.value = list()

#Defining generic class for all types of pressure changers like Pumps, Compressors and Expanders
class _PressureChangers(_EquipmentOneInletOutlet):
    def __init__(self,**inputs) -> None:
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
            self._inlet_pressure.value = inputs['suction_pressure']
            if ('differential_pressure' in inputs and 'performance_curve' in inputs or
                'differential_pressure' in inputs and 'discharge_pressure' in inputs or
                'performance_curve' in inputs and 'discharge_pressure' in inputs):
                raise Exception('Please input only one of discharge_pressure, differential_pressure or performance_curve \
                                 with suction pressure')
        if 'discharge_pressure' in inputs:
            if (self.suction_pressure != None and 
                'differential_pressure' in inputs):
                raise Exception("Please enter ethier one of discharge_pressure or differential_pressure")
            self._outlet_pressure = inputs['discharge_pressure']
        
        if 'differential_pressure' in inputs:
            if ((self.suction_pressure != None or self.discharge_pressure != None) and
                 'performance_curve' in inputs):
                 raise Exception('Please input only one of differential pressure or performance_curve')
            self.differential_pressure = inputs['differential_pressure'] 
                 
        self._performance_curve = pd.DataFrame()
        if 'performance_curve' in inputs:
            self.performace_curve = inputs['performance_curve']
        
        self._efficiency = None if 'efficiency' not in inputs else inputs['efficiency']
        
    @_EquipmentOneInletOutlet.inlet_pressure.getter
    def inlet_pressure(self):
        return str(self._inlet_pressure.value)
    @_EquipmentOneInletOutlet.inlet_pressure.setter
    def inlet_pressure(self,value):
        self._inlet_pressure.value = value
        if self._differential_pressure!=None:
            self._outlet_pressure.value = self._inlet_pressure.value + self._differential_pressure
    @property
    def suction_pressure(self):
        return self._inlet_pressure
    @suction_pressure.setter
    def suction_pressure(self, value):
        self.inlet_pressure = value

    @_EquipmentOneInletOutlet.outlet_pressure.getter
    def outlet_pressure(self):
        return self._outlet_pressure
    @_EquipmentOneInletOutlet.outlet_pressure.setter
    def outlet_pressure(self,value):
        self._outlet_pressure.value = value
        if self._differential_pressure!=None:
            self._inlet_pressure.value = self._outlet_pressure.value - self._differential_pressure
    @property
    def discharge_pressure(self):
        return self._outlet_pressure
    @discharge_pressure.setter
    def discharge_pressure(self, value):
        self.outlet_pressure = value
    
    @_EquipmentOneInletOutlet.pressure_drop.getter
    def pressure_drop(self):
        print('child getter')
        return -1 * self.differential_pressure
    @_EquipmentOneInletOutlet.pressure_drop.setter
    def pressure_drop(self,value):
        self.differential_pressure = -1 * value      
    @property
    def differential_pressure(self):
        return self._differential_pressure
    @differential_pressure.setter
    def differential_pressure(self, value):
        self._differential_pressure = value
        if self._inlet_pressure.value != None:
            self._outlet_pressure.value = self._inlet_pressure.value + value
        elif self._outlet_pressure.value != None:
            self._inlet_pressure.value = self._outlet_pressure.value - value

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
class _Vessels(_EquipmentMultipleInletOutlet):
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        self.ID = None if 'ID' not in inputs else inputs['ID']
        self.length = None if 'length' not in inputs else inputs['length']
        
        self.LLLL = None if 'LLLL' not in inputs else inputs['LLLL']
        self.LLL = None if 'LLL' not in inputs else inputs['LLL']
        self.NLL = None if 'NLL' not in inputs else inputs['NLL']
        self.HLL = None if 'HLL' not in inputs else inputs['HLL']
        self.HHLL = None if 'HHLL' not in inputs else inputs['HHLL']

#Defining generic class for all types of heat exchangers NEEDS SUPER CLASS WITH MULTI INPUT AND OUTPUT
class _Exchanger(_EquipmentMultipleInletOutlet):
    def __init__(self, **inputs) -> None:
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
class CentrifugalPump(_PressureChangers):
    items = []    
    def __init__(self, **inputs) -> None:
        super().__init__( **inputs)
        self.min_flow = None if 'min_flow' not in inputs else inputs['min_flow']
        self.NPSHr = None if 'NPSHr' not in inputs else inputs['NPSHr']
        self.NPSHa = None if 'NPSHa' not in inputs else inputs['NPSHa']
        self.inlet_energy_tag = None if 'inlet_energy_tag' not in inputs else inputs['inlet_energy_tag']
        CentrifugalPump.items.append(self)
    
    def __eq__(self, other):
        if isinstance(other, CentrifugalPump):
            return self.tag == other.tag
        else:
            return False
    
    def __repr__(self):
        return "Centrifugal Pump with tag: " + self.tag
    def __hash__(self):
        return hash(self.__repr__())

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
    
class PositiveDisplacementPump(_PressureChangers):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        PositiveDisplacementPump.items.append(self)
    
    def __eq__(self, other):
        if isinstance(other, PositiveDisplacementPump):
            return self.tag == other.tag
        else:
            return False
    
    def __repr__(self):
        return "Positive Displacement Pump with tag: " + self.tag
    def __hash__(self):
        return hash(self.__repr__())
    
    @classmethod
    def list_objects(cls):
        return cls.items
# End of final classes of pumps

# Start of final classes of Compressors and Expanders
class CentrifugalCompressor(_PressureChangers):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        self.methane = Chemical('methane',
                         T = self.inlet_temperature,
                         P = self._inlet_pressure.value)
        if 'adiabatic_efficiency' not in inputs and 'polytropic_efficiency' in inputs:
            self.polytropic_efficiency = inputs['polytropic_efficiency']
        else:
            self.adiabatic_efficiency = 0.7 if 'adiabatic_efficiency' not in inputs else inputs['adiabatic_efficiency']
        self.inlet_energy_tag = None if 'inlet_energy_tag' not in inputs else inputs['inlet_energy_tag']
        CentrifugalCompressor.items.append(self)
    
    def __eq__(self, other):
        if isinstance(other, CentrifugalCompressor):
            return self.tag == other.tag
        else:
            return False
    
    def __repr__(self):
        return "Positive Displacement Pump with tag: " + self.tag
    def __hash__(self):
        return hash(self.__repr__())

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
        return compressible_fluid.isentropic_efficiency(P1 = self._inlet_pressure.value,
                                                        P2 = self._outlet_pressure.value,
                                                        k = self.methane.isentropic_exponent,
                                                        eta_s = self.adiabatic_efficiency)
    @polytropic_efficiency.setter
    def polytropic_efficiency(self, value):
        self.adiabatic_efficiency = compressible_fluid.isentropic_efficiency(P1 = self._inlet_pressure.value,
                                                                             P2 = self._outlet_pressure.value,
                                                                             k = self.methane.isentropic_exponent,
                                                                             eta_p = value)
    @property
    def power(self):
        work = compressible_fluid.isentropic_work_compression(T1 = self.inlet_temperature,
                                                              k = self.methane.isentropic_exponent,
                                                              Z = self.methane.Z,
                                                              P1 = self._inlet_pressure.value,
                                                              P2 = self._outlet_pressure.value,
                                                              eta = self.adiabatic_efficiency)
        return work * self.inlet_mass_flowrate / self.methane.MW
    @classmethod
    def list_objects(cls):
        return cls.items

class Expander(_PressureChangers):
    items = []
    def __init__(self, **inputs) -> None:
        self.outlet_energy_tag = None if 'outlet_energy_tag' not in inputs else inputs['outlet_energy_tag']
        super().__init__(**inputs)
        Expander.items.append(self)
        
    def __eq__(self, other):
        if isinstance(other, Expander):
            return self.tag == other.tag
        else:
            return False
    
    def __repr__(self):
        return "Expander with tag: " + self.tag
    def __hash__(self):
        return hash(self.__repr__())
    
    @classmethod
    def list_objects(cls):
        return cls.items

# End of final classes of compressors

# Start of final classes of Piping and Instruments
class PipeSegment(_EquipmentOneInletOutlet):
    items = []
    def __init__(self, **inputs) -> None:
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
        PipeSegment.items.append(self)
        
    def __eq__(self, other):
        if isinstance(other, PipeSegment):
            return self.tag == other.tag
        else:
            return False
    
    def __repr__(self):
        return "Pipe Segment with tag: " + self.tag   #ADD SEGMENT TYPE!!
    def __hash__(self):
        return hash(self.__repr__())

    @property
    def pressure_drop(self):
        from fluids.friction import friction_factor
        from fluids.core import Reynolds, K_from_f, dP_from_K
        if (self._inlet_pressure.value == None or
            self._outlet_pressure.value == None or
            self.inlet_mass_flowrate == 0):
            return 0
        roughness = (4.57e-5, 4.5e-5, 0.000259, 1.5e-5, 1.5e-6) #in meters
        water = Chemical('water',
                         T = self.inlet_temperature,
                         P = self._inlet_pressure.value)
        Re = Reynolds(V=(self.inlet_mass_flowrate/water.rhol)/(pi* self.ID**2)/4,
                      D=self.ID, 
                      rho=water.rhol, 
                      mu=water.mul)
        fd = friction_factor(Re, eD=roughness[self.material-1]/self.ID)
        K = K_from_f(fd=fd, L=self.length, D=self.ID)        
        drop = round(dP_from_K(K, rho=1000, V=3),3)
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

class ControlValve(_EquipmentOneInletOutlet):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        ControlValve.items.append(self)
    
    def __eq__(self, other):
        if isinstance(other, ControlValve):
            return self.tag == other.tag
        else:
            return False
    
    def __repr__(self):
        return "Control Valve with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @property
    def Kv(self):
        # UPDATE BELOW BASED ON STREAMS
        water = Chemical('water',
                         T = self.inlet_temperature,
                         P = self._inlet_pressure.value)
        if water.phase == 'l':
            return cv_calculations.size_control_valve_l(water.rhol, water.Psat, water.Pc, water.mul,
                                                        self._inlet_pressure.value, self._outlet_pressure.value, 
                                                        self.inlet_mass_flowrate/water.rhol)
        elif water.phase == 'g':
            return cv_calculations.size_control_valve_g(T = self.inlet_temperature, 
                                                        MW = water.MW,
                                                        mu= 1.48712E-05, # water.mug,
                                                        gamma = water.isentropic_exponent, 
                                                        Z = water.Zg,
                                                        P1 = self._inlet_pressure.value, 
                                                        P2 = self._outlet_pressure.value, 
                                                        Q = self.inlet_mass_flowrate/water.rhog)
        else:
            raise Exception('Possibility of fluid solification at control valve')

    @classmethod
    def list_objects(cls):
        return cls.items
        
class PressureSafetyValve(_EquipmentOneInletOutlet):
    items = []
    def __init__(self, **inputs) -> None:
        
        PressureSafetyValve.items.append(self)
        super().__init__(**inputs)
    
    def __eq__(self, other):
        if isinstance(other, PressureSafetyValve):
            return self.tag == other.tag
        else:
            return False

    
    def __repr__(self):
        return "Pressure Safety Valve with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @classmethod
    def list_objects(cls):
        return cls.items

class FlowMeter(_EquipmentOneInletOutlet):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        FlowMeter.items.append(self)
    
    def __eq__(self, other):
        if isinstance(other, FlowMeter):
            return self.tag == other.tag
        else:
            return False
    
    def __repr__(self):
        return "Flow Meter with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @classmethod
    def list_objects(cls):
        return cls.items
# End of final classes of Piping and instruments

# Start of final classes of vessels
class VerticalSeparator(_Vessels):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        VerticalSeparator.items.append(self)
    
    def __eq__(self, other):
        if isinstance(other, VerticalSeparator):
            return self.tag == other.tag
        else:
            return False
    
    def __repr__(self):
        return "Vertical Separator with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @classmethod
    def list_objects(cls):
        return cls.items

class HorizontalSeparator(_Vessels):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        HorizontalSeparator.items.append(self)
    
    def __eq__(self, other):
        if isinstance(other, HorizontalSeparator):
            return self.tag == other.tag
        else:
            return False
    
    def __repr__(self):
        return "Horizontal Separator with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @classmethod
    def list_objects(cls):
        return cls.items

class Column(_Vessels):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        Column.items.append(self)
    
    def __eq__(self, other):
        if isinstance(other, Column):
            return self.tag == other.tag
        else:
            return False
    
    def __repr__(self):
        return "Column with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())
    
    @classmethod
    def list_objects(cls):
        return cls.items

class Tank(_Vessels):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        Tank.items.append(self)
    
    def __eq__(self, other):
        if isinstance(other, Tank):
            return self.tag == other.tag
        else:
            return False
    
    def __repr__(self):
        return "Tank with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())
    
    @classmethod
    def list_objects(cls):
        return cls.items
# End of final classes of vessels

# Start of final classes of heat exchangers
class ShellnTubeExchanger(_Exchanger):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        ShellnTubeExchanger.items.append(self)
    
    def __eq__(self, other):
        if isinstance(other, ShellnTubeExchanger):
            return self.tag == other.tag
        else:
            return False
    
    def __repr__(self):
        return "Shell & Tube Exchanger with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())
    
    @classmethod
    def list_objects(cls):
        return cls.items

class AirCoolers(_Exchanger):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        AirCoolers.items.append(self)
    
    def __eq__(self, other):
        if isinstance(other, AirCoolers):
            return self.tag == other.tag
        else:
            return False
    
    def __repr__(self):
        return "Air Coolers with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())
    
    @classmethod
    def list_objects(cls):
        return cls.items
# End of final classes of heat exchangers      

#Get equipment index function
def get_equipment_index(tag, equipment_type=None):
    
    #If equipment_type is known to the user
    if equipment_type in ['Centrifugal Pump', 'centrifugal pump', 'centrifugal pumps', 'Centrifugal Pumps']:
        return _get_equipment_index_from_quipment_list(tag, CentrifugalPump.list_objects())
    elif equipment_type in ['Positive Displacement Pump', 'PD pumps', 'resiprocating pumps', 'positive displacement pump']:
        return _get_equipment_index_from_quipment_list(tag, PositiveDisplacementPump.list_objects())
    elif equipment_type in ['Centrifugal Compressor', 'centrifugal compressor', 'centrifugal compressors','Centrifugal COmpressors']:
        return _get_equipment_index_from_quipment_list(tag, CentrifugalCompressor.list_objects())
    elif equipment_type in ['Expander', 'expander','expanders','Expanders']:
        return _get_equipment_index_from_quipment_list(tag, Expander.list_objects())
    elif equipment_type in ['Pipe Segment', 'pipe segment', 'piping', 'pipe','Pipe','pipes','Pipes']:
        return _get_equipment_index_from_quipment_list(tag, PipeSegment.list_objects())
    elif equipment_type in ['Control Value', 'cv', 'control valve', 'CV', 'control valves', 'Control Valves']:
        return _get_equipment_index_from_quipment_list(tag, ControlValve.list_objects())
    elif equipment_type in ['Pressure Safety Valve', 'PSV', 'psv', 'safety valves', 'PSVs']:
        return _get_equipment_index_from_quipment_list(tag, PressureSafetyValve.list_objects())
    elif equipment_type in ['Flow Meter', 'flow meter', 'Flow Meters', 'flow meters']:
        return _get_equipment_index_from_quipment_list(tag, FlowMeter.list_objects())
    elif equipment_type in ['Vertical Separator']:
        return _get_equipment_index_from_quipment_list(tag, VerticalSeparator.list_objects())
    elif equipment_type in ['Horizontal Separator']:
        return _get_equipment_index_from_quipment_list(tag, HorizontalSeparator.list_objects())
    elif equipment_type in ['Column', 'column', 'columns', 'Columns']:
        return _get_equipment_index_from_quipment_list(tag, Column.list_objects())
    elif equipment_type in ['Tank', 'tank', 'Tanks', 'tanks']:
        return _get_equipment_index_from_quipment_list(tag, Tank.list_objects())
    elif equipment_type in ['Shell and Tube Heat exchanger', 'S&T HE', 'S&T Heat Exchanger'] :
        return _get_equipment_index_from_quipment_list(tag, ShellnTubeExchanger.list_objects())
    elif equipment_type in ['Air Cooler', 'Air Coolers', 'air coolers']:
        return _get_equipment_index_from_quipment_list(tag, AirCoolers.list_objects())
    
    
    #If user knows the general type of the equipment
    elif equipment_type in ['Pump', 'pump', 'Pumps', 'pumps']:
        return [(_get_equipment_index_from_quipment_list(tag, CentrifugalPump.list_objects()),'Centrifugal Pump'),
                (_get_equipment_index_from_quipment_list(tag, PositiveDisplacementPump.list_objects()),'Positive Displacement Pump')]


    elif equipment_type in ['vessel', 'vessels', 'Vessels', 'Vessel']:
        return [(_get_equipment_index_from_quipment_list(tag, VerticalSeparator.list_objects()),'Verticle Vessel'),
                (_get_equipment_index_from_quipment_list(tag, HorizontalSeparator.list_objects()),'Horizontal Separator'),
                (_get_equipment_index_from_quipment_list(tag, Column.list_objects()),'Column'),
                (_get_equipment_index_from_quipment_list(tag, Tank.list_objects()),'Tank')
                ]
    
    elif equipment_type in ['valve', 'Valve', 'instrument', 'Instrument']:
        return [(_get_equipment_index_from_quipment_list(tag, ControlValve.list_objects()),'Control Valve'),
                (_get_equipment_index_from_quipment_list(tag, PressureSafetyValve.list_objects()),'Pressure Safety Valve'),
                (_get_equipment_index_from_quipment_list(tag, FlowMeter.list_objects()),'Flow Meter')
                ]
    
    elif equipment_type in ['exchangers', 'Exchanger', 'heat exchanger', 'Heat Exchanger',
                            'Heat Exchangers', 'heat exchangers']:
        return  [(_get_equipment_index_from_quipment_list(tag, ShellnTubeExchanger.list_objects()),'Shell and Tube Exchanger'),
                (_get_equipment_index_from_quipment_list(tag, AirCoolers.list_objects()),'Air Cooler')]
    
    # If the user does not know the type of equipment at all
    elif equipment_type == None:
        return (get_equipment_index(tag,'Pump') + 
                get_equipment_index(tag, 'vessel') +
                get_equipment_index(tag, 'valve') +
                get_equipment_index(tag, 'exchangers'))
    else:
        raise Exception('''Invalid Equipment type!! 
                           Valid equipment types are:
                            * Centrifugal Pump
                            * Positive Displacement Pump
                            * Pump if you don't remember the exact type
                            * Centrifugal Compressor
                            * Expander
                            * Pipe Segment
                            * Control Value or CV
                            * Pressure Safety Valve or PSV
                            * Flow Meter
                            * Instruments or Valves if you don't remember the exact type
                            * Vertical Separator
                            * Horizontal Separator
                            * Column
                            * Tank
                            * Vessels if you don't remember the exact type
                            * S&T Heat Exchanger
                            * Air Cooler
                            * Exchanger if you don't remember the exact type''')
    
def _get_equipment_index_from_quipment_list(tag, equipment_list):
    list_of_none_tag_equipments =[]
    for index, equipment in enumerate(equipment_list):
        if equipment.tag == None and tag==None:
            list_of_none_tag_equipments.append(index)           
        elif equipment.tag == tag:
            return index

    return list_of_none_tag_equipments