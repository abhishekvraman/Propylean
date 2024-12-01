from pandas import Series as PdSeries
from pyspark.pandas import Series as SpkSeries
from propylean.validators import _Validators
from propylean.properties import _Property
from tabulate import tabulate

class Series():
    def __init__(self, data, prop, unit=None, index=None, is_spark=False,
                 dtype=None, name=None, copy=False) -> None:
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
                index:
                    Required: No
                    Type: Array type
                    Description: Refer Pandas.series or pyspark.series documention.
                dtype:
                    Required: No
                    Type: Array type
                    Description: Refer Pandas.series or pyspark.series documention
                name:
                    Required: No
                    Type: Array type
                    Description: Refer Pandas.series or pyspark.series documention
                copy:
                    Required: No
                    Type: Array type
                    Description: Refer Pandas.series or pyspark.series documention

            RETURN VALUE:
                Type: Series
                Description: 
            
            ERROR RAISED:
                Type:
                Description: 
            
            SAMPLE USE CASES:
                >>> from propylean import Series
                >>> from propylean.properties import Length
                >>> r = [1, 2]
                >>> ser = Series(r, prop=Length copy=False)
            
        """
        self._prop = None
        self._unit = None
        self.prop = prop
        self._is_spark = is_spark
        self.unit = unit if unit is not None else prop().unit
        if isinstance(data, PdSeries):
            self.instance = data
        elif isinstance(data, SpkSeries):
            self.instance = data
            self._is_spark = True
        elif is_spark:
            self.instance = SpkSeries(data=data,index=index,dtype=dtype,
                                      name=name, copy=copy)
        else:
            self.instance = PdSeries(data=data,index=index,dtype=dtype,
                                      name=name, copy=copy)
    
    @property
    def prop(self):
        return self._prop
    @prop.setter
    def prop(self, value):
        _Validators.validate_child_class("prop", value, _Property, "physical or dimensionless property from propylean.properties")
        self._prop = value
    @property
    def unit(self):
        return self._unit
    @unit.setter
    def unit(self, value):
        _Validators.validate_property_unit(self._prop, value)
        self._unit = value

    def __repr__(self) -> str:
        values_to_tabulate = []
        for val in self.instance.head().array.tolist():
            values_to_tabulate.append([val])
        if len(self.instance.array.tolist()) > 5:
            values_to_tabulate.append([":"])
            values_to_tabulate.append([":"])
            
        return "Property: {}\nunit: {}\n".format(self._prop.__name__, self._unit) + tabulate(values_to_tabulate)
    
    def __getattr__(self, name):
        return self.instance.__getattribute__(name)
    
    def __add__(self, other):
        self._arithmetic_operation(other, "+")        
            
    def __sub__(self, other):
        self._arithmetic_operation(other, "-")

    def __truediv__(self, other):
        self._arithmetic_operation(other, "/")

    def _arithmetic_operation(self, other, arithmetic_operater):
        if isinstance(other, Series) and not isinstance(other._prop, self._prop):
            raise Exception("Physical property of both Series operands must be same. You provided {} {} {}".format(self._prop, arithmetic_operater, other.prop))
        if isinstance(other, _Property) and self.unit != other.unit:
            other.unit = self.unit                    
        elif self.unit != other.unit:
            raise Exception("Operand unit of measurment do not match.")
        
        if isinstance(other, Series):
            if arithmetic_operater == "+":
                data = self.instance.add(other.instance)
            elif arithmetic_operater == "-":
                data = self.instance.sub(other.instance)
            elif arithmetic_operater == "/":
                data = self.instance.truediv(other.instance)
        else:
            if arithmetic_operater == "+":     
                data = self.instance + other.value
            elif arithmetic_operater == "-":
                data = self.instance - other.value
            elif arithmetic_operater == "/":
                data = self.instance / other.value

        return type(self)(data=data, prop=self.prop,
                        unit=self.unit, index=self.instance.index, 
                        is_spark=self._is_spark, dtype=self.instance.dtype, 
                        name=self.instance.name, copy=self.instance.copy)
