import pytest
import unittest
from propylean.equipments.storages import Sphere
from propylean import properties as prop

class test_Sphere(unittest.TestCase):
    def test_Sphere_representation(self):
        vessel = Sphere(tag="TKS-4555")
        self.assertIn("Sphere with tag: TKS-4555", str(vessel))
    
    def test_Sphere_blanketing(self):
        v_1 = Sphere(is_blanketed=True, tag="Propylene Export Storage")
        v_1.operating_pressure = prop.Pressure(1.5, "atm")
        self.assertEqual(v_1.blanketing.inlet_pressure, prop.Pressure(1.5, "atm"))
        self.assertEqual(v_1.blanketing.outlet_pressure, prop.Pressure(1.5, "atm"))

        self.assertIn("Blanketing with tag: Propylene Export Storage_blanketing",
                      str(v_1.blanketing))

    @pytest.mark.negative
    def test_Sphere_inlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.inlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_Sphere_outlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.outlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_Sphere_pressure_drop_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.pressure_drop = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'pressure_drop'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                    

    @pytest.mark.negative
    def test_Sphere_design_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.design_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_Sphere_inlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.inlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_Sphere_outlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.outlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_Sphere_temperature_decrease_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.temperature_decrease = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'temperature_decrease'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_Sphere_temperature_increase_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.temperature_increase = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'temperature_increase'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                                      

    @pytest.mark.negative
    def test_Sphere_design_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.design_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_Sphere_inlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.inlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_Sphere_outlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.outlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_Sphere_energy_in_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.energy_in = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_in'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))      

    @pytest.mark.negative
    def test_Sphere_energy_out_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.energy_out = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_out'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                      

    @pytest.mark.negative
    def test_Sphere_ID_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            horizontal_vessel = Sphere(
                                               ID=[4, "m"], length=(10, "m"),
                                               head_type="flat")
        self.assertIn("Incorrect type '<class 'list'>' provided to 'ID'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.ID = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'ID'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_Sphere_length_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            horizontal_vessel = Sphere(
                                               ID=(4, "m"), length=[10, "m"],
                                               head_type="flat")
        self.assertIn("Incorrect type '<class 'list'>' provided to 'length'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.length = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'length'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                  

    @pytest.mark.negative
    def test_Sphere_heayd_type_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            horizontal_vessel = Sphere(
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type=["flat"])
        self.assertIn("Incorrect type '<class 'list'>' provided to 'head_type'. Should be '<class 'str'>'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.head_type = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'head_type'. Should be '<class 'str'>'",
                      str(exp))

    @pytest.mark.negative
    def test_Sphere_LLLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.LLLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'LLLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                    

    @pytest.mark.negative
    def test_Sphere_LLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.LLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'LLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_Sphere_NLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.NLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'NLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_Sphere_HLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.HLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'HLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_Sphere_HHLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.HHLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'HHLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))   

    @pytest.mark.negative
    def test_Sphere_operating_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.operating_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'operating_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))  

    @pytest.mark.negative
    def test_Sphere_operating_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.operating_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'operating_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                
                      
    @pytest.mark.negative
    def test_Sphere_heayd_type_incorrect_value(self):
        with pytest.raises(Exception) as exp:
            Vertical_vessel = Sphere(
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type="flatop")
        self.assertIn("Incorrect value \'flatop\' provided to \'head_type\'. Should be among \'[\'hemispherical\', \'elliptical\', \'torispherical\', \'flat\']\'.\\n            ",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = Sphere()
            m4.head_type = "flatop"
        self.assertIn("Incorrect value \'flatop\' provided to \'head_type\'. Should be among \'[\'hemispherical\', \'elliptical\', \'torispherical\', \'flat\']\'.\\n            ",
                      str(exp))                       