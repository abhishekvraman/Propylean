import pytest
import unittest
import pandas as pd
from propylean.series import Series as pplSeries
from propylean.properties import Time, Power
from pyspark.sql import SparkSession
from pyspark.pandas import Series as spkSeries

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
r = [1, 2]
df = spkSeries(r,copy=False)


class test_Series_pyspark(unittest.TestCase): 

    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_Series_pyspark_instantiation_required_only(self):
        pps = pplSeries(data={'a': 1, 'b': 2, 'c': 3}, 
                        prop=Power, is_spark=True)
        self.assertEqual(pps.prop, Power)
        self.assertEqual(pps.unit, "W")

    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_Series_pyspark_instantiation_unit(self):
        pps = pplSeries(data={'a': 1, 'b': 2, 'c': 3}, is_spark=True,
                        prop=Power, unit="MMBTU/h")
        self.assertEqual(pps.prop, Power)
        self.assertEqual(pps.unit, "MMBTU/h")

    @pytest.mark.positive         
    def test_Series_pyspark_representation(self):
        pps = pplSeries(df, prop=Time)
        self.assertIn("Property: Time", str(pps))
        self.assertIn("unit: s", str(pps))
        pps = pplSeries(df, prop=Time, unit="hour")
        self.assertIn("Property: Time", str(pps))
        self.assertIn("unit: hour", str(pps))
    
    @pytest.mark.negative
    def test_Series_pyspark_incorrect_instantiation_required_only(self):
        from propylean import CentrifugalCompressor
        with pytest.raises(Exception) as exp:
            pps = pplSeries(df, prop=CentrifugalCompressor)
        self.assertIn("Invalid type provided for 'prop'. Should be a class of type physical or dimensionless property from propylean.properties.",
                      str(exp))
        
    @pytest.mark.negative
    def test_Series_pyspark_incorrect_instantiation_unit(self):
        with pytest.raises(Exception) as exp:
            pps = pplSeries(df, prop=Time, unit="C")
        self.assertIn("Selected unit is not supported or a correct unit of Time",
                      str(exp))