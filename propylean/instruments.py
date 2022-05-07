from propylean import streams
import propylean.properties as prop
from propylean.generic_equipment_classes import _EquipmentOneInletOutlet
from propylean.settings import Settings
from propylean.constants import Constants
from fluids import control_valve as cv_calculations

class ControlValve(_EquipmentOneInletOutlet):
    items = []
    def __init__(self, **inputs) -> None:
        """ 
        DESCRIPTION:
            Final class for creating objects to represent a Control Valve.
        
        PARAMETERS:
            Read _EquipmentOneInletOutlet class for more arguments for this class
        
        RETURN VALUE:
            Type: ControlValve
            Description: Returns an object of type ControlValve with all properties of
                         a control valve used in process industry.
        
        ERROR RAISED:
            Type:
            Description:
        
        SAMPLE USE CASES:
            >>> CV_1 = ControlValve(tag="CV1")
            >>> print(CV_1)
            Contrl Valve with tag: CV1
        """
        self._index = len(ControlValve.items)
        super().__init__( **inputs)
        del self.energy_in
        del self.energy_out
        ControlValve.items.append(self)
    
    def __repr__(self):
        return "Control Valve with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @property
    def Kv(self):
        self = self._get_equipment_object(self)
        if (self._outlet_material_stream_tag is None and
            self._inlet_material_stream_tag is None):
            raise Exception("PipeSegment should be connected with MaterialStream either at inlet or outlet")
        P1 = self.inlet_pressure
        P2 = self.outlet_pressure
        P1.unit = P2.unit = "Pa"
        stream_tag = self._inlet_material_stream_tag if self._outlet_material_stream_tag is None else self._outlet_material_stream_tag
        stream_index = streams.get_stream_index(stream_tag, "material")
        density = self._stream_object_property_getter(stream_index, "material", "density")
        phase = self._stream_object_property_getter(stream_index, "material", "phase")
        d_viscosity = self._stream_object_property_getter(stream_index, "material", "d_viscosity")
        isentropic_exponent = self._stream_object_property_getter(stream_index, "material", "isentropic_exponent")
        MW = self._stream_object_property_getter(stream_index, "material", "molecular_weight")
        
        Psat = self._stream_object_property_getter(stream_index, "material", "Psat")
        Pc = self._stream_object_property_getter(stream_index, "material", "Pc")
        if phase == 'l':
            return cv_calculations.size_control_valve_l(density.value, Psat, Pc, d_viscosity.value,
                                                        P1.value, P2.value, 
                                                        self.inlet_mass_flowrate.value/density.value)
        elif phase == 'g':
            Z_g = self._stream_object_property_getter(stream_index, "material", "Z_g")
            return cv_calculations.size_control_valve_g(T = self.inlet_temperature.value, 
                                                        MW = MW,
                                                        mu= d_viscosity,
                                                        gamma = isentropic_exponent, 
                                                        Z = Z_g,
                                                        P1 = P1.value, 
                                                        P2 = P2.value, 
                                                        Q = self.inlet_mass_flowrate.value/density.value)
        else:
            raise Exception('Possibility of fluid solification inside the control valve')

    def connect_stream(self, 
                       stream_object=None, 
                       direction=None, 
                       stream_tag=None, 
                       stream_type=None,
                       stream_governed=True):
        if ((stream_object is not None and 
            isinstance(stream_object, streams.EnergyStream)) or
            stream_type in ['energy', 'power', 'e', 'p']):
            raise Exception("No energy stream is associated  with control valve.")
        return super().connect_stream(direction=direction, 
                                      stream_object=stream_object, 
                                      stream_tag=stream_tag, 
                                      stream_type=stream_type,
                                      stream_governed=stream_governed)
    
    def disconnect_stream(self, stream_object=None, direction=None, stream_tag=None, stream_type=None):
        if ((stream_object is not None and 
            isinstance(stream_object, streams.EnergyStream)) or
            stream_type in ['energy', 'power', 'e', 'p']):
            raise Exception("No energy stream is associated  with control valve.")
        return super().disconnect_stream(stream_object, direction, stream_tag, stream_type)

    @classmethod
    def list_objects(cls):
        return cls.items
        
class PressureSafetyValve(_EquipmentOneInletOutlet):
    items = []
    def __init__(self, **inputs) -> None:  
        self._index = len(PressureSafetyValve.items)     
        super().__init__( **inputs)
        PressureSafetyValve.items.append(self)
    
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
        self._index = len(FlowMeter.items)
        super().__init__( **inputs)
        del self.energy_out
        del self.energy_in
        FlowMeter.items.append(self)

    def __repr__(self):
        return "Flow Meter with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @classmethod
    def list_objects(cls):
        return cls.items
# End of final classes of Piping and instruments