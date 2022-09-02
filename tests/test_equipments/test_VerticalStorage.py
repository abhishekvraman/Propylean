import pytest
import unittest
from propylean.equipments.storages import VerticalStorage
from propylean import properties as prop

class test_VerticalStorage(unittest.TestCase):
    def test_VerticalStorage_representation(self):
        vessel = VerticalStorage(tag="Silo_1")
        self.assertIn("Vertical Storage with tag: Silo_1", str(vessel))
    
    def test_VerticalStorage_blanketing(self):
        v_1 = VerticalStorage(is_blanketed=True, tag="Ethenol_feed_tank")
        v_1.operating_pressure = prop.Pressure(1.5, "atm")
        self.assertEqual(v_1.blanketing.inlet_pressure, prop.Pressure(1.5, "atm"))
        self.assertEqual(v_1.blanketing.outlet_pressure, prop.Pressure(1.5, "atm"))

        self.assertIn("Blanketing with tag: Ethenol_feed_tank_blanketing",
                      str(v_1.blanketing))

    @pytest.mark.negative
    def test_VerticalStorage_inlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.inlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_VerticalStorage_outlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.outlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_VerticalStorage_pressure_drop_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.pressure_drop = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'pressure_drop'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                    

    @pytest.mark.negative
    def test_VerticalStorage_design_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.design_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_VerticalStorage_inlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.inlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_VerticalStorage_outlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.outlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_VerticalStorage_temperature_decrease_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.temperature_decrease = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'temperature_decrease'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_VerticalStorage_temperature_increase_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.temperature_increase = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'temperature_increase'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                                      

    @pytest.mark.negative
    def test_VerticalStorage_design_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.design_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_VerticalStorage_inlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.inlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_VerticalStorage_outlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.outlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_VerticalStorage_energy_in_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.energy_in = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_in'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))      

    @pytest.mark.negative
    def test_VerticalStorage_energy_out_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.energy_out = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_out'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))   

    @pytest.mark.negative
    def test_VerticalStorage_ID_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            horizontal_vessel = VerticalStorage(
                                               ID=[4, "m"], length=(10, "m"),
                                               head_type="flat")
        self.assertIn("Incorrect type '<class 'list'>' provided to 'ID'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.ID = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'ID'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_VerticalStorage_length_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            horizontal_vessel = VerticalStorage(
                                               ID=(4, "m"), length=[10, "m"],
                                               head_type="flat")
        self.assertIn("Incorrect type '<class 'list'>' provided to 'length'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.length = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'length'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                  

    @pytest.mark.negative
    def test_VerticalStorage_heayd_type_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            horizontal_vessel = VerticalStorage(
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type=["flat"])
        self.assertIn("Incorrect type '<class 'list'>' provided to 'head_type'. Should be '<class 'str'>'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.head_type = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'head_type'. Should be '<class 'str'>'",
                      str(exp))

    @pytest.mark.negative
    def test_VerticalStorage_LLLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.LLLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'LLLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                    

    @pytest.mark.negative
    def test_VerticalStorage_LLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.LLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'LLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_VerticalStorage_NLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.NLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'NLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_VerticalStorage_HLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.HLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'HLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_VerticalStorage_HHLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.HHLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'HHLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))   

    @pytest.mark.negative
    def test_VerticalStorage_operating_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.operating_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'operating_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))  

    @pytest.mark.negative
    def test_VerticalStorage_operating_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.operating_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'operating_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                  
                      
    @pytest.mark.negative
    def test_VerticalStorage_heayd_type_incorrect_value(self):
        with pytest.raises(Exception) as exp:
            Vertical_vessel = VerticalStorage(
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type="flatop")
        self.assertIn("Incorrect value \'flatop\' provided to \'head_type\'. Should be among \'[\'hemispherical\', \'elliptical\', \'torispherical\', \'flat\']\'.\\n            ",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.head_type = "flatop"
        self.assertIn("Incorrect value \'flatop\' provided to \'head_type\'. Should be among \'[\'hemispherical\', \'elliptical\', \'torispherical\', \'flat\']\'.\\n            ",
                      str(exp))                       