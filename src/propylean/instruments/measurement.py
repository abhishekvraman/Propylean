from propylean.equipments.generic_equipment_classes import _EquipmentOneInletOutlet

class _MeasuringInstruments(object):
    def __init__(self, measured_property, measurment_unit, **inputs) -> None:
        """ 
            DESCRIPTION:
                Parent class for all instruments having primary task to
                measure properties.
            
            PARAMETERS:
                measured_property:
                    Required: Yes
                    Type: propylean.property
                    Acceptable values: All properties that can be measured.
                    Default value: NA
                    Description: Property class that the instrument measures.
                
                measurment_unit:
                    Required: Yes
                    Type: string
                    Acceptable values: All units.
                    Default value: NA
                    Description: Unit that the instrument measures.    
                
                range:
                    Required: No
                    Type: tuple
                    Acceptable values: Tuple with two elements. 
                                       First representing minimum measured and second maximum. 
                    Default value: NA
                    Description: Specifies the range of instrument can measure.
                 

            RETURN VALUE:
                Type: _MeasuringInstruments
                Description: 
            
            ERROR RAISED:
                Type:
                Description: 
            
            SAMPLE USE CASES:
                >>>  class AwesomeMesuringDevice(_MeasuringInstruments):
                >>>     def __init__(**kwargs):
                >>>         some_property = 20
                
        """
        self.measured_property = measured_property
        self.measured_unit = measurment_unit
        self.range = range

class FlowMeter(_EquipmentOneInletOutlet, _MeasuringInstruments):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__( **inputs)
        del self.energy_out
        del self.energy_in
        self._index = len(FlowMeter.items)
        FlowMeter.items.append(self)

    def __repr__(self):
        self = self._get_equipment_object(self)
        return "Flow Meter with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @classmethod
    def list_objects(cls):
        return cls.items

class PressureGuage(_MeasuringInstruments):
    items = []
    def __init__(self) -> None:
        pass

class TemperatureGuage(_MeasuringInstruments):
    items = []
    def __init__(self) -> None:
        pass
