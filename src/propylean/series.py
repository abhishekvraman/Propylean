from pandas import Series as PdSeries
from propylean.validators import _Validators
from propylean.properties import _Property

class Series(PdSeries):
    def __init__(self, data, prop, unit=None, index=None, 
                 dtype=None, name=None, copy=False, fastpath=False) -> None:
        """
        DESCRIPTION:
                Class which wraps Pandas and PySpark Series.
            
            PARAMETERS:  
                data:
                    Required: Yes
                    Type: pandas.Series or pyspark.Series or array-like, dict, or scalar value
                    Acceptable values: Float or int in data structure mentioned in type
                    Default value: NA
                    Description: The data for the series that forms a time series.

                prop:
                    Required: Yes
                    Type: propylean.property
                    Acceptable values: All properties that can be measured.
                    Default value: NA
                    Description: Property class for the series data.
                
                unit:
                    Required: No
                    Type: string
                    Acceptable values: All units associated with property specified in 'prop'.
                    Default value: NA
                    Description: Unit that the property of the series has. If not specified, default unit of
                                 the property is considered.

                
            RETURN VALUE:
                Type: Series
                Description: 
            
            ERROR RAISED:
                Type:
                Description: 
            
            SAMPLE USE CASES:
                >>>  class AwesomeMesuringDevice(_MeasuringInstruments):
                >>>     def __init__(**kwargs):
                >>>         some_property = 20
            
        """
        super().__init__(data=data, index=index, dtype=dtype, 
                         name=name, copy=copy, fastpath=fastpath)
        self._prop = None
        self._unit = None
        self.prop = prop
        self.unit = unit
    
    @property
    def prop(self):
        return self._prop
    @prop.setter
    def prop(self, value):
        _Validators.validate_child_class("prop", value, _Property, "physical or dimensionless property from propylean.properties")
        self._prop = value
    