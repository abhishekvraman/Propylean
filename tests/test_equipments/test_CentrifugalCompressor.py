import pytest
import unittest
from propylean.equipments.rotary import CentrifugalCompressor
from propylean.streams import MaterialStream, EnergyStream
import propylean.properties as prop
import pandas as pd
from propylean.settings import Settings
from propylean import MaterialStream, EnergyStream

class test_CentrifugalCompressor(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_CentrifugalCompressor_instantiation_only_tag(self):
        compressor = CentrifugalCompressor(tag="compressor_1")
        self.assertEqual(compressor.tag, "compressor_1")
        self.assertEqual(compressor.pressure_drop, prop.Pressure(0))
        self.assertEqual(compressor.differential_pressure, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_CentrifugalCompressor_instantiation_tag_and_differential_pressure(self):
        compressor = CentrifugalCompressor(tag="compressor_2",
                                            differential_pressure=prop.Pressure(100, 'bar'))
        self.assertEqual(compressor.tag, "compressor_2")
        self.assertEqual(compressor.differential_pressure, prop.Pressure(100, 'bar'))
        self.assertEqual(compressor.pressure_drop, prop.Pressure(-100, 'bar'))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_CentrifugalCompressor_instantiation_no_arguments(self):
        compressor = CentrifugalCompressor()
        self.assertIsNotNone(compressor.tag)
        self.assertEqual(compressor.pressure_drop, prop.Pressure(0))
        self.assertEqual(compressor.differential_pressure, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_CentrifugalCompressor_instantiation_efficiency_adiabatic_setting(self):
        compressor = CentrifugalCompressor(tag="compressor_3",
                                            differential_pressure=(10, 'bar'),
                                            efficiency=0.6)
        self.assertEqual(compressor.tag, "compressor_3")
        self.assertEqual(compressor.differential_pressure, prop.Pressure(10, 'bar'))
        # By defaul setting is adiabatic/isentropic
        Settings.compressor_process = "isenTROpiC"
        self.assertEqual(compressor.efficiency, 0.6)
        self.assertEqual(compressor.adiabatic_efficiency, 0.6)
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_CentrifugalCompressor_instantiation_efficiency_polytropic_setting(self):
        compressor = CentrifugalCompressor(differential_pressure=(10, 'bar'),
                                           efficiency=0.6)
        self.assertEqual(compressor.differential_pressure, prop.Pressure(10, 'bar'))
        Settings.compressor_process = "polYtROpic"
        self.assertEqual(compressor.efficiency, 0.6)
        self.assertEqual(compressor.polytropic_efficiency, 0.6)
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_CentrifugalCompressor_instantiation_compressor_curves(self):
        performance_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2]}])
        compressor = CentrifugalCompressor(tag="compressor_4",
                                            performance_curve=performance_curve)
        self.assertEqual(compressor.performace_curve.shape, performance_curve.shape)
    
    @pytest.mark.positive
    def test_CentrifugalCompressor_representation(self):
        compressor = CentrifugalCompressor(tag="compressor_5")
        self.assertIn("Centrifugal Compressor with tag: compressor_5", str(compressor))
    
    @pytest.mark.positive
    def test_CentrifugalCompressor_setting_inlet_pressure(self):
        compressor = CentrifugalCompressor(tag="compressor_6",
                                            differential_pressure=(10, 'bar'))
        compressor.inlet_pressure = (30, 'bar')
        self.assertEqual(compressor.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(compressor.outlet_pressure, prop.Pressure(40, 'bar'))
    
    @pytest.mark.positive
    def test_CentrifugalCompressor_setting_outlet_pressure(self):
        compressor = CentrifugalCompressor(tag="compressor_7",
                               differential_pressure=(10, 'bar'))
        compressor.outlet_pressure = (40, 'bar')
        self.assertEqual(compressor.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(compressor.outlet_pressure, prop.Pressure(40, 'bar'))
    
    @pytest.mark.positive
    def test_CentrifugalCompressor_setting_inlet_temperature(self):
        compressor = CentrifugalCompressor(tag="compressor_8",
                               differential_pressure=(10, 'bar'))
        compressor.inlet_temperature = (50, 'C')
        self.assertEqual(compressor.inlet_temperature, prop.Temperature(50, 'C'))
    
    @pytest.mark.positive
    def test_CentrifugalCompressor_setting_outlet_temperature(self):
        compressor = CentrifugalCompressor(tag="compressor_9",
                               differential_pressure=(10, 'bar'))
        compressor.outlet_temperature = (130, 'F')
        self.assertEqual(compressor.outlet_temperature, prop.Temperature(129.99999, 'F'))
    
    @pytest.mark.positive
    def test_CentrifugalCompressor_setting_inlet_mass_flowrate(self):
        compressor = CentrifugalCompressor(tag="compressor_10",
                               differential_pressure=(10, 'bar'))
        compressor.inlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(compressor.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(compressor.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_CentrifugalCompressor_setting_outlet_mass_flowrate(self):
        compressor = CentrifugalCompressor(tag="compressor_11",
                               differential_pressure=(10, 'bar'))
        compressor.outlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(compressor.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(compressor.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_CentrifugalCompressor_connection_with_material_stream_inlet_stream_governed(self):
        compressor = CentrifugalCompressor(tag="compressor_12",
                               differential_pressure=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_compressor_12",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(compressor.connect_stream(inlet_stream, 'in', stream_governed=True))
        # Test inlet properties of compressor are equal to inlet stream's.
        self.assertEqual(compressor.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(compressor.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(compressor.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(compressor.outlet_pressure, compressor.inlet_pressure+compressor.differential_pressure)
        self.assertLess(compressor.inlet_temperature.value, compressor.outlet_temperature.value)
        self.assertEqual(compressor.inlet_temperature.unit, compressor.outlet_temperature.unit)
        self.assertEqual(compressor.inlet_mass_flowrate, compressor.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_CentrifugalCompressor_connection_with_material_stream_outlet_stream_governed(self):
        compressor = CentrifugalCompressor(tag="compressor_13",
                               differential_pressure=(10, 'bar'))
        outlet_stream = MaterialStream(tag="Outlet_compressor_13",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(compressor.connect_stream(outlet_stream, 'out', stream_governed=True))
        # Test outlet properties of compressor are equal to outlet stream's.
        self.assertEqual(compressor.outlet_pressure, outlet_stream.pressure)
        self.assertAlmostEqual(compressor.outlet_temperature.value, outlet_stream.temperature.value, 3)
        self.assertEqual(compressor.outlet_temperature.unit, outlet_stream.temperature.unit)
        self.assertEqual(compressor.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertAlmostEqual(compressor.inlet_pressure.value, (compressor.outlet_pressure-compressor.differential_pressure).value, 5)
        self.assertEqual(compressor.inlet_pressure.unit, compressor.outlet_pressure.unit, compressor.differential_pressure.unit)
        self.assertLess(compressor.inlet_temperature.value, compressor.outlet_temperature.value)
        self.assertEqual(compressor.inlet_mass_flowrate, compressor.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_CentrifugalCompressor_connection_with_material_stream_inlet_equipment_governed(self):
        compressor = CentrifugalCompressor(tag="compressor_14",
                               differential_pressure=(10, 'bar'))

        compressor.inlet_pressure = (30, 'bar')
        compressor.inlet_mass_flowrate = (1000, 'kg/h')
        compressor.inlet_temperature = (320, 'K')
        inlet_stream = MaterialStream(tag="Inlet_compressor_14")
        # Test connection is made.
        self.assertTrue(compressor.connect_stream(inlet_stream, 'in', stream_governed=False))
        # Test inlet properties of compressor are equal to inlet stream's.
        self.assertEqual(compressor.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(compressor.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(compressor.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(compressor.outlet_pressure, compressor.inlet_pressure+compressor.differential_pressure)
        self.assertLess(compressor.inlet_temperature.value, compressor.outlet_temperature.value)
        self.assertEqual(compressor.inlet_mass_flowrate, compressor.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_CentrifugalCompressor_connection_with_material_stream_outlet_equipment_governed(self):
        compressor = CentrifugalCompressor(tag="compressor_15",
                               differential_pressure=(10, 'bar'))
        compressor.outlet_pressure = (130, 'bar')
        compressor.outlet_mass_flowrate = (1000, 'kg/h')
        compressor.outlet_temperature = (30, 'C')
        outlet_stream = MaterialStream(tag="Outlet_compressor_15")
        # Test connection is made.
        self.assertTrue(compressor.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test outlet properties of compressor are equal to outlet stream's.
        self.assertEqual(compressor.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(compressor.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(compressor.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(compressor.inlet_pressure, compressor.outlet_pressure-compressor.differential_pressure)
        self.assertLess(compressor.inlet_temperature.value, compressor.outlet_temperature.value)
        self.assertEqual(compressor.inlet_mass_flowrate, compressor.outlet_mass_flowrate)
    
    # TODO Uncomment below when power setting feature is provided.
    # @pytest.mark.positive
    # def test_CentrifugalCompressor_connection_with_energy_stream_inlet_stream_governed(self):
    #     compressor = CentrifugalCompressor(tag="compressor_16",
    #                            differential_pressure=(10, 'bar'))
    #     compressor_power = EnergyStream(tag="Power_compressor_16", amount=(10,"MW"))
    #     # Test connection is made.
    #     self.assertTrue(compressor.connect_stream(compressor_power, stream_governed=True))
    #     # Test inlet properties of compressor are equal to outlet stream's.
    #     self.assertEqual(compressor.energy_in, compressor_power.amount)
    #     self.assertEqual(compressor.power, compressor_power.unit)

    @pytest.mark.positive
    def test_CentrifugalCompressor_connection_with_energy_stream_inlet_equipment_governed(self):
        compressor = CentrifugalCompressor(tag="compressor_17",
                               differential_pressure=(10, 'bar'))
        compressor_power = EnergyStream(tag="Power_compressor_17", amount=(10, "MW"))
        compressor_inlet = MaterialStream(mass_flowrate=(1000, 'kg/h'),
                                          pressure=(30, 'bar'),
                                          temperature=(25, 'C'))
        compressor_inlet.isentropic_exponent = 1.36952
        compressor_inlet.Z_g = 0.94024
        compressor_inlet.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        # Test connection is made.
        self.assertTrue(compressor.connect_stream(compressor_inlet, "in", stream_governed=True))
        self.assertTrue(compressor.connect_stream(compressor_power, stream_governed=False))
        # Test inlet properties of compressor are equal to outlet stream's.
        self.assertGreater(compressor_power.amount.value, 0)
        self.assertGreater(compressor.power.value, 0)
        self.assertAlmostEqual(compressor.power.value, compressor_power.amount.value)
        self.assertEqual(compressor.power.unit, compressor_power.amount.unit)
    
    @pytest.mark.positive
    def test_CentrifugalCompressor_stream_disconnection_by_stream_object(self):
        compressor = CentrifugalCompressor(tag="compressor_18",
                               differential_pressure=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_compressor_18")
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        outlet_stream = MaterialStream(tag="Outlet_compressor_18")
        compressor_power = EnergyStream(tag="Power_compressor_18")
        # Test connection is made.
        self.assertTrue(compressor.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(compressor.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(compressor.connect_stream(compressor_power))
        # Test disconnection
        self.assertTrue(compressor.disconnect_stream(inlet_stream))
        self.assertTrue(compressor.disconnect_stream(outlet_stream))
        self.assertTrue(compressor.disconnect_stream(compressor_power))
        self.assertIsNone(compressor._inlet_material_stream_tag)
        self.assertIsNone(compressor._outlet_material_stream_tag)
        self.assertIsNone(compressor._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_CentrifugalCompressor_stream_disconnection_by_stream_tag(self):
        compressor = CentrifugalCompressor(tag="compressor_19",
                               differential_pressure=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_compressor_19")
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        outlet_stream = MaterialStream(tag="Outlet_compressor_19")
        compressor_power = EnergyStream(tag="Power_compressor_19")
        # Test connection is made.
        self.assertTrue(compressor.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(compressor.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertEqual(inlet_stream.components, outlet_stream.components)
        self.assertTrue(compressor.connect_stream(compressor_power))
        # Test disconnection
        self.assertTrue(compressor.disconnect_stream(stream_tag="Inlet_compressor_19"))
        self.assertTrue(compressor.disconnect_stream(stream_tag="Outlet_compressor_19"))
        self.assertTrue(compressor.disconnect_stream(stream_tag="Power_compressor_19"))
        self.assertIsNone(compressor._inlet_material_stream_tag)
        self.assertIsNone(compressor._outlet_material_stream_tag)
        self.assertIsNone(compressor._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_CentrifugalCompressor_stream_disconnection_by_direction_stream_type(self):
        compressor = CentrifugalCompressor(tag="compressor_20",
                               differential_pressure=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_compressor_20")
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        outlet_stream = MaterialStream(tag="Outlet_compressor_20")
        compressor_power = EnergyStream(tag="Power_compressor_20")
        # Test connection is made.
        self.assertTrue(compressor.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(compressor.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(compressor.connect_stream(compressor_power))
        # Test disconnection
        self.assertTrue(compressor.disconnect_stream(direction="in", stream_type="Material"))
        self.assertTrue(compressor.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        self.assertTrue(compressor.disconnect_stream(stream_type="energy"))
        self.assertIsNone(compressor._inlet_material_stream_tag)
        self.assertIsNone(compressor._outlet_material_stream_tag)
        self.assertIsNone(compressor._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)

    @pytest.mark.positive
    def test_CentrifugalCompressor_adiabatic_head_calulcation(self):
        compressor = CentrifugalCompressor(differential_pressure=(10, 'bar'),
                                           efficiency=75)
        inlet_stream = MaterialStream(mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(25, 'C'))
        outlet_stream = MaterialStream()
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        Settings.compressor_process="ADIABATIC"
        compressor.connect_stream(inlet_stream, 'in', stream_governed=True)
        compressor.connect_stream(outlet_stream, 'out', stream_governed=False)
        compressor_head = compressor.head
        compressor_head.unit = "m"
        self.assertGreater(compressor_head.value, 0)
    
    @pytest.mark.positive
    def test_CentrifugalCompressor_polytropic_head_calulcation(self):
        compressor = CentrifugalCompressor(tag="compressor_21",
                               differential_pressure=(10, 'bar'),
                               efficiency=75)
        inlet_stream = MaterialStream(tag="Inlet_compressor_21",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(25, 'C'))
        outlet_stream = MaterialStream()
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        Settings.compressor_process="POLYTROPIC"
        compressor.connect_stream(inlet_stream, 'in', stream_governed=True)
        compressor.connect_stream(outlet_stream, 'out', stream_governed=False)
        compressor_head = compressor.head
        compressor_head.unit = "m"
        self.assertGreater(compressor_head.value, 0)
    
    @pytest.mark.positive
    def test_CentrifugalCompressor_power_calculations(self):
        compressor = CentrifugalCompressor(tag="compressor_22",
                               differential_pressure=(10, 'bar'),
                               efficiency=40)
        inlet_stream = MaterialStream(tag="Inlet_compressor_22",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(25, 'C'))
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        compressor.connect_stream(inlet_stream, 'in', stream_governed=True)
        self.assertGreater(compressor.power.value, 0)

    @pytest.mark.negative
    def test_CentrifugalCompressor_inlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalCompressor()
            m4.inlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_CentrifugalCompressor_outlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalCompressor()
            m4.outlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_CentrifugalCompressor_pressure_drop_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalCompressor()
            m4.pressure_drop = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'pressure_drop'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                    

    @pytest.mark.negative
    def test_CentrifugalCompressor_design_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalCompressor()
            m4.design_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_CentrifugalCompressor_inlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalCompressor()
            m4.inlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_CentrifugalCompressor_outlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalCompressor()
            m4.outlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

                                                     
    @pytest.mark.negative
    def test_CentrifugalCompressor_design_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalCompressor()
            m4.design_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_CentrifugalCompressor_inlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalCompressor()
            m4.inlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_CentrifugalCompressor_outlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalCompressor()
            m4.outlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_CentrifugalCompressor_energy_in_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalCompressor()
            m4.energy_in = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_in'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))      

    @pytest.mark.negative
    def test_CentrifugalCompressor_energy_out_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalCompressor()
            m4.energy_out = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_out'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_CentrifugalCompressor_stream_connecion_disconnection_incorrect_type(self):
        cv = CentrifugalCompressor(tag="compressor_2232",
                               differential_pressure=(10, 'bar'),
                               efficiency=40)
        inlet_stream = MaterialStream(tag="Inlet_compressor_2232",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(25, 'C'))
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
                    
        with pytest.raises(Exception) as exp:
            cv.connect_stream([inlet_stream], 'in', stream_governed=True)
        self.assertIn("Incorrect type \'<class \'list\'>\' provided to \'stream_object\'. Should be \'(<class \'propylean.streams.MaterialStream\'>, <class \'propylean.streams.EnergyStream\'>)\'.\\n            ",
                      str(exp)) 
        
        with pytest.raises(Exception) as exp:
            cv.connect_stream(inlet_stream, ['in'], stream_governed=True)
        self.assertIn("Incorrect type \'<class \'list\'>\' provided to \'direction\'. Should be \'<class \'str\'>\'.\\n            ",
                      str(exp)) 
        with pytest.raises(Exception) as exp:
            cv.connect_stream(inlet_stream, 'in', stream_governed=[True])
        self.assertIn("Incorrect type \'<class \'list\'>\' provided to \'stream_governed\'. Should be \'<class \'bool\'>\'.\\n            ",
                      str(exp)) 

        cv.connect_stream(inlet_stream, 'in', stream_governed=True)
        with pytest.raises(Exception) as exp:
            cv.disconnect_stream(stream_tag=["Inlet_cv_19"])
        self.assertIn("Incorrect type \'<class \'list\'>\' provided to \'stream_tag\'. Should be \'<class \'str\'>\'.\\n            ",
                      str(exp))    

    @pytest.mark.negative
    def test_CentrifugalCompressor_stream_disconnection_before_connecion(self):  
        cv = CentrifugalCompressor(tag="compressor_223332",
                               differential_pressure=(10, 'bar'),
                               efficiency=40)
        inlet_stream = MaterialStream(tag="Inlet_compress2232",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(25, 'C'))
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        import warnings
        with warnings.catch_warnings(record=True) as exp:
            cv.disconnect_stream(inlet_stream)
         
        self.assertIn("Already there is no connection.",
                      str(exp[-1].message))                  

    @pytest.mark.mapping
    def test_CentrifugalCompressor_stream_equipment_mapping(self):
        from propylean.equipments.abstract_equipment_classes import _material_stream_equipment_map as mse_map
        from propylean.equipments.abstract_equipment_classes import _energy_stream_equipment_map as ese_map
        comp = CentrifugalCompressor(
                               differential_pressure=(10, 'bar'))
        inlet_stream = MaterialStream()
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        outlet_stream = MaterialStream()
        energy_in = EnergyStream()
        energy_out = EnergyStream()

        comp.connect_stream(inlet_stream, direction="in", stream_governed=True)
        comp.connect_stream(outlet_stream, direction="out", stream_governed=False)
        comp.connect_stream(energy_in, direction="in")
        with pytest.raises(Exception) as exp:
            comp.connect_stream(energy_out, direction="out")
        self.assertIn("CentrifugalCompressor only supports energy inlet.",
                      str(exp))

        self.assertEqual(mse_map[inlet_stream.index][2], comp.index)
        self.assertEqual(mse_map[inlet_stream.index][3], comp.__class__)
        self.assertEqual(mse_map[outlet_stream.index][0], comp.index)
        self.assertEqual(mse_map[outlet_stream.index][1], comp.__class__) 

        self.assertEqual(ese_map[energy_in.index][2], comp.index)
        self.assertEqual(ese_map[energy_in.index][3], comp.__class__)
        self.assertIsNone(ese_map[energy_in.index][0])
        self.assertIsNone(ese_map[energy_in.index][1])   

        comp.disconnect_stream(inlet_stream)
        comp.disconnect_stream(outlet_stream)
        comp.disconnect_stream(energy_in, direction="in")
        with pytest.raises(Exception) as exp:
            comp.disconnect_stream(energy_out, direction="out")  
        self.assertIn("CentrifugalCompressor only supports energy inlet.",
                      str(exp))

        self.assertIsNone(mse_map[inlet_stream.index][2])
        self.assertIsNone(mse_map[inlet_stream.index][3])
        self.assertIsNone(mse_map[outlet_stream.index][0])
        self.assertIsNone(mse_map[outlet_stream.index][1]) 

        self.assertIsNone(ese_map[energy_in.index][2])
        self.assertIsNone(ese_map[energy_in.index][3]) 
        self.assertIsNone(ese_map[energy_in.index][1])
        self.assertIsNone(ese_map[energy_in.index][0])  

    @pytest.mark.delete 
    def test_comp_stream_equipment_delete_without_connection(self):
        comp = CentrifugalCompressor()   
        repr(comp)
        comp.delete()
        with pytest.raises(Exception) as exp:
            repr(comp)
        self.assertIn("Equipment does not exist!",
                      str(exp))
    
    @pytest.mark.delete 
    def test_comp_stream_equipment_delete_with_connection(self):
        from propylean.equipments.abstract_equipment_classes import _material_stream_equipment_map as mse_map
        from propylean.equipments.abstract_equipment_classes import _energy_stream_equipment_map as ese_map
        comp = CentrifugalCompressor(
                               differential_pressure=(10, 'bar'))
        inlet_stream = MaterialStream()
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        outlet_stream = MaterialStream()
        energy_in = EnergyStream()
        energy_out = EnergyStream()

        comp.connect_stream(inlet_stream, direction="in", stream_governed=True)
        comp.connect_stream(outlet_stream, direction="out", stream_governed=False)
        comp.connect_stream(energy_in, direction="in")

        repr(comp)
        comp.delete()
        with pytest.raises(Exception) as exp:
            repr(comp)
        self.assertIn("Equipment does not exist!",
                      str(exp))

        self.assertIsNone(mse_map[inlet_stream.index][2])
        self.assertIsNone(mse_map[inlet_stream.index][3])
        self.assertIsNone(mse_map[outlet_stream.index][0])
        self.assertIsNone(mse_map[outlet_stream.index][1]) 

        self.assertIsNone(ese_map[energy_in.index][2])
        self.assertIsNone(ese_map[energy_in.index][3])