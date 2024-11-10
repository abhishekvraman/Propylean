import pytest
import unittest
from propylean.equipments.rotary import TurboExpander
from propylean.streams import MaterialStream, EnergyStream
import propylean.properties as prop
import pandas as pd
from propylean.settings import Settings
from propylean import MaterialStream, EnergyStream

class test_TurboExpander(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_TurboExpander_instantiation_only_tag(self):
        expander = TurboExpander(tag="expander_1")
        self.assertEqual(expander.tag, "expander_1")
        self.assertEqual(expander.pressure_drop, prop.Pressure(0))
        self.assertEqual(expander.differential_pressure, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_TurboExpander_instantiation_tag_and_differential_pressure(self):
        expander = TurboExpander(tag="expander_2",
                                            differential_pressure=prop.Pressure(100, 'bar'))
        self.assertEqual(expander.tag, "expander_2")
        self.assertEqual(expander.differential_pressure, prop.Pressure(100, 'bar'))
        self.assertEqual(expander.pressure_drop, prop.Pressure(-100, 'bar'))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_TurboExpander_instantiation_no_arguments(self):
        expander = TurboExpander()
        self.assertIsNotNone(expander.tag)
        self.assertEqual(expander.pressure_drop, prop.Pressure(0))
        self.assertEqual(expander.differential_pressure, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_TurboExpander_instantiation_efficiency_adiabatic_setting(self):
        expander = TurboExpander(tag="expander_3",
                                            differential_pressure=(10, 'bar'),
                                            efficiency=0.6)
        self.assertEqual(expander.tag, "expander_3")
        self.assertEqual(expander.differential_pressure, prop.Pressure(10, 'bar'))
        # By defaul setting is adiabatic/isentropic
        Settings.expander_process = "isenTROpiC"
        eff = prop.Efficiency(0.6)
        self.assertEqual(expander.efficiency, eff)
        self.assertEqual(expander.adiabatic_efficiency, eff)
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_TurboExpander_instantiation_efficiency_polytropic_setting(self):
        expander = TurboExpander(differential_pressure=(10, 'bar'),
                                           efficiency=0.6)
        self.assertEqual(expander.differential_pressure, prop.Pressure(10, 'bar'))
        Settings.expander_process = "polYtROpic"
        eff = prop.Efficiency(0.6)
        self.assertEqual(expander.efficiency, eff)
        self.assertEqual(expander.polytropic_efficiency, eff)
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_TurboExpander_instantiation_expander_curves(self):
        performance_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2]}])
        expander = TurboExpander(tag="expander_4",
                                            performance_curve=performance_curve)
        self.assertEqual(expander.performace_curve.shape, performance_curve.shape)
    
    @pytest.mark.positive
    def test_TurboExpander_representation(self):
        expander = TurboExpander(tag="expander_5")
        self.assertIn("TurboExpander with tag: expander_5", str(expander))
    
    @pytest.mark.positive
    def test_TurboExpander_setting_inlet_pressure(self):
        expander = TurboExpander(tag="expander_6",
                                            differential_pressure=(10, 'bar'))
        expander.inlet_pressure = (30, 'bar')
        self.assertEqual(expander.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(expander.outlet_pressure, prop.Pressure(40, 'bar'))
    
    @pytest.mark.positive
    def test_TurboExpander_setting_outlet_pressure(self):
        expander = TurboExpander(tag="expander_7",
                               differential_pressure=(10, 'bar'))
        expander.outlet_pressure = (40, 'bar')
        self.assertEqual(expander.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(expander.outlet_pressure, prop.Pressure(40, 'bar'))
    
    @pytest.mark.positive
    def test_TurboExpander_setting_inlet_temperature(self):
        expander = TurboExpander(tag="expander_8",
                               differential_pressure=(10, 'bar'))
        expander.inlet_temperature = (50, 'C')
        self.assertEqual(expander.inlet_temperature, prop.Temperature(50, 'C'))
        
    
    @pytest.mark.positive
    def test_TurboExpander_setting_outlet_temperature(self):
        expander = TurboExpander(tag="expander_9",
                               differential_pressure=(100, 'bar'))
        expander.outlet_temperature = (129.99999, 'F')
        self.assertEqual(expander.outlet_temperature, prop.Temperature(129.99999, 'F'))
    
    @pytest.mark.positive
    def test_TurboExpander_setting_inlet_mass_flowrate(self):
        expander = TurboExpander(tag="expander_10",
                               differential_pressure=(10, 'bar'))
        expander.inlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(expander.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(expander.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_TurboExpander_setting_outlet_mass_flowrate(self):
        expander = TurboExpander(tag="expander_11",
                               differential_pressure=(10, 'bar'))
        expander.outlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(expander.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(expander.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_TurboExpander_connection_with_material_stream_inlet_stream_governed(self):
        expander = TurboExpander(tag="expander_12",
                               differential_pressure=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_expander_12",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(expander.connect_stream(inlet_stream, 'in', stream_governed=True))
        # Test inlet properties of expander are equal to inlet stream's.
        self.assertEqual(expander.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(expander.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(expander.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(expander.outlet_pressure, expander.inlet_pressure+expander.differential_pressure)
        self.assertGreater(expander.inlet_temperature.value, expander.outlet_temperature.value)
        self.assertEqual(expander.inlet_temperature.unit, expander.outlet_temperature.unit)
        self.assertEqual(expander.inlet_mass_flowrate, expander.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_TurboExpander_connection_with_material_stream_outlet_stream_governed(self):
        expander = TurboExpander(tag="expander_13",
                               differential_pressure=(10, 'bar'))
        outlet_stream = MaterialStream(tag="Outlet_expander_13",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(expander.connect_stream(outlet_stream, 'out', stream_governed=True))
        # Test outlet properties of expander are equal to outlet stream's.
        self.assertEqual(expander.outlet_pressure, outlet_stream.pressure)
        self.assertAlmostEqual(expander.outlet_temperature.value, outlet_stream.temperature.value, 3)
        self.assertEqual(expander.outlet_temperature.unit, outlet_stream.temperature.unit)
        self.assertEqual(expander.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertAlmostEqual(expander.inlet_pressure.value, (expander.outlet_pressure-expander.differential_pressure).value, 5)
        self.assertEqual(expander.inlet_pressure.unit, expander.outlet_pressure.unit, expander.differential_pressure.unit)
        self.assertGreater(expander.inlet_temperature.value, expander.outlet_temperature.value)
        self.assertEqual(expander.inlet_mass_flowrate, expander.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_TurboExpander_connection_with_material_stream_inlet_equipment_governed(self):
        expander = TurboExpander(tag="expander_14",
                               differential_pressure=(10, 'bar'))

        expander.inlet_pressure = (30, 'bar')
        expander.inlet_mass_flowrate = (1000, 'kg/h')
        expander.inlet_temperature = (320, 'K')
        inlet_stream = MaterialStream(tag="Inlet_expander_14")
        # Test connection is made.
        self.assertTrue(expander.connect_stream(inlet_stream, 'in', stream_governed=False))
        # Test inlet properties of expander are equal to inlet stream's.
        self.assertEqual(expander.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(expander.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(expander.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(expander.outlet_pressure, expander.inlet_pressure+expander.differential_pressure)
        self.assertGreater(expander.inlet_temperature.value, expander.outlet_temperature.value)
        self.assertEqual(expander.inlet_mass_flowrate, expander.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_TurboExpander_connection_with_material_stream_outlet_equipment_governed(self):
        expander = TurboExpander(tag="expander_15",
                               differential_pressure=(10, 'bar'))
        expander.outlet_pressure = (130, 'bar')
        expander.outlet_mass_flowrate = (1000, 'kg/h')
        expander.outlet_temperature = (30, 'C')
        outlet_stream = MaterialStream(tag="Outlet_expander_15")
        # Test connection is made.
        self.assertTrue(expander.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test outlet properties of expander are equal to outlet stream's.
        self.assertEqual(expander.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(expander.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(expander.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(expander.inlet_pressure, expander.outlet_pressure-expander.differential_pressure)
        self.assertGreater(expander.inlet_temperature.value, expander.outlet_temperature.value)
        self.assertEqual(expander.inlet_mass_flowrate, expander.outlet_mass_flowrate)
    
    # TODO Uncomment below when power setting feature is provided.
    # @pytest.mark.positive
    # def test_TurboExpander_connection_with_energy_stream_inlet_stream_governed(self):
    #     expander = TurboExpander(tag="expander_16",
    #                            differential_pressure=(10, 'bar'))
    #     expander_power = EnergyStream(tag="Power_expander_16", amount=(10,"MW"))
    #     # Test connection is made.
    #     self.assertTrue(expander.connect_stream(expander_power, stream_governed=True))
    #     # Test inlet properties of expander are equal to outlet stream's.
    #     self.assertEqual(expander.energy_out, expander_power.amount)
    #     self.assertEqual(expander.power, expander_power.unit)

    @pytest.mark.positive
    def test_TurboExpander_connection_with_energy_stream_inlet_equipment_governed(self):
        expander = TurboExpander(tag="expander_17",
                               differential_pressure=(10, 'bar'))
        expander_power = EnergyStream(tag="Power_expander_17", amount=(10, "MW"))
        expander_inlet = MaterialStream(mass_flowrate=(1000, 'kg/h'),
                                          pressure=(30, 'bar'),
                                          temperature=(25, 'C'))
        expander_inlet.isentropic_exponent = 1.36952
        expander_inlet.Z_g = 0.94024
        expander_inlet.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        # Test connection is made.
        self.assertTrue(expander.connect_stream(expander_inlet, "in", stream_governed=True))
        self.assertTrue(expander.connect_stream(expander_power, stream_governed=False))
        # Test inlet properties of expander are equal to outlet stream's.
        self.assertAlmostEqual(expander.power.value, expander_power.amount.value)
        self.assertEqual(expander.power.unit, expander_power.amount.unit)
    
    @pytest.mark.positive
    def test_TurboExpander_stream_disconnection_by_stream_object(self):
        expander = TurboExpander(tag="expander_18",
                               differential_pressure=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_expander_18")
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        outlet_stream = MaterialStream(tag="Outlet_expander_18")
        expander_power = EnergyStream(tag="Power_expander_18")
        # Test connection is made.
        self.assertTrue(expander.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(expander.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(expander.connect_stream(expander_power))
        # Test disconnection
        self.assertTrue(expander.disconnect_stream(inlet_stream))
        self.assertTrue(expander.disconnect_stream(outlet_stream))
        self.assertTrue(expander.disconnect_stream(expander_power))
        self.assertIsNone(expander._inlet_material_stream_tag)
        self.assertIsNone(expander._outlet_material_stream_tag)
        self.assertIsNone(expander._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_TurboExpander_stream_disconnection_by_stream_tag(self):
        expander = TurboExpander(tag="expander_19",
                               differential_pressure=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_expander_19")
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        outlet_stream = MaterialStream(tag="Outlet_expander_19")
        expander_power = EnergyStream(tag="Power_expander_19")
        # Test connection is made.
        self.assertTrue(expander.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(expander.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertEqual(inlet_stream.components, outlet_stream.components)
        self.assertTrue(expander.connect_stream(expander_power))
        # Test disconnection
        self.assertTrue(expander.disconnect_stream(stream_tag="Inlet_expander_19"))
        self.assertTrue(expander.disconnect_stream(stream_tag="Outlet_expander_19"))
        self.assertTrue(expander.disconnect_stream(stream_tag="Power_expander_19"))
        self.assertIsNone(expander._inlet_material_stream_tag)
        self.assertIsNone(expander._outlet_material_stream_tag)
        self.assertIsNone(expander._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_TurboExpander_stream_disconnection_by_direction_stream_type(self):
        expander = TurboExpander(tag="expander_20",
                               differential_pressure=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_expander_20")
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        outlet_stream = MaterialStream(tag="Outlet_expander_20")
        expander_power = EnergyStream(tag="Power_expander_20")
        # Test connection is made.
        self.assertTrue(expander.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(expander.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(expander.connect_stream(expander_power))
        # Test disconnection
        self.assertTrue(expander.disconnect_stream(direction="in", stream_type="Material"))
        self.assertTrue(expander.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        self.assertTrue(expander.disconnect_stream(stream_type="energy"))
        self.assertIsNone(expander._inlet_material_stream_tag)
        self.assertIsNone(expander._outlet_material_stream_tag)
        self.assertIsNone(expander._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)

    @pytest.mark.positive
    def test_TurboExpander_adiabatic_head_calulcation(self):
        expander = TurboExpander(differential_pressure=(10, 'bar'),
                                           efficiency=75)
        inlet_stream = MaterialStream(mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(25, 'C'))
        outlet_stream = MaterialStream()
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        Settings.expander_process="ADIABATIC"
        expander.connect_stream(inlet_stream, 'in', stream_governed=True)
        expander.connect_stream(outlet_stream, 'out', stream_governed=False)
        expander_head = expander.head
        expander_head.unit = "m"
        self.assertGreater(expander_head.value, 0)
    
    @pytest.mark.positive
    def test_TurboExpander_polytropic_head_calulcation(self):
        expander = TurboExpander(tag="expander_21",
                               differential_pressure=(10, 'bar'),
                               efficiency=75)
        inlet_stream = MaterialStream(tag="Inlet_expander_21",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(25, 'C'))
        outlet_stream = MaterialStream()
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        Settings.expander_process="POLYTROPIC"
        expander.connect_stream(inlet_stream, 'in', stream_governed=True)
        expander.connect_stream(outlet_stream, 'out', stream_governed=False)
        expander_head = expander.head
        expander_head.unit = "m"
        self.assertGreater(expander_head.value, 0)
    
    @pytest.mark.positive
    def test_TurboExpander_power_calculations(self):
        expander = TurboExpander(tag="expander_22",
                               differential_pressure=(10, 'bar'),
                               efficiency=40)
        inlet_stream = MaterialStream(tag="Inlet_expander_22",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(25, 'C'))
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        expander.connect_stream(inlet_stream, 'in', stream_governed=True)
        self.assertGreater(expander.power.value, 0)

    @pytest.mark.negative
    def test_TurboExpander_inlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TurboExpander()
            m4.inlet_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_pressure'. Can be any one from '('Pressure', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))

    @pytest.mark.negative
    def test_TurboExpander_outlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TurboExpander()
            m4.outlet_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_pressure'. Can be any one from '('Pressure', 'int', 'float', 'tuple', 'Series')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_TurboExpander_pressure_drop_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TurboExpander()
            m4.pressure_drop = []
        self.assertIn("Incorrect type 'list' provided to 'pressure_drop'. Can be any one from '('Pressure', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))                                    

    @pytest.mark.negative
    def test_TurboExpander_design_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TurboExpander()
            m4.design_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'design_pressure'. Can be any one from '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_TurboExpander_inlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TurboExpander()
            m4.inlet_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_temperature'. Can be any one from '('Temperature', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))

    @pytest.mark.negative
    def test_TurboExpander_outlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TurboExpander()
            m4.outlet_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_temperature'. Can be any one from '('Temperature', 'int', 'float', 'tuple', 'Series')'",
                      str(exp)) 
                                                     
    @pytest.mark.negative
    def test_TurboExpander_design_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TurboExpander()
            m4.design_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'design_temperature'. Can be any one from '('Temperature', 'int', 'float', 'tuple', 'Series')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_TurboExpander_inlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TurboExpander()
            m4.inlet_mass_flowrate = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_mass_flowrate'. Can be any one from '('MassFlowRate', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))                   

    @pytest.mark.negative
    def test_TurboExpander_outlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TurboExpander()
            m4.outlet_mass_flowrate = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_mass_flowrate'. Can be any one from '('MassFlowRate', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))

    @pytest.mark.negative
    def test_TurboExpander_energy_out_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TurboExpander()
            m4.energy_out = []
        self.assertIn("Incorrect type 'list' provided to 'energy_out'. Can be any one from '('Power', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))      

    @pytest.mark.negative
    def test_TurboExpander_energy_out_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TurboExpander()
            m4.energy_out = []
        self.assertIn("Incorrect type 'list' provided to 'energy_out'. Can be any one from '('Power', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))

    @pytest.mark.negative
    def test_TurboExpander_stream_connecion_disconnection_incorrect_type(self):
        cv = TurboExpander(tag="expander_2232",
                               differential_pressure=(10, 'bar'),
                               efficiency=40)
        inlet_stream = MaterialStream(tag="Inlet_expander_2232",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(25, 'C'))
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
                    
        with pytest.raises(Exception) as exp:
            cv.connect_stream([inlet_stream], 'in', stream_governed=True)
        self.assertIn("Incorrect type \'list\' provided to \'stream_object\'. Can be any one from \'('MaterialStream', 'EnergyStream')\'",
                      str(exp)) 
        
        with pytest.raises(Exception) as exp:
            cv.connect_stream(inlet_stream, ['in'], stream_governed=True)
        self.assertIn("Incorrect type \'list\' provided to \'direction\'. Should be \'str\'",
                      str(exp)) 
        with pytest.raises(Exception) as exp:
            cv.connect_stream(inlet_stream, 'in', stream_governed=[True])
        self.assertIn("Incorrect type \'list\' provided to \'stream_governed\'. Should be \'bool\'",
                      str(exp)) 

        cv.connect_stream(inlet_stream, 'in', stream_governed=True)
        with pytest.raises(Exception) as exp:
            cv.disconnect_stream(stream_tag=["Inlet_cv_19"])
        self.assertIn("Incorrect type \'list\' provided to \'stream_tag\'. Should be \'str\'",
                      str(exp))    

    @pytest.mark.negative
    def test_TurboExpander_stream_disconnection_before_connecion(self):  
        cv = TurboExpander(tag="expander_223332",
                               differential_pressure=(10, 'bar'),
                               efficiency=40)
        inlet_stream = MaterialStream(tag="Inlet_exps2232",
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
    def test_TurboExpander_stream_equipment_mapping(self):
        from propylean.equipments.abstract_equipment_classes import _material_stream_equipment_map as mse_map
        from propylean.equipments.abstract_equipment_classes import _energy_stream_equipment_map as ese_map
        comp = TurboExpander(
                               differential_pressure=(10, 'bar'))
        inlet_stream = MaterialStream()
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        outlet_stream = MaterialStream()
        energy_out = EnergyStream(tag="9999")
        energy_in = EnergyStream(tag="uyyth")

        comp.connect_stream(inlet_stream, direction="in", stream_governed=True)
        comp.connect_stream(outlet_stream, direction="out", stream_governed=False)
        
        with pytest.raises(Exception) as exp:
            comp.connect_stream(energy_in, direction="in")
        self.assertIn("TurboExpander only supports energy outlet.",
                      str(exp))

        self.assertEqual(mse_map[inlet_stream.index][2], comp.index)
        self.assertEqual(mse_map[inlet_stream.index][3], comp.__class__)
        self.assertEqual(mse_map[outlet_stream.index][0], comp.index)
        self.assertEqual(mse_map[outlet_stream.index][1], comp.__class__) 
        
        self.assertIsNotNone(comp.index)
        comp.connect_stream(energy_out)
        self.assertEqual(ese_map[energy_out.index][0], comp.index)
        self.assertEqual(ese_map[energy_out.index][1], comp.__class__) 
        self.assertIsNone(ese_map[energy_out.index][2])
        self.assertIsNone(ese_map[energy_out.index][3])   

        comp.disconnect_stream(inlet_stream)
        comp.disconnect_stream(outlet_stream)
        
        with pytest.raises(Exception) as exp:
            comp.disconnect_stream(energy_out, direction="in")  
        self.assertIn("TurboExpander only supports energy outlet.",
                      str(exp))
        

        self.assertIsNone(mse_map[inlet_stream.index][2])
        self.assertIsNone(mse_map[inlet_stream.index][3])
        self.assertIsNone(mse_map[outlet_stream.index][0])
        self.assertIsNone(mse_map[outlet_stream.index][1]) 
        print(ese_map)
        print(energy_out.index)
        comp.disconnect_stream(energy_out)
        print(ese_map[energy_out.index])
        self.assertIsNone(ese_map[energy_out.index][2])
        self.assertIsNone(ese_map[energy_out.index][3]) 
        self.assertIsNone(ese_map[energy_out.index][1])
        self.assertIsNone(ese_map[energy_out.index][0])  

    @pytest.mark.delete 
    def test_comp_stream_equipment_delete_without_connection(self):
        comp = TurboExpander()   
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
        comp = TurboExpander(
                               differential_pressure=(10, 'bar'))
        inlet_stream = MaterialStream()
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        outlet_stream = MaterialStream()
        energy_out = EnergyStream(tag="0909809")

        comp.connect_stream(inlet_stream, direction="in", stream_governed=True)
        comp.connect_stream(outlet_stream, direction="out", stream_governed=False)
        comp.connect_stream(energy_out, direction="out")

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

        self.assertIsNone(ese_map[energy_out.index][2])
        self.assertIsNone(ese_map[energy_out.index][3])
        self.assertIsNone(ese_map[energy_out.index][0])
        self.assertIsNone(ese_map[energy_out.index][1])