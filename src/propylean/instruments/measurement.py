from propylean.equipments.generic_equipment_classes import _EquipmentOneInletOutlet
from propylean.validators import _Validators
from propylean.properties import _Property, Pressure, Temperature, VolumetricFlowRate
from propylean.series import Series

# Base class for all instruments that measures (makes observations).
# Classes derived from this act as data store.
class _MeasuringInstruments(object):
    items = []
    def __init__(self, measured_property, measured_unit, **inputs) -> None:
        """ 
            DESCRIPTION:
                Parent class for all instruments having primary task to
                measure properties as observations which could be stored in
                a databases.
            
            PARAMETERS:            
                measured_property:
                    Required: Yes
                    Type: propylean.property
                    Acceptable values: All properties that can be measured.
                    Default value: NA
                    Description: Property class that the instrument measures.
                
                measured_unit:
                    Required: Yes
                    Type: string
                    Acceptable values: All units associated with measured_property.
                    Default value: NA
                    Description: Unit that the instrument measures for the measured_property.

                tag:
                    Required: No
                    Type: str
                    Acceptable values: Any string type
                    Default value: None
                    Description: Instrument tag the user wants to provide. If not provided, then tag is automatically generated.
                
                i_range:
                    Required: No
                    Type: tuple
                    Acceptable values: Tuple with two elements. 
                                       First element representing minimum measured and second element
                                       representing the maximum value instrument can measure.
                                       Both are inclusive.
                    Default value: NA
                    Description: Specifies the Range of the instrument. That is minimum to maximum
                                 values that can be measured.
                
                resolution:
                    Required: No
                    Type: float or int
                    Acceptable values: All positive values.
                    Default value: NA
                    Description: Specifies the Resolution of the instrument.

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
        self._measured_property = measured_property
        self.measured_unit = measured_unit
        self._i_range = inputs.pop("i_range", None)
        self._resolution = inputs.pop("resolution", None)
        if self._resolution is not None:
            self.resolution = self._resolution
        self._observations = None
        self.tag = inputs.pop("tag", self._create_instrument_tag())
        
    def _get_instrument_index(cls, tag):
        for index, instrument in enumerate(cls.items):
            if instrument.tag == tag:
                return index
        return None
    
    @classmethod
    def _get_instrument_object(cls, obj):
        try:
            return cls.items[obj.index]
        except IndexError:
            raise Exception("Instrument does not exist!")
        except AttributeError:
            return obj
    
    @classmethod
    def _update_instrument_object(cls, obj):
        _Validators.validate_arg_prop_value_type("obj", obj, cls)
        try:
            cls.items[obj.index] = obj
        except:
            pass
    
    @property
    def index(self):
      return self._index
    
    @property
    def tag(self):
        return self._tag
    @tag.setter
    def tag(self, value):
        _Validators.validate_arg_prop_value_type("tag", value, (str))
        if self._check_tag_assigned(value):
            msg = "Tag '{}' already assigned!".format(value)
            raise Exception(msg)
        else:
            self._tag = value
    
    def _create_instrument_tag(cls):
        i = 1
        class_name = type(cls).__name__
        tag = class_name+ "_" + str(i)
        while cls._check_tag_assigned(tag):
            tag = class_name+ "_" + str(i)
            i += 1
        return tag
    def _check_tag_assigned(cls, tag):
        for instru in cls.items:
            if tag == instru.tag:
                return True
        return False
    
    @property
    def measured_property(self):
        self = self._get_instrument_object(self)
        return self._measured_property
    @measured_property.setter
    def measured_property(self, value):
        _Validators.validate_child_class("measured_property",
                                         value,
                                         _Property,
                                         "propylean.property")
        self = self._get_instrument_object(self)
        self._measured_property = value
        self._update_instrument_object(self)

    @property
    def measured_unit(self):
        self = self._get_instrument_object(self)
        return self._measured_unit
    @measured_unit.setter
    def measured_unit(self, value):
        #Need to get list of units based on measured_property and validate.
        self = self._get_instrument_object(self)
        _Validators.validate_arg_prop_value_type(arg_prop_name="measured_unit",
                                                 value=value,
                                                 correct_types=str)
        # Validate the unit.
        self.measured_property(unit=value)

        self._measured_unit = value
        self._update_instrument_object(self)
    
    @property
    def i_range(self):
        self = self._get_instrument_object(self)
        return self._i_range
    @i_range.setter
    def i_range(self, value):
        _Validators.validate_arg_prop_value_type("i_range", value, tuple)
        self = self._get_instrument_object(self)
        self._i_range = value
        self._update_instrument_object(self)

    @property
    def resolution(self):
        self = self._get_instrument_object(self)
        return self._resolution
    @resolution.setter
    def resolution(self, value):
        _Validators.validate_arg_prop_value_type("resolution", value, (int, float))
        _Validators.validate_positive_value("resolution", value)
        self = self._get_instrument_object(self)
        self._resolution = value
        self._update_instrument_object(self)

    @property
    def observations(self):
        self = self._get_instrument_object(self)
        return self._observations
    @observations.setter
    def observations(self, value):
        _Validators.validate_arg_prop_value_type("observations", value, Series)
        self._observations = value
        self._update_instrument_object(self)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.tag == other.tag
        else:
            return False
    
    
class PressureGuage(_MeasuringInstruments):
    items = []
    def __init__(self, measured_unit="Pa", **inputs) -> None:
        super().__init__(measured_property=Pressure, measured_unit=measured_unit, **inputs)
        self._index = len(PressureGuage.items)
        PressureGuage.items.append(self)

    def __repr__(self):
        self = self._get_instrument_object(self)
        return "PressureGuage with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @classmethod
    def list_objects(cls):
        return cls.items
    
    @_MeasuringInstruments.measured_property.setter
    def measured_property(self, value):
        raise Exception("Cannot set measured_property of PressureGuage")


class TemperatureGuage(_MeasuringInstruments):
    items = []
    def __init__(self, measured_unit="C", **inputs) -> None:
        super().__init__(measured_property=Temperature, measured_unit=measured_unit, **inputs)
        self._index = len(TemperatureGuage.items)
        TemperatureGuage.items.append(self)

    def __repr__(self):
        self = self._get_instrument_object(self)
        return "TemperatureGuage with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @classmethod
    def list_objects(cls):
        return cls.items

    @_MeasuringInstruments.measured_property.setter
    def measured_property(self, value):
        raise Exception("Cannot set measured_property of TemperatureGuage")

class FlowMeter(_EquipmentOneInletOutlet): 
    """
      Eventhough Flow meter is an instrument, it kind of acts like an
      inline equipment as it shares properties and is connected to equipments(pipes)
      on both inlet and outlet.
    """ 
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