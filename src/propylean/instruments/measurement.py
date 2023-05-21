from propylean.equipments.generic_equipment_classes import _EquipmentOneInletOutlet

class _MeasuringInstruments(object):
    def __init__(self,**inputs) -> None:
        """ 
            DESCRIPTION:
                Parent class for all instruments which has primary task to
                measure observations.
            
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
                
                observed_series:
                    Required: No
                    Type: Series
                    Description: Specifies the time series observed by the instrument.  

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
class FlowMeter(_EquipmentOneInletOutlet):
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
