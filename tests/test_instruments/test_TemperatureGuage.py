import pytest
import unittest
from propylean.instruments.measurement import TemperatureGuage
from propylean.streams import MaterialStream, EnergyStream
import propylean.properties as prop

class test_TemperatureGuage(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_TemperatureGuage_instantiation_only_tag(self):
        pg_1 = TemperatureGuage(tag="PG-101")
        self.assertEqual(pg_1.tag, "PG-101")
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_TemperatureGuage_instantiation_tag_and_temperature(self):
        temperature_guage = TemperatureGuage(tag="temperature_guage_2",
                          measured_unit='C')
        self.assertEqual(temperature_guage.tag, "temperature_guage_2")
        self.assertEqual(temperature_guage.measured_property, prop.Temperature)
        self.assertEqual(temperature_guage.measured_unit, 'C')
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_TemperatureGuage_instantiation_no_arguments(self):
        temperature_guage = TemperatureGuage()
        self.assertIsNotNone(temperature_guage.tag)
        self.assertEqual(temperature_guage.measured_property, prop.Temperature)
        self.assertEqual(temperature_guage.measured_unit, 'C')
    
    @pytest.mark.positive
    def test_TemperatureGuage_representation(self):
        temperature_guage = TemperatureGuage(tag="temperature_guage_5")
        self.assertIn("TemperatureGuage with tag: temperature_guage_5", str(temperature_guage))
    
    @pytest.mark.negative
    def test_TemperatureGuage_measured_unit_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.measured_unit = []
        self.assertIn("Incorrect type 'list' provided to 'measured_unit'. Should be 'str'",
                      str(exp))

    @pytest.mark.negative
    def test_TemperatureGuage_measured_property_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.measured_property = []
        self.assertIn("Cannot set measured_property of TemperatureGuage",
                      str(exp)) 

    @pytest.mark.negative
    def test_TemperatureGuage_i_range_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.i_range = []
        self.assertIn("Incorrect type 'list' provided to 'i_range'. Should be 'tuple'",
                      str(exp))                                    

    # @pytest.mark.negative
    # def test_TemperatureGuage_design_temperature_incorrect_type_to_value(self):
    #     with pytest.raises(Exception) as exp:
    #         m4 = TemperatureGuage()
    #         m4.design_temperature = []
    #     self.assertIn("Incorrect type 'list' provided to 'design_temperature'. Can be any one from '('Temperature', 'int', 'float', 'tuple', 'Series')'",
    #                   str(exp)) 


    @pytest.mark.negative
    def test_TemperatureGuage_resolution_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.resolution = []
        self.assertIn("Incorrect type 'list' provided to 'resolution'. Can be any one from '('int', 'float')'",
                      str(exp)) 
    
    @pytest.mark.negative
    def test_TemperatureGuage_resolution_incorrect_value_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.resolution = -1
        self.assertIn("Value passed to 'resolution' should be greater than 0.",
                      str(exp)) 
