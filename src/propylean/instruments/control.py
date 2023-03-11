from propylean import streams
import propylean.properties as prop
from propylean.equipments.generic_equipment_classes import _EquipmentOneInletOutlet
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
        super().__init__( **inputs)
        del self.energy_in
        del self.energy_out
        self._index = len(ControlValve.items)
        ControlValve.items.append(self)
    
    def __repr__(self):
        self = self._get_equipment_object(self)
        return "Control Valve with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @property
    def Cv(self):
        self = self._get_equipment_object(self)
        if (self._outlet_material_stream_tag is None and
            self._inlet_material_stream_tag is None):
            raise Exception("PipeSegment should be connected with MaterialStream either at inlet or outlet")
        P1 = self.inlet_pressure
        P2 = self.outlet_pressure
        P1.unit = P2.unit = "Pa"
        is_inlet = True if self._outlet_material_stream_tag is None else False
        density = self._connected_stream_property_getter(is_inlet, "material", "density")
        phase = self._connected_stream_property_getter(is_inlet, "material", "phase")
        d_viscosity = self._connected_stream_property_getter(is_inlet, "material", "d_viscosity")
        isentropic_exponent = self._connected_stream_property_getter(is_inlet, "material", "isentropic_exponent")
        MW = self._connected_stream_property_getter(is_inlet, "material", "molecular_weight")
        Psat = self._connected_stream_property_getter(is_inlet, "material", "Psat")
        Pc = self._connected_stream_property_getter(is_inlet, "material", "Pc")
        if phase == 'l':
            return cv_calculations.size_control_valve_l(density.value, Psat.value, Pc.value, d_viscosity.value,
                                                        P1.value, P2.value, 
                                                        self.inlet_mass_flowrate.value/density.value)
        elif phase == 'g' or phase == 'l/g':
            Z_g = self._connected_stream_property_getter(is_inlet, "material", "Z_g")
            return cv_calculations.size_control_valve_g(T = self.inlet_temperature.value, 
                                                        MW = MW.value,
                                                        mu= d_viscosity.value,
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
            stream_type in ['energy', 'e']):
            raise Exception("No energy stream is associated  with control valve.")
        return super().connect_stream(direction=direction, 
                                      stream_object=stream_object, 
                                      stream_tag=stream_tag, 
                                      stream_type=stream_type,
                                      stream_governed=stream_governed)
    
    def disconnect_stream(self, stream_object=None, direction=None, stream_tag=None, stream_type=None):
        if ((stream_object is not None and 
            isinstance(stream_object, streams.EnergyStream)) or
            stream_type in ['energy', 'e']):
            raise Exception("No energy stream is associated  with control valve.")
        return super().disconnect_stream(stream_object, direction, stream_tag, stream_type)

    @classmethod
    def list_objects(cls):
        return cls.items
        