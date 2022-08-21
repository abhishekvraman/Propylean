import pytest
import unittest
from propylean.equipments.rotary import PositiveDisplacementPump
from propylean.streams import MaterialStream, EnergyStream
import propylean.properties as prop
import pandas as pd
from unittest.mock import patch

class test_PositiveDisplacementPump(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_PositiveDisplacementPump_instantiation_only_tag(self):
        pump = PositiveDisplacementPump(tag="PDPump_1")
        self.assertEqual(pump.tag, "PDPump_1")
        self.assertEqual(pump.pressure_drop, prop.Pressure(0))
        self.assertEqual(pump.differential_pressure, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_PositiveDisplacementPump_instantiation_tag_and_differential_pressure(self):
        pump = PositiveDisplacementPump(tag="PDPump_2",
                               differential_pressure=prop.Pressure(100, 'bar'))
        self.assertEqual(pump.tag, "PDPump_2")
        self.assertEqual(pump.differential_pressure, prop.Pressure(100, 'bar'))
        self.assertEqual(pump.pressure_drop, prop.Pressure(-100, 'bar'))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_PositiveDisplacementPump_instantiation_no_arguments(self):
        pump = PositiveDisplacementPump()
        self.assertIsNotNone(pump.tag)
        self.assertEqual(pump.pressure_drop, prop.Pressure(0))
        self.assertEqual(pump.differential_pressure, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_PositiveDisplacementPump_instantiation_npshr_efficiency(self):
        pump = PositiveDisplacementPump(tag="PDPump_3",
                               differential_pressure=(100, 'bar'),
                               NPSHr=(4, 'm'),
                               efficiency=70 )
        self.assertEqual(pump.tag, "PDPump_3")
        self.assertEqual(pump.differential_pressure, prop.Pressure(100, 'bar'))
        self.assertEqual(pump.NPSHr, prop.Length(4, 'm'))
        self.assertEqual(pump.efficiency, 70)
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_PositiveDisplacementPump_instantiation_PDpump_curves(self):
        performance_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2]}])
        pump = PositiveDisplacementPump(tag="PDPump_4",
                               performance_curve=performance_curve)
        self.assertEqual(pump.performace_curve.shape, performance_curve.shape)
    
    @pytest.mark.positive
    def test_PositiveDisplacementPump_representation(self):
        pump = PositiveDisplacementPump(tag="PDPump_5")
        self.assertIn("Positive Displacement Pump with tag: PDPump_5", str(pump))
    
    @pytest.mark.positive
    def test_PositiveDisplacementPump_setting_inlet_pressure(self):
        pump = PositiveDisplacementPump(tag="PDPump_6",
                               differential_pressure=(100, 'bar'))
        pump.inlet_pressure = (30, 'bar')
        self.assertEqual(pump.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(pump.outlet_pressure, prop.Pressure(130, 'bar'))
    
    @pytest.mark.positive
    def test_PositiveDisplacementPump_setting_outlet_pressure(self):
        pump = PositiveDisplacementPump(tag="PDPump_7",
                               differential_pressure=(100, 'bar'))
        pump.outlet_pressure = (130, 'bar')
        self.assertEqual(pump.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(pump.outlet_pressure, prop.Pressure(130, 'bar'))
    
    @pytest.mark.positive
    def test_PositiveDisplacementPump_setting_inlet_temperature(self):
        pump = PositiveDisplacementPump(tag="PDPump_8",
                               differential_pressure=(100, 'bar'))
        pump.inlet_temperature = (50, 'C')
        self.assertEqual(pump.inlet_temperature, prop.Temperature(50, 'C'))
        self.assertEqual(pump.outlet_temperature, prop.Temperature(50, 'C'))
    
    @pytest.mark.positive
    def test_PositiveDisplacementPump_setting_outlet_temperature(self):
        pump = PositiveDisplacementPump(tag="PDPump_9",
                               differential_pressure=(100, 'bar'))
        pump.outlet_temperature = (130, 'F')
        self.assertLess(abs(pump.inlet_temperature.value-130), 0.0001)
        self.assertEqual(pump.inlet_temperature.unit, 'F')
        self.assertLess(abs(pump.outlet_temperature.value-130), 0.0001)
        self.assertEqual(pump.outlet_temperature.unit, 'F')
    
    @pytest.mark.positive
    def test_PositiveDisplacementPump_setting_inlet_mass_flowrate(self):
        pump = PositiveDisplacementPump(tag="PDPump_10",
                               differential_pressure=(100, 'bar'))
        pump.inlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(pump.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(pump.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_PositiveDisplacementPump_setting_outlet_mass_flowrate(self):
        pump = PositiveDisplacementPump(tag="PDPump_11",
                               differential_pressure=(100, 'bar'))
        pump.outlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(pump.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(pump.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_PositiveDisplacementPump_connection_with_material_stream_inlet_stream_governed(self):
        pump = PositiveDisplacementPump(tag="PDPump_12",
                               differential_pressure=(100, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_PDPump_12",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(pump.connect_stream(inlet_stream, 'in', stream_governed=True))
        # Test inlet properties of pump are equal to inlet stream's.
        self.assertEqual(pump.inlet_pressure, inlet_stream.pressure)
        self.assertAlmostEqual(pump.inlet_temperature.value, inlet_stream.temperature.value, 3)
        self.assertEqual(pump.inlet_temperature.unit, inlet_stream.temperature.unit)
        self.assertEqual(pump.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(pump.outlet_pressure, pump.inlet_pressure+pump.differential_pressure)
        self.assertLess(abs(pump.inlet_temperature.value - pump.outlet_temperature.value), 0.001)
        self.assertEqual(pump.inlet_temperature.unit, pump.outlet_temperature.unit)
        self.assertEqual(pump.inlet_mass_flowrate, pump.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_PositiveDisplacementPump_connection_with_material_stream_outlet_stream_governed(self):
        pump = PositiveDisplacementPump(tag="PDPump_13",
                               differential_pressure=(100, 'bar'))
        outlet_stream = MaterialStream(tag="Outlet_PDPump_13",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(pump.connect_stream(outlet_stream, 'out', stream_governed=True))
        # Test outlet properties of pump are equal to outlet stream's.
        self.assertEqual(pump.outlet_pressure, outlet_stream.pressure)
        self.assertAlmostEqual(pump.outlet_temperature.value, outlet_stream.temperature.value, 3)
        self.assertEqual(pump.outlet_temperature.unit, outlet_stream.temperature.unit)
        self.assertEqual(pump.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(pump.inlet_pressure, pump.outlet_pressure-pump.differential_pressure)
        self.assertLess(abs(pump.inlet_temperature.value-pump.outlet_temperature.value),0.0001)
        self.assertEqual(pump.inlet_mass_flowrate, pump.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_PositiveDisplacementPump_connection_with_material_stream_inlet_equipment_governed(self):
        pump = PositiveDisplacementPump(tag="PDPump_14",
                               differential_pressure=(100, 'bar'))

        pump.inlet_pressure = (30, 'bar')
        pump.inlet_mass_flowrate = (1000, 'kg/h')
        pump.inlet_temperature = (320, 'K')
        inlet_stream = MaterialStream(tag="Inlet_PDPump_14")
        # Test connection is made.
        self.assertTrue(pump.connect_stream(inlet_stream, 'in', stream_governed=False))
        # Test inlet properties of pump are equal to inlet stream's.
        self.assertEqual(pump.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(pump.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(pump.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(pump.outlet_pressure, pump.inlet_pressure+pump.differential_pressure)
        self.assertEqual(pump.inlet_temperature, pump.outlet_temperature)
        self.assertEqual(pump.inlet_mass_flowrate, pump.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_PositiveDisplacementPump_connection_with_material_stream_outlet_equipment_governed(self):
        pump = PositiveDisplacementPump(tag="PDPump_15",
                               differential_pressure=(100, 'bar'))
        pump.outlet_pressure = (130, 'bar')
        pump.outlet_mass_flowrate = (1000, 'kg/h')
        pump.outlet_temperature = (30, 'C')
        outlet_stream = MaterialStream(tag="Outlet_PDPump_15")
        # Test connection is made.
        self.assertTrue(pump.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test outlet properties of pump are equal to outlet stream's.
        self.assertEqual(pump.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(pump.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(pump.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(pump.inlet_pressure, pump.outlet_pressure-pump.differential_pressure)
        self.assertEqual(pump.inlet_temperature, pump.outlet_temperature)
        self.assertEqual(pump.inlet_mass_flowrate, pump.outlet_mass_flowrate)
    
    # TODO Uncomment below when power setting feature is provided.
    # @pytest.mark.positive
    # def test_PositiveDisplacementPump_connection_with_energy_stream_inlet_stream_governed(self):
    #     pump = PositiveDisplacementPump(tag="PDPump_16",
    #                            differential_pressure=(100, 'bar'))
    #     pump_power = EnergyStream(tag="Power_PDPump_16", amount=(10,"MW"))
    #     # Test connection is made.
    #     self.assertTrue(pump.connect_stream(pump_power, stream_governed=True))
    #     # Test inlet properties of pump are equal to outlet stream's.
    #     self.assertEqual(pump.energy_in, pump_power.amount)
    #     self.assertEqual(pump.power, pump_power.unit)

    pytest.mark.positive
    def test_PositiveDisplacementPump_connection_with_energy_stream_inlet_equipment_governed(self):
        pump = PositiveDisplacementPump(tag="PDPump_17",
                               differential_pressure=(100, 'bar'))
        pump_power = EnergyStream(tag="Power_PDPump_17", amount=(10,"MW"))
        pump_inlet = MaterialStream(mass_flowrate=(1000, 'kg/h'),
                                    pressure=(30, 'bar'),
                                    temperature=(25, 'C'))
        pump_inlet.components = prop.Components({"water": 1})
        # Test connection is made.
        self.assertTrue(pump.connect_stream(pump_inlet, "in", stream_governed=True))
        self.assertTrue(pump.connect_stream(pump_power))
        # Test inlet properties of pump are equal to outlet stream's.
        # self.assertAlmostEqual(pump.power.value, pump_power.amount.value)
        # self.assertEqual(pump.power.unit, pump_power.amount.unit)
        self.assertGreater(pump.power.value, 0)
    
    @pytest.mark.positive
    def test_PositiveDisplacementPump_stream_disconnection_by_stream_object(self):
        pump = PositiveDisplacementPump(tag="PDPump_18",
                               differential_pressure=(100, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_PDPump_18")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_PDPump_18")
        pump_power = EnergyStream(tag="Power_PDPump_18")
        # Test connection is made.
        self.assertTrue(pump.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(pump.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(pump.connect_stream(pump_power))
        # Test disconnection
        self.assertTrue(pump.disconnect_stream(inlet_stream))
        self.assertTrue(pump.disconnect_stream(outlet_stream))
        self.assertTrue(pump.disconnect_stream(pump_power))
        self.assertIsNone(pump._inlet_material_stream_tag)
        self.assertIsNone(pump._outlet_material_stream_tag)
        self.assertIsNone(pump._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    @pytest.mark.temp
    def test_PositiveDisplacementPump_stream_disconnection_by_stream_tag(self):
        pump = PositiveDisplacementPump(tag="PDPump_19",
                               differential_pressure=(100, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_PDPump_19")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_PDPump_19")
        pump_power = EnergyStream(tag="Power_PDPump_19")
        # Test connection is made.
        self.assertTrue(pump.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(pump.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertEqual(inlet_stream.components, outlet_stream.components)
        self.assertTrue(pump.connect_stream(pump_power))
        # Test disconnection
        self.assertTrue(pump.disconnect_stream(stream_tag="Inlet_PDPump_19"))
        self.assertTrue(pump.disconnect_stream(stream_tag="Outlet_PDPump_19"))
        self.assertTrue(pump.disconnect_stream(stream_tag="Power_PDPump_19"))
        self.assertIsNone(pump._inlet_material_stream_tag)
        self.assertIsNone(pump._outlet_material_stream_tag)
        self.assertIsNone(pump._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_PositiveDisplacementPump_stream_disconnection_by_direction_stream_type(self):
        pump = PositiveDisplacementPump(tag="PDPump_20",
                               differential_pressure=(100, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_PDPump_20")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_PDPump_20")
        pump_power = EnergyStream(tag="Power_PDPump_20")
        # Test connection is made.
        self.assertTrue(pump.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(pump.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(pump.connect_stream(pump_power))
        # Test disconnection
        self.assertTrue(pump.disconnect_stream(direction="In", stream_type="Material"))
        self.assertTrue(pump.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        self.assertTrue(pump.disconnect_stream(stream_type="energy"))
        self.assertIsNone(pump._inlet_material_stream_tag)
        self.assertIsNone(pump._outlet_material_stream_tag)
        self.assertIsNone(pump._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)

    @pytest.mark.positive
    def test_PositiveDisplacementPump_head_calulcation(self):
        pump = PositiveDisplacementPump(tag="PDPump_21",
                               differential_pressure=(100, 'bar'),
                               efficiency=75)
        inlet_stream = MaterialStream(tag="Inlet_PDPump_21",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(25, 'C'))
        inlet_stream.components = prop.Components({"water": 1})
        pump.connect_stream(inlet_stream, 'in', stream_governed=True)
        pressure = prop.Pressure(100, 'bar')
        pressure.unit = "Pa"
        expected_head_value = 10000000 / (9.8 * inlet_stream.density.value)
        pump_head = pump.head
        pump_head.unit = "m"
        self.assertAlmostEqual(expected_head_value, pump_head.value)
    
    @pytest.mark.positive
    def test_PositiveDisplacementPump_power_calulcations(self):
        pump = PositiveDisplacementPump(tag="PDPump_22",
                               differential_pressure=(100, 'bar'),
                               efficiency=40)
        inlet_stream = MaterialStream(tag="Inlet_PDPump_22",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(25, 'C'))
        inlet_stream.components = prop.Components({"water": 1})
        pump.connect_stream(inlet_stream, 'in', stream_governed=True)
        pressure = prop.Pressure(100, 'bar')
        pressure.unit = "Pa"
        expected_power = prop.Power(2.78676, "W")
        pump_power = pump.power
        # pump_power.unit = "kW"
        # self.assertAlmostEqual(expected_power, pump_power.value, 2)
        self.assertGreater(pump_power.value, 0)
        self.assertEqual(pump_power.unit, 'hp')

    @pytest.mark.negative
    def test_PositiveDisplacementPump_inlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PositiveDisplacementPump()
            m4.inlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_PositiveDisplacementPump_outlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PositiveDisplacementPump()
            m4.outlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_PositiveDisplacementPump_pressure_drop_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PositiveDisplacementPump()
            m4.pressure_drop = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'pressure_drop'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                    

    @pytest.mark.negative
    def test_PositiveDisplacementPump_design_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PositiveDisplacementPump()
            m4.design_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_PositiveDisplacementPump_inlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PositiveDisplacementPump()
            m4.inlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_PositiveDisplacementPump_outlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PositiveDisplacementPump()
            m4.outlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_PositiveDisplacementPump_temperature_decrease_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PositiveDisplacementPump()
            m4.temperature_decrease = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'temperature_decrease'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_PositiveDisplacementPump_temperature_increase_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PositiveDisplacementPump()
            m4.temperature_increase = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'temperature_increase'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                                      

    @pytest.mark.negative
    def test_PositiveDisplacementPump_design_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PositiveDisplacementPump()
            m4.design_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_PositiveDisplacementPump_inlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PositiveDisplacementPump()
            m4.inlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_PositiveDisplacementPump_outlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PositiveDisplacementPump()
            m4.outlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_PositiveDisplacementPump_energy_in_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PositiveDisplacementPump()
            m4.energy_in = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_in'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))      

    @pytest.mark.negative
    def test_PositiveDisplacementPump_energy_out_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PositiveDisplacementPump()
            m4.energy_out = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_out'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))