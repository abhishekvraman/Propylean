import pytest
import unittest
from propylean.instruments.control import ControlValve
from propylean.streams import MaterialStream
import propylean.properties as prop

class test_ControlValve(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_ControlValve_instantiation_only_tag(self):
        cv = ControlValve(tag="cv_1")
        self.assertEqual(cv.tag, "cv_1")
        self.assertEqual(cv.pressure_drop, prop.Pressure(0))
        self.assertEqual(cv.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_ControlValve_instantiation_tag_and_pressure_drop(self):
        cv = ControlValve(tag="cv_2",
                          pressure_drop=prop.Pressure(100, 'bar'))
        self.assertEqual(cv.tag, "cv_2")
        self.assertEqual(cv.pressure_drop, prop.Pressure(100, 'bar'))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_ControlValve_instantiation_no_arguments(self):
        cv = ControlValve()
        self.assertIsNotNone(cv.tag)
        self.assertEqual(cv.pressure_drop, prop.Pressure(0))
        self.assertEqual(cv.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    def test_ControlValve_representation(self):
        cv = ControlValve(tag="cv_5")
        self.assertIn("Control Valve with tag: cv_5", str(cv))
    
    @pytest.mark.positive
    def test_ControlValve_setting_inlet_pressure(self):
        cv = ControlValve(tag="cv_6",
                          pressure_drop=(10, 'bar'))
        cv.inlet_pressure = (30, 'bar')
        self.assertEqual(cv.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(cv.outlet_pressure, prop.Pressure(20, 'bar'))
    
    @pytest.mark.positive
    def test_ControlValve_setting_outlet_pressure(self):
        cv = ControlValve(tag="cv_7",
                          pressure_drop=(10, 'bar'))
        cv.outlet_pressure = (20, 'bar')
        self.assertEqual(cv.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(cv.outlet_pressure, prop.Pressure(20, 'bar'))
    
    @pytest.mark.positive
    def test_ControlValve_setting_inlet_temperature(self):
        cv = ControlValve(tag="cv_8",
                          pressure_drop=(10, 'bar'))
        cv.inlet_temperature = (50, 'C')
        self.assertEqual(cv.inlet_temperature, prop.Temperature(50, 'C'))
        self.assertEqual(cv.outlet_temperature, prop.Temperature(50, 'C'))
    
    @pytest.mark.positive
    def test_ControlValve_setting_outlet_temperature(self):
        cv = ControlValve(tag="cv_9",
                          pressure_drop=(10, 'bar'))
        cv.outlet_temperature = (130, 'F')
        self.assertLess(abs(cv.inlet_temperature.value-130), 0.0001)
        self.assertEqual(cv.inlet_temperature.unit, 'F')
        self.assertLess(abs(cv.outlet_temperature.value-130), 0.0001)
        self.assertEqual(cv.outlet_temperature.unit, 'F')
    
    @pytest.mark.positive
    def test_ControlValve_setting_inlet_mass_flowrate(self):
        cv = ControlValve(tag="cv_10",
                          pressure_drop=(10, 'bar'))
        cv.inlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(cv.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(cv.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_ControlValve_setting_outlet_mass_flowrate(self):
        cv = ControlValve(tag="cv_11",
                          pressure_drop=(100, 'bar'))
        cv.outlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(cv.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(cv.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_ControlValve_connection_with_material_stream_inlet_stream_governed(self):
        cv = ControlValve(tag="cv_12",
                          pressure_drop=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_cv_12",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(cv.connect_stream(inlet_stream, 'in', stream_governed=True))
        # Test inlet properties of cv are equal to inlet stream's.
        self.assertEqual(cv.inlet_pressure, inlet_stream.pressure)
        self.assertAlmostEqual(cv.inlet_temperature.value, inlet_stream.temperature.value, 3)
        self.assertEqual(cv.inlet_temperature.unit, inlet_stream.temperature.unit)
        self.assertEqual(cv.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(cv.outlet_pressure, cv.inlet_pressure - cv.pressure_drop)
        self.assertLess(abs(cv.inlet_temperature.value - cv.outlet_temperature.value), 0.001)
        self.assertEqual(cv.inlet_temperature.unit, cv.outlet_temperature.unit)
        self.assertEqual(cv.inlet_mass_flowrate, cv.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_ControlValve_connection_with_material_stream_outlet_stream_governed(self):
        cv = ControlValve(tag="cv_13",
                          pressure_drop=(10, 'bar'))
        outlet_stream = MaterialStream(tag="Outlet_cv_13",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(cv.connect_stream(outlet_stream, 'out', stream_governed=True))
        # Test outlet properties of cv are equal to outlet stream's.
        self.assertEqual(cv.outlet_pressure, outlet_stream.pressure)
        self.assertAlmostEqual(cv.outlet_temperature.value, outlet_stream.temperature.value, 3)
        self.assertEqual(cv.outlet_temperature.unit, outlet_stream.temperature.unit)
        self.assertEqual(cv.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(cv.inlet_pressure, cv.outlet_pressure + cv.pressure_drop)
        self.assertLess(abs(cv.inlet_temperature.value-cv.outlet_temperature.value),0.0001)
        self.assertEqual(cv.inlet_mass_flowrate, cv.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_ControlValve_connection_with_material_stream_inlet_equipment_governed(self):
        cv = ControlValve(tag="cv_14",
                          pressure_drop=(10, 'bar'))

        cv.inlet_pressure = (30, 'bar')
        cv.inlet_mass_flowrate = (1000, 'kg/h')
        cv.inlet_temperature = (320, 'K')
        inlet_stream = MaterialStream(tag="Inlet_cv_14", pressure=(20, 'bar'))
        # Test connection is made.
        self.assertTrue(cv.connect_stream(inlet_stream, 'in', stream_governed=False))
        # Test inlet properties of cv are equal to inlet stream's.
        self.assertEqual(cv.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(cv.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(cv.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(cv.outlet_pressure, cv.inlet_pressure - cv.pressure_drop)
        self.assertEqual(cv.inlet_temperature, cv.outlet_temperature)
        self.assertEqual(cv.inlet_mass_flowrate, cv.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_ControlValve_connection_with_material_stream_outlet_equipment_governed(self):
        cv = ControlValve(tag="cv_15",
                          pressure_drop=(10, 'bar'))
        cv.outlet_pressure = (130, 'bar')
        cv.outlet_mass_flowrate = (1000, 'kg/h')
        cv.outlet_temperature = (30, 'C')
        outlet_stream = MaterialStream(tag="Outlet_cv_15", pressure=(20, 'bar'))
        # Test connection is made.
        self.assertTrue(cv.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test outlet properties of cv are equal to outlet stream's.
        self.assertEqual(cv.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(cv.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(cv.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(cv.inlet_pressure, cv.outlet_pressure + cv.pressure_drop)
        self.assertEqual(cv.inlet_temperature, cv.outlet_temperature)
        self.assertEqual(cv.inlet_mass_flowrate, cv.outlet_mass_flowrate)
    
    @pytest.mark.positive
    def test_ControlValve_stream_disconnection_by_stream_object(self):
        cv = ControlValve(tag="cv_18",
                          pressure_drop=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_cv_18", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_cv_18")
    
        # Test connection is made.
        self.assertTrue(cv.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(cv.connect_stream(outlet_stream, 'out', stream_governed=False))
        
        # Test disconnection
        self.assertTrue(cv.disconnect_stream(inlet_stream))
        self.assertTrue(cv.disconnect_stream(outlet_stream))
        
        self.assertIsNone(cv._inlet_material_stream_tag)
        self.assertIsNone(cv._outlet_material_stream_tag)
        self.assertIsNone(cv._outlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    @pytest.mark.temp
    def test_ControlValve_stream_disconnection_by_stream_tag(self):
        cv = ControlValve(tag="cv_19",
                          pressure_drop=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_cv_19", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_cv_19")
    
        # Test connection is made.
        self.assertTrue(cv.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(cv.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertEqual(inlet_stream.components, outlet_stream.components)
        
        # Test disconnection
        self.assertTrue(cv.disconnect_stream(stream_tag="Inlet_cv_19"))
        self.assertTrue(cv.disconnect_stream(stream_tag="Outlet_cv_19"))
        
        self.assertIsNone(cv._inlet_material_stream_tag)
        self.assertIsNone(cv._outlet_material_stream_tag)
        self.assertIsNone(cv._outlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_ControlValve_stream_disconnection_by_direction_stream_type(self):
        cv = ControlValve(tag="cv_20",
                          pressure_drop=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_cv_20", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_cv_20")
   
        # Test connection is made.
        self.assertTrue(cv.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(cv.connect_stream(outlet_stream, 'out', stream_governed=False))
     
        # Test disconnection
        self.assertTrue(cv.disconnect_stream(direction="in", stream_type="Material"))
        self.assertTrue(cv.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        
        self.assertIsNone(cv._inlet_material_stream_tag)
        self.assertIsNone(cv._outlet_material_stream_tag)
        self.assertIsNone(cv._outlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_ControlValve_Cv_calulcations_gas(self):
        cv = ControlValve(tag="cv_23",
                          pressure_drop=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_cv_23",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(1E6, 'Pa'),
                                      temperature=(350, 'K'))
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.phase = "g"
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        inlet_stream.d_viscosity = prop.DViscosity(0.01162, 'cP')
        inlet_stream.density = prop.Density(21.34756)
        cv.connect_stream(inlet_stream, 'in', stream_governed=True)
        # TODO: Improve calulation accuracy
        self.assertGreater(cv.Cv, 0)

    @pytest.mark.positive
    def test_ControlValve_Cv_calulcations_liquid(self):
        cv = ControlValve(tag="cv_24",
                          pressure_drop=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_cv_24",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(25, 'C'))
        inlet_stream.components = prop.Components({"water": 1})
        cv.connect_stream(inlet_stream, 'in', stream_governed=True)
        # TODO: Improve calulation accuracy
        self.assertGreater(cv.Cv, 0)

    @pytest.mark.negative
    def test_ControlValve_inlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = ControlValve()
            m4.inlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_ControlValve_outlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = ControlValve()
            m4.outlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_ControlValve_pressure_drop_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = ControlValve()
            m4.pressure_drop = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'pressure_drop'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                    

    @pytest.mark.negative
    def test_ControlValve_design_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = ControlValve()
            m4.design_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_ControlValve_inlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = ControlValve()
            m4.inlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_ControlValve_outlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = ControlValve()
            m4.outlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_ControlValve_temperature_decrease_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = ControlValve()
            m4.temperature_decrease = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'temperature_decrease'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_ControlValve_temperature_increase_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = ControlValve()
            m4.temperature_increase = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'temperature_increase'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                                      

    @pytest.mark.negative
    def test_ControlValve_design_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = ControlValve()
            m4.design_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_ControlValve_inlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = ControlValve()
            m4.inlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_ControlValve_outlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = ControlValve()
            m4.outlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_ControlValve_energy_in_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = ControlValve()
            m4.energy_in = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_in'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))      

    @pytest.mark.negative
    def test_ControlValve_energy_out_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = ControlValve()
            m4.energy_out = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_out'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))        