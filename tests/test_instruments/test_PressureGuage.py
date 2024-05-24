import pytest
import unittest
from propylean.instruments.measurement import PressureGuage
from propylean.streams import MaterialStream, EnergyStream
import propylean.properties as prop

class test_PressureGuage(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_PressureGuage_instantiation_only_tag(self):
        pg_1 = PressureGuage(tag="PG-101")
        self.assertEqual(pg_1.tag, "PG-101")
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_PressureGuage_instantiation_tag_and_pressure(self):
        pressure_guage = PressureGuage(tag="pressure_guage_2",
                          measured_unit='bar')
        self.assertEqual(pressure_guage.tag, "pressure_guage_2")
        self.assertEqual(pressure_guage.measured_property, prop.Pressure)
        self.assertEqual(pressure_guage.measured_unit, 'bar')
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_PressureGuage_instantiation_no_arguments(self):
        pressure_guage = PressureGuage()
        self.assertIsNotNone(pressure_guage.tag)
        self.assertEqual(pressure_guage.measured_property, prop.Pressure)
        self.assertEqual(pressure_guage.measured_unit, 'Pa')
    
    @pytest.mark.positive
    def test_PressureGuage_representation(self):
        pressure_guage = PressureGuage(tag="pressure_guage_5")
        self.assertIn("PressureGuage with tag: pressure_guage_5", str(pressure_guage))
    
    @pytest.mark.negative
    def test_PressureGuage_measured_unit_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PressureGuage()
            m4.measured_unit = []
        self.assertIn("Incorrect type 'list' provided to 'measured_unit'. Should be 'str'",
                      str(exp))

    @pytest.mark.negative
    def test_PressureGuage_measured_property_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PressureGuage()
            m4.measured_property = []
        self.assertIn("Cannot set measured_property of PressureGuage",
                      str(exp)) 

    @pytest.mark.negative
    def test_PressureGuage_i_range_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PressureGuage()
            m4.i_range = []
        self.assertIn("Incorrect type 'list' provided to 'i_range'. Should be 'tuple'",
                      str(exp))                                    

    # @pytest.mark.negative
    # def test_PressureGuage_design_pressure_incorrect_type_to_value(self):
    #     with pytest.raises(Exception) as exp:
    #         m4 = PressureGuage()
    #         m4.design_pressure = []
    #     self.assertIn("Incorrect type 'list' provided to 'design_pressure'. Can be any one from '('Pressure', 'int', 'float', 'tuple')'",
    #                   str(exp)) 


    @pytest.mark.negative
    def test_PressureGuage_resolution_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PressureGuage()
            m4.resolution = []
        self.assertIn("Incorrect type 'list' provided to 'resolution'. Can be any one from '('int', 'float')'",
                      str(exp)) 
    
    @pytest.mark.negative
    def test_PressureGuage_resolution_incorrect_value_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PressureGuage()
            m4.resolution = -1
        self.assertIn("Value passed to 'resolution' should be greater than 0.",
                      str(exp)) 
