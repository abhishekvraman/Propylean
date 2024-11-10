import pytest
import unittest
import pandas as pd
from propylean.series import Series as pplSeries
from propylean.properties import Time, Power
d = {'a': 1, 'b': 2, 'c': 3}
df = pd.Series(data=d, index=['a', 'b', 'c'])


class test_Series_pandas(unittest.TestCase): 

    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_Series_pandas_instantiation_required_only(self):
        pps = pplSeries(data={'a': 1, 'b': 2, 'c': 3}, 
                        prop=Power)
        self.assertEqual(pps.prop, Power)
        self.assertEqual(pps.unit, "W")

    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_Series_pandas_instantiation_unit(self):
        pps = pplSeries(data={'a': 1, 'b': 2, 'c': 3}, 
                        prop=Power, unit="MMBTU/h")
        self.assertEqual(pps.prop, Power)
        self.assertEqual(pps.unit, "MMBTU/h")

    @pytest.mark.positive         
    def test_Series_pandas_representation(self):
        pps = pplSeries(df,prop=Time)
        self.assertIn("Property: Time", str(pps))
        self.assertIn("unit: s", str(pps))
        pps = pplSeries(df,prop=Time, unit="hour")
        self.assertIn("Property: Time", str(pps))
        self.assertIn("unit: hour", str(pps))
    
    # @pytest.mark.negative
    # def test_Series_pandas_
